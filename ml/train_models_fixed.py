"""
Fixed training script for traditional ML models
Handles both JSON and CSV data formats correctly
"""
import json
import os
import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score
)
from sklearn.neural_network import MLPClassifier
import pickle
import warnings
warnings.filterwarnings('ignore')


def load_data(data_path):
    """Load and preprocess dataset"""
    print(f"Loading data from {data_path}...")

    if data_path.endswith('.json'):
        # Load JSON format
        with open(data_path, 'r') as f:
            data = json.load(f)

        if 'data' in data:
            records = data['data']
        else:
            records = data

        # Flatten nested JSON to DataFrame
        rows = []
        for p in records:
            row = {
                "age": p.get("demographics", {}).get("age", 0),
                "gender": 1 if p.get("demographics", {}).get("gender") == "Female" else 0,
                "education_years": p.get("demographics", {}).get("education_years", 0),
                "has_apoe4": 1 if p.get("genetics", {}).get("has_apoe4") else 0,
                "family_history_ad": 1 if p.get("genetics", {}).get("family_history_ad") else 0,
                "mmse_total": p.get("cognitive_scores", {}).get("mmse_total", 0),
                "moca_total": p.get("cognitive_scores", {}).get("moca_total", 0),
                "adas_cog_13": p.get("cognitive_scores", {}).get("adas_cog_13", 0),
                "faq_total": p.get("cognitive_scores", {}).get("faq_total", 0),
                "cdr_global": p.get("cognitive_scores", {}).get("cdr_global", 0),
                "diagnosis_stage": p.get("cognitive_scores", {}).get("diagnosis_stage", "normal"),
                "hippocampus_left": p.get("neuroimaging", {}).get("hippocampus_left", 0),
                "hippocampus_right": p.get("neuroimaging", {}).get("hippocampus_right", 0),
                "amyloid_pet_suvr": p.get("neuroimaging", {}).get("amyloid_pet_suvr", 0),
                "tau_pet_suvr": p.get("neuroimaging", {}).get("tau_pet_suvr", 0),
                "total_brain": p.get("neuroimaging", {}).get("total_brain", 0),
                "ventricular_volume": p.get("neuroimaging", {}).get("ventricular_volume", 0),
                "csf_abeta42": p.get("biomarkers", {}).get("csf", {}).get("csf_abeta42", 0),
                "csf_ptau181": p.get("biomarkers", {}).get("csf", {}).get("csf_ptau181", 0),
                "csf_total_tau": p.get("biomarkers", {}).get("csf", {}).get("csf_total_tau", 0),
                "amyloid_positive": 1 if p.get("biomarkers", {}).get("amyloid_positive") else 0,
                "tau_positive": 1 if p.get("biomarkers", {}).get("tau_positive") else 0,
                "hypertension": 1 if p.get("medical_history", {}).get("hypertension") else 0,
                "diabetes": 1 if p.get("medical_history", {}).get("diabetes") else 0,
                "cardiovascular": 1 if p.get("medical_history", {}).get("cardiovascular") else 0,
                "depression": 1 if p.get("medical_history", {}).get("depression") else 0,
                "words_per_minute": p.get("speech_analysis", {}).get("words_per_minute", 0),
                "coherence_score": p.get("speech_analysis", {}).get("coherence_score", 0),
                "adl_basic_score": p.get("daily_activities", {}).get("adl_basic_score", 0),
                "adl_instrumental_score": p.get("daily_activities", {}).get("adl_instrumental_score", 0),
                "risk_score": p.get("risk_assessment", {}).get("composite_risk_score", 0)
            }
            rows.append(row)

        df = pd.DataFrame(rows)

    elif data_path.endswith('.csv'):
        # Load CSV format - already flattened
        df = pd.read_csv(data_path)

        # Encode gender if it's a string
        if 'gender' in df.columns and df['gender'].dtype == 'object':
            df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})

        # Ensure boolean fields are 0/1
        bool_cols = ['has_apoe4', 'family_history_ad', 'amyloid_positive', 'tau_positive',
                     'hypertension', 'diabetes', 'cardiovascular', 'depression']
        for col in bool_cols:
            if col in df.columns:
                df[col] = df[col].astype(int)

    print(f"Loaded {len(df):,} records")
    return df


def prepare_features(df):
    """Prepare features and labels"""
    feature_cols = [
        'age', 'gender', 'education_years', 'has_apoe4', 'family_history_ad',
        'mmse_total', 'moca_total', 'adas_cog_13', 'faq_total',
        'hippocampus_left', 'hippocampus_right', 'amyloid_pet_suvr', 'tau_pet_suvr',
        'total_brain', 'ventricular_volume',
        'csf_abeta42', 'csf_ptau181', 'csf_total_tau',
        'amyloid_positive', 'tau_positive',
        'hypertension', 'diabetes', 'cardiovascular', 'depression',
        'words_per_minute', 'coherence_score',
        'adl_basic_score', 'adl_instrumental_score', 'risk_score'
    ]

    # Filter to available columns
    available_cols = [c for c in feature_cols if c in df.columns]
    print(f"Using {len(available_cols)} features")

    # Prepare X and y
    X = df[available_cols].fillna(0).values
    y = df['diagnosis_stage'].values

    return X, y, available_cols


def train_models(X, y, output_dir='models'):
    """Train and save all models"""
    print("\n" + "="*70)
    print("MODEL TRAINING")
    print("="*70)

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nTrain: {len(X_train):,} | Test: {len(X_test):,}")

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Encode labels
    label_encoder = LabelEncoder()
    y_train_encoded = label_encoder.fit_transform(y_train)
    y_test_encoded = label_encoder.transform(y_test)

    print(f"Classes: {list(label_encoder.classes_)}")

    # Define models
    models = {
        'Random Forest': RandomForestClassifier(
            n_estimators=200, max_depth=15, min_samples_split=5,
            n_jobs=-1, random_state=42
        ),
        'Gradient Boosting': GradientBoostingClassifier(
            n_estimators=150, max_depth=8, learning_rate=0.1,
            random_state=42
        ),
        'Neural Network': MLPClassifier(
            hidden_layer_sizes=(128, 64, 32),
            activation='relu', solver='adam', max_iter=500,
            early_stopping=True, random_state=42
        )
    }

    results = {}
    trained_models = {}

    # Train each model
    for name, model in models.items():
        print(f"\n--- Training {name} ---")
        start = datetime.now()

        model.fit(X_train_scaled, y_train_encoded)
        y_pred = model.predict(X_test_scaled)

        accuracy = accuracy_score(y_test_encoded, y_pred)
        precision = precision_score(y_test_encoded, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test_encoded, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test_encoded, y_pred, average='weighted', zero_division=0)

        elapsed = (datetime.now() - start).total_seconds()

        results[name] = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'training_time': elapsed
        }

        trained_models[name] = model

        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1 Score:  {f1:.4f}")
        print(f"  Time:      {elapsed:.2f}s")

    # Create ensemble
    print(f"\n--- Training Ensemble ---")
    estimators = [(name, model) for name, model in trained_models.items()]
    ensemble = VotingClassifier(estimators=estimators, voting='soft')
    ensemble.fit(X_train_scaled, y_train_encoded)

    y_pred = ensemble.predict(X_test_scaled)
    accuracy = accuracy_score(y_test_encoded, y_pred)
    f1 = f1_score(y_test_encoded, y_pred, average='weighted', zero_division=0)

    results['Ensemble'] = {'accuracy': accuracy, 'f1_score': f1}
    trained_models['Ensemble'] = ensemble

    print(f"  Accuracy: {accuracy:.4f}")
    print(f"  F1 Score: {f1:.4f}")

    # Save models
    print(f"\n--- Saving Models ---")
    for name, model in trained_models.items():
        filename = f"{output_dir}/{name.lower().replace(' ', '_')}_model.pkl"
        with open(filename, 'wb') as f:
            pickle.dump(model, f)
        print(f"  Saved: {filename}")

    # Save scaler and encoder
    with open(f"{output_dir}/scaler.pkl", 'wb') as f:
        pickle.dump(scaler, f)
    with open(f"{output_dir}/label_encoder.pkl", 'wb') as f:
        pickle.dump(label_encoder, f)

    print(f"  Saved: {output_dir}/scaler.pkl")
    print(f"  Saved: {output_dir}/label_encoder.pkl")

    # Save results
    with open(f"{output_dir}/training_results.json", 'w') as f:
        json.dump(results, f, indent=2)

    # Generate report
    print("\n" + "="*70)
    print("TRAINING COMPLETE")
    print("="*70)
    print(f"\nModels saved to: {output_dir}/")
    print("\nModel Performance Summary:")
    print("-" * 70)
    for name, res in results.items():
        acc = res.get('accuracy', 0)
        f1_val = res.get('f1_score', 0)
        print(f"{name:<20} | Accuracy: {acc:.4f} | F1: {f1_val:.4f}")

    return trained_models, scaler, label_encoder


if __name__ == "__main__":
    # Find data file
    data_files = [
        "data/sample_training_data.json",
        "data/sample_training_data.csv",
        "data/alzheimers_420k_dataset.json"
    ]

    data_path = None
    for path in data_files:
        if os.path.exists(path):
            data_path = path
            break

    if not data_path:
        print("ERROR: No dataset found. Run generate_sample_data.py first.")
        exit(1)

    # Load data
    df = load_data(data_path)

    # Prepare features
    X, y, feature_names = prepare_features(df)
    print(f"Feature matrix shape: {X.shape}")

    # Train models
    models, scaler, encoder = train_models(X, y, output_dir='models')

    print("\n" + "="*70)
    print("SUCCESS! Models are ready for use.")
    print("="*70)
