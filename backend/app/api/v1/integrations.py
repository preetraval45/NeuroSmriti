"""
Integration & Automation API Endpoints
EHR integration, wearable sync, smart home, calendar, pharmacy, insurance
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.integration_service import (
    ehr_integration_service,
    wearable_sync_service,
    smart_home_service,
    calendar_sync_service,
    pharmacy_service,
    insurance_service
)
from loguru import logger

router = APIRouter(prefix="/integrations", tags=["Integration & Automation"])


# ===== Pydantic Models =====

class EHRConnectionRequest(BaseModel):
    patient_id: int
    ehr_system: str  # epic, cerner, allscripts, athenahealth
    credentials: Dict[str, str]
    auto_sync: bool = True


class WearableConnectionRequest(BaseModel):
    patient_id: int
    device_type: str  # apple_watch, fitbit, garmin, samsung_health
    oauth_token: str


class SmartHomeDeviceRequest(BaseModel):
    patient_id: int
    device_type: str  # alexa, google_home, homekit
    device_id: str
    capabilities: List[str]


class ReminderRequest(BaseModel):
    patient_id: int
    reminder_type: str  # medication, appointment, exercise, hydration
    message: str
    schedule: Dict[str, Any]  # cron-like schedule or specific times


class CalendarSyncRequest(BaseModel):
    patient_id: int
    calendar_service: str  # google, outlook, apple
    oauth_token: str
    sync_direction: str = "bidirectional"  # import, export, bidirectional


class PharmacyConnectionRequest(BaseModel):
    patient_id: int
    pharmacy_name: str
    pharmacy_npi: str
    auto_refill_enabled: bool = True


class InsuranceClaimRequest(BaseModel):
    patient_id: int
    service_date: datetime
    service_type: str
    provider_id: str
    amount: float
    diagnosis_codes: List[str]


# ===== EHR Integration =====

@router.post("/ehr/connect")
async def connect_ehr_system(request: EHRConnectionRequest):
    """
    Connect to Electronic Health Record system

    Supported EHRs:
    - Epic: MyChart API
    - Cerner: HealtheLife
    - Allscripts: FollowMyHealth
    - Athenahealth: Patient API

    Uses SMART on FHIR standard
    """
    try:
        connection = ehr_integration_service.connect_ehr(
            patient_id=request.patient_id,
            ehr_system=request.ehr_system,
            credentials=request.credentials,
            auto_sync=request.auto_sync
        )
        return connection
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error connecting EHR: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ehr/sync/{patient_id}")
async def sync_ehr_data(patient_id: int, background_tasks: BackgroundTasks):
    """
    Sync data from EHR to NeuroSmriti

    Imports:
    - Lab results
    - Medications
    - Allergies
    - Immunizations
    - Problem list
    - Visit summaries
    """
    try:
        background_tasks.add_task(ehr_integration_service.sync_patient_data, patient_id)
        return {
            "message": "EHR sync started",
            "patient_id": patient_id,
            "status": "processing"
        }
    except Exception as e:
        logger.error(f"Error syncing EHR data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ehr/sync-status/{patient_id}")
async def get_ehr_sync_status(patient_id: int):
    """Get status of last EHR sync"""
    try:
        status = ehr_integration_service.get_sync_status(patient_id)
        return status
    except Exception as e:
        logger.error(f"Error getting sync status: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Wearable Device Sync =====

@router.post("/wearables/connect")
async def connect_wearable(request: WearableConnectionRequest):
    """
    Connect wearable device for health data sync

    Supported devices:
    - Apple Watch: HealthKit integration
    - Fitbit: Web API
    - Garmin: Health API
    - Samsung Health: Partner API

    Syncs: Steps, heart rate, sleep, activity, etc.
    """
    try:
        connection = wearable_sync_service.connect_device(
            patient_id=request.patient_id,
            device_type=request.device_type,
            oauth_token=request.oauth_token
        )
        return connection
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error connecting wearable: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/wearables/data/{patient_id}")
async def get_wearable_data(
    patient_id: int,
    data_type: Optional[str] = None,
    days: int = 7
):
    """
    Get synced wearable data

    Data types: steps, heart_rate, sleep, activity, exercise
    """
    try:
        data = wearable_sync_service.get_patient_data(
            patient_id=patient_id,
            data_type=data_type,
            days=days
        )
        return data
    except Exception as e:
        logger.error(f"Error getting wearable data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/wearables/sync/{patient_id}")
async def sync_wearable_data(patient_id: int, background_tasks: BackgroundTasks):
    """Manually trigger wearable data sync"""
    try:
        background_tasks.add_task(wearable_sync_service.sync_data, patient_id)
        return {
            "message": "Wearable sync started",
            "patient_id": patient_id,
            "status": "processing"
        }
    except Exception as e:
        logger.error(f"Error syncing wearable data: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Smart Home Integration =====

@router.post("/smart-home/connect")
async def connect_smart_home_device(request: SmartHomeDeviceRequest):
    """
    Connect smart home device for medication reminders and alerts

    Devices:
    - Amazon Alexa: Voice reminders, emergency calls
    - Google Home: Medication reminders, calendar
    - Apple HomeKit: Automation triggers

    Capabilities: reminders, announcements, emergency_contact
    """
    try:
        connection = smart_home_service.connect_device(
            patient_id=request.patient_id,
            device_type=request.device_type,
            device_id=request.device_id,
            capabilities=request.capabilities
        )
        return connection
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error connecting smart home device: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/smart-home/send-reminder")
async def send_smart_home_reminder(request: ReminderRequest):
    """Send reminder through smart home device"""
    try:
        result = smart_home_service.send_reminder(
            patient_id=request.patient_id,
            reminder_type=request.reminder_type,
            message=request.message
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error sending reminder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/smart-home/schedule-reminder")
async def schedule_recurring_reminder(request: ReminderRequest):
    """Schedule recurring reminder"""
    try:
        schedule = smart_home_service.schedule_reminder(
            patient_id=request.patient_id,
            reminder_type=request.reminder_type,
            message=request.message,
            schedule=request.schedule
        )
        return schedule
    except Exception as e:
        logger.error(f"Error scheduling reminder: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Calendar Sync =====

@router.post("/calendar/connect")
async def connect_calendar(request: CalendarSyncRequest):
    """
    Connect calendar for appointment sync

    Services:
    - Google Calendar: OAuth 2.0
    - Outlook Calendar: Microsoft Graph API
    - Apple Calendar: iCloud API

    Syncs doctor appointments, medication schedules, cognitive tests
    """
    try:
        connection = calendar_sync_service.connect_calendar(
            patient_id=request.patient_id,
            calendar_service=request.calendar_service,
            oauth_token=request.oauth_token,
            sync_direction=request.sync_direction
        )
        return connection
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error connecting calendar: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/calendar/upcoming/{patient_id}")
async def get_upcoming_appointments(patient_id: int, days: int = 30):
    """Get upcoming appointments from synced calendar"""
    try:
        appointments = calendar_sync_service.get_upcoming_appointments(
            patient_id=patient_id,
            days=days
        )
        return {"appointments": appointments}
    except Exception as e:
        logger.error(f"Error getting appointments: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/calendar/add-appointment")
async def add_appointment_to_calendar(
    patient_id: int,
    title: str,
    start_time: datetime,
    duration_minutes: int,
    description: Optional[str] = None,
    location: Optional[str] = None
):
    """Add appointment to synced calendar"""
    try:
        event = calendar_sync_service.add_appointment(
            patient_id=patient_id,
            title=title,
            start_time=start_time,
            duration_minutes=duration_minutes,
            description=description,
            location=location
        )
        return event
    except Exception as e:
        logger.error(f"Error adding appointment: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Pharmacy Integration =====

@router.post("/pharmacy/connect")
async def connect_pharmacy(request: PharmacyConnectionRequest):
    """
    Connect to pharmacy for prescription management

    Features:
    - Auto-refill reminders
    - Delivery scheduling
    - Prescription history
    - Drug interaction checks
    """
    try:
        connection = pharmacy_service.connect_pharmacy(
            patient_id=request.patient_id,
            pharmacy_name=request.pharmacy_name,
            pharmacy_npi=request.pharmacy_npi,
            auto_refill_enabled=request.auto_refill_enabled
        )
        return connection
    except Exception as e:
        logger.error(f"Error connecting pharmacy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/pharmacy/prescriptions/{patient_id}")
async def get_prescriptions(patient_id: int, active_only: bool = True):
    """Get patient prescriptions"""
    try:
        prescriptions = pharmacy_service.get_prescriptions(
            patient_id=patient_id,
            active_only=active_only
        )
        return {"prescriptions": prescriptions}
    except Exception as e:
        logger.error(f"Error getting prescriptions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/pharmacy/refill/{prescription_id}")
async def request_refill(prescription_id: str, delivery: bool = False):
    """Request prescription refill"""
    try:
        refill = pharmacy_service.request_refill(
            prescription_id=prescription_id,
            delivery=delivery
        )
        return refill
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error requesting refill: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Insurance Portal =====

@router.post("/insurance/submit-claim")
async def submit_insurance_claim(request: InsuranceClaimRequest):
    """
    Submit insurance claim

    Supports major insurers:
    - Medicare/Medicaid
    - Private insurance (Aetna, UnitedHealthcare, Cigna, etc.)

    Auto-fills CPT codes for common Alzheimer's services
    """
    try:
        claim = insurance_service.submit_claim(
            patient_id=request.patient_id,
            service_date=request.service_date,
            service_type=request.service_type,
            provider_id=request.provider_id,
            amount=request.amount,
            diagnosis_codes=request.diagnosis_codes
        )
        return claim
    except Exception as e:
        logger.error(f"Error submitting insurance claim: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insurance/claims/{patient_id}")
async def get_insurance_claims(patient_id: int, status: Optional[str] = None):
    """
    Get insurance claim history

    Status: pending, approved, denied, resubmitted
    """
    try:
        claims = insurance_service.get_claims(
            patient_id=patient_id,
            status=status
        )
        return {"claims": claims}
    except Exception as e:
        logger.error(f"Error getting insurance claims: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insurance/coverage/{patient_id}")
async def get_coverage_info(patient_id: int):
    """Get insurance coverage information for Alzheimer's care"""
    try:
        coverage = insurance_service.get_coverage_info(patient_id)
        return coverage
    except Exception as e:
        logger.error(f"Error getting coverage info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/insurance/eligibility/{patient_id}")
async def check_eligibility(patient_id: int, service_type: str):
    """Check insurance eligibility for specific service"""
    try:
        eligibility = insurance_service.check_eligibility(
            patient_id=patient_id,
            service_type=service_type
        )
        return eligibility
    except Exception as e:
        logger.error(f"Error checking eligibility: {e}")
        raise HTTPException(status_code=500, detail=str(e))
