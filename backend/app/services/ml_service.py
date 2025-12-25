"""
ML Model Service for loading and inference
Provides a singleton service to load trained models and make predictions
"""
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MLModelService:
    """Singleton service for ML model operations"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLModelService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.model_path = Path(__file__).parent.parent / "ml" / "models"
        self.traditional_models = {}
        self.scaler = None
        self.label_encoder = None
        self.models_loaded = False
        self._initialized = True

        logger.info(f"ML Service initialized. Model path: {self.model_path}")

    def load_traditional_models(self) -> bool:
        """
        Load scikit-learn models for Alzheimer's stage prediction

        Returns:
            bool: True if models loaded successfully
        """
        try:
            # Check if model files exist
            ensemble_path = self.model_path / "ensemble_model.pkl"
            scaler_path = self.model_path / "scaler.pkl"
            encoder_path = self.model_path / "label_encoder.pkl"

            if not ensemble_path.exists():
                logger.warning(f"Ensemble model not found at {ensemble_path}")
                return False

            # Load ensemble model
            with open(ensemble_path, "rb") as f:
                self.traditional_models["ensemble"] = pickle.load(f)
            logger.info("Loaded ensemble model")

            # Load scaler
            with open(scaler_path, "rb") as f:
                self.scaler = pickle.load(f)
            logger.info("Loaded feature scaler")

            # Load label encoder
            with open(encoder_path, "rb") as f:
                self.label_encoder = pickle.load(f)
            logger.info("Loaded label encoder")

            # Try to load individual models for feature importance
            for model_name in ["random_forest_model", "gradient_boosting_model", "neural_network_model"]:
                model_file = self.model_path / f"{model_name}.pkl"
                if model_file.exists():
                    with open(model_file, "rb") as f:
                        self.traditional_models[model_name] = pickle.load(f)
                    logger.info(f"Loaded {model_name}")

            self.models_loaded = True
            logger.info("All traditional ML models loaded successfully")
            return True

        except Exception as e:
            logger.error(f"Error loading traditional models: {e}")
            return False

    def predict_stage(self, patient_data: Dict) -> Dict[str, Any]:
        """
        Predict Alzheimer's stage using traditional ML ensemble

        Args:
            patient_data: Dictionary containing patient features

        Returns:
            Dictionary with prediction results
        """
        if not self.models_loaded:
            logger.info("Models not loaded, attempting to load...")
            if not self.load_traditional_models():
                return self._get_mock_prediction(patient_data)

        try:
            # Extract and prepare features
            features = self._extract_features(patient_data)

            # Scale features
            features_scaled = self.scaler.transform([features])

            # Get ensemble model
            model = self.traditional_models["ensemble"]

            # Predict
            prediction = model.predict(features_scaled)[0]
            probabilities = model.predict_proba(features_scaled)[0]

            # Decode stage
            predicted_stage = self.label_encoder.inverse_transform([prediction])[0]

            # Map to numeric stage (0-7)
            stage_mapping = {
                "normal": 0,
                "mci": 1,
                "mild_ad": 2,
                "moderate_ad": 4,
                "severe_ad": 6
            }

            numeric_stage = stage_mapping.get(predicted_stage, 1)

            # Calculate stage probabilities
            stage_probs = {}
            for idx, prob in enumerate(probabilities):
                stage_name = self.label_encoder.classes_[idx]
                stage_num = stage_mapping.get(stage_name, 1)
                stage_probs[str(stage_num)] = round(float(prob), 4)

            # Determine progression risk
            confidence = float(max(probabilities))
            if predicted_stage in ["moderate_ad", "severe_ad"]:
                progression_risk = "high"
                estimated_months = np.random.randint(3, 12)
            elif predicted_stage == "mild_ad":
                progression_risk = "medium"
                estimated_months = np.random.randint(12, 24)
            elif predicted_stage == "mci":
                progression_risk = "low"
                estimated_months = np.random.randint(24, 48)
            else:
                progression_risk = "very_low"
                estimated_months = None

            # Get contributing factors
            contributing_factors = self._get_contributing_factors(patient_data, predicted_stage)

            return {
                "predicted_stage": numeric_stage,
                "stage_name": predicted_stage,
                "confidence": round(confidence, 4),
                "stage_probabilities": stage_probs,
                "progression_risk": progression_risk,
                "estimated_progression_months": estimated_months,
                "top_contributing_factors": contributing_factors,
                "model_version": "1.0.0",
                "prediction_timestamp": datetime.utcnow().isoformat()
            }

        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return self._get_mock_prediction(patient_data)

    def _extract_features(self, patient_data: Dict) -> List[float]:
        """Extract features from patient data in correct order"""

        # Feature order must match training data
        features = [
            patient_data.get("age", 70),
            1 if patient_data.get("gender") == "Female" else 0,
            patient_data.get("education_years", 12),
            1 if patient_data.get("has_apoe4", False) else 0,
            1 if patient_data.get("family_history_ad", False) else 0,
            patient_data.get("mmse_total", 25),
            patient_data.get("moca_total", 24),
            patient_data.get("adas_cog_13", 15),
            patient_data.get("faq_total", 5),
            patient_data.get("hippocampus_left", 3.0),
            patient_data.get("hippocampus_right", 3.0),
            patient_data.get("amyloid_pet_suvr", 1.2),
            patient_data.get("tau_pet_suvr", 1.3),
            patient_data.get("total_brain", 1200),
            patient_data.get("ventricular_volume", 30),
            patient_data.get("csf_abeta42", 600),
            patient_data.get("csf_ptau181", 40),
            patient_data.get("csf_total_tau", 500),
            1 if patient_data.get("amyloid_positive", False) else 0,
            1 if patient_data.get("tau_positive", False) else 0,
            1 if patient_data.get("hypertension", False) else 0,
            1 if patient_data.get("diabetes", False) else 0,
            1 if patient_data.get("cardiovascular", False) else 0,
            1 if patient_data.get("depression", False) else 0,
            patient_data.get("words_per_minute", 120),
            patient_data.get("coherence_score", 0.8),
            patient_data.get("adl_basic_score", 5),
            patient_data.get("adl_instrumental_score", 7),
            patient_data.get("risk_score", 0.3)
        ]

        return features

    def _get_contributing_factors(self, patient_data: Dict, predicted_stage: str) -> List[str]:
        """Identify key contributing factors for the prediction"""

        factors = []

        # Cognitive scores
        mmse = patient_data.get("mmse_total", 25)
        if mmse < 24:
            factors.append(f"MMSE score of {mmse}/30 indicates cognitive impairment")

        moca = patient_data.get("moca_total", 24)
        if moca < 26:
            factors.append(f"MoCA score of {moca}/30 suggests memory deficits")

        # Biomarkers
        if patient_data.get("amyloid_positive", False):
            factors.append("Elevated amyloid PET scan indicates β-amyloid plaques")

        if patient_data.get("tau_positive", False):
            factors.append("Elevated tau PET scan shows neurofibrillary tangles")

        # Hippocampal atrophy
        hippo_left = patient_data.get("hippocampus_left", 3.0)
        hippo_right = patient_data.get("hippocampus_right", 3.0)
        avg_hippo = (hippo_left + hippo_right) / 2
        if avg_hippo < 2.5:
            factors.append(f"Significant hippocampal atrophy detected ({avg_hippo:.1f} cm³)")

        # Genetics
        if patient_data.get("has_apoe4", False):
            factors.append("APOE4 gene presence increases AD risk")

        # Age
        age = patient_data.get("age", 70)
        if age > 75:
            factors.append(f"Age {age} is a significant risk factor")

        # Speech
        wpm = patient_data.get("words_per_minute", 120)
        if wpm < 100:
            factors.append(f"Reduced speech fluency ({wpm:.0f} words/min)")

        # Return top 5 factors
        return factors[:5] if factors else ["Assessment based on comprehensive clinical evaluation"]

    def _get_mock_prediction(self, patient_data: Dict) -> Dict[str, Any]:
        """Return mock prediction when models aren't available"""

        logger.warning("Using mock prediction - models not loaded")

        # Simple heuristic based on MMSE
        mmse = patient_data.get("mmse_total", 25)

        if mmse >= 27:
            stage = 0
            stage_name = "normal"
            probs = {"0": 0.85, "1": 0.10, "2": 0.03, "3": 0.01, "4": 0.01}
            risk = "very_low"
        elif mmse >= 24:
            stage = 1
            stage_name = "mci"
            probs = {"0": 0.05, "1": 0.75, "2": 0.15, "3": 0.03, "4": 0.02}
            risk = "low"
        elif mmse >= 20:
            stage = 2
            stage_name = "mild_ad"
            probs = {"0": 0.02, "1": 0.10, "2": 0.75, "3": 0.10, "4": 0.03}
            risk = "medium"
        elif mmse >= 10:
            stage = 4
            stage_name = "moderate_ad"
            probs = {"0": 0.01, "1": 0.02, "2": 0.10, "3": 0.75, "4": 0.12}
            risk = "high"
        else:
            stage = 6
            stage_name = "severe_ad"
            probs = {"0": 0.00, "1": 0.01, "2": 0.02, "3": 0.10, "4": 0.87}
            risk = "high"

        return {
            "predicted_stage": stage,
            "stage_name": stage_name,
            "confidence": 0.75,
            "stage_probabilities": probs,
            "progression_risk": risk,
            "estimated_progression_months": 18 if risk != "very_low" else None,
            "top_contributing_factors": self._get_contributing_factors(patient_data, stage_name),
            "model_version": "mock-1.0.0",
            "prediction_timestamp": datetime.utcnow().isoformat(),
            "note": "Using heuristic prediction - ML models not loaded"
        }

    def predict_memory_decay(self, memory_graph: Dict) -> Dict[str, Any]:
        """
        Predict memory decay for patient's memory graph
        TODO: Implement MemoryGNN inference when PyTorch models are available

        Args:
            memory_graph: Dictionary containing memory nodes and connections

        Returns:
            Dictionary with memory decay predictions
        """
        logger.warning("Memory decay prediction using heuristic - GNN model not implemented")

        # Mock implementation for now
        memories = memory_graph.get("memories", [])
        high_risk_memories = []

        for memory in memories:
            recall_strength = memory.get("recall_strength", 80)
            memory_type = memory.get("type", "person")

            # Simple heuristic: lower recall = higher risk
            decay_probability = 1.0 - (recall_strength / 100.0)

            if decay_probability > 0.6:  # High risk threshold
                days_critical = int((recall_strength / 100.0) * 30)

                high_risk_memories.append({
                    "memory_id": memory.get("id"),
                    "name": memory.get("name"),
                    "type": memory_type,
                    "decay_probability": round(decay_probability, 2),
                    "days_until_critical": days_critical,
                    "intervention_recommended": decay_probability > 0.75
                })

        # Sort by decay probability
        high_risk_memories.sort(key=lambda x: x["decay_probability"], reverse=True)

        return {
            "patient_id": memory_graph.get("patient_id"),
            "high_risk_memories": high_risk_memories[:10],  # Top 10
            "total_memories": len(memories),
            "at_risk_count": len([m for m in memories if (1.0 - m.get("recall_strength", 80) / 100.0) > 0.4]),
            "intervention_recommended_count": len([m for m in high_risk_memories if m["intervention_recommended"]]),
            "model_version": "heuristic-1.0.0",
            "prediction_timestamp": datetime.utcnow().isoformat()
        }


# Singleton instance
ml_service = MLModelService()
