"""
Safety & Monitoring API Endpoints
GPS wandering, fall detection, activity monitoring, medication compliance,
home safety, caregiver burnout
"""

from fastapi import APIRouter, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from app.services.safety_monitoring_service import (
    gps_wandering_service,
    fall_detection_service,
    activity_monitoring_service,
    medication_compliance_service,
    home_safety_service,
    caregiver_burnout_service
)
from loguru import logger

router = APIRouter(prefix="/safety", tags=["Safety & Monitoring"])


# ===== Pydantic Models =====

class SafeZoneRequest(BaseModel):
    patient_id: int
    zone_name: str
    center_lat: float
    center_lon: float
    radius_meters: float
    active_times: Optional[List[dict]] = None


class LocationCheckRequest(BaseModel):
    patient_id: int
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None


class AccelerometerDataRequest(BaseModel):
    patient_id: int
    accelerometer_readings: List[dict]
    sampling_rate_hz: int = 50


class ActivityLogRequest(BaseModel):
    patient_id: int
    activity_type: str
    duration_minutes: int
    timestamp: Optional[datetime] = None


class MedicationScheduleRequest(BaseModel):
    patient_id: int
    medications: List[dict]


class MedicationVerificationRequest(BaseModel):
    patient_id: int
    medication_name: str
    photo_path: Optional[str] = None
    timestamp: Optional[datetime] = None


class HomeSafetyAssessmentRequest(BaseModel):
    patient_id: int
    home_type: str = "house"


class AssessmentUpdateRequest(BaseModel):
    assessment_id: str
    category: str
    item: str
    completed: bool
    notes: Optional[str] = None


class BurnoutAssessmentRequest(BaseModel):
    caregiver_id: int
    responses: dict


# ===== GPS Wandering Detection Endpoints =====

@router.post("/gps/create-safe-zone")
async def create_safe_zone(request: SafeZoneRequest):
    """
    Create geofence safe zone for wandering detection

    Example active_times: [{"start": "08:00", "end": "20:00"}]
    """
    try:
        result = gps_wandering_service.create_safe_zone(
            patient_id=request.patient_id,
            zone_name=request.zone_name,
            center_lat=request.center_lat,
            center_lon=request.center_lon,
            radius_meters=request.radius_meters,
            active_times=request.active_times
        )
        return result
    except Exception as e:
        logger.error(f"Error creating safe zone: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/gps/check-location")
async def check_location(request: LocationCheckRequest):
    """
    Check if patient location is within safe zones

    Triggers wandering alert if outside safe zone during active hours
    """
    try:
        result = gps_wandering_service.check_location(
            patient_id=request.patient_id,
            latitude=request.latitude,
            longitude=request.longitude,
            timestamp=request.timestamp
        )
        return result
    except Exception as e:
        logger.error(f"Error checking location: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/gps/safe-zones/{patient_id}")
async def get_safe_zones(patient_id: int):
    """Get all safe zones for patient"""
    try:
        zones = gps_wandering_service.safe_zones.get(patient_id, [])
        return {"patient_id": patient_id, "safe_zones": zones}
    except Exception as e:
        logger.error(f"Error getting safe zones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Fall Detection Endpoints =====

@router.post("/fall-detection/analyze")
async def analyze_fall_detection(request: AccelerometerDataRequest):
    """
    Analyze accelerometer data for fall detection

    Accelerometer readings format:
    [{"x": 0.1, "y": 0.2, "z": 9.8, "timestamp": "2024-01-01T12:00:00"}, ...]
    """
    try:
        result = fall_detection_service.analyze_accelerometer_data(
            patient_id=request.patient_id,
            accelerometer_readings=request.accelerometer_readings,
            sampling_rate_hz=request.sampling_rate_hz
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing fall detection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fall-detection/history/{patient_id}")
async def get_fall_history(patient_id: int):
    """Get fall detection history for patient"""
    try:
        falls = [f for f in fall_detection_service.fall_history if f["patient_id"] == patient_id]
        return {"patient_id": patient_id, "fall_events": falls}
    except Exception as e:
        logger.error(f"Error getting fall history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Activity Monitoring Endpoints =====

@router.post("/activity/log")
async def log_activity(request: ActivityLogRequest):
    """
    Log patient activity

    Activity types: walking, sleeping, eating, social, cognitive_task
    """
    try:
        result = activity_monitoring_service.log_activity(
            patient_id=request.patient_id,
            activity_type=request.activity_type,
            duration_minutes=request.duration_minutes,
            timestamp=request.timestamp
        )
        return result
    except Exception as e:
        logger.error(f"Error logging activity: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activity/analyze/{patient_id}")
async def analyze_activity_patterns(patient_id: int, days: int = 7):
    """
    Analyze activity patterns for anomalies

    Detects: reduced activity, sleep issues, social isolation
    """
    try:
        result = activity_monitoring_service.analyze_daily_patterns(
            patient_id=patient_id,
            analysis_days=days
        )
        return result
    except Exception as e:
        logger.error(f"Error analyzing activity patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/activity/set-baseline/{patient_id}")
async def set_activity_baseline(patient_id: int):
    """Set baseline activity pattern (uses last 14 days)"""
    try:
        activity_monitoring_service.set_baseline(patient_id)
        return {"message": "Baseline set successfully", "patient_id": patient_id}
    except Exception as e:
        logger.error(f"Error setting baseline: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Medication Compliance Endpoints =====

@router.post("/medication/set-schedule")
async def set_medication_schedule(request: MedicationScheduleRequest):
    """
    Set medication schedule for patient

    Medications format:
    [{"name": "Donepezil", "dosage": "10mg", "times": ["08:00", "20:00"]}]
    """
    try:
        result = medication_compliance_service.set_medication_schedule(
            patient_id=request.patient_id,
            medications=request.medications
        )
        return result
    except Exception as e:
        logger.error(f"Error setting medication schedule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/medication/verify")
async def verify_medication_taken(request: MedicationVerificationRequest):
    """Verify medication was taken (with optional photo)"""
    try:
        result = medication_compliance_service.verify_medication_taken(
            patient_id=request.patient_id,
            medication_name=request.medication_name,
            photo_path=request.photo_path,
            timestamp=request.timestamp
        )
        return result
    except Exception as e:
        logger.error(f"Error verifying medication: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/medication/compliance/{patient_id}")
async def get_compliance_report(patient_id: int, days: int = 7):
    """Get medication compliance report"""
    try:
        result = medication_compliance_service.get_compliance_report(
            patient_id=patient_id,
            days=days
        )
        return result
    except Exception as e:
        logger.error(f"Error getting compliance report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Home Safety Checklist Endpoints =====

@router.post("/home-safety/create-assessment")
async def create_home_assessment(request: HomeSafetyAssessmentRequest):
    """Create home safety assessment"""
    try:
        result = home_safety_service.create_assessment(
            patient_id=request.patient_id,
            home_type=request.home_type
        )
        return result
    except Exception as e:
        logger.error(f"Error creating home assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/home-safety/update-item")
async def update_assessment_item(request: AssessmentUpdateRequest):
    """Update home safety checklist item"""
    try:
        result = home_safety_service.update_assessment(
            assessment_id=request.assessment_id,
            category=request.category,
            item=request.item,
            completed=request.completed,
            notes=request.notes
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating assessment item: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/home-safety/report/{assessment_id}")
async def get_assessment_report(assessment_id: str):
    """Get full home safety assessment report with recommendations"""
    try:
        result = home_safety_service.get_assessment_report(assessment_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting assessment report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/home-safety/checklist")
async def get_safety_checklist():
    """Get complete home safety checklist template"""
    return {"checklist": home_safety_service.SAFETY_CHECKLIST}


# ===== Caregiver Burnout Monitoring Endpoints =====

@router.post("/caregiver/assess-burnout")
async def assess_caregiver_burnout(request: BurnoutAssessmentRequest):
    """
    Assess caregiver burnout and get recommendations

    Response scores (1-5 scale):
    - feel_overwhelmed
    - time_for_self
    - emotional_strain
    - physical_exhaustion
    - sleep_quality
    - social_isolation
    - financial_stress
    - relationship_strain
    """
    try:
        result = caregiver_burnout_service.assess_burnout(
            caregiver_id=request.caregiver_id,
            responses=request.responses
        )
        return result
    except Exception as e:
        logger.error(f"Error assessing caregiver burnout: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/caregiver/stress-trend/{caregiver_id}")
async def get_caregiver_stress_trend(caregiver_id: int, days: int = 30):
    """Get caregiver stress trend over time"""
    try:
        result = caregiver_burnout_service.get_stress_trend(
            caregiver_id=caregiver_id,
            days=days
        )
        return result
    except Exception as e:
        logger.error(f"Error getting stress trend: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/caregiver/resources")
async def get_caregiver_resources():
    """Get caregiver support resources"""
    return {
        "hotlines": [
            {"name": "National Caregiver Support", "phone": "1-800-XXX-XXXX"},
            {"name": "Alzheimer's Association 24/7 Helpline", "phone": "1-800-272-3900"}
        ],
        "online_resources": [
            {"title": "Caregiver Support Groups", "url": "https://www.alz.org/help-support"},
            {"title": "Respite Care Locator", "url": "https://archrespite.org/respitelocator"},
            {"title": "Family Caregiver Alliance", "url": "https://www.caregiver.org"}
        ],
        "local_services": [
            "Adult day care programs",
            "In-home respite care",
            "Meal delivery services",
            "Transportation assistance"
        ]
    }
