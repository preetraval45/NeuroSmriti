"""
Model Explainability Service using SHAP and LIME
Provides interpretable explanations for ML model predictions
"""

import numpy as np
import shap
import lime
import lime.lime_tabular
from typing import Dict, List, Any, Optional
import pickle
from pathlib import Path
import pandas as pd
from loguru import logger


class ExplainabilityService:
    """Service for generating model explanations using SHAP and LIME"""

    def __init__(self, model_path: Path = None):
        self.model_path = model_path or Path(__file__).parent.parent / "ml" / "models"
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        self.shap_explainer = None
        self.lime_explainer = None
        self.background_data = None

    def load_model(self, model_name: str = "ensemble_model.pkl"):
        """Load trained model and preprocessing objects"""
        try:
            # Load model
            model_file = self.model_path / model_name
            with open(model_file, "rb") as f:
                self.model = pickle.load(f)

            # Load scaler
            scaler_file = self.model_path / "scaler.pkl"
            with open(scaler_file, "rb") as f:
                self.scaler = pickle.load(f)

            # Load label encoder
            label_encoder_file = self.model_path / "label_encoder.pkl"
            with open(label_encoder_file, "rb") as f:
                self.label_encoder = pickle.load(f)

            # Define feature names (29 clinical features)
            self.feature_names = [
                'age', 'gender', 'education_years', 'apoe4_positive',
                'mmse_score', 'moca_score', 'cdr_score', 'gds_score',
                'faq_score', 'adas_cog_score', 'npi_score',
                'hippocampal_volume', 'ventricular_volume', 'brain_volume',
                'csf_abeta', 'csf_tau', 'csf_ptau', 'fdg_pet',
                'pib_pet', 'av45_pet', 'speech_pause_ratio',
                'word_finding_difficulty', 'gait_speed', 'stride_variability',
                'sleep_efficiency', 'rem_sleep_percentage',
                'physical_activity_minutes', 'social_engagement_score',
                'cognitive_reserve_score'
            ]

            logger.info(f"Loaded model {model_name} for explainability")

        except Exception as e:
            logger.error(f"Error loading model for explainability: {e}")
            raise

    def initialize_explainers(self, background_data: np.ndarray = None):
        """Initialize SHAP and LIME explainers"""
        try:
            if background_data is not None:
                self.background_data = background_data
            else:
                # Use synthetic background data if none provided
                self.background_data = self._generate_background_data()

            # Initialize SHAP explainer (TreeExplainer for ensemble models)
            if hasattr(self.model, 'estimators_'):
                # Ensemble model - use TreeExplainer
                self.shap_explainer = shap.TreeExplainer(self.model)
            else:
                # Use KernelExplainer as fallback
                self.shap_explainer = shap.KernelExplainer(
                    self.model.predict_proba,
                    self.background_data[:100]  # Use sample for kernel explainer
                )

            # Initialize LIME explainer
            self.lime_explainer = lime.lime_tabular.LimeTabularExplainer(
                training_data=self.background_data,
                feature_names=self.feature_names,
                class_names=self.label_encoder.classes_.tolist(),
                mode='classification',
                discretize_continuous=True
            )

            logger.info("Initialized SHAP and LIME explainers")

        except Exception as e:
            logger.error(f"Error initializing explainers: {e}")
            raise

    def _generate_background_data(self, n_samples: int = 1000) -> np.ndarray:
        """Generate synthetic background data for explainers"""
        np.random.seed(42)

        # Generate realistic ranges for each feature
        background = np.column_stack([
            np.random.normal(72, 8, n_samples),  # age
            np.random.randint(0, 2, n_samples),  # gender
            np.random.normal(14, 3, n_samples),  # education_years
            np.random.randint(0, 2, n_samples),  # apoe4_positive
            np.random.normal(24, 5, n_samples),  # mmse_score
            np.random.normal(22, 5, n_samples),  # moca_score
            np.random.uniform(0, 2, n_samples),  # cdr_score
            np.random.normal(5, 3, n_samples),   # gds_score
            np.random.normal(8, 7, n_samples),   # faq_score
            np.random.normal(18, 10, n_samples), # adas_cog_score
            np.random.normal(8, 6, n_samples),   # npi_score
            np.random.normal(3200, 500, n_samples),  # hippocampal_volume
            np.random.normal(45000, 15000, n_samples),  # ventricular_volume
            np.random.normal(1100000, 100000, n_samples),  # brain_volume
            np.random.normal(650, 200, n_samples),  # csf_abeta
            np.random.normal(350, 150, n_samples),  # csf_tau
            np.random.normal(50, 25, n_samples),  # csf_ptau
            np.random.normal(1.3, 0.2, n_samples),  # fdg_pet
            np.random.normal(1.4, 0.3, n_samples),  # pib_pet
            np.random.normal(1.2, 0.3, n_samples),  # av45_pet
            np.random.uniform(0, 0.3, n_samples),  # speech_pause_ratio
            np.random.randint(0, 10, n_samples),  # word_finding_difficulty
            np.random.normal(1.0, 0.2, n_samples),  # gait_speed
            np.random.normal(0.1, 0.05, n_samples),  # stride_variability
            np.random.uniform(0.7, 0.95, n_samples),  # sleep_efficiency
            np.random.uniform(0.15, 0.25, n_samples),  # rem_sleep_percentage
            np.random.normal(30, 15, n_samples),  # physical_activity_minutes
            np.random.normal(6, 2, n_samples),  # social_engagement_score
            np.random.normal(100, 15, n_samples)  # cognitive_reserve_score
        ])

        # Scale the background data
        background_scaled = self.scaler.transform(background)

        return background_scaled

    def explain_with_shap(self, features: np.ndarray, top_n: int = 10) -> Dict[str, Any]:
        """
        Generate SHAP explanations for a prediction

        Args:
            features: Scaled feature array (1D or 2D)
            top_n: Number of top features to return

        Returns:
            Dictionary with SHAP values and feature importance
        """
        try:
            if self.shap_explainer is None:
                self.initialize_explainers()

            # Ensure 2D array
            if len(features.shape) == 1:
                features = features.reshape(1, -1)

            # Calculate SHAP values
            shap_values = self.shap_explainer.shap_values(features)

            # For multi-class, shap_values is a list of arrays (one per class)
            if isinstance(shap_values, list):
                # Use the predicted class
                predicted_class = self.model.predict(features)[0]
                class_idx = np.where(self.label_encoder.classes_ == predicted_class)[0][0]
                shap_values_for_pred = shap_values[class_idx][0]
            else:
                shap_values_for_pred = shap_values[0]

            # Get feature importance (absolute SHAP values)
            feature_importance = np.abs(shap_values_for_pred)

            # Sort features by importance
            top_indices = np.argsort(feature_importance)[-top_n:][::-1]

            top_features = []
            for idx in top_indices:
                top_features.append({
                    "feature": self.feature_names[idx],
                    "shap_value": float(shap_values_for_pred[idx]),
                    "importance": float(feature_importance[idx]),
                    "feature_value": float(features[0][idx])
                })

            return {
                "method": "SHAP",
                "top_features": top_features,
                "base_value": float(self.shap_explainer.expected_value) if hasattr(self.shap_explainer, 'expected_value') else 0.0,
                "explanation": self._generate_shap_explanation(top_features)
            }

        except Exception as e:
            logger.error(f"Error generating SHAP explanation: {e}")
            raise

    def explain_with_lime(self, features: np.ndarray, top_n: int = 10) -> Dict[str, Any]:
        """
        Generate LIME explanations for a prediction

        Args:
            features: Scaled feature array (1D or 2D)
            top_n: Number of top features to return

        Returns:
            Dictionary with LIME explanations and feature importance
        """
        try:
            if self.lime_explainer is None:
                self.initialize_explainers()

            # Ensure 1D array for LIME
            if len(features.shape) == 2:
                features = features[0]

            # Generate LIME explanation
            explanation = self.lime_explainer.explain_instance(
                features,
                self.model.predict_proba,
                num_features=top_n,
                top_labels=1
            )

            # Extract feature importance
            predicted_class = self.model.predict(features.reshape(1, -1))[0]
            class_idx = np.where(self.label_encoder.classes_ == predicted_class)[0][0]

            lime_list = explanation.as_list(label=class_idx)

            top_features = []
            for feature_desc, weight in lime_list[:top_n]:
                # Parse feature description (format: "feature_name <= value" or "feature_name > value")
                feature_name = feature_desc.split()[0]
                top_features.append({
                    "feature": feature_name,
                    "lime_weight": float(weight),
                    "importance": abs(float(weight)),
                    "description": feature_desc
                })

            return {
                "method": "LIME",
                "top_features": top_features,
                "prediction_probability": float(explanation.predict_proba[class_idx]),
                "explanation": self._generate_lime_explanation(top_features, predicted_class)
            }

        except Exception as e:
            logger.error(f"Error generating LIME explanation: {e}")
            raise

    def get_comprehensive_explanation(
        self,
        features: np.ndarray,
        top_n: int = 10
    ) -> Dict[str, Any]:
        """
        Get both SHAP and LIME explanations for comprehensive interpretability

        Args:
            features: Scaled feature array
            top_n: Number of top features to return

        Returns:
            Dictionary with both SHAP and LIME explanations
        """
        try:
            shap_explanation = self.explain_with_shap(features, top_n)
            lime_explanation = self.explain_with_lime(features, top_n)

            # Get prediction
            prediction = self.model.predict(features.reshape(1, -1))[0]
            prediction_proba = self.model.predict_proba(features.reshape(1, -1))[0]

            # Combine explanations
            return {
                "prediction": prediction,
                "prediction_confidence": float(np.max(prediction_proba)),
                "all_class_probabilities": {
                    cls: float(prob)
                    for cls, prob in zip(self.label_encoder.classes_, prediction_proba)
                },
                "shap": shap_explanation,
                "lime": lime_explanation,
                "consensus_features": self._find_consensus_features(
                    shap_explanation["top_features"],
                    lime_explanation["top_features"]
                )
            }

        except Exception as e:
            logger.error(f"Error generating comprehensive explanation: {e}")
            raise

    def _generate_shap_explanation(self, top_features: List[Dict]) -> str:
        """Generate human-readable explanation from SHAP values"""
        if not top_features:
            return "No significant features identified."

        explanations = []
        for feat in top_features[:5]:
            direction = "increases" if feat["shap_value"] > 0 else "decreases"
            explanations.append(
                f"{feat['feature']} (value: {feat['feature_value']:.2f}) {direction} "
                f"the prediction risk by {abs(feat['shap_value']):.3f}"
            )

        return "Key factors: " + "; ".join(explanations)

    def _generate_lime_explanation(self, top_features: List[Dict], predicted_class: str) -> str:
        """Generate human-readable explanation from LIME weights"""
        if not top_features:
            return "No significant features identified."

        explanations = []
        for feat in top_features[:5]:
            direction = "supports" if feat["lime_weight"] > 0 else "contradicts"
            explanations.append(
                f"{feat['description']} {direction} the {predicted_class} prediction "
                f"(weight: {abs(feat['lime_weight']):.3f})"
            )

        return "Key factors: " + "; ".join(explanations)

    def _find_consensus_features(
        self,
        shap_features: List[Dict],
        lime_features: List[Dict]
    ) -> List[str]:
        """Find features that both SHAP and LIME agree are important"""
        shap_names = {f["feature"] for f in shap_features[:10]}
        lime_names = {f["feature"] for f in lime_features[:10]}

        consensus = list(shap_names & lime_names)
        return consensus


# Singleton instance
explainability_service = ExplainabilityService()
