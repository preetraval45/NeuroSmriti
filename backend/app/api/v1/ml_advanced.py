"""
Advanced ML API Endpoints
Explainability, Uncertainty, Multimodal Fusion, Continuous Learning
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import numpy as np

from app.core.database import get_db
from app.models.patient import Patient
from app.services.explainability_service import explainability_service
from app.services.uncertainty_service import uncertainty_service
from app.services.multimodal_fusion_service import multimodal_fusion_service
from app.services.continuous_learning_service import continuous_learning_service
from app.services.ml_service import ml_service
from app.services.speech_analysis_service import speech_analysis_service
from app.services.behavioral_analysis_service import (
    eye_tracking_service, gait_service, sleep_service, sentiment_service
)
from app.services.advanced_cognitive_service import (
    handwriting_service, facial_recognition_service, temporal_modeling_service
)
from loguru import logger

router = APIRouter(prefix="/ml", tags=["Advanced ML"])


# Request/Response Models
class ExplainabilityRequest(BaseModel):
    patient_id: int
    method: Optional[str] = "comprehensive"  # "shap", "lime", "comprehensive"
    top_n: int = 10


class ExplainabilityResponse(BaseModel):
    patient_id: int
    method: str
    prediction: str
    confidence: float
    explanations: Dict[str, Any]


class UncertaintyRequest(BaseModel):
    patient_id: int
    methods: Optional[List[str]] = ["ensemble", "bootstrap"]


class UncertaintyResponse(BaseModel):
    patient_id: int
    base_prediction: Dict[str, Any]
    uncertainty_analysis: Dict[str, Any]
    reliability: str


class MultimodalRequest(BaseModel):
    patient_id: int
    use_clinical: bool = True
    image_required: bool = False


class ContinuousLearningFeedback(BaseModel):
    patient_id: int
    predicted_stage: str
    true_stage: str
    confidence: float
    clinician_notes: Optional[str] = None


# Endpoints

@router.post("/explain", response_model=ExplainabilityResponse)
async def explain_prediction(
    request: ExplainabilityRequest,
    db: Session = Depends(get_db)
):
    """
    Get explainable AI analysis for a patient's prediction

    Returns SHAP/LIME explanations showing which features contributed most to the prediction
    """
    try:
        # Fetch patient
        patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Prepare patient data
        patient_data = {
            'age': patient.age,
            'gender': 0 if patient.gender == 'Male' else 1,
            'education_years': patient.education_years or 14,
            'apoe4_positive': patient.apoe4_positive or 0,
            'mmse_score': patient.mmse_score or 24,
            'moca_score': patient.moca_score or 22,
            'cdr_score': patient.cdr_score or 0,
            'gds_score': patient.gds_score or 5,
            'faq_score': patient.faq_score or 0,
            'adas_cog_score': patient.adas_cog_score or 10,
            'npi_score': patient.npi_score or 0,
            'hippocampal_volume': patient.hippocampal_volume or 3200,
            'ventricular_volume': patient.ventricular_volume or 45000,
            'brain_volume': patient.brain_volume or 1100000,
            'csf_abeta': patient.csf_abeta or 650,
            'csf_tau': patient.csf_tau or 350,
            'csf_ptau': patient.csf_ptau or 50,
            'fdg_pet': patient.fdg_pet or 1.3,
            'pib_pet': patient.pib_pet or 1.4,
            'av45_pet': patient.av45_pet or 1.2,
            'speech_pause_ratio': patient.speech_pause_ratio or 0.1,
            'word_finding_difficulty': patient.word_finding_difficulty or 2,
            'gait_speed': patient.gait_speed or 1.0,
            'stride_variability': patient.stride_variability or 0.1,
            'sleep_efficiency': patient.sleep_efficiency or 0.85,
            'rem_sleep_percentage': patient.rem_sleep_percentage or 0.20,
            'physical_activity_minutes': patient.physical_activity_minutes or 30,
            'social_engagement_score': patient.social_engagement_score or 6,
            'cognitive_reserve_score': patient.cognitive_reserve_score or 100
        }

        # Get prediction from ML service
        prediction_result = ml_service.predict_stage(patient_data)

        # Extract and scale features
        features = list(patient_data.values())
        features_scaled = ml_service.scaler.transform([features])

        # Load explainability service
        explainability_service.load_model()
        explainability_service.initialize_explainers()

        # Get explanations
        if request.method == "shap":
            explanations = explainability_service.explain_with_shap(features_scaled, request.top_n)
        elif request.method == "lime":
            explanations = explainability_service.explain_with_lime(features_scaled, request.top_n)
        else:  # comprehensive
            explanations = explainability_service.get_comprehensive_explanation(features_scaled, request.top_n)

        return ExplainabilityResponse(
            patient_id=request.patient_id,
            method=request.method,
            prediction=prediction_result["stage"],
            confidence=prediction_result["confidence"],
            explanations=explanations
        )

    except Exception as e:
        logger.error(f"Error in explainability endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/uncertainty", response_model=UncertaintyResponse)
async def quantify_uncertainty(
    request: UncertaintyRequest,
    db: Session = Depends(get_db)
):
    """
    Quantify prediction uncertainty using multiple methods

    Returns confidence intervals and reliability scores for the prediction
    """
    try:
        # Fetch patient
        patient = db.query(Patient).filter(Patient.id == request.patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Prepare patient data
        patient_data = {
            'age': patient.age,
            'gender': 0 if patient.gender == 'Male' else 1,
            'education_years': patient.education_years or 14,
            'apoe4_positive': patient.apoe4_positive or 0,
            'mmse_score': patient.mmse_score or 24,
            'moca_score': patient.moca_score or 22,
            'cdr_score': patient.cdr_score or 0,
            'gds_score': patient.gds_score or 5,
            'faq_score': patient.faq_score or 0,
            'adas_cog_score': patient.adas_cog_score or 10,
            'npi_score': patient.npi_score or 0,
            'hippocampal_volume': patient.hippocampal_volume or 3200,
            'ventricular_volume': patient.ventricular_volume or 45000,
            'brain_volume': patient.brain_volume or 1100000,
            'csf_abeta': patient.csf_abeta or 650,
            'csf_tau': patient.csf_tau or 350,
            'csf_ptau': patient.csf_ptau or 50,
            'fdg_pet': patient.fdg_pet or 1.3,
            'pib_pet': patient.pib_pet or 1.4,
            'av45_pet': patient.av45_pet or 1.2,
            'speech_pause_ratio': patient.speech_pause_ratio or 0.1,
            'word_finding_difficulty': patient.word_finding_difficulty or 2,
            'gait_speed': patient.gait_speed or 1.0,
            'stride_variability': patient.stride_variability or 0.1,
            'sleep_efficiency': patient.sleep_efficiency or 0.85,
            'rem_sleep_percentage': patient.rem_sleep_percentage or 0.20,
            'physical_activity_minutes': patient.physical_activity_minutes or 30,
            'social_engagement_score': patient.social_engagement_score or 6,
            'cognitive_reserve_score': patient.cognitive_reserve_score or 100
        }

        # Extract and scale features
        features = list(patient_data.values())
        features_scaled = ml_service.scaler.transform([features])

        # Load uncertainty service
        uncertainty_service.load_model()

        # Get comprehensive uncertainty analysis
        uncertainty_analysis = uncertainty_service.get_comprehensive_uncertainty(
            features_scaled[0],
            methods=request.methods
        )

        return UncertaintyResponse(
            patient_id=request.patient_id,
            base_prediction=uncertainty_analysis["base_prediction"],
            uncertainty_analysis=uncertainty_analysis,
            reliability=uncertainty_analysis["reliability"]
        )

    except Exception as e:
        logger.error(f"Error in uncertainty endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/multimodal/predict")
async def multimodal_prediction(
    patient_id: int,
    db: Session = Depends(get_db),
    brain_scan: Optional[UploadFile] = File(None)
):
    """
    Make prediction using multimodal data (clinical + imaging)

    Combines clinical features with brain scan analysis for enhanced accuracy
    """
    try:
        # Fetch patient
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Prepare clinical data
        clinical_data = {
            'age': patient.age,
            'gender': 0 if patient.gender == 'Male' else 1,
            'education_years': patient.education_years or 14,
            'apoe4_positive': patient.apoe4_positive or 0,
            'mmse_score': patient.mmse_score or 24,
            'moca_score': patient.moca_score or 22,
            'cdr_score': patient.cdr_score or 0,
            'gds_score': patient.gds_score or 5,
            'faq_score': patient.faq_score or 0,
            'adas_cog_score': patient.adas_cog_score or 10,
            'npi_score': patient.npi_score or 0,
            'hippocampal_volume': patient.hippocampal_volume or 3200,
            'ventricular_volume': patient.ventricular_volume or 45000,
            'brain_volume': patient.brain_volume or 1100000,
            'csf_abeta': patient.csf_abeta or 650,
            'csf_tau': patient.csf_tau or 350,
            'csf_ptau': patient.csf_ptau or 50,
            'fdg_pet': patient.fdg_pet or 1.3,
            'pib_pet': patient.pib_pet or 1.4,
            'av45_pet': patient.av45_pet or 1.2,
            'speech_pause_ratio': patient.speech_pause_ratio or 0.1,
            'word_finding_difficulty': patient.word_finding_difficulty or 2,
            'gait_speed': patient.gait_speed or 1.0,
            'stride_variability': patient.stride_variability or 0.1,
            'sleep_efficiency': patient.sleep_efficiency or 0.85,
            'rem_sleep_percentage': patient.rem_sleep_percentage or 0.20,
            'physical_activity_minutes': patient.physical_activity_minutes or 30,
            'social_engagement_score': patient.social_engagement_score or 6,
            'cognitive_reserve_score': patient.cognitive_reserve_score or 100
        }

        # Handle brain scan if provided
        image_path = None
        if brain_scan:
            # Save uploaded file temporarily
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                content = await brain_scan.read()
                tmp.write(content)
                image_path = tmp.name

        # Load multimodal service
        multimodal_fusion_service.load_model()

        # Make prediction
        result = multimodal_fusion_service.predict(
            clinical_data=clinical_data,
            image_path=image_path
        )

        # Clean up temporary file
        if image_path:
            import os
            os.unlink(image_path)

        return result

    except Exception as e:
        logger.error(f"Error in multimodal prediction: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/continuous-learning/feedback")
async def submit_feedback(
    feedback: ContinuousLearningFeedback,
    db: Session = Depends(get_db)
):
    """
    Submit feedback for continuous learning

    Allows clinicians to provide ground truth labels for model improvement
    """
    try:
        # Fetch patient
        patient = db.query(Patient).filter(Patient.id == feedback.patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Prepare patient data
        patient_data = {
            'age': patient.age,
            'gender': 0 if patient.gender == 'Male' else 1,
            'education_years': patient.education_years or 14,
            'apoe4_positive': patient.apoe4_positive or 0,
            'mmse_score': patient.mmse_score or 24,
            'moca_score': patient.moca_score or 22,
            'cdr_score': patient.cdr_score or 0,
            'gds_score': patient.gds_score or 5,
            'faq_score': patient.faq_score or 0,
            'adas_cog_score': patient.adas_cog_score or 10,
            'npi_score': patient.npi_score or 0,
            'hippocampal_volume': patient.hippocampal_volume or 3200,
            'ventricular_volume': patient.ventricular_volume or 45000,
            'brain_volume': patient.brain_volume or 1100000,
            'csf_abeta': patient.csf_abeta or 650,
            'csf_tau': patient.csf_tau or 350,
            'csf_ptau': patient.csf_ptau or 50,
            'fdg_pet': patient.fdg_pet or 1.3,
            'pib_pet': patient.pib_pet or 1.4,
            'av45_pet': patient.av45_pet or 1.2,
            'speech_pause_ratio': patient.speech_pause_ratio or 0.1,
            'word_finding_difficulty': patient.word_finding_difficulty or 2,
            'gait_speed': patient.gait_speed or 1.0,
            'stride_variability': patient.stride_variability or 0.1,
            'sleep_efficiency': patient.sleep_efficiency or 0.85,
            'rem_sleep_percentage': patient.rem_sleep_percentage or 0.20,
            'physical_activity_minutes': patient.physical_activity_minutes or 30,
            'social_engagement_score': patient.social_engagement_score or 6,
            'cognitive_reserve_score': patient.cognitive_reserve_score or 100
        }

        # Submit to continuous learning service
        continuous_learning_service.add_new_sample(
            patient_data=patient_data,
            true_label=feedback.true_stage,
            prediction=feedback.predicted_stage,
            confidence=feedback.confidence
        )

        return {
            "message": "Feedback submitted successfully",
            "patient_id": feedback.patient_id,
            "buffer_status": continuous_learning_service.get_performance_metrics()
        }

    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/continuous-learning/metrics")
async def get_learning_metrics():
    """
    Get continuous learning performance metrics

    Returns model performance history and buffer status
    """
    try:
        metrics = continuous_learning_service.get_performance_metrics()
        return metrics

    except Exception as e:
        logger.error(f"Error getting learning metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models/registry")
async def get_model_registry():
    """
    Get information about available models

    Returns model versions, performance, and capabilities
    """
    try:
        import json
        from pathlib import Path

        model_path = Path(__file__).parent.parent.parent / "ml" / "models"

        registry_file = model_path / "model_registry.json"
        if registry_file.exists():
            with open(registry_file, "r") as f:
                registry = json.load(f)
        else:
            registry = {"message": "Model registry not found"}

        # Add advanced models if available
        advanced_registry_file = model_path / "advanced_model_registry.json"
        if advanced_registry_file.exists():
            with open(advanced_registry_file, "r") as f:
                registry["advanced_models"] = json.load(f)

        return registry

    except Exception as e:
        logger.error(f"Error getting model registry: {e}")
        raise HTTPException(status_code=500, detail=str(e))
