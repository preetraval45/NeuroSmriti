"""
Communication API Endpoints
Video calls, family portal, care team chat, translation, TTS, emergency alerts
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

from app.core.database import get_db
from app.services.communication_service import (
    video_chat_service,
    family_portal_service,
    care_team_chat_service,
    translation_service,
    text_to_speech_service,
    emergency_alert_service
)
from loguru import logger

router = APIRouter(prefix="/communication", tags=["Communication"])


# ===== Pydantic Models =====

class VideoRoomRequest(BaseModel):
    patient_id: int
    provider_id: int
    scheduled_time: Optional[datetime] = None
    duration_minutes: int = 30


class JoinRoomRequest(BaseModel):
    room_id: str
    token: str
    user_id: int


class FamilyMemberRequest(BaseModel):
    patient_id: int
    email: EmailStr
    relationship: str
    permissions: List[str]


class ConversationRequest(BaseModel):
    patient_id: int
    participants: List[dict]
    subject: str


class MessageRequest(BaseModel):
    conversation_id: str
    sender_id: int
    message_text: str
    attachments: Optional[List[str]] = None


class TranslationRequest(BaseModel):
    text: str
    source_lang: str
    target_lang: str


class TextToSpeechRequest(BaseModel):
    text: str
    voice_id: str = "en-US-female"
    speed: float = 1.0
    pitch: float = 1.0


class EmergencyContactsRequest(BaseModel):
    patient_id: int
    contacts: List[dict]


class EmergencyAlertRequest(BaseModel):
    patient_id: int
    alert_type: str
    location: Optional[dict] = None
    message: Optional[str] = None


# ===== Video Chat Endpoints =====

@router.post("/video/create-room")
async def create_video_room(request: VideoRoomRequest):
    """
    Create a video consultation room

    Returns room ID and access tokens for patient and provider
    """
    try:
        result = video_chat_service.create_room(
            patient_id=request.patient_id,
            provider_id=request.provider_id,
            scheduled_time=request.scheduled_time,
            duration_minutes=request.duration_minutes
        )
        return result
    except Exception as e:
        logger.error(f"Error creating video room: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/video/join-room")
async def join_video_room(request: JoinRoomRequest):
    """Join a video room with token verification"""
    try:
        result = video_chat_service.join_room(
            room_id=request.room_id,
            token=request.token,
            user_id=request.user_id
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error joining video room: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/video/end-session/{room_id}")
async def end_video_session(room_id: str):
    """End video session and get summary"""
    try:
        result = video_chat_service.end_session(room_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error ending video session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Family Portal Endpoints =====

@router.post("/family-portal/add-member")
async def add_family_member(request: FamilyMemberRequest):
    """
    Add family member with specific permissions

    Permissions: view_assessments, view_medications, view_appointments,
                 view_care_plan, receive_alerts
    """
    try:
        result = family_portal_service.add_family_member(
            patient_id=request.patient_id,
            family_member_email=request.email,
            relationship=request.relationship,
            permissions=request.permissions
        )
        return result
    except Exception as e:
        logger.error(f"Error adding family member: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/family-portal/updates/{patient_id}/{member_id}")
async def get_patient_updates(patient_id: int, member_id: str, days: int = 7):
    """Get patient updates for family member"""
    try:
        result = family_portal_service.get_patient_updates(
            patient_id=patient_id,
            member_id=member_id,
            days=days
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting patient updates: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Care Team Chat Endpoints =====

@router.post("/chat/create-conversation")
async def create_conversation(request: ConversationRequest):
    """Create HIPAA-compliant care team conversation"""
    try:
        result = care_team_chat_service.create_conversation(
            patient_id=request.patient_id,
            participants=request.participants,
            subject=request.subject
        )
        return result
    except Exception as e:
        logger.error(f"Error creating conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat/send-message")
async def send_message(request: MessageRequest):
    """Send HIPAA-compliant message"""
    try:
        result = care_team_chat_service.send_message(
            conversation_id=request.conversation_id,
            sender_id=request.sender_id,
            message_text=request.message_text,
            attachments=request.attachments
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/chat/messages/{conversation_id}/{user_id}")
async def get_messages(conversation_id: str, user_id: int, limit: int = 50):
    """Get messages for conversation"""
    try:
        messages = care_team_chat_service.get_messages(
            conversation_id=conversation_id,
            user_id=user_id,
            limit=limit
        )
        return {"messages": messages}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting messages: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Translation Endpoints =====

@router.post("/translate")
async def translate_text(request: TranslationRequest):
    """Translate text between languages"""
    try:
        result = translation_service.translate_text(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error translating text: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/translate/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    languages = translation_service.get_supported_languages()
    return {"languages": languages}


# ===== Text-to-Speech Endpoints =====

@router.post("/tts/synthesize")
async def synthesize_speech(request: TextToSpeechRequest):
    """
    Convert text to speech configuration

    Client will use Web Speech API to actually play audio
    """
    try:
        result = text_to_speech_service.synthesize_speech(
            text=request.text,
            voice_id=request.voice_id,
            speed=request.speed,
            pitch=request.pitch
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error synthesizing speech: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tts/voices")
async def get_available_voices():
    """Get list of available TTS voices"""
    voices = text_to_speech_service.get_available_voices()
    return {"voices": voices}


# ===== Emergency Alert Endpoints =====

@router.post("/emergency/set-contacts")
async def set_emergency_contacts(request: EmergencyContactsRequest):
    """Set emergency contacts for patient"""
    try:
        result = emergency_alert_service.set_emergency_contacts(
            patient_id=request.patient_id,
            contacts=request.contacts
        )
        return result
    except Exception as e:
        logger.error(f"Error setting emergency contacts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/emergency/trigger-alert")
async def trigger_emergency_alert(request: EmergencyAlertRequest):
    """
    Trigger emergency alert to all contacts

    Alert types: fall, wandering, medical, panic_button
    """
    try:
        result = emergency_alert_service.trigger_emergency_alert(
            patient_id=request.patient_id,
            alert_type=request.alert_type,
            location=request.location,
            message=request.message
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error triggering emergency alert: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/emergency/alert-history/{patient_id}")
async def get_alert_history(patient_id: int, days: int = 30):
    """Get emergency alert history"""
    try:
        alerts = emergency_alert_service.get_alert_history(
            patient_id=patient_id,
            days=days
        )
        return {"alerts": alerts}
    except Exception as e:
        logger.error(f"Error getting alert history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
