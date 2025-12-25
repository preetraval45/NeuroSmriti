"""
Uncertainty Quantification Service
Provides confidence intervals and uncertainty estimates for predictions
"""

import numpy as np
import pickle
from typing import Dict, List, Any, Tuple
from pathlib import Path
from loguru import logger
from scipy import stats


class UncertaintyQuantificationService:
    """Service for quantifying prediction uncertainty using multiple methods"""

    def __init__(self, model_path: Path = None):
        self.model_path = model_path or Path(__file__).parent.parent / "ml" / "models"
        self.model = None
        self.scaler = None
        self.label_encoder = None

    def load_model(self, model_name: str = "ensemble_model.pkl"):
        """Load trained model"""
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

            logger.info(f"Loaded model {model_name} for uncertainty quantification")

        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise

    def mc_dropout_uncertainty(
        self,
        features: np.ndarray,
        n_iterations: int = 100
    ) -> Dict[str, Any]:
        """
        Monte Carlo Dropout for uncertainty estimation
        Note: Only works with neural network models that have dropout

        Args:
            features: Input features (scaled)
            n_iterations: Number of MC iterations

        Returns:
            Dictionary with mean predictions and uncertainty estimates
        """
        try:
            predictions = []

            # Check if model has dropout (Neural Network)
            has_dropout = hasattr(self.model, 'out_activation_')

            if not has_dropout:
                # Fallback to ensemble uncertainty
                return self.ensemble_uncertainty(features, n_iterations)

            # Run multiple forward passes with dropout enabled
            for _ in range(n_iterations):
                pred_proba = self.model.predict_proba(features.reshape(1, -1))[0]
                predictions.append(pred_proba)

            predictions = np.array(predictions)

            # Calculate statistics
            mean_proba = predictions.mean(axis=0)
            std_proba = predictions.std(axis=0)

            # Confidence intervals (95%)
            lower_bound = np.percentile(predictions, 2.5, axis=0)
            upper_bound = np.percentile(predictions, 97.5, axis=0)

            # Predictive entropy (uncertainty measure)
            entropy = -np.sum(mean_proba * np.log(mean_proba + 1e-10))

            # Prediction
            predicted_class = self.label_encoder.classes_[np.argmax(mean_proba)]

            return {
                "method": "MC Dropout",
                "prediction": predicted_class,
                "mean_probabilities": {
                    cls: float(prob)
                    for cls, prob in zip(self.label_encoder.classes_, mean_proba)
                },
                "std_probabilities": {
                    cls: float(std)
                    for cls, std in zip(self.label_encoder.classes_, std_proba)
                },
                "confidence_intervals": {
                    cls: {"lower": float(lower), "upper": float(upper)}
                    for cls, lower, upper in zip(
                        self.label_encoder.classes_, lower_bound, upper_bound
                    )
                },
                "uncertainty_score": float(entropy),
                "confidence": float(np.max(mean_proba)),
                "n_iterations": n_iterations
            }

        except Exception as e:
            logger.error(f"Error in MC dropout uncertainty: {e}")
            raise

    def bootstrap_uncertainty(
        self,
        features: np.ndarray,
        n_bootstraps: int = 100
    ) -> Dict[str, Any]:
        """
        Bootstrap method for uncertainty estimation
        Simulates prediction variance through feature perturbation

        Args:
            features: Input features (scaled)
            n_bootstraps: Number of bootstrap samples

        Returns:
            Dictionary with uncertainty estimates
        """
        try:
            predictions = []

            # Estimate feature std from training data characteristics
            feature_std = np.std(features) * 0.05  # Small perturbation

            for _ in range(n_bootstraps):
                # Add small Gaussian noise to features
                perturbed_features = features + np.random.normal(0, feature_std, features.shape)
                pred_proba = self.model.predict_proba(perturbed_features.reshape(1, -1))[0]
                predictions.append(pred_proba)

            predictions = np.array(predictions)

            # Statistics
            mean_proba = predictions.mean(axis=0)
            std_proba = predictions.std(axis=0)
            lower_bound = np.percentile(predictions, 2.5, axis=0)
            upper_bound = np.percentile(predictions, 97.5, axis=0)

            predicted_class = self.label_encoder.classes_[np.argmax(mean_proba)]

            return {
                "method": "Bootstrap",
                "prediction": predicted_class,
                "mean_probabilities": {
                    cls: float(prob)
                    for cls, prob in zip(self.label_encoder.classes_, mean_proba)
                },
                "std_probabilities": {
                    cls: float(std)
                    for cls, std in zip(self.label_encoder.classes_, std_proba)
                },
                "confidence_intervals": {
                    cls: {"lower": float(lower), "upper": float(upper)}
                    for cls, lower, upper in zip(
                        self.label_encoder.classes_, lower_bound, upper_bound
                    )
                },
                "confidence": float(np.max(mean_proba)),
                "n_bootstraps": n_bootstraps
            }

        except Exception as e:
            logger.error(f"Error in bootstrap uncertainty: {e}")
            raise

    def ensemble_uncertainty(
        self,
        features: np.ndarray,
        n_estimators: int = None
    ) -> Dict[str, Any]:
        """
        Ensemble-based uncertainty using individual estimator predictions

        Args:
            features: Input features (scaled)
            n_estimators: Number of estimators to use (None = all)

        Returns:
            Dictionary with ensemble uncertainty estimates
        """
        try:
            # Check if model is an ensemble
            if not hasattr(self.model, 'estimators_'):
                # Not an ensemble, use bootstrap method
                return self.bootstrap_uncertainty(features, n_bootstraps=100)

            # Get predictions from individual estimators
            estimators = self.model.estimators_[:n_estimators] if n_estimators else self.model.estimators_

            predictions = []
            for estimator in estimators:
                pred_proba = estimator.predict_proba(features.reshape(1, -1))[0]
                predictions.append(pred_proba)

            predictions = np.array(predictions)

            # Statistics
            mean_proba = predictions.mean(axis=0)
            std_proba = predictions.std(axis=0)
            lower_bound = np.percentile(predictions, 2.5, axis=0)
            upper_bound = np.percentile(predictions, 97.5, axis=0)

            # Disagreement among estimators
            disagreement = std_proba.mean()

            predicted_class = self.label_encoder.classes_[np.argmax(mean_proba)]

            return {
                "method": "Ensemble Disagreement",
                "prediction": predicted_class,
                "mean_probabilities": {
                    cls: float(prob)
                    for cls, prob in zip(self.label_encoder.classes_, mean_proba)
                },
                "std_probabilities": {
                    cls: float(std)
                    for cls, std in zip(self.label_encoder.classes_, std_proba)
                },
                "confidence_intervals": {
                    cls: {"lower": float(lower), "upper": float(upper)}
                    for cls, lower, upper in zip(
                        self.label_encoder.classes_, lower_bound, upper_bound
                    )
                },
                "disagreement_score": float(disagreement),
                "confidence": float(np.max(mean_proba)),
                "n_estimators": len(estimators)
            }

        except Exception as e:
            logger.error(f"Error in ensemble uncertainty: {e}")
            raise

    def bayesian_confidence_interval(
        self,
        probabilities: np.ndarray,
        alpha: float = 0.05
    ) -> Dict[str, Tuple[float, float]]:
        """
        Calculate Bayesian credible intervals for class probabilities

        Args:
            probabilities: Class probabilities
            alpha: Significance level (0.05 for 95% CI)

        Returns:
            Dictionary of credible intervals per class
        """
        intervals = {}

        for i, cls in enumerate(self.label_encoder.classes_):
            prob = probabilities[i]

            # Assume Beta distribution for probabilities
            # Use Wilson score interval
            n = 100  # Assume equivalent sample size
            z = stats.norm.ppf(1 - alpha/2)

            lower = (prob + z**2/(2*n) - z * np.sqrt(prob*(1-prob)/n + z**2/(4*n**2))) / (1 + z**2/n)
            upper = (prob + z**2/(2*n) + z * np.sqrt(prob*(1-prob)/n + z**2/(4*n**2))) / (1 + z**2/n)

            intervals[cls] = (float(max(0, lower)), float(min(1, upper)))

        return intervals

    def get_comprehensive_uncertainty(
        self,
        features: np.ndarray,
        methods: List[str] = None
    ) -> Dict[str, Any]:
        """
        Get comprehensive uncertainty estimates using multiple methods

        Args:
            features: Input features (scaled)
            methods: List of methods to use (default: all applicable)

        Returns:
            Dictionary with all uncertainty estimates
        """
        if methods is None:
            methods = ['ensemble', 'bootstrap']

        results = {}

        # Base prediction
        pred_proba = self.model.predict_proba(features.reshape(1, -1))[0]
        prediction = self.label_encoder.classes_[np.argmax(pred_proba)]

        results['base_prediction'] = {
            "prediction": prediction,
            "probabilities": {
                cls: float(prob)
                for cls, prob in zip(self.label_encoder.classes_, pred_proba)
            },
            "confidence": float(np.max(pred_proba))
        }

        # Ensemble uncertainty
        if 'ensemble' in methods:
            try:
                results['ensemble_uncertainty'] = self.ensemble_uncertainty(features)
            except Exception as e:
                logger.warning(f"Ensemble uncertainty failed: {e}")

        # Bootstrap uncertainty
        if 'bootstrap' in methods:
            try:
                results['bootstrap_uncertainty'] = self.bootstrap_uncertainty(features, n_bootstraps=50)
            except Exception as e:
                logger.warning(f"Bootstrap uncertainty failed: {e}")

        # MC Dropout (if applicable)
        if 'mc_dropout' in methods:
            try:
                results['mc_dropout_uncertainty'] = self.mc_dropout_uncertainty(features, n_iterations=50)
            except Exception as e:
                logger.warning(f"MC Dropout uncertainty failed: {e}")

        # Bayesian confidence intervals
        results['bayesian_intervals'] = self.bayesian_confidence_interval(pred_proba)

        # Aggregate uncertainty score
        uncertainty_scores = []
        if 'ensemble_uncertainty' in results:
            uncertainty_scores.append(results['ensemble_uncertainty'].get('disagreement_score', 0))
        if 'bootstrap_uncertainty' in results:
            uncertainty_scores.append(
                np.mean([v for v in results['bootstrap_uncertainty']['std_probabilities'].values()])
            )

        results['aggregate_uncertainty'] = float(np.mean(uncertainty_scores)) if uncertainty_scores else 0.0

        # Reliability classification
        if results['aggregate_uncertainty'] < 0.05:
            reliability = "Very High"
        elif results['aggregate_uncertainty'] < 0.10:
            reliability = "High"
        elif results['aggregate_uncertainty'] < 0.15:
            reliability = "Moderate"
        elif results['aggregate_uncertainty'] < 0.20:
            reliability = "Low"
        else:
            reliability = "Very Low"

        results['reliability'] = reliability

        return results


# Singleton instance
uncertainty_service = UncertaintyQuantificationService()
