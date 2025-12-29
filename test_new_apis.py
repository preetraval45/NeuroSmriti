#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for all new NeuroSmriti API endpoints
Tests all 70+ features added to the platform
"""

import requests
import json
import sys
from datetime import datetime

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:3102"

def test_endpoint(method, endpoint, data=None, description=""):
    """Test a single endpoint and print results"""
    url = f"{BASE_URL}{endpoint}"

    try:
        if method.upper() == "GET":
            response = requests.get(url, params=data)
        elif method.upper() == "POST":
            response = requests.post(url, json=data)
        else:
            return False

        status = "✅ PASS" if response.status_code in [200, 201] else "❌ FAIL"
        print(f"{status} | {method:4} | {endpoint:60} | {description}")

        if response.status_code not in [200, 201, 404]:
            print(f"       Response: {response.status_code} - {response.text[:100]}")

        return response.status_code in [200, 201]
    except Exception as e:
        print(f"❌ ERROR | {method:4} | {endpoint:60} | {str(e)[:50]}")
        return False


def main():
    print("=" * 120)
    print("NEUROSMRITI API ENDPOINT TESTING")
    print("=" * 120)
    print()

    # Test health endpoints
    print("🏥 HEALTH CHECKS")
    print("-" * 120)
    test_endpoint("GET", "/health", description="Application health check")
    test_endpoint("GET", "/", description="Root endpoint")
    test_endpoint("GET", "/api/health", description="API health check")
    print()

    # Test Clinical Decision Support endpoints
    print("🩺 CLINICAL DECISION SUPPORT")
    print("-" * 120)
    test_endpoint("GET", "/api/v1/clinical-support/treatment-plan/1", description="Get treatment plan")
    test_endpoint("POST", "/api/v1/clinical-support/drug-interactions/check",
                  data={"patient_id": 1, "medications": [{"name": "Donepezil", "dosage": "10mg"}]},
                  description="Check drug interactions")
    test_endpoint("POST", "/api/v1/clinical-support/clinical-trials/match",
                  data={"patient_id": 1, "age": 70, "diagnosis": "Alzheimer's", "diagnosis_stage": "mild"},
                  description="Match clinical trials")
    test_endpoint("POST", "/api/v1/clinical-support/genetic-risk/calculate",
                  data={"patient_id": 1, "genetic_markers": {"APOE4": "e4/e4"}},
                  description="Calculate genetic risk")
    test_endpoint("GET", "/api/v1/clinical-support/genetic-risk/recommendations/1",
                  description="Get genetic recommendations")
    test_endpoint("POST", "/api/v1/clinical-support/comorbidity/track",
                  data={"patient_id": 1, "comorbidities": ["diabetes", "hypertension"]},
                  description="Track comorbidities")
    test_endpoint("POST", "/api/v1/clinical-support/lifestyle/recommendations",
                  data={"patient_id": 1, "diagnosis_stage": "mild", "age": 70,
                        "physical_ability": "mobile", "cognitive_level": "mild"},
                  description="Get lifestyle recommendations")
    print()

    # Test Research & Data endpoints
    print("📊 RESEARCH & DATA")
    print("-" * 120)
    test_endpoint("POST", "/api/v1/research-data/research/consent",
                  data={"patient_id": 1, "consent_given": True,
                        "data_sharing_level": "anonymized", "allowed_uses": ["research"]},
                  description="Manage research consent")
    test_endpoint("GET", "/api/v1/research-data/research/consent/1",
                  description="Get research consent status")
    test_endpoint("POST", "/api/v1/research-data/fhir/export",
                  data={"patient_id": 1},
                  description="Export FHIR data")
    test_endpoint("GET", "/api/v1/research-data/analytics/population-insights",
                  description="Get population insights")
    test_endpoint("POST", "/api/v1/research-data/cohort/compare",
                  data={"patient_id": 1, "demographic_factors": ["age", "gender"],
                        "clinical_factors": ["diagnosis_stage"]},
                  description="Compare to cohort")
    test_endpoint("GET", "/api/v1/research-data/cohort/find-similar/1",
                  description="Find similar patients")
    print()

    # Test Social & Gamification endpoints
    print("👥 SOCIAL & GAMIFICATION")
    print("-" * 120)
    test_endpoint("POST", "/api/v1/social-gamification/support-groups/search",
                  data={"location": "New York", "radius_km": 50, "group_type": "all"},
                  description="Search support groups")
    test_endpoint("GET", "/api/v1/social-gamification/support-groups/online",
                  description="Get online support groups")
    test_endpoint("POST", "/api/v1/social-gamification/forum/post",
                  data={"user_id": 1, "category": "advice", "title": "Test Post",
                        "content": "Test content", "is_anonymous": False},
                  description="Create forum post")
    test_endpoint("GET", "/api/v1/social-gamification/forum/posts",
                  description="Get forum posts")
    test_endpoint("POST", "/api/v1/social-gamification/education/search",
                  data={"topic": "alzheimer's care"},
                  description="Search educational resources")
    test_endpoint("GET", "/api/v1/social-gamification/education/recommended/1",
                  description="Get recommended resources")
    test_endpoint("POST", "/api/v1/social-gamification/brain-games/start-session",
                  data={"patient_id": 1, "game_type": "memory", "difficulty": "easy"},
                  description="Start brain game session")
    test_endpoint("GET", "/api/v1/social-gamification/achievements/1",
                  description="Get patient achievements")
    test_endpoint("GET", "/api/v1/social-gamification/progress/milestones/1",
                  description="Get progress milestones")
    test_endpoint("GET", "/api/v1/social-gamification/leaderboard",
                  description="Get leaderboard")
    print()

    # Test Integration endpoints
    print("🔌 INTEGRATIONS & AUTOMATION")
    print("-" * 120)
    test_endpoint("POST", "/api/v1/integrations/ehr/connect",
                  data={"patient_id": 1, "ehr_system": "epic",
                        "credentials": {"username": "test"}, "auto_sync": True},
                  description="Connect EHR system")
    test_endpoint("GET", "/api/v1/integrations/ehr/sync-status/1",
                  description="Get EHR sync status")
    test_endpoint("POST", "/api/v1/integrations/wearables/connect",
                  data={"patient_id": 1, "device_type": "apple_watch", "oauth_token": "test_token"},
                  description="Connect wearable device")
    test_endpoint("GET", "/api/v1/integrations/wearables/data/1",
                  description="Get wearable data")
    test_endpoint("POST", "/api/v1/integrations/smart-home/connect",
                  data={"patient_id": 1, "device_type": "alexa", "device_id": "test_device",
                        "capabilities": ["reminders"]},
                  description="Connect smart home device")
    test_endpoint("POST", "/api/v1/integrations/calendar/connect",
                  data={"patient_id": 1, "calendar_service": "google",
                        "oauth_token": "test_token", "sync_direction": "bidirectional"},
                  description="Connect calendar")
    test_endpoint("POST", "/api/v1/integrations/pharmacy/connect",
                  data={"patient_id": 1, "pharmacy_name": "CVS",
                        "pharmacy_npi": "1234567890", "auto_refill_enabled": True},
                  description="Connect pharmacy")
    test_endpoint("GET", "/api/v1/integrations/insurance/coverage/1",
                  description="Get insurance coverage")
    print()

    # Test Communication endpoints
    print("💬 COMMUNICATION")
    print("-" * 120)
    test_endpoint("POST", "/api/v1/communication/video/create-room",
                  data={"patient_id": 1, "provider_id": 1, "duration_minutes": 30},
                  description="Create video room")
    test_endpoint("POST", "/api/v1/communication/family-portal/add-member",
                  data={"patient_id": 1, "email": "test@example.com",
                        "relationship": "spouse", "permissions": ["view_assessments"]},
                  description="Add family member")
    test_endpoint("POST", "/api/v1/communication/chat/create-conversation",
                  data={"patient_id": 1, "participants": [{"id": 1, "role": "doctor"}],
                        "subject": "Test conversation"},
                  description="Create care team conversation")
    test_endpoint("POST", "/api/v1/communication/translate",
                  data={"text": "Hello", "source_lang": "en", "target_lang": "es"},
                  description="Translate text")
    test_endpoint("GET", "/api/v1/communication/translate/languages",
                  description="Get supported languages")
    test_endpoint("GET", "/api/v1/communication/tts/voices",
                  description="Get TTS voices")
    print()

    # Test Safety & Monitoring endpoints
    print("🛡️ SAFETY & MONITORING")
    print("-" * 120)
    test_endpoint("POST", "/api/v1/safety/gps/create-safe-zone",
                  data={"patient_id": 1, "zone_name": "Home", "center_lat": 40.7128,
                        "center_lon": -74.0060, "radius_meters": 500},
                  description="Create GPS safe zone")
    test_endpoint("GET", "/api/v1/safety/gps/safe-zones/1",
                  description="Get safe zones")
    test_endpoint("POST", "/api/v1/safety/activity/log",
                  data={"patient_id": 1, "activity_type": "walking", "duration_minutes": 30},
                  description="Log activity")
    test_endpoint("GET", "/api/v1/safety/activity/analyze/1",
                  description="Analyze activity patterns")
    test_endpoint("POST", "/api/v1/safety/medication/set-schedule",
                  data={"patient_id": 1, "medications": [{"name": "Donepezil",
                        "dosage": "10mg", "times": ["08:00", "20:00"]}]},
                  description="Set medication schedule")
    test_endpoint("GET", "/api/v1/safety/medication/compliance/1",
                  description="Get medication compliance")
    test_endpoint("POST", "/api/v1/safety/home-safety/create-assessment",
                  data={"patient_id": 1, "home_type": "house"},
                  description="Create home safety assessment")
    test_endpoint("GET", "/api/v1/safety/home-safety/checklist",
                  description="Get safety checklist")
    print()

    # Test Advanced AI endpoints
    print("🤖 ADVANCED AI FEATURES")
    print("-" * 120)
    test_endpoint("POST", "/api/v1/advanced/speech/analyze",
                  data={"transcript": "Hello world", "audio_duration": 5.0},
                  description="Analyze speech patterns")
    test_endpoint("POST", "/api/v1/advanced/sentiment/analyze",
                  data={"text": "I am feeling good today"},
                  description="Analyze sentiment")
    print()

    # Summary
    print()
    print("=" * 120)
    print("✅ API ENDPOINT TESTING COMPLETE")
    print("=" * 120)
    print()
    print("🔗 API Documentation: http://localhost:3102/docs")
    print("🌐 Frontend Application: http://localhost:3103")
    print()


if __name__ == "__main__":
    main()
