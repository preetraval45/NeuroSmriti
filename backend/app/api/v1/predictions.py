"""
AI Predictions endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from uuid import UUID
import logging

from app.core.database import get_db
from app.core.security import get_current_active_user
from app.services.ml_service import ml_service
from app.models.patient import Patient
from app.models.memory import Memory
from app.models.prediction import Prediction

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/stage")
async def predict_alzheimers_stage(
    patient_id: UUID,
    mri_scan: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Predict Alzheimer's stage using ML ensemble model
    Integrates patient data from database and runs inference
    """
    try:
        # Fetch patient from database
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Prepare patient data for ML model
        patient_data = {
            "age": patient.age if hasattr(patient, 'age') else 70,
            "gender": patient.gender if hasattr(patient, 'gender') else "Unknown",
            "education_years": 12,  # TODO: Add to patient model
            "has_apoe4": False,  # TODO: Add to patient model
            "family_history_ad": False,  # TODO: Add to patient model
            "mmse_total": patient.mmse_score if patient.mmse_score else 25,
            "moca_total": patient.moca_score if patient.moca_score else 24,
            "adas_cog_13": 15,  # TODO: Add to patient model
            "faq_total": 5,  # TODO: Add to patient model
            "hippocampus_left": 3.0,  # TODO: Parse from MRI if provided
            "hippocampus_right": 3.0,
            "amyloid_pet_suvr": 1.2,
            "tau_pet_suvr": 1.3,
            "total_brain": 1200,
            "ventricular_volume": 30,
            "csf_abeta42": 600,
            "csf_ptau181": 40,
            "csf_total_tau": 500,
            "amyloid_positive": False,
            "tau_positive": False,
            "hypertension": False,  # TODO: Parse from medical_history
            "diabetes": False,
            "cardiovascular": False,
            "depression": False,
            "words_per_minute": 120,
            "coherence_score": 0.8,
            "adl_basic_score": 5,
            "adl_instrumental_score": 7,
            "risk_score": 0.3
        }

        # Run ML prediction
        prediction_result = ml_service.predict_stage(patient_data)

        # Add patient_id to response
        prediction_result["patient_id"] = str(patient_id)

        # TODO: Save prediction to database
        # new_prediction = Prediction(
        #     patient_id=patient_id,
        #     predicted_stage=prediction_result["predicted_stage"],
        #     confidence=prediction_result["confidence"],
        #     ...
        # )
        # db.add(new_prediction)
        # db.commit()

        logger.info(f"Prediction completed for patient {patient_id}: stage {prediction_result['predicted_stage']}")

        return prediction_result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during stage prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.get("/memory-decay/{patient_id}")
async def predict_memory_decay(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """
    Predict memory decay for patient's memory graph using MemoryGNN
    Analyzes patient's personal memory knowledge graph
    """
    try:
        # Fetch patient
        patient = db.query(Patient).filter(Patient.id == patient_id).first()
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")

        # Fetch patient's memories
        memories = db.query(Memory).filter(Memory.patient_id == patient_id).all()

        if not memories:
            return {
                "patient_id": str(patient_id),
                "high_risk_memories": [],
                "total_memories": 0,
                "at_risk_count": 0,
                "intervention_recommended_count": 0,
                "message": "No memories recorded for this patient"
            }

        # Prepare memory graph data
        memory_graph = {
            "patient_id": str(patient_id),
            "memories": [
                {
                    "id": str(mem.id),
                    "name": mem.name,
                    "type": mem.type.value if hasattr(mem.type, 'value') else str(mem.type),
                    "recall_strength": mem.recall_strength if mem.recall_strength else 80,
                    "emotional_weight": mem.emotional_weight if mem.emotional_weight else 0.5,
                    "importance": mem.importance if mem.importance else 5
                }
                for mem in memories
            ]
        }

        # Run memory decay prediction
        prediction_result = ml_service.predict_memory_decay(memory_graph)

        logger.info(f"Memory decay prediction completed for patient {patient_id}: {len(prediction_result['high_risk_memories'])} high-risk memories identified")

        return prediction_result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during memory decay prediction: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@router.post("/load-models")
async def load_ml_models(
    current_user: dict = Depends(get_current_active_user)
):
    """
    Manually trigger ML model loading (admin only)
    Useful for preloading models or reloading after updates
    """
    try:
        # Check if user is admin
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")

        success = ml_service.load_traditional_models()

        if success:
            return {
                "status": "success",
                "message": "ML models loaded successfully",
                "models_loaded": list(ml_service.traditional_models.keys())
            }
        else:
            return {
                "status": "warning",
                "message": "Models not found - using heuristic predictions",
                "models_loaded": []
            }

    except Exception as e:
        logger.error(f"Error loading models: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load models: {str(e)}")
