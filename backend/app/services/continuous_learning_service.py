"""
Continuous Learning Service
Enables models to learn from new patient data over time
"""

import numpy as np
import pandas as pd
import pickle
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
from loguru import logger
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import json


class ContinuousLearningService:
    """
    Service for continuous model improvement with new data

    Features:
    - Incremental learning with new patient data
    - Performance monitoring and drift detection
    - Automated retraining triggers
    - Model versioning
    """

    def __init__(self, model_path: Path = None):
        self.model_path = model_path or Path(__file__).parent.parent / "ml" / "models"
        self.data_buffer_path = Path("/tmp") / "data_buffer"
        self.data_buffer_path.mkdir(parents=True, exist_ok=True)

        self.model = None
        self.scaler = None
        self.label_encoder = None

        self.performance_history = []
        self.data_buffer = []

        self.min_samples_for_retrain = 100
        self.performance_threshold = 0.90  # Trigger retrain if accuracy drops below this

    def load_model(self, model_name: str = "ensemble_model.pkl"):
        """Load current production model"""
        try:
            model_file = self.model_path / model_name
            with open(model_file, "rb") as f:
                self.model = pickle.load(f)

            scaler_file = self.model_path / "scaler.pkl"
            with open(scaler_file, "rb") as f:
                self.scaler = pickle.load(f)

            label_encoder_file = self.model_path / "label_encoder.pkl"
            with open(label_encoder_file, "rb") as f:
                self.label_encoder = pickle.load(f)

            logger.info(f"Loaded model {model_name} for continuous learning")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def add_new_sample(
        self,
        patient_data: Dict[str, Any],
        true_label: str,
        prediction: str,
        confidence: float
    ):
        """
        Add new patient data to the learning buffer

        Args:
            patient_data: Patient clinical features
            true_label: Ground truth diagnosis (confirmed by clinician)
            prediction: Model's prediction
            confidence: Model confidence in prediction
        """
        try:
            sample = {
                "timestamp": datetime.now().isoformat(),
                "patient_data": patient_data,
                "true_label": true_label,
                "prediction": prediction,
                "confidence": confidence,
                "correct": true_label == prediction
            }

            self.data_buffer.append(sample)

            # Save to disk
            buffer_file = self.data_buffer_path / f"sample_{len(self.data_buffer)}.json"
            with open(buffer_file, "w") as f:
                json.dump(sample, f, indent=2)

            logger.info(f"Added new sample to learning buffer (total: {len(self.data_buffer)})")

            # Check if retraining is needed
            if len(self.data_buffer) >= self.min_samples_for_retrain:
                self.check_and_retrain()

        except Exception as e:
            logger.error(f"Error adding new sample: {e}")
            raise

    def check_and_retrain(self):
        """Check if model performance has degraded and trigger retraining if needed"""
        try:
            # Calculate recent accuracy
            recent_samples = self.data_buffer[-self.min_samples_for_retrain:]
            recent_accuracy = sum(s["correct"] for s in recent_samples) / len(recent_samples)

            logger.info(f"Recent accuracy on {len(recent_samples)} samples: {recent_accuracy:.4f}")

            # Check for concept drift or performance degradation
            if recent_accuracy < self.performance_threshold:
                logger.warning(
                    f"Performance degradation detected! "
                    f"Accuracy {recent_accuracy:.4f} < threshold {self.performance_threshold}"
                )
                self.trigger_retraining()
            else:
                logger.info(f"Model performance is satisfactory ({recent_accuracy:.4f})")

        except Exception as e:
            logger.error(f"Error checking model performance: {e}")

    def trigger_retraining(self):
        """Trigger model retraining with accumulated new data"""
        try:
            logger.info("Triggering model retraining...")

            # Load accumulated data
            X_new, y_new = self._prepare_buffer_data()

            if len(X_new) < 50:
                logger.warning(f"Insufficient data for retraining ({len(X_new)} samples)")
                return

            # Load original training data
            original_data_file = self.model_path.parent.parent / "data" / "synthetic_alzheimers_data.csv"

            if original_data_file.exists():
                df_original = pd.read_csv(original_data_file)

                # Encode gender
                if 'gender' in df_original.columns and df_original['gender'].dtype == 'object':
                    df_original['gender'] = df_original['gender'].map({'Male': 0, 'Female': 1})

                X_original = df_original.drop(['patient_id', 'stage'], axis=1, errors='ignore')
                y_original = df_original['stage']

                # Combine original and new data
                X_combined = pd.concat([X_original, pd.DataFrame(X_new, columns=X_original.columns)])
                y_combined = pd.concat([y_original, pd.Series(y_new)])

            else:
                # Use only new data if original not available
                X_combined = pd.DataFrame(X_new)
                y_combined = pd.Series(y_new)

            logger.info(f"Combined dataset size: {len(X_combined)} samples")

            # Retrain model
            self._retrain_model(X_combined, y_combined)

        except Exception as e:
            logger.error(f"Error during retraining: {e}")

    def _prepare_buffer_data(self) -> tuple:
        """Convert buffer data to training format"""
        X = []
        y = []

        for sample in self.data_buffer:
            features = self._extract_features(sample["patient_data"])
            X.append(features)
            y.append(sample["true_label"])

        return np.array(X), y

    def _extract_features(self, patient_data: Dict) -> list:
        """Extract features from patient data"""
        features = [
            patient_data.get('age', 70),
            patient_data.get('gender', 0),
            patient_data.get('education_years', 14),
            patient_data.get('apoe4_positive', 0),
            patient_data.get('mmse_score', 24),
            patient_data.get('moca_score', 22),
            patient_data.get('cdr_score', 0),
            patient_data.get('gds_score', 5),
            patient_data.get('faq_score', 0),
            patient_data.get('adas_cog_score', 10),
            patient_data.get('npi_score', 0),
            patient_data.get('hippocampal_volume', 3200),
            patient_data.get('ventricular_volume', 45000),
            patient_data.get('brain_volume', 1100000),
            patient_data.get('csf_abeta', 650),
            patient_data.get('csf_tau', 350),
            patient_data.get('csf_ptau', 50),
            patient_data.get('fdg_pet', 1.3),
            patient_data.get('pib_pet', 1.4),
            patient_data.get('av45_pet', 1.2),
            patient_data.get('speech_pause_ratio', 0.1),
            patient_data.get('word_finding_difficulty', 2),
            patient_data.get('gait_speed', 1.0),
            patient_data.get('stride_variability', 0.1),
            patient_data.get('sleep_efficiency', 0.85),
            patient_data.get('rem_sleep_percentage', 0.20),
            patient_data.get('physical_activity_minutes', 30),
            patient_data.get('social_engagement_score', 6),
            patient_data.get('cognitive_reserve_score', 100)
        ]
        return features

    def _retrain_model(self, X: pd.DataFrame, y: pd.Series):
        """Retrain model with new data"""
        try:
            from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
            from sklearn.neural_network import MLPClassifier
            from sklearn.preprocessing import StandardScaler, LabelEncoder

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

            # Train ensemble model (using same architecture as original)
            models = {
                'rf': RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1),
                'gb': GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=7, random_state=42),
                'nn': MLPClassifier(hidden_layers=(128, 64, 32), max_iter=500, random_state=42)
            }

            # Train individual models
            for name, model in models.items():
                logger.info(f"Training {name}...")
                model.fit(X_train_scaled, y_train)

            # Create ensemble (simple voting)
            from sklearn.ensemble import VotingClassifier
            ensemble = VotingClassifier(
                estimators=list(models.items()),
                voting='soft',
                n_jobs=-1
            )

            logger.info("Training ensemble...")
            ensemble.fit(X_train_scaled, y_train)

            # Evaluate
            y_pred = ensemble.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)

            logger.info(f"\nRetrained Model Performance:")
            logger.info(f"Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
            logger.info(f"\nClassification Report:")
            logger.info(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

            # Save new model with version
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_model_file = self.model_path / f"ensemble_model_v{version}.pkl"

            with open(new_model_file, "wb") as f:
                pickle.dump(ensemble, f)

            with open(self.model_path / "scaler.pkl", "wb") as f:
                pickle.dump(scaler, f)

            with open(self.model_path / "label_encoder.pkl", "wb") as f:
                pickle.dump(label_encoder, f)

            # Update production model if performance is better
            if accuracy >= self.performance_threshold:
                with open(self.model_path / "ensemble_model.pkl", "wb") as f:
                    pickle.dump(ensemble, f)

                logger.info(f"✓ Updated production model (accuracy: {accuracy:.4f})")

                # Clear buffer after successful retraining
                self.data_buffer = []
                for f in self.data_buffer_path.glob("sample_*.json"):
                    f.unlink()

            # Log performance history
            self.performance_history.append({
                "timestamp": datetime.now().isoformat(),
                "version": version,
                "accuracy": accuracy,
                "samples_used": len(X)
            })

            # Save performance history
            with open(self.model_path / "performance_history.json", "w") as f:
                json.dump(self.performance_history, f, indent=2)

        except Exception as e:
            logger.error(f"Error retraining model: {e}")
            raise

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current model performance metrics"""
        try:
            if not self.data_buffer:
                return {
                    "buffer_size": 0,
                    "recent_accuracy": None,
                    "message": "No new data in buffer"
                }

            recent_samples = self.data_buffer[-min(100, len(self.data_buffer)):]
            recent_accuracy = sum(s["correct"] for s in recent_samples) / len(recent_samples)

            # Average confidence
            avg_confidence = np.mean([s["confidence"] for s in recent_samples])

            return {
                "buffer_size": len(self.data_buffer),
                "recent_accuracy": recent_accuracy,
                "average_confidence": avg_confidence,
                "samples_until_retrain": max(0, self.min_samples_for_retrain - len(self.data_buffer)),
                "performance_history": self.performance_history[-5:]  # Last 5 retraining events
            }

        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return {"error": str(e)}


# Singleton instance
continuous_learning_service = ContinuousLearningService()
