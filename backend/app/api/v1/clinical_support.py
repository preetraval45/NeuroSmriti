"""
Clinical Decision Support API Endpoints
Treatment plans, drug interactions, clinical trials, genetic risks, comorbidities, lifestyle
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.clinical_support_service import (
    treatment_plan_service,
    drug_interaction_service,
    clinical_trial_service,
    genetic_risk_service,
    comorbidity_service,
    lifestyle_recommendation_service
)
from loguru import logger

router = APIRouter(prefix="/clinical-support", tags=["Clinical Decision Support"])


# ===== Pydantic Models =====

class TreatmentPlanRequest(BaseModel):
    patient_id: int
    diagnosis_stage: str  # early, moderate, severe
    cognitive_score: float
    comorbidities: Optional[List[str]] = None
    current_medications: Optional[List[str]] = None


class DrugInteractionRequest(BaseModel):
    patient_id: int
    medications: List[Dict[str, str]]  # [{"name": "Donepezil", "dosage": "10mg"}]


class ClinicalTrialRequest(BaseModel):
    patient_id: int
    age: int
    diagnosis: str
    diagnosis_stage: str
    location: Optional[str] = None
    max_distance_km: Optional[int] = 50


class GeneticRiskRequest(BaseModel):
    patient_id: int
    genetic_markers: Dict[str, str]  # {"APOE4": "e4/e4", "TREM2": "normal"}
    family_history: Optional[List[str]] = None


class ComorbidityRequest(BaseModel):
    patient_id: int
    comorbidities: List[str]
    vital_signs: Optional[Dict[str, float]] = None


class LifestyleRecommendationRequest(BaseModel):
    patient_id: int
    diagnosis_stage: str
    age: int
    physical_ability: str  # mobile, limited, wheelchair
    cognitive_level: str  # mild, moderate, severe
    preferences: Optional[Dict[str, Any]] = None


# ===== Treatment Plan Generator =====

@router.post("/treatment-plan/generate")
async def generate_treatment_plan(request: TreatmentPlanRequest):
    """
    Generate AI-powered personalized treatment plan

    Returns comprehensive treatment recommendations including:
    - Medications
    - Cognitive therapies
    - Lifestyle interventions
    - Monitoring schedule
    """
    try:
        result = treatment_plan_service.generate_treatment_plan(
            patient_id=request.patient_id,
            diagnosis_stage=request.diagnosis_stage,
            cognitive_score=request.cognitive_score,
            comorbidities=request.comorbidities or [],
            current_medications=request.current_medications or []
        )
        return result
    except Exception as e:
        logger.error(f"Error generating treatment plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/treatment-plan/{patient_id}")
async def get_treatment_plan(patient_id: int):
    """Get current treatment plan for patient"""
    try:
        plan = treatment_plan_service.get_current_plan(patient_id)
        if not plan:
            raise HTTPException(status_code=404, detail="No treatment plan found")
        return plan
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting treatment plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Drug Interaction Checker =====

@router.post("/drug-interactions/check")
async def check_drug_interactions(request: DrugInteractionRequest):
    """
    Check for dangerous medication combinations

    Returns:
    - Interaction warnings (severity: critical, moderate, minor)
    - Alternative medication suggestions
    - Monitoring recommendations
    """
    try:
        result = drug_interaction_service.check_interactions(
            patient_id=request.patient_id,
            medications=request.medications
        )
        return result
    except Exception as e:
        logger.error(f"Error checking drug interactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/drug-interactions/add-medication")
async def add_medication_check(patient_id: int, medication: Dict[str, str]):
    """Check interactions when adding a new medication to existing regimen"""
    try:
        result = drug_interaction_service.check_new_medication(
            patient_id=patient_id,
            new_medication=medication
        )
        return result
    except Exception as e:
        logger.error(f"Error checking new medication: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Clinical Trial Matcher =====

@router.post("/clinical-trials/match")
async def match_clinical_trials(request: ClinicalTrialRequest):
    """
    Match patient with relevant clinical trials

    Searches ClinicalTrials.gov and other databases
    Returns trials sorted by relevance and proximity
    """
    try:
        result = clinical_trial_service.match_trials(
            patient_id=request.patient_id,
            age=request.age,
            diagnosis=request.diagnosis,
            diagnosis_stage=request.diagnosis_stage,
            location=request.location,
            max_distance_km=request.max_distance_km
        )
        return result
    except Exception as e:
        logger.error(f"Error matching clinical trials: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/clinical-trials/details/{trial_id}")
async def get_trial_details(trial_id: str):
    """Get detailed information about a specific clinical trial"""
    try:
        details = clinical_trial_service.get_trial_details(trial_id)
        if not details:
            raise HTTPException(status_code=404, detail="Trial not found")
        return details
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting trial details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Genetic Risk Calculator =====

@router.post("/genetic-risk/calculate")
async def calculate_genetic_risk(request: GeneticRiskRequest):
    """
    Calculate genetic risk score for Alzheimer's

    Analyzes:
    - APOE4 genotype (strongest genetic risk factor)
    - TREM2, SORL1, ABCA7, and other risk genes
    - Family history

    Returns risk score and personalized recommendations
    """
    try:
        result = genetic_risk_service.calculate_risk(
            patient_id=request.patient_id,
            genetic_markers=request.genetic_markers,
            family_history=request.family_history or []
        )
        return result
    except Exception as e:
        logger.error(f"Error calculating genetic risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/genetic-risk/recommendations/{patient_id}")
async def get_genetic_recommendations(patient_id: int):
    """Get personalized recommendations based on genetic risk profile"""
    try:
        recommendations = genetic_risk_service.get_recommendations(patient_id)
        return recommendations
    except Exception as e:
        logger.error(f"Error getting genetic recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Comorbidity Tracker =====

@router.post("/comorbidity/track")
async def track_comorbidities(request: ComorbidityRequest):
    """
    Track and analyze comorbidities that affect Alzheimer's progression

    Monitors:
    - Diabetes (affects vascular health)
    - Hypertension (vascular dementia risk)
    - Cardiovascular disease
    - Depression
    - Sleep disorders
    """
    try:
        result = comorbidity_service.track_comorbidities(
            patient_id=request.patient_id,
            comorbidities=request.comorbidities,
            vital_signs=request.vital_signs
        )
        return result
    except Exception as e:
        logger.error(f"Error tracking comorbidities: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/comorbidity/risk-assessment/{patient_id}")
async def assess_comorbidity_risk(patient_id: int):
    """Get risk assessment based on comorbidities"""
    try:
        assessment = comorbidity_service.assess_risk(patient_id)
        return assessment
    except Exception as e:
        logger.error(f"Error assessing comorbidity risk: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Lifestyle Recommendations =====

@router.post("/lifestyle/recommendations")
async def get_lifestyle_recommendations(request: LifestyleRecommendationRequest):
    """
    Generate personalized lifestyle recommendations

    Includes:
    - Diet (Mediterranean, MIND diet)
    - Physical exercise (aerobic, strength, balance)
    - Cognitive activities (puzzles, learning, social)
    - Sleep hygiene
    - Social engagement
    """
    try:
        result = lifestyle_recommendation_service.generate_recommendations(
            patient_id=request.patient_id,
            diagnosis_stage=request.diagnosis_stage,
            age=request.age,
            physical_ability=request.physical_ability,
            cognitive_level=request.cognitive_level,
            preferences=request.preferences or {}
        )
        return result
    except Exception as e:
        logger.error(f"Error generating lifestyle recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/lifestyle/track-adherence/{patient_id}")
async def track_lifestyle_adherence(patient_id: int, days: int = 30):
    """Track patient adherence to lifestyle recommendations"""
    try:
        adherence = lifestyle_recommendation_service.track_adherence(
            patient_id=patient_id,
            days=days
        )
        return adherence
    except Exception as e:
        logger.error(f"Error tracking lifestyle adherence: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/lifestyle/log-activity")
async def log_lifestyle_activity(
    patient_id: int,
    activity_type: str,
    duration_minutes: int,
    details: Optional[Dict[str, Any]] = None
):
    """Log lifestyle activity for adherence tracking"""
    try:
        result = lifestyle_recommendation_service.log_activity(
            patient_id=patient_id,
            activity_type=activity_type,
            duration_minutes=duration_minutes,
            details=details or {}
        )
        return result
    except Exception as e:
        logger.error(f"Error logging lifestyle activity: {e}")
        raise HTTPException(status_code=500, detail=str(e))
