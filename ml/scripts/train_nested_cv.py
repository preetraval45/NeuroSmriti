"""
Train MemoryGNN with Nested Cross-Validation (10 folds)

Nested CV provides unbiased performance estimates by separating:
- Outer loop: Performance estimation (10-fold CV)
- Inner loop: Hyperparameter tuning (5-fold CV)

This prevents overfitting during model selection and provides
clinical-grade validation suitable for real-world deployment.
"""

import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
from sklearn.model_selection import KFold, ParameterGrid
import pickle
import os
import sys
import numpy as np
from tqdm import tqdm
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.memory_gnn import MemoryGNN, MemoryDecayLoss


def train_epoch(model, loader, optimizer, criterion, device):
    """Train for one epoch"""
    model.train()
    total_loss = 0

    for batch in loader:
        batch = batch.to(device)
        optimizer.zero_grad()

        # Forward pass
        node_pred, graph_pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)

        # Compute loss
        loss = criterion(node_pred, batch.y_node, graph_pred, batch.y_graph)

        # Backward pass
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(loader)


def evaluate(model, loader, criterion, device):
    """Evaluate model with comprehensive metrics"""
    model.eval()
    total_loss = 0
    node_mae = 0
    graph_mae = 0
    node_mse = 0
    graph_mse = 0

    all_node_preds = []
    all_node_targets = []
    all_graph_preds = []
    all_graph_targets = []

    with torch.no_grad():
        for batch in loader:
            batch = batch.to(device)

            # Forward pass
            node_pred, graph_pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)

            # Loss
            loss = criterion(node_pred, batch.y_node, graph_pred, batch.y_graph)
            total_loss += loss.item()

            # MAE and MSE metrics
            node_mae += F.l1_loss(node_pred, batch.y_node).item()
            graph_mae += F.l1_loss(graph_pred, batch.y_graph).item()
            node_mse += F.mse_loss(node_pred, batch.y_node).item()
            graph_mse += F.mse_loss(graph_pred, batch.y_graph).item()

            # Store predictions for advanced metrics
            all_node_preds.append(node_pred.cpu())
            all_node_targets.append(batch.y_node.cpu())
            all_graph_preds.append(graph_pred.cpu())
            all_graph_targets.append(batch.y_graph.cpu())

    # Concatenate all predictions
    all_node_preds = torch.cat(all_node_preds, dim=0)
    all_node_targets = torch.cat(all_node_targets, dim=0)
    all_graph_preds = torch.cat(all_graph_preds, dim=0)
    all_graph_targets = torch.cat(all_graph_targets, dim=0)

    # Calculate R² score
    node_ss_res = torch.sum((all_node_targets - all_node_preds) ** 2)
    node_ss_tot = torch.sum((all_node_targets - torch.mean(all_node_targets)) ** 2)
    node_r2 = 1 - (node_ss_res / node_ss_tot)

    graph_ss_res = torch.sum((all_graph_targets - all_graph_preds) ** 2)
    graph_ss_tot = torch.sum((all_graph_targets - torch.mean(all_graph_targets)) ** 2)
    graph_r2 = 1 - (graph_ss_res / graph_ss_tot)

    return {
        'loss': total_loss / len(loader),
        'node_mae': node_mae / len(loader),
        'graph_mae': graph_mae / len(loader),
        'node_mse': node_mse / len(loader),
        'graph_mse': graph_mse / len(loader),
        'node_r2': node_r2.item(),
        'graph_r2': graph_r2.item(),
    }


def train_with_hyperparams(train_data, val_data, hyperparams, device, max_epochs=30):
    """Train model with specific hyperparameters"""

    # Create dataloaders
    train_loader = DataLoader(train_data, batch_size=hyperparams['batch_size'], shuffle=True)
    val_loader = DataLoader(val_data, batch_size=hyperparams['batch_size'], shuffle=False)

    # Initialize model
    model = MemoryGNN(
        num_node_features=10,
        hidden_channels=hyperparams['hidden_channels'],
        num_heads=hyperparams['num_heads'],
        num_layers=hyperparams['num_layers'],
        dropout=hyperparams['dropout']
    ).to(device)

    # Loss and optimizer
    criterion = MemoryDecayLoss(alpha=0.7, beta=0.3)
    optimizer = torch.optim.Adam(model.parameters(), lr=hyperparams['learning_rate'])
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=3, verbose=False
    )

    # Training loop with early stopping
    best_val_loss = float('inf')
    patience = 5
    patience_counter = 0

    for epoch in range(max_epochs):
        # Train
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)

        # Validate
        val_metrics = evaluate(model, val_loader, criterion, device)

        # Scheduler step
        scheduler.step(val_metrics['loss'])

        # Early stopping
        if val_metrics['loss'] < best_val_loss:
            best_val_loss = val_metrics['loss']
            best_metrics = val_metrics
            patience_counter = 0
        else:
            patience_counter += 1

        if patience_counter >= patience:
            break

    return best_metrics


def nested_cross_validation(data, device, n_outer_folds=10, n_inner_folds=5):
    """
    Perform Nested Cross-Validation

    Outer loop: 10-fold CV for unbiased performance estimation
    Inner loop: 5-fold CV for hyperparameter selection
    """

    print("="*70)
    print("NESTED CROSS-VALIDATION WITH 10 FOLDS")
    print("="*70)
    print(f"Total samples: {len(data)}")
    print(f"Outer folds: {n_outer_folds}")
    print(f"Inner folds: {n_inner_folds}")
    print("="*70)

    # Hyperparameter grid
    param_grid = {
        'hidden_channels': [32, 64, 128],
        'num_heads': [2, 4, 8],
        'num_layers': [2, 3, 4],
        'dropout': [0.1, 0.3, 0.5],
        'learning_rate': [0.001, 0.0005],
        'batch_size': [16, 32]
    }

    # Outer cross-validation
    outer_kfold = KFold(n_splits=n_outer_folds, shuffle=True, random_state=42)

    outer_results = []
    best_hyperparams_per_fold = []

    for outer_fold, (train_val_idx, test_idx) in enumerate(outer_kfold.split(data)):
        print(f"\n{'='*70}")
        print(f"OUTER FOLD {outer_fold + 1}/{n_outer_folds}")
        print(f"{'='*70}")

        # Split data
        train_val_data = [data[i] for i in train_val_idx]
        test_data = [data[i] for i in test_idx]

        print(f"Train+Val: {len(train_val_data)}, Test: {len(test_data)}")

        # Inner cross-validation for hyperparameter tuning
        inner_kfold = KFold(n_splits=n_inner_folds, shuffle=True, random_state=42)

        best_hyperparams = None
        best_avg_val_loss = float('inf')

        print(f"\nInner CV: Tuning hyperparameters...")

        # Sample hyperparameters (full grid search would be too expensive)
        # Using random search with 20 combinations
        np.random.seed(42)
        all_params = list(ParameterGrid(param_grid))
        sampled_params = np.random.choice(len(all_params),
                                         min(20, len(all_params)),
                                         replace=False)

        for param_idx in tqdm(sampled_params, desc="Hyperparameter search"):
            hyperparams = all_params[param_idx]

            inner_val_losses = []

            for inner_fold, (train_idx, val_idx) in enumerate(inner_kfold.split(train_val_data)):
                train_data_inner = [train_val_data[i] for i in train_idx]
                val_data_inner = [train_val_data[i] for i in val_idx]

                # Train with these hyperparameters
                val_metrics = train_with_hyperparams(
                    train_data_inner,
                    val_data_inner,
                    hyperparams,
                    device,
                    max_epochs=20  # Reduced for inner CV
                )

                inner_val_losses.append(val_metrics['loss'])

            # Average validation loss across inner folds
            avg_val_loss = np.mean(inner_val_losses)

            if avg_val_loss < best_avg_val_loss:
                best_avg_val_loss = avg_val_loss
                best_hyperparams = hyperparams

        print(f"\nBest hyperparameters for fold {outer_fold + 1}:")
        for key, value in best_hyperparams.items():
            print(f"  {key}: {value}")
        print(f"  Avg validation loss: {best_avg_val_loss:.4f}")

        best_hyperparams_per_fold.append(best_hyperparams)

        # Train final model on all train_val_data with best hyperparameters
        print(f"\nTraining final model for outer fold {outer_fold + 1}...")

        # Split train_val_data into train and validation
        train_size = int(0.85 * len(train_val_data))
        train_data_final = train_val_data[:train_size]
        val_data_final = train_val_data[train_size:]

        train_loader = DataLoader(train_data_final, batch_size=best_hyperparams['batch_size'], shuffle=True)
        val_loader = DataLoader(val_data_final, batch_size=best_hyperparams['batch_size'], shuffle=False)
        test_loader = DataLoader(test_data, batch_size=best_hyperparams['batch_size'], shuffle=False)

        # Initialize and train model
        model = MemoryGNN(
            num_node_features=10,
            hidden_channels=best_hyperparams['hidden_channels'],
            num_heads=best_hyperparams['num_heads'],
            num_layers=best_hyperparams['num_layers'],
            dropout=best_hyperparams['dropout']
        ).to(device)

        criterion = MemoryDecayLoss(alpha=0.7, beta=0.3)
        optimizer = torch.optim.Adam(model.parameters(), lr=best_hyperparams['learning_rate'])
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer, mode='min', factor=0.5, patience=5, verbose=False
        )

        best_val_loss = float('inf')
        patience = 10
        patience_counter = 0

        for epoch in range(50):
            train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
            val_metrics = evaluate(model, val_loader, criterion, device)
            scheduler.step(val_metrics['loss'])

            if val_metrics['loss'] < best_val_loss:
                best_val_loss = val_metrics['loss']
                # Save best model state
                best_model_state = model.state_dict().copy()
                patience_counter = 0
            else:
                patience_counter += 1

            if patience_counter >= patience:
                break

        # Load best model and evaluate on test set
        model.load_state_dict(best_model_state)
        test_metrics = evaluate(model, test_loader, criterion, device)

        print(f"\nOuter Fold {outer_fold + 1} Test Results:")
        print(f"  Loss: {test_metrics['loss']:.4f}")
        print(f"  Node MAE: {test_metrics['node_mae']:.4f}")
        print(f"  Graph MAE: {test_metrics['graph_mae']:.4f}")
        print(f"  Node R²: {test_metrics['node_r2']:.4f}")
        print(f"  Graph R²: {test_metrics['graph_r2']:.4f}")

        outer_results.append(test_metrics)

        # Save fold model
        torch.save({
            'fold': outer_fold + 1,
            'model_state_dict': best_model_state,
            'hyperparameters': best_hyperparams,
            'test_metrics': test_metrics
        }, f'../models/memory_gnn_fold_{outer_fold + 1}.pth')

    # Aggregate results across all folds
    print("\n" + "="*70)
    print("FINAL NESTED CV RESULTS (10 FOLDS)")
    print("="*70)

    metrics_names = ['loss', 'node_mae', 'graph_mae', 'node_mse', 'graph_mse', 'node_r2', 'graph_r2']

    for metric in metrics_names:
        values = [result[metric] for result in outer_results]
        mean_val = np.mean(values)
        std_val = np.std(values)
        ci_95 = 1.96 * std_val / np.sqrt(len(values))

        print(f"\n{metric.upper()}:")
        print(f"  Mean: {mean_val:.4f}")
        print(f"  Std:  {std_val:.4f}")
        print(f"  95% CI: [{mean_val - ci_95:.4f}, {mean_val + ci_95:.4f}]")

    # Save results
    results_dict = {
        'timestamp': datetime.now().isoformat(),
        'n_outer_folds': n_outer_folds,
        'n_inner_folds': n_inner_folds,
        'outer_results': [
            {k: float(v) if isinstance(v, (np.floating, float)) else v
             for k, v in result.items()}
            for result in outer_results
        ],
        'best_hyperparams_per_fold': best_hyperparams_per_fold,
        'summary': {
            metric: {
                'mean': float(np.mean([result[metric] for result in outer_results])),
                'std': float(np.std([result[metric] for result in outer_results])),
                'ci_95': float(1.96 * np.std([result[metric] for result in outer_results]) /
                              np.sqrt(len(outer_results)))
            }
            for metric in metrics_names
        }
    }

    with open('../models/nested_cv_results.json', 'w') as f:
        json.dump(results_dict, f, indent=2)

    print("\n" + "="*70)
    print("Results saved to: ../models/nested_cv_results.json")
    print("="*70)

    return results_dict


def load_data(data_dir='../data/synthetic'):
    """Load preprocessed data"""
    with open(f'{data_dir}/train.pkl', 'rb') as f:
        train_data = pickle.load(f)

    with open(f'{data_dir}/val.pkl', 'rb') as f:
        val_data = pickle.load(f)

    with open(f'{data_dir}/test.pkl', 'rb') as f:
        test_data = pickle.load(f)

    # Combine all data for nested CV
    all_data = train_data + val_data + test_data

    return all_data


def main():
    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load data
    print("\nLoading data...")
    all_data = load_data()
    print(f"Total samples: {len(all_data)}")

    # Perform nested cross-validation
    results = nested_cross_validation(all_data, device, n_outer_folds=10, n_inner_folds=5)

    print("\n✓ Nested Cross-Validation completed successfully!")


if __name__ == "__main__":
    main()
