"""
Train MemoryGNN on synthetic data
"""

import torch
import torch.nn.functional as F
from torch_geometric.loader import DataLoader
import pickle
import os
import sys
from tqdm import tqdm

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.memory_gnn import MemoryGNN, MemoryDecayLoss


def load_data(data_dir='../data/synthetic'):
    """Load preprocessed data"""
    with open(f'{data_dir}/train.pkl', 'rb') as f:
        train_data = pickle.load(f)

    with open(f'{data_dir}/val.pkl', 'rb') as f:
        val_data = pickle.load(f)

    with open(f'{data_dir}/test.pkl', 'rb') as f:
        test_data = pickle.load(f)

    return train_data, val_data, test_data


def train_epoch(model, loader, optimizer, criterion, device):
    """Train for one epoch"""
    model.train()
    total_loss = 0
    total_node_loss = 0
    total_graph_loss = 0

    for batch in tqdm(loader, desc="Training"):
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
    """Evaluate model"""
    model.eval()
    total_loss = 0
    node_mae = 0
    graph_mae = 0

    with torch.no_grad():
        for batch in loader:
            batch = batch.to(device)

            # Forward pass
            node_pred, graph_pred = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)

            # Loss
            loss = criterion(node_pred, batch.y_node, graph_pred, batch.y_graph)
            total_loss += loss.item()

            # MAE metrics
            node_mae += F.l1_loss(node_pred, batch.y_node).item()
            graph_mae += F.l1_loss(graph_pred, batch.y_graph).item()

    return {
        'loss': total_loss / len(loader),
        'node_mae': node_mae / len(loader),
        'graph_mae': graph_mae / len(loader)
    }


def main():
    # Hyperparameters
    BATCH_SIZE = 32
    HIDDEN_CHANNELS = 64
    NUM_HEADS = 4
    NUM_LAYERS = 3
    DROPOUT = 0.3
    LEARNING_RATE = 0.001
    NUM_EPOCHS = 50

    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load data
    print("\nLoading data...")
    train_data, val_data, test_data = load_data()
    print(f"Train: {len(train_data)}, Val: {len(val_data)}, Test: {len(test_data)}")

    # Create dataloaders
    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_data, batch_size=BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False)

    # Initialize model
    print("\nInitializing model...")
    model = MemoryGNN(
        num_node_features=10,
        hidden_channels=HIDDEN_CHANNELS,
        num_heads=NUM_HEADS,
        num_layers=NUM_LAYERS,
        dropout=DROPOUT
    ).to(device)

    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    # Loss and optimizer
    criterion = MemoryDecayLoss(alpha=0.7, beta=0.3)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=5, verbose=True
    )

    # Training loop
    print("\nStarting training...")
    best_val_loss = float('inf')
    patience = 10
    patience_counter = 0

    for epoch in range(NUM_EPOCHS):
        print(f"\nEpoch {epoch + 1}/{NUM_EPOCHS}")

        # Train
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)

        # Validate
        val_metrics = evaluate(model, val_loader, criterion, device)

        # Scheduler step
        scheduler.step(val_metrics['loss'])

        print(f"Train Loss: {train_loss:.4f}")
        print(f"Val Loss: {val_metrics['loss']:.4f} | "
              f"Node MAE: {val_metrics['node_mae']:.4f} | "
              f"Graph MAE: {val_metrics['graph_mae']:.4f}")

        # Save best model
        if val_metrics['loss'] < best_val_loss:
            best_val_loss = val_metrics['loss']
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_loss': val_metrics['loss'],
                'hyperparameters': {
                    'hidden_channels': HIDDEN_CHANNELS,
                    'num_heads': NUM_HEADS,
                    'num_layers': NUM_LAYERS,
                    'dropout': DROPOUT
                }
            }, '../models/memory_gnn_best.pth')
            print("✓ Saved best model!")
            patience_counter = 0
        else:
            patience_counter += 1

        # Early stopping
        if patience_counter >= patience:
            print(f"\nEarly stopping after {epoch + 1} epochs")
            break

    # Test evaluation
    print("\n" + "="*50)
    print("Final Evaluation on Test Set")
    print("="*50)

    # Load best model
    checkpoint = torch.load('../models/memory_gnn_best.pth')
    model.load_state_dict(checkpoint['model_state_dict'])

    test_metrics = evaluate(model, test_loader, criterion, device)

    print(f"\nTest Results:")
    print(f"Loss: {test_metrics['loss']:.4f}")
    print(f"Node MAE (decay prediction): {test_metrics['node_mae']:.4f}")
    print(f"Graph MAE (risk score): {test_metrics['graph_mae']:.4f}")

    # Convert MAE to percentage
    print(f"\nNode MAE as percentage: {test_metrics['node_mae'] * 100:.2f}%")
    print(f"Graph MAE as percentage: {test_metrics['graph_mae'] * 100:.2f}%")

    # Accuracy metrics (within 10% threshold)
    model.eval()
    correct_30 = 0
    correct_90 = 0
    correct_180 = 0
    total_nodes = 0

    with torch.no_grad():
        for batch in test_loader:
            batch = batch.to(device)
            node_pred, _ = model(batch.x, batch.edge_index, batch.edge_attr, batch.batch)

            # Check if predictions are within 10% of ground truth
            diff = torch.abs(node_pred - batch.y_node)
            correct_30 += (diff[:, 0] < 0.1).sum().item()
            correct_90 += (diff[:, 1] < 0.1).sum().item()
            correct_180 += (diff[:, 2] < 0.1).sum().item()
            total_nodes += batch.x.size(0)

    print(f"\nAccuracy (within 10% threshold):")
    print(f"30-day forecast: {100 * correct_30 / total_nodes:.2f}%")
    print(f"90-day forecast: {100 * correct_90 / total_nodes:.2f}%")
    print(f"180-day forecast: {100 * correct_180 / total_nodes:.2f}%")

    print("\n" + "="*50)
    print("Training completed successfully!")
    print(f"Best model saved to: ../models/memory_gnn_best.pth")
    print("="*50)


if __name__ == "__main__":
    main()
