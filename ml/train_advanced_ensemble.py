"""
Advanced Ensemble Models with Stacking, XGBoost, LightGBM, and CatBoost
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, StackingClassifier, VotingClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import lightgbm as lgb
import catboost as cb


def load_and_prepare_data(data_path: Path):
    """Load and prepare training data"""
    print("Loading data...")
    df = pd.read_csv(data_path)

    # Encode categorical variables
    if 'gender' in df.columns and df['gender'].dtype == 'object':
        df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})

    # Separate features and target
    X = df.drop(['patient_id', 'stage'], axis=1, errors='ignore')
    y = df['stage']

    return X, y


def create_base_models():
    """Create diverse base models for ensemble"""
    base_models = {
        # Traditional ML
        'random_forest': RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        ),
        'gradient_boosting': GradientBoostingClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=7,
            min_samples_split=5,
            random_state=42
        ),
        'neural_network': MLPClassifier(
            hidden_layers=(128, 64, 32),
            activation='relu',
            solver='adam',
            learning_rate_init=0.001,
            max_iter=500,
            early_stopping=True,
            random_state=42
        ),

        # Advanced Gradient Boosting
        'xgboost': xgb.XGBClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=7,
            min_child_weight=3,
            gamma=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1,
            eval_metric='mlogloss'
        ),
        'lightgbm': lgb.LGBMClassifier(
            n_estimators=200,
            learning_rate=0.1,
            max_depth=7,
            num_leaves=31,
            min_child_samples=20,
            subsample=0.8,
            colsample_bytree=0.8,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1,
            verbose=-1
        ),
        'catboost': cb.CatBoostClassifier(
            iterations=200,
            learning_rate=0.1,
            depth=7,
            l2_leaf_reg=3,
            random_seed=42,
            verbose=False,
            thread_count=-1
        )
    }

    return base_models


def create_stacking_ensemble(base_models):
    """Create stacking ensemble with meta-learner"""
    # Select best base models for stacking
    estimators = [
        ('xgboost', base_models['xgboost']),
        ('lightgbm', base_models['lightgbm']),
        ('catboost', base_models['catboost']),
        ('random_forest', base_models['random_forest']),
        ('neural_network', base_models['neural_network'])
    ]

    # Meta-learner (Logistic Regression with regularization)
    meta_learner = LogisticRegression(
        C=1.0,
        max_iter=1000,
        random_state=42,
        multi_class='multinomial'
    )

    # Create stacking classifier
    stacking_clf = StackingClassifier(
        estimators=estimators,
        final_estimator=meta_learner,
        cv=5,
        n_jobs=-1,
        verbose=1
    )

    return stacking_clf


def create_voting_ensemble(base_models):
    """Create voting ensemble (soft voting)"""
    estimators = [
        ('xgboost', base_models['xgboost']),
        ('lightgbm', base_models['lightgbm']),
        ('catboost', base_models['catboost']),
        ('random_forest', base_models['random_forest'])
    ]

    voting_clf = VotingClassifier(
        estimators=estimators,
        voting='soft',
        n_jobs=-1,
        verbose=True
    )

    return voting_clf


def train_and_evaluate_model(model, X_train, y_train, X_test, y_test, model_name, label_encoder):
    """Train and evaluate a single model"""
    print(f"\n{'='*60}")
    print(f"Training {model_name}...")
    print(f"{'='*60}")

    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)

    # Accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nAccuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")

    # Classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

    # Confusion matrix
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Per-class accuracy
    print("\nPer-Class Accuracy:")
    for stage in label_encoder.classes_:
        mask = y_test == stage
        if mask.sum() > 0:
            stage_acc = accuracy_score(y_test[mask], y_pred[mask])
            print(f"  {stage}: {stage_acc:.4f} ({stage_acc*100:.2f}%)")

    return {
        'model': model,
        'accuracy': accuracy,
        'predictions': y_pred,
        'probabilities': y_pred_proba
    }


def main():
    # Paths
    script_dir = Path(__file__).parent
    data_dir = script_dir / "data"
    model_dir = script_dir / "models"
    model_dir.mkdir(exist_ok=True)

    # Load data
    train_file = data_dir / "synthetic_alzheimers_data.csv"
    if not train_file.exists():
        print(f"Error: Training data not found at {train_file}")
        print("Please run generate_sample_data.py first")
        return

    X, y = load_and_prepare_data(train_file)

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    print(f"Features: {X_train.shape[1]}")
    print(f"Classes: {label_encoder.classes_}")

    # Create base models
    base_models = create_base_models()

    # Train individual models
    results = {}

    # Train base models
    for name, model in base_models.items():
        result = train_and_evaluate_model(
            model, X_train_scaled, y_train, X_test_scaled, y_test,
            name, label_encoder
        )
        results[name] = result

        # Save individual model
        model_file = model_dir / f"{name}_model.pkl"
        with open(model_file, "wb") as f:
            pickle.dump(model, f)
        print(f"Saved {name} model to {model_file}")

    # Create and train stacking ensemble
    print("\n" + "="*60)
    print("Creating Stacking Ensemble...")
    print("="*60)
    stacking_model = create_stacking_ensemble(base_models)
    stacking_result = train_and_evaluate_model(
        stacking_model, X_train_scaled, y_train, X_test_scaled, y_test,
        "Stacking Ensemble", label_encoder
    )
    results['stacking'] = stacking_result

    # Save stacking model
    with open(model_dir / "stacking_ensemble_model.pkl", "wb") as f:
        pickle.dump(stacking_model, f)

    # Create and train voting ensemble
    print("\n" + "="*60)
    print("Creating Voting Ensemble...")
    print("="*60)
    voting_model = create_voting_ensemble(base_models)
    voting_result = train_and_evaluate_model(
        voting_model, X_train_scaled, y_train, X_test_scaled, y_test,
        "Voting Ensemble", label_encoder
    )
    results['voting'] = voting_result

    # Save voting model
    with open(model_dir / "voting_ensemble_model.pkl", "wb") as f:
        pickle.dump(voting_model, f)

    # Save scaler and label encoder
    with open(model_dir / "scaler_advanced.pkl", "wb") as f:
        pickle.dump(scaler, f)

    with open(model_dir / "label_encoder_advanced.pkl", "wb") as f:
        pickle.dump(label_encoder, f)

    # Summary
    print("\n" + "="*60)
    print("FINAL RESULTS SUMMARY")
    print("="*60)

    sorted_results = sorted(results.items(), key=lambda x: x[1]['accuracy'], reverse=True)

    print("\nModel Rankings:")
    for i, (name, result) in enumerate(sorted_results, 1):
        print(f"{i}. {name:25s} - Accuracy: {result['accuracy']:.4f} ({result['accuracy']*100:.2f}%)")

    best_model_name = sorted_results[0][0]
    best_accuracy = sorted_results[0][1]['accuracy']

    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Accuracy: {best_accuracy:.4f} ({best_accuracy*100:.2f}%)")

    # Save best model as main ensemble
    best_model = results[best_model_name]['model']
    with open(model_dir / "ensemble_model.pkl", "wb") as f:
        pickle.dump(best_model, f)

    print(f"\n✓ All models trained and saved to {model_dir}")
    print(f"✓ Best model saved as ensemble_model.pkl")

    # Model registry
    registry = {
        "models": {
            name: {
                "accuracy": float(result['accuracy']),
                "filename": f"{name}_model.pkl"
            }
            for name, result in results.items()
        },
        "best_model": best_model_name,
        "feature_names": list(X.columns),
        "classes": label_encoder.classes_.tolist(),
        "num_features": X_train.shape[1]
    }

    with open(model_dir / "advanced_model_registry.json", "w") as f:
        import json
        json.dump(registry, f, indent=2)

    print(f"✓ Model registry saved to advanced_model_registry.json")


if __name__ == "__main__":
    main()
