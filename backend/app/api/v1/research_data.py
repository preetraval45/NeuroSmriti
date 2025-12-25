"""
Research & Data API Endpoints
Research contribution, FHIR export, report generation, analytics, cohort analysis, predictive analytics
"""

from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
import io

from app.services.research_data_service import (
    research_contribution_service,
    fhir_export_service,
    report_generation_service,
    analytics_service,
    cohort_analysis_service,
    predictive_analytics_service
)
from loguru import logger

router = APIRouter(prefix="/research-data", tags=["Research & Data"])


# ===== Pydantic Models =====

class ResearchConsentRequest(BaseModel):
    patient_id: int
    consent_given: bool
    data_sharing_level: str  # anonymized, aggregated, identifiable
    allowed_uses: List[str]  # research, education, commercial


class FHIRExportRequest(BaseModel):
    patient_id: int
    resource_types: Optional[List[str]] = None  # Patient, Observation, Condition, etc.
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class ReportGenerationRequest(BaseModel):
    patient_id: int
    report_type: str  # comprehensive, cognitive_only, medication_summary
    include_charts: bool = True
    include_timeline: bool = True
    date_range_days: Optional[int] = 90


class CohortAnalysisRequest(BaseModel):
    patient_id: int
    demographic_factors: List[str]  # age, gender, education, ethnicity
    clinical_factors: List[str]  # diagnosis_stage, apoe4_status, comorbidities


class PredictiveAnalyticsRequest(BaseModel):
    patient_id: int
    prediction_type: str  # cognitive_decline, hospitalization, caregiver_burnout
    forecast_months: int = 12
    confidence_level: float = 0.95


# ===== Research Contribution =====

@router.post("/research/consent")
async def manage_research_consent(request: ResearchConsentRequest):
    """
    Manage patient consent for research data contribution

    Data sharing levels:
    - anonymized: No identifying information
    - aggregated: Combined with other data
    - identifiable: Full medical records (requires explicit consent)
    """
    try:
        result = research_contribution_service.manage_consent(
            patient_id=request.patient_id,
            consent_given=request.consent_given,
            data_sharing_level=request.data_sharing_level,
            allowed_uses=request.allowed_uses
        )
        return result
    except Exception as e:
        logger.error(f"Error managing research consent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/research/consent/{patient_id}")
async def get_research_consent(patient_id: int):
    """Get current research consent status"""
    try:
        consent = research_contribution_service.get_consent_status(patient_id)
        return consent
    except Exception as e:
        logger.error(f"Error getting research consent: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/research/contribute/{patient_id}")
async def contribute_data_to_research(patient_id: int):
    """
    Contribute anonymized patient data to research databases

    Only executed if patient has given consent
    Returns contribution ID for tracking
    """
    try:
        result = research_contribution_service.contribute_data(patient_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error contributing data to research: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== FHIR Export =====

@router.post("/fhir/export")
async def export_fhir_data(request: FHIRExportRequest):
    """
    Export patient data in FHIR (Fast Healthcare Interoperability Resources) format

    Compatible with major EHR systems: Epic, Cerner, Allscripts, etc.

    Resource types:
    - Patient: Demographics and identifiers
    - Observation: Cognitive tests, vital signs
    - Condition: Diagnoses and comorbidities
    - MedicationRequest: Prescriptions
    - CarePlan: Treatment plans
    - DocumentReference: Reports and imaging
    """
    try:
        fhir_bundle = fhir_export_service.export_patient_data(
            patient_id=request.patient_id,
            resource_types=request.resource_types,
            start_date=request.start_date,
            end_date=request.end_date
        )
        return fhir_bundle
    except Exception as e:
        logger.error(f"Error exporting FHIR data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fhir/validate/{patient_id}")
async def validate_fhir_export(patient_id: int):
    """Validate FHIR export against official schema"""
    try:
        validation = fhir_export_service.validate_export(patient_id)
        return validation
    except Exception as e:
        logger.error(f"Error validating FHIR export: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Report Generation =====

@router.post("/reports/generate")
async def generate_medical_report(request: ReportGenerationRequest):
    """
    Generate comprehensive PDF report for healthcare providers

    Includes:
    - Cognitive assessment timeline with charts
    - Medication history
    - Intervention effectiveness
    - Risk predictions
    - Clinical recommendations
    """
    try:
        pdf_bytes = report_generation_service.generate_pdf_report(
            patient_id=request.patient_id,
            report_type=request.report_type,
            include_charts=request.include_charts,
            include_timeline=request.include_timeline,
            date_range_days=request.date_range_days
        )

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=patient_{request.patient_id}_report.pdf"}
        )
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/reports/history/{patient_id}")
async def get_report_history(patient_id: int):
    """Get history of generated reports"""
    try:
        history = report_generation_service.get_report_history(patient_id)
        return {"patient_id": patient_id, "reports": history}
    except Exception as e:
        logger.error(f"Error getting report history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Analytics Dashboard =====

@router.get("/analytics/population-insights")
async def get_population_insights(
    min_age: Optional[int] = None,
    max_age: Optional[int] = None,
    diagnosis_stage: Optional[str] = None
):
    """
    Population-level insights for researchers

    Aggregated, anonymized data showing:
    - Demographic distributions
    - Cognitive decline trends
    - Intervention effectiveness
    - Comorbidity correlations
    """
    try:
        insights = analytics_service.get_population_insights(
            min_age=min_age,
            max_age=max_age,
            diagnosis_stage=diagnosis_stage
        )
        return insights
    except Exception as e:
        logger.error(f"Error getting population insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/intervention-effectiveness")
async def analyze_intervention_effectiveness(intervention_type: str):
    """
    Analyze effectiveness of interventions across population

    Intervention types: medication, cognitive_training, lifestyle, etc.
    """
    try:
        analysis = analytics_service.analyze_intervention_effectiveness(
            intervention_type=intervention_type
        )
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing intervention effectiveness: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/risk-factors")
async def analyze_risk_factors():
    """Analyze correlation between risk factors and cognitive decline"""
    try:
        analysis = analytics_service.analyze_risk_factors()
        return analysis
    except Exception as e:
        logger.error(f"Error analyzing risk factors: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Cohort Analysis =====

@router.post("/cohort/compare")
async def compare_to_cohort(request: CohortAnalysisRequest):
    """
    Compare patient to similar demographic and clinical cohorts

    Provides context for:
    - Expected cognitive trajectory
    - Treatment response predictions
    - Benchmark comparisons
    """
    try:
        comparison = cohort_analysis_service.compare_patient_to_cohort(
            patient_id=request.patient_id,
            demographic_factors=request.demographic_factors,
            clinical_factors=request.clinical_factors
        )
        return comparison
    except Exception as e:
        logger.error(f"Error comparing to cohort: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cohort/find-similar/{patient_id}")
async def find_similar_patients(patient_id: int, limit: int = 10):
    """
    Find similar anonymized patients for comparison

    Matches on: age, gender, diagnosis stage, APOE4 status, comorbidities
    All data is anonymized for privacy
    """
    try:
        similar = cohort_analysis_service.find_similar_patients(
            patient_id=patient_id,
            limit=limit
        )
        return {"patient_id": patient_id, "similar_patients": similar}
    except Exception as e:
        logger.error(f"Error finding similar patients: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Predictive Analytics =====

@router.post("/predictive/forecast")
async def forecast_cognitive_trajectory(request: PredictiveAnalyticsRequest):
    """
    Forecast future cognitive trajectory using ML models

    Prediction types:
    - cognitive_decline: MMSE/MoCA score predictions
    - hospitalization: Risk of hospitalization
    - caregiver_burnout: Caregiver stress levels
    - mortality: Survival analysis

    Returns predictions with confidence intervals
    """
    try:
        forecast = predictive_analytics_service.generate_forecast(
            patient_id=request.patient_id,
            prediction_type=request.prediction_type,
            forecast_months=request.forecast_months,
            confidence_level=request.confidence_level
        )
        return forecast
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating forecast: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictive/risk-score/{patient_id}")
async def calculate_comprehensive_risk_score(patient_id: int):
    """
    Calculate comprehensive risk score combining multiple factors

    Considers:
    - Cognitive trajectory
    - Genetic factors
    - Comorbidities
    - Social determinants
    - Lifestyle factors
    """
    try:
        risk_score = predictive_analytics_service.calculate_risk_score(patient_id)
        return risk_score
    except Exception as e:
        logger.error(f"Error calculating risk score: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/predictive/what-if/{patient_id}")
async def what_if_analysis(
    patient_id: int,
    intervention: str,
    adherence_rate: float = 0.8
):
    """
    What-if analysis: Predict outcomes with different interventions

    Examples:
    - "What if patient starts donepezil?"
    - "What if patient exercises 3x/week?"
    - "What if caregiver gets respite care?"
    """
    try:
        analysis = predictive_analytics_service.what_if_analysis(
            patient_id=patient_id,
            intervention=intervention,
            adherence_rate=adherence_rate
        )
        return analysis
    except Exception as e:
        logger.error(f"Error performing what-if analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))
