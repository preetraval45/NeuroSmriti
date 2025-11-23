"""
NeuroSmriti - Alzheimer's Detection Model Training and Testing
Trains machine learning models on the 400K+ synthetic dataset

Models:
1. Random Forest - For baseline classification
2. XGBoost - For high-performance gradient boosting
3. Neural Network - Deep learning approach
4. Ensemble - Combined model for best accuracy
"""

import json
import os
import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Any
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

# Try importing optional dependencies
try:
    import xgboost as xgb
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("XGBoost not installed. Using GradientBoosting instead.")


class AlzheimersModelTrainer:
    """Train and evaluate Alzheimer's detection models."""

    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models = {}
        self.results = {}

    def load_data(self, data_path: str = None) -> pd.DataFrame:
        """Load dataset from JSON or CSV."""
        path = data_path or self.data_path

        if path.endswith('.json'):
            print(f"Loading JSON data from {path}...")
            with open(path, 'r') as f:
                data = json.load(f)

            if 'data' in data:
                records = data['data']
            else:
                records = data

            # Flatten nested JSON to DataFrame
            rows = []
            for p in records:
                row = self._flatten_patient(p)
                rows.append(row)

            df = pd.DataFrame(rows)

        elif path.endswith('.csv'):
            print(f"Loading CSV data from {path}...")
            df = pd.read_csv(path)

        else:
            raise ValueError("Unsupported file format. Use .json or .csv")

        print(f"Loaded {len(df):,} records with {len(df.columns)} features")
        return df

    def _flatten_patient(self, p: Dict) -> Dict:
        """Flatten nested patient record for ML processing."""
        row = {
            "patient_id": p.get("patient_id", ""),
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
        return row

    def prepare_features(self, df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare features and labels for training."""
        # Define feature columns
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

        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)

        # Scale features
        X_scaled = self.scaler.fit_transform(X)

        return X_scaled, y_encoded, available_cols

    def train_models(self, X: np.ndarray, y: np.ndarray, test_size: float = 0.2):
        """Train multiple models and evaluate performance."""
        print("\n" + "=" * 60)
        print("MODEL TRAINING")
        print("=" * 60)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        print(f"\nTraining set: {len(X_train):,} samples")
        print(f"Test set: {len(X_test):,} samples")

        # Define models
        models_to_train = {
            'Random Forest': RandomForestClassifier(
                n_estimators=200,
                max_depth=15,
                min_samples_split=5,
                n_jobs=-1,
                random_state=42
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=150,
                max_depth=8,
                learning_rate=0.1,
                random_state=42
            ),
            'Neural Network': MLPClassifier(
                hidden_layer_sizes=(128, 64, 32),
                activation='relu',
                solver='adam',
                max_iter=500,
                early_stopping=True,
                random_state=42
            )
        }

        if HAS_XGB:
            models_to_train['XGBoost'] = xgb.XGBClassifier(
                n_estimators=200,
                max_depth=10,
                learning_rate=0.1,
                use_label_encoder=False,
                eval_metric='mlogloss',
                random_state=42
            )

        # Train and evaluate each model
        for name, model in models_to_train.items():
            print(f"\n--- Training {name} ---")
            start_time = datetime.now()

            # Train
            model.fit(X_train, y_train)

            # Predict
            y_pred = model.predict(X_test)
            y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None

            # Calculate metrics
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')

            # ROC AUC for multi-class
            if y_pred_proba is not None:
                try:
                    roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='weighted')
                except:
                    roc_auc = None
            else:
                roc_auc = None

            training_time = (datetime.now() - start_time).total_seconds()

            # Store results
            self.models[name] = model
            self.results[name] = {
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': f1,
                'roc_auc': roc_auc,
                'training_time': training_time,
                'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
                'classification_report': classification_report(y_test, y_pred, target_names=self.label_encoder.classes_)
            }

            print(f"  Accuracy: {accuracy:.4f}")
            print(f"  Precision: {precision:.4f}")
            print(f"  Recall: {recall:.4f}")
            print(f"  F1 Score: {f1:.4f}")
            if roc_auc:
                print(f"  ROC AUC: {roc_auc:.4f}")
            print(f"  Training Time: {training_time:.2f}s")

        # Create ensemble model
        print(f"\n--- Training Ensemble Model ---")
        estimators = [(name, model) for name, model in self.models.items() if name != 'Ensemble']
        ensemble = VotingClassifier(estimators=estimators, voting='soft')
        ensemble.fit(X_train, y_train)

        y_pred = ensemble.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')

        self.models['Ensemble'] = ensemble
        self.results['Ensemble'] = {
            'accuracy': accuracy,
            'f1_score': f1
        }
        print(f"  Ensemble Accuracy: {accuracy:.4f}")
        print(f"  Ensemble F1 Score: {f1:.4f}")

        # Store test data for later evaluation
        self.X_test = X_test
        self.y_test = y_test

        return self.results

    def cross_validate(self, X: np.ndarray, y: np.ndarray, cv: int = 5):
        """Perform cross-validation on best model."""
        print(f"\n--- {cv}-Fold Cross Validation ---")

        cv_results = {}
        skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)

        for name, model in self.models.items():
            if name == 'Ensemble':
                continue

            scores = cross_val_score(model, X, y, cv=skf, scoring='accuracy', n_jobs=-1)
            cv_results[name] = {
                'mean_accuracy': scores.mean(),
                'std_accuracy': scores.std(),
                'scores': scores.tolist()
            }
            print(f"  {name}: {scores.mean():.4f} (+/- {scores.std()*2:.4f})")

        return cv_results

    def feature_importance(self, feature_names: List[str]) -> pd.DataFrame:
        """Get feature importance from tree-based models."""
        print("\n--- Feature Importance ---")

        importance_data = []

        for name in ['Random Forest', 'Gradient Boosting', 'XGBoost']:
            if name in self.models:
                model = self.models[name]
                if hasattr(model, 'feature_importances_'):
                    importances = model.feature_importances_
                    for feat, imp in zip(feature_names, importances):
                        importance_data.append({
                            'model': name,
                            'feature': feat,
                            'importance': imp
                        })

        if importance_data:
            df = pd.DataFrame(importance_data)
            avg_importance = df.groupby('feature')['importance'].mean().sort_values(ascending=False)
            print("\nTop 10 Most Important Features:")
            for i, (feat, imp) in enumerate(avg_importance.head(10).items()):
                print(f"  {i+1}. {feat}: {imp:.4f}")
            return df

        return pd.DataFrame()

    def save_models(self, output_dir: str = "models"):
        """Save trained models to disk."""
        os.makedirs(output_dir, exist_ok=True)

        # Save models
        for name, model in self.models.items():
            filename = f"{output_dir}/{name.lower().replace(' ', '_')}_model.pkl"
            with open(filename, 'wb') as f:
                pickle.dump(model, f)
            print(f"Saved {name} to {filename}")

        # Save scaler and encoder
        with open(f"{output_dir}/scaler.pkl", 'wb') as f:
            pickle.dump(self.scaler, f)
        with open(f"{output_dir}/label_encoder.pkl", 'wb') as f:
            pickle.dump(self.label_encoder, f)

        # Save results
        with open(f"{output_dir}/training_results.json", 'w') as f:
            # Convert numpy arrays to lists
            results_json = {}
            for name, res in self.results.items():
                results_json[name] = {k: v if not isinstance(v, np.ndarray) else v.tolist() for k, v in res.items()}
            json.dump(results_json, f, indent=2)

        print(f"\nAll models saved to {output_dir}/")

    def generate_report(self) -> str:
        """Generate a comprehensive training report."""
        report = []
        report.append("=" * 70)
        report.append("NEUROSMRITI - ALZHEIMER'S DETECTION MODEL TRAINING REPORT")
        report.append("=" * 70)
        report.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        report.append("\n\n## MODEL PERFORMANCE SUMMARY\n")
        report.append("-" * 50)

        # Create comparison table
        metrics = ['accuracy', 'precision', 'recall', 'f1_score', 'roc_auc']
        header = f"{'Model':<20} | " + " | ".join([f"{m:<12}" for m in metrics])
        report.append(header)
        report.append("-" * len(header))

        for name, results in self.results.items():
            row = f"{name:<20} | "
            for metric in metrics:
                val = results.get(metric)
                if val is not None:
                    row += f"{val:<12.4f} | "
                else:
                    row += f"{'N/A':<12} | "
            report.append(row)

        report.append("\n\n## CLASSIFICATION REPORTS\n")

        for name, results in self.results.items():
            if 'classification_report' in results:
                report.append(f"\n### {name}")
                report.append("-" * 40)
                report.append(results['classification_report'])

        report.append("\n\n## BEST MODEL RECOMMENDATION\n")

        # Find best model
        best_model = max(self.results.items(), key=lambda x: x[1].get('f1_score', 0))
        report.append(f"Best Model: {best_model[0]}")
        report.append(f"F1 Score: {best_model[1]['f1_score']:.4f}")
        report.append(f"Accuracy: {best_model[1]['accuracy']:.4f}")

        return "\n".join(report)


def run_training_pipeline(data_path: str = None):
    """Run the complete training pipeline."""
    print("\n" + "=" * 70)
    print("NEUROSMRITI - ALZHEIMER'S DETECTION MODEL TRAINING")
    print("=" * 70 + "\n")

    # Initialize trainer
    trainer = AlzheimersModelTrainer()

    # Find data file
    if data_path is None:
        possible_paths = [
            "data/alzheimers_420k_dataset.json",
            "data/alzheimers_420k_dataset.csv",
            "data/alzheimers_400k_dataset.json",
            "data/sample_alzheimers_data.json"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                data_path = path
                break

    if data_path is None or not os.path.exists(data_path):
        print("No dataset found. Generating sample data...")
        from data.generate_large_dataset import generate_large_dataset
        generate_large_dataset(
            total_patients=10000,  # Small sample for testing
            output_json="data/sample_training_data.json",
            output_csv="data/sample_training_data.csv"
        )
        data_path = "data/sample_training_data.csv"

    # Load data
    df = trainer.load_data(data_path)

    # Prepare features
    X, y, feature_names = trainer.prepare_features(df)
    print(f"\nFeature matrix shape: {X.shape}")
    print(f"Label distribution: {dict(zip(*np.unique(y, return_counts=True)))}")

    # Train models
    results = trainer.train_models(X, y)

    # Cross-validation
    cv_results = trainer.cross_validate(X, y)

    # Feature importance
    importance_df = trainer.feature_importance(feature_names)

    # Save models
    trainer.save_models("models")

    # Generate report
    report = trainer.generate_report()
    print("\n" + report)

    # Save report
    with open("models/training_report.txt", 'w') as f:
        f.write(report)

    print("\n" + "=" * 70)
    print("TRAINING COMPLETE")
    print("=" * 70)

    return trainer


if __name__ == "__main__":
    run_training_pipeline()
