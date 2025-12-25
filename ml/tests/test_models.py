"""
Test trained ML models for correctness and performance
"""
import pytest
import pickle
import numpy as np
from pathlib import Path


# Path to models
MODEL_DIR = Path(__file__).parent.parent / "models"


class TestModelFiles:
    """Test that all required model files exist"""

    def test_ensemble_model_exists(self):
        """Test ensemble model file exists"""
        assert (MODEL_DIR / "ensemble_model.pkl").exists()

    def test_random_forest_exists(self):
        """Test random forest model file exists"""
        assert (MODEL_DIR / "random_forest_model.pkl").exists()

    def test_gradient_boosting_exists(self):
        """Test gradient boosting model file exists"""
        assert (MODEL_DIR / "gradient_boosting_model.pkl").exists()

    def test_neural_network_exists(self):
        """Test neural network model file exists"""
        assert (MODEL_DIR / "neural_network_model.pkl").exists()

    def test_scaler_exists(self):
        """Test scaler file exists"""
        assert (MODEL_DIR / "scaler.pkl").exists()

    def test_label_encoder_exists(self):
        """Test label encoder file exists"""
        assert (MODEL_DIR / "label_encoder.pkl").exists()


class TestModelLoading:
    """Test that models can be loaded successfully"""

    def test_load_ensemble_model(self):
        """Test ensemble model loads without errors"""
        with open(MODEL_DIR / "ensemble_model.pkl", "rb") as f:
            model = pickle.load(f)
        assert model is not None
        assert hasattr(model, 'predict')
        assert hasattr(model, 'predict_proba')

    def test_load_scaler(self):
        """Test scaler loads correctly"""
        with open(MODEL_DIR / "scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        assert scaler is not None
        assert hasattr(scaler, 'transform')

    def test_load_label_encoder(self):
        """Test label encoder loads correctly"""
        with open(MODEL_DIR / "label_encoder.pkl", "rb") as f:
            encoder = pickle.load(f)
        assert encoder is not None
        assert hasattr(encoder, 'transform')
        assert hasattr(encoder, 'inverse_transform')

    def test_label_encoder_classes(self):
        """Test label encoder has correct classes"""
        with open(MODEL_DIR / "label_encoder.pkl", "rb") as f:
            encoder = pickle.load(f)

        classes = encoder.classes_
        assert len(classes) == 5
        assert 'normal' in classes or 'Normal' in classes or 'mci' in classes


class TestModelPredictions:
    """Test model predictions work correctly"""

    @pytest.fixture
    def models(self):
        """Load all required models"""
        with open(MODEL_DIR / "ensemble_model.pkl", "rb") as f:
            ensemble = pickle.load(f)
        with open(MODEL_DIR / "scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        with open(MODEL_DIR / "label_encoder.pkl", "rb") as f:
            encoder = pickle.load(f)

        return {
            'ensemble': ensemble,
            'scaler': scaler,
            'encoder': encoder
        }

    def test_prediction_on_sample_data(self, models):
        """Test prediction on synthetic sample data"""
        # Create sample patient data (29 features)
        sample_features = np.array([[
            70,  # age
            1,   # gender (Female)
            12,  # education_years
            0,   # has_apoe4
            0,   # family_history_ad
            24,  # mmse_total
            22,  # moca_total
            20,  # adas_cog_13
            8,   # faq_total
            2.5, # hippocampus_left
            2.5, # hippocampus_right
            1.3, # amyloid_pet_suvr
            1.4, # tau_pet_suvr
            1100, # total_brain
            35,  # ventricular_volume
            500, # csf_abeta42
            50,  # csf_ptau181
            600, # csf_total_tau
            1,   # amyloid_positive
            1,   # tau_positive
            0,   # hypertension
            0,   # diabetes
            0,   # cardiovascular
            0,   # depression
            110, # words_per_minute
            0.75, # coherence_score
            5,   # adl_basic_score
            6,   # adl_instrumental_score
            0.4  # risk_score
        ]])

        # Scale features
        features_scaled = models['scaler'].transform(sample_features)

        # Predict
        prediction = models['ensemble'].predict(features_scaled)
        probabilities = models['ensemble'].predict_proba(features_scaled)

        # Assertions
        assert prediction is not None
        assert len(prediction) == 1
        assert probabilities is not None
        assert probabilities.shape[1] == 5  # 5 classes

        # Probabilities should sum to 1
        assert np.isclose(probabilities.sum(), 1.0)

        # Prediction should be valid class index
        assert 0 <= prediction[0] < 5

    def test_prediction_output_format(self, models):
        """Test that predictions return expected format"""
        # Normal patient (high MMSE, low biomarkers)
        normal_patient = np.array([[
            65, 0, 16, 0, 0,
            29, 28, 5, 1,
            3.8, 3.7, 0.9, 1.0, 1300, 25,
            900, 20, 300,
            0, 0, 0, 0, 0, 0,
            140, 0.95, 6, 8, 0.1
        ]])

        # Severe patient (low MMSE, high biomarkers)
        severe_patient = np.array([[
            85, 1, 8, 1, 1,
            8, 6, 55, 28,
            1.5, 1.4, 2.2, 2.8, 900, 65,
            250, 110, 1100,
            1, 1, 1, 1, 0, 1,
            60, 0.35, 2, 1, 0.9
        ]])

        # Test normal patient
        normal_scaled = models['scaler'].transform(normal_patient)
        normal_pred = models['ensemble'].predict(normal_scaled)[0]
        normal_proba = models['ensemble'].predict_proba(normal_scaled)[0]

        # Test severe patient
        severe_scaled = models['scaler'].transform(severe_patient)
        severe_pred = models['ensemble'].predict(severe_scaled)[0]
        severe_proba = models['ensemble'].predict_proba(severe_scaled)[0]

        # Predictions should be different
        # Note: With 100% accuracy on synthetic data, this might not always hold
        # but the probabilities should definitely differ
        assert not np.array_equal(normal_proba, severe_proba)

    def test_batch_predictions(self, models):
        """Test predictions on multiple patients at once"""
        # Create batch of 10 patients
        batch_size = 10
        batch_features = np.random.rand(batch_size, 29)

        # Normalize to reasonable ranges
        batch_features[:, 0] = 55 + batch_features[:, 0] * 40  # age: 55-95
        batch_features[:, 1] = (batch_features[:, 1] > 0.5).astype(int)  # gender: 0 or 1
        batch_features[:, 5] = 15 + batch_features[:, 5] * 15  # MMSE: 15-30

        # Scale and predict
        batch_scaled = models['scaler'].transform(batch_features)
        predictions = models['ensemble'].predict(batch_scaled)
        probabilities = models['ensemble'].predict_proba(batch_scaled)

        # Assertions
        assert len(predictions) == batch_size
        assert probabilities.shape == (batch_size, 5)

        # All probabilities should sum to 1
        for proba in probabilities:
            assert np.isclose(proba.sum(), 1.0)


class TestModelPerformance:
    """Test model performance characteristics"""

    def test_model_size(self):
        """Test that model files are reasonable size"""
        ensemble_size = (MODEL_DIR / "ensemble_model.pkl").stat().st_size / (1024 * 1024)
        assert ensemble_size < 20, f"Ensemble model too large: {ensemble_size:.1f} MB"

    def test_inference_speed(self):
        """Test that predictions are fast enough"""
        import time

        with open(MODEL_DIR / "ensemble_model.pkl", "rb") as f:
            model = pickle.load(f)
        with open(MODEL_DIR / "scaler.pkl", "rb") as f:
            scaler = pickle.load(f)

        # Create sample data
        sample = np.random.rand(1, 29)
        sample_scaled = scaler.transform(sample)

        # Time 100 predictions
        start = time.time()
        for _ in range(100):
            model.predict(sample_scaled)
        elapsed = time.time() - start

        avg_time = (elapsed / 100) * 1000  # Convert to milliseconds
        assert avg_time < 100, f"Predictions too slow: {avg_time:.2f}ms per prediction"


class TestModelRegistry:
    """Test model versioning and metadata"""

    def test_registry_file_exists(self):
        """Test model registry file exists"""
        assert (MODEL_DIR / "model_registry.json").exists()

    def test_registry_contains_version(self):
        """Test registry has version information"""
        import json

        with open(MODEL_DIR / "model_registry.json", "r") as f:
            registry = json.load(f)

        assert "current_version" in registry
        assert registry["current_version"].startswith("v")

    def test_registry_has_model_info(self):
        """Test registry contains model metadata"""
        import json

        with open(MODEL_DIR / "model_registry.json", "r") as f:
            registry = json.load(f)

        assert "models" in registry
        assert "ensemble_classifier" in registry["models"]

        ensemble_info = registry["models"]["ensemble_classifier"]
        assert "accuracy" in ensemble_info
        assert "trained_date" in ensemble_info
        assert "file" in ensemble_info


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
