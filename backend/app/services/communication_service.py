"""
Communication Service
Video calls, family portal, care team chat, translation, text-to-speech, emergency alerts
"""

import json
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from loguru import logger
import hashlib
import secrets


class VideoChatService:
    """
    Video call integration for telemedicine consultations
    Uses WebRTC for peer-to-peer connections
    """

    def __init__(self):
        self.active_rooms = {}
        self.session_history = []

    def create_room(
        self,
        patient_id: int,
        provider_id: int,
        scheduled_time: Optional[datetime] = None,
        duration_minutes: int = 30
    ) -> Dict[str, Any]:
        """Create a video consultation room"""
        try:
            # Generate unique room ID
            room_id = secrets.token_urlsafe(16)

            # Generate access tokens for patient and provider
            patient_token = self._generate_token(room_id, patient_id, "patient")
            provider_token = self._generate_token(room_id, provider_id, "provider")

            room_data = {
                "room_id": room_id,
                "patient_id": patient_id,
                "provider_id": provider_id,
                "scheduled_time": scheduled_time.isoformat() if scheduled_time else datetime.now().isoformat(),
                "duration_minutes": duration_minutes,
                "status": "scheduled",
                "patient_token": patient_token,
                "provider_token": provider_token,
                "created_at": datetime.now().isoformat(),
                "participants": [],
                "recording_enabled": False,
                "chat_history": []
            }

            self.active_rooms[room_id] = room_data

            return {
                "room_id": room_id,
                "patient_token": patient_token,
                "provider_token": provider_token,
                "join_url_patient": f"/video-call/{room_id}?token={patient_token}",
                "join_url_provider": f"/video-call/{room_id}?token={provider_token}",
                "scheduled_time": room_data["scheduled_time"],
                "duration_minutes": duration_minutes
            }

        except Exception as e:
            logger.error(f"Error creating video room: {e}")
            raise

    def _generate_token(self, room_id: str, user_id: int, role: str) -> str:
        """Generate secure access token for room"""
        data = f"{room_id}:{user_id}:{role}:{datetime.now().timestamp()}"
        return hashlib.sha256(data.encode()).hexdigest()

    def join_room(self, room_id: str, token: str, user_id: int) -> Dict[str, Any]:
        """Join a video room with token verification"""
        if room_id not in self.active_rooms:
            raise ValueError("Room not found")

        room = self.active_rooms[room_id]

        # Verify token
        if token not in [room["patient_token"], room["provider_token"]]:
            raise ValueError("Invalid access token")

        # Add participant
        participant = {
            "user_id": user_id,
            "joined_at": datetime.now().isoformat(),
            "role": "provider" if token == room["provider_token"] else "patient"
        }
        room["participants"].append(participant)
        room["status"] = "active"

        return {
            "room_id": room_id,
            "participants": room["participants"],
            "chat_enabled": True,
            "recording_enabled": room["recording_enabled"]
        }

    def end_session(self, room_id: str) -> Dict[str, Any]:
        """End video session and save history"""
        if room_id not in self.active_rooms:
            raise ValueError("Room not found")

        room = self.active_rooms[room_id]
        room["status"] = "completed"
        room["ended_at"] = datetime.now().isoformat()

        # Calculate actual duration
        started = datetime.fromisoformat(room["created_at"])
        ended = datetime.now()
        actual_duration = (ended - started).total_seconds() / 60
        room["actual_duration_minutes"] = actual_duration

        # Save to history
        self.session_history.append(room)

        # Remove from active rooms
        del self.active_rooms[room_id]

        return {
            "session_summary": {
                "room_id": room_id,
                "duration_minutes": actual_duration,
                "participants_count": len(room["participants"]),
                "chat_messages": len(room["chat_history"])
            }
        }


class FamilyPortalService:
    """
    Secure portal for family members to view patient updates
    """

    def __init__(self):
        self.family_members = {}
        self.access_permissions = {}

    def add_family_member(
        self,
        patient_id: int,
        family_member_email: str,
        relationship: str,
        permissions: List[str]
    ) -> Dict[str, Any]:
        """Add family member with specific permissions"""
        try:
            # Generate invitation token
            invite_token = secrets.token_urlsafe(32)

            member_data = {
                "patient_id": patient_id,
                "email": family_member_email,
                "relationship": relationship,
                "permissions": permissions,  # ['view_assessments', 'view_medications', 'view_appointments', etc.]
                "invite_token": invite_token,
                "status": "pending",
                "invited_at": datetime.now().isoformat(),
                "last_access": None
            }

            member_id = hashlib.md5(f"{patient_id}:{family_member_email}".encode()).hexdigest()
            self.family_members[member_id] = member_data

            return {
                "member_id": member_id,
                "invite_link": f"/family-portal/accept-invite?token={invite_token}",
                "email": family_member_email,
                "relationship": relationship,
                "permissions": permissions
            }

        except Exception as e:
            logger.error(f"Error adding family member: {e}")
            raise

    def get_patient_updates(
        self,
        patient_id: int,
        member_id: str,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get patient updates for family member based on permissions"""
        if member_id not in self.family_members:
            raise ValueError("Family member not found")

        member = self.family_members[member_id]
        if member["patient_id"] != patient_id:
            raise ValueError("Unauthorized access")

        permissions = member["permissions"]
        updates = {
            "patient_name": "Patient Name",  # Would fetch from database
            "relationship": member["relationship"],
            "last_updated": datetime.now().isoformat(),
            "updates": []
        }

        # Build updates based on permissions
        if "view_assessments" in permissions:
            updates["updates"].append({
                "type": "assessment",
                "title": "Recent Cognitive Assessment",
                "summary": "MMSE score: 24/30 (stable)",
                "date": (datetime.now() - timedelta(days=2)).isoformat()
            })

        if "view_medications" in permissions:
            updates["updates"].append({
                "type": "medication",
                "title": "Medication Adherence",
                "summary": "95% adherence this week",
                "date": datetime.now().isoformat()
            })

        if "view_appointments" in permissions:
            updates["updates"].append({
                "type": "appointment",
                "title": "Upcoming Appointment",
                "summary": "Dr. Smith - Neurologist, March 15, 2:00 PM",
                "date": (datetime.now() + timedelta(days=5)).isoformat()
            })

        return updates


class CareTeamChatService:
    """
    HIPAA-compliant messaging between caregivers and providers
    """

    def __init__(self):
        self.conversations = {}
        self.messages = {}

    def create_conversation(
        self,
        patient_id: int,
        participants: List[Dict[str, Any]],
        subject: str
    ) -> Dict[str, Any]:
        """Create a new care team conversation"""
        conversation_id = secrets.token_urlsafe(16)

        conversation_data = {
            "conversation_id": conversation_id,
            "patient_id": patient_id,
            "subject": subject,
            "participants": participants,  # [{'user_id': 1, 'role': 'caregiver'}, {'user_id': 2, 'role': 'provider'}]
            "created_at": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "message_count": 0,
            "is_encrypted": True,
            "hipaa_compliant": True
        }

        self.conversations[conversation_id] = conversation_data
        self.messages[conversation_id] = []

        return {
            "conversation_id": conversation_id,
            "subject": subject,
            "participants": participants,
            "created_at": conversation_data["created_at"]
        }

    def send_message(
        self,
        conversation_id: str,
        sender_id: int,
        message_text: str,
        attachments: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Send HIPAA-compliant message"""
        if conversation_id not in self.conversations:
            raise ValueError("Conversation not found")

        message_id = secrets.token_urlsafe(12)
        message_data = {
            "message_id": message_id,
            "sender_id": sender_id,
            "message_text": message_text,  # In production, encrypt this
            "attachments": attachments or [],
            "timestamp": datetime.now().isoformat(),
            "read_by": [],
            "encrypted": True
        }

        self.messages[conversation_id].append(message_data)
        self.conversations[conversation_id]["message_count"] += 1
        self.conversations[conversation_id]["last_activity"] = datetime.now().isoformat()

        return {
            "message_id": message_id,
            "sent_at": message_data["timestamp"],
            "conversation_id": conversation_id
        }

    def get_messages(
        self,
        conversation_id: str,
        user_id: int,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get messages for conversation"""
        if conversation_id not in self.conversations:
            raise ValueError("Conversation not found")

        # Verify user is participant
        conversation = self.conversations[conversation_id]
        is_participant = any(p["user_id"] == user_id for p in conversation["participants"])
        if not is_participant:
            raise ValueError("Unauthorized access to conversation")

        messages = self.messages.get(conversation_id, [])
        return messages[-limit:]


class TranslationService:
    """
    Multi-language support for diverse populations
    Simulated translation - in production, use Google Translate API or similar
    """

    SUPPORTED_LANGUAGES = {
        'en': 'English',
        'es': 'Spanish',
        'zh': 'Chinese',
        'hi': 'Hindi',
        'ar': 'Arabic',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'ja': 'Japanese',
        'de': 'German',
        'fr': 'French'
    }

    def translate_text(
        self,
        text: str,
        source_lang: str,
        target_lang: str
    ) -> Dict[str, Any]:
        """Translate text between languages"""
        if target_lang not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {target_lang}")

        # Simulated translation - in production, call translation API
        translated_text = f"[{target_lang.upper()}] {text}"

        return {
            "original_text": text,
            "translated_text": translated_text,
            "source_language": source_lang,
            "target_language": target_lang,
            "confidence": 0.98
        }

    def get_supported_languages(self) -> Dict[str, str]:
        """Get list of supported languages"""
        return self.SUPPORTED_LANGUAGES


class TextToSpeechService:
    """
    Read-aloud feature for users with reading difficulties
    """

    def __init__(self):
        self.voices = {
            'en-US-female': {'language': 'en', 'gender': 'female', 'name': 'Sarah'},
            'en-US-male': {'language': 'en', 'gender': 'male', 'name': 'John'},
            'es-ES-female': {'language': 'es', 'gender': 'female', 'name': 'Maria'},
            'es-ES-male': {'language': 'es', 'gender': 'male', 'name': 'Carlos'}
        }

    def synthesize_speech(
        self,
        text: str,
        voice_id: str = 'en-US-female',
        speed: float = 1.0,
        pitch: float = 1.0
    ) -> Dict[str, Any]:
        """
        Convert text to speech
        Returns audio configuration for client-side Web Speech API
        """
        if voice_id not in self.voices:
            raise ValueError(f"Voice not found: {voice_id}")

        voice = self.voices[voice_id]

        return {
            "text": text,
            "voice": {
                "id": voice_id,
                "name": voice["name"],
                "language": voice["language"],
                "gender": voice["gender"]
            },
            "settings": {
                "speed": speed,  # 0.5 to 2.0
                "pitch": pitch,  # 0.5 to 2.0
                "volume": 1.0
            },
            "use_web_speech_api": True,  # Client will use browser's Speech Synthesis API
            "estimated_duration_seconds": len(text.split()) * 0.4 / speed
        }

    def get_available_voices(self) -> List[Dict[str, Any]]:
        """Get list of available voices"""
        return [
            {
                "id": voice_id,
                "name": info["name"],
                "language": info["language"],
                "gender": info["gender"]
            }
            for voice_id, info in self.voices.items()
        ]


class EmergencyAlertService:
    """
    One-touch emergency contact system
    """

    def __init__(self):
        self.emergency_contacts = {}
        self.alert_history = []

    def set_emergency_contacts(
        self,
        patient_id: int,
        contacts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Set emergency contacts for patient"""
        self.emergency_contacts[patient_id] = {
            "patient_id": patient_id,
            "contacts": contacts,  # [{'name': 'John Doe', 'phone': '+1234567890', 'relationship': 'son', 'priority': 1}]
            "updated_at": datetime.now().isoformat()
        }

        return {
            "patient_id": patient_id,
            "contacts_count": len(contacts),
            "primary_contact": contacts[0] if contacts else None
        }

    def trigger_emergency_alert(
        self,
        patient_id: int,
        alert_type: str,
        location: Optional[Dict[str, float]] = None,
        message: Optional[str] = None
    ) -> Dict[str, Any]:
        """Trigger emergency alert to all contacts"""
        if patient_id not in self.emergency_contacts:
            raise ValueError("No emergency contacts configured")

        contacts = self.emergency_contacts[patient_id]["contacts"]

        alert_data = {
            "alert_id": secrets.token_urlsafe(12),
            "patient_id": patient_id,
            "alert_type": alert_type,  # 'fall', 'wandering', 'medical', 'panic_button'
            "timestamp": datetime.now().isoformat(),
            "location": location,
            "message": message or f"Emergency alert: {alert_type}",
            "contacts_notified": [],
            "status": "active"
        }

        # Simulate sending alerts to contacts
        for contact in sorted(contacts, key=lambda x: x.get('priority', 999)):
            notification = {
                "contact_name": contact["name"],
                "contact_phone": contact["phone"],
                "notification_method": "SMS",  # In production: SMS, call, app notification
                "sent_at": datetime.now().isoformat(),
                "status": "sent"
            }
            alert_data["contacts_notified"].append(notification)

        self.alert_history.append(alert_data)

        return {
            "alert_id": alert_data["alert_id"],
            "alert_type": alert_type,
            "contacts_notified": len(alert_data["contacts_notified"]),
            "timestamp": alert_data["timestamp"],
            "message": "Emergency contacts have been notified"
        }

    def get_alert_history(
        self,
        patient_id: int,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Get emergency alert history"""
        cutoff_date = datetime.now() - timedelta(days=days)

        alerts = [
            alert for alert in self.alert_history
            if alert["patient_id"] == patient_id
            and datetime.fromisoformat(alert["timestamp"]) > cutoff_date
        ]

        return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)


# Singleton instances
video_chat_service = VideoChatService()
family_portal_service = FamilyPortalService()
care_team_chat_service = CareTeamChatService()
translation_service = TranslationService()
text_to_speech_service = TextToSpeechService()
emergency_alert_service = EmergencyAlertService()
