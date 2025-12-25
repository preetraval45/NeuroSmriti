"""
Safety & Monitoring Service
GPS wandering detection, fall detection, activity monitoring, medication compliance,
home safety checklist, caregiver burnout monitoring
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta, time
from loguru import logger
import secrets


class GPSWanderingService:
    """
    Geofencing alerts when patient leaves safe zones
    """

    def __init__(self):
        self.safe_zones = {}
        self.location_history = {}
        self.wandering_alerts = []

    def create_safe_zone(
        self,
        patient_id: int,
        zone_name: str,
        center_lat: float,
        center_lon: float,
        radius_meters: float,
        active_times: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Create geofence safe zone"""
        zone_id = secrets.token_urlsafe(8)

        zone_data = {
            "zone_id": zone_id,
            "patient_id": patient_id,
            "name": zone_name,
            "center": {"latitude": center_lat, "longitude": center_lon},
            "radius_meters": radius_meters,
            "active_times": active_times or [{"start": "00:00", "end": "23:59"}],  # 24/7 by default
            "created_at": datetime.now().isoformat(),
            "enabled": True
        }

        if patient_id not in self.safe_zones:
            self.safe_zones[patient_id] = []
        self.safe_zones[patient_id].append(zone_data)

        return {
            "zone_id": zone_id,
            "zone_name": zone_name,
            "radius_meters": radius_meters,
            "status": "active"
        }

    def check_location(
        self,
        patient_id: int,
        latitude: float,
        longitude: float,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Check if patient location is within safe zones"""
        if timestamp is None:
            timestamp = datetime.now()

        # Store location history
        if patient_id not in self.location_history:
            self.location_history[patient_id] = []
        self.location_history[patient_id].append({
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": timestamp.isoformat()
        })

        # Check against safe zones
        zones = self.safe_zones.get(patient_id, [])
        current_time = timestamp.time()

        inside_safe_zone = False
        active_zones = []

        for zone in zones:
            if not zone["enabled"]:
                continue

            # Check if current time is within zone's active times
            is_time_active = False
            for time_range in zone["active_times"]:
                start = datetime.strptime(time_range["start"], "%H:%M").time()
                end = datetime.strptime(time_range["end"], "%H:%M").time()
                if start <= current_time <= end:
                    is_time_active = True
                    break

            if not is_time_active:
                continue

            active_zones.append(zone["name"])

            # Calculate distance from zone center
            distance = self._calculate_distance(
                latitude, longitude,
                zone["center"]["latitude"], zone["center"]["longitude"]
            )

            if distance <= zone["radius_meters"]:
                inside_safe_zone = True
                break

        result = {
            "patient_id": patient_id,
            "location": {"latitude": latitude, "longitude": longitude},
            "timestamp": timestamp.isoformat(),
            "inside_safe_zone": inside_safe_zone,
            "active_zones": active_zones,
            "alert_triggered": False
        }

        # Trigger wandering alert if outside safe zone
        if not inside_safe_zone and active_zones:
            alert = self._trigger_wandering_alert(patient_id, latitude, longitude, timestamp)
            result["alert_triggered"] = True
            result["alert"] = alert

        return result

    def _calculate_distance(
        self,
        lat1: float, lon1: float,
        lat2: float, lon2: float
    ) -> float:
        """Calculate distance between two GPS coordinates in meters (Haversine formula)"""
        R = 6371000  # Earth's radius in meters

        phi1 = np.radians(lat1)
        phi2 = np.radians(lat2)
        delta_phi = np.radians(lat2 - lat1)
        delta_lambda = np.radians(lon2 - lon1)

        a = (np.sin(delta_phi / 2) ** 2 +
             np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

        return R * c

    def _trigger_wandering_alert(
        self,
        patient_id: int,
        latitude: float,
        longitude: float,
        timestamp: datetime
    ) -> Dict[str, Any]:
        """Trigger wandering alert"""
        alert = {
            "alert_id": secrets.token_urlsafe(12),
            "patient_id": patient_id,
            "alert_type": "wandering",
            "location": {"latitude": latitude, "longitude": longitude},
            "timestamp": timestamp.isoformat(),
            "status": "active",
            "severity": "high"
        }

        self.wandering_alerts.append(alert)
        logger.warning(f"Wandering alert for patient {patient_id} at ({latitude}, {longitude})")

        return alert


class FallDetectionService:
    """
    Smartphone accelerometer-based fall detection
    """

    def __init__(self):
        self.fall_threshold = 2.5  # g-force threshold
        self.impact_duration_threshold = 0.5  # seconds
        self.fall_history = []

    def analyze_accelerometer_data(
        self,
        patient_id: int,
        accelerometer_readings: List[Dict[str, float]],
        sampling_rate_hz: int = 50
    ) -> Dict[str, Any]:
        """
        Analyze accelerometer data for fall detection

        Args:
            accelerometer_readings: [{'x': 0.1, 'y': 0.2, 'z': 9.8, 'timestamp': '...'}, ...]
            sampling_rate_hz: Sampling rate of accelerometer
        """
        if not accelerometer_readings:
            return {"fall_detected": False}

        # Calculate magnitude of acceleration vector
        magnitudes = []
        for reading in accelerometer_readings:
            magnitude = np.sqrt(reading['x']**2 + reading['y']**2 + reading['z']**2)
            magnitudes.append(magnitude)

        magnitudes = np.array(magnitudes)

        # Detect sudden spike (impact)
        impact_detected = np.max(magnitudes) > self.fall_threshold * 9.81  # Convert to m/s²

        # Detect prolonged low movement after impact (person not getting up)
        if impact_detected:
            impact_index = np.argmax(magnitudes)
            window_size = int(sampling_rate_hz * 2)  # 2 seconds after impact

            if impact_index + window_size < len(magnitudes):
                post_impact_data = magnitudes[impact_index:impact_index + window_size]
                low_movement = np.mean(post_impact_data) < 1.5 * 9.81  # Low activity

                if low_movement:
                    return self._trigger_fall_alert(
                        patient_id,
                        accelerometer_readings[impact_index],
                        confidence=0.85
                    )

        return {
            "fall_detected": False,
            "max_acceleration": float(np.max(magnitudes)) / 9.81,  # in g-force
            "analysis_timestamp": datetime.now().isoformat()
        }

    def _trigger_fall_alert(
        self,
        patient_id: int,
        impact_data: Dict[str, Any],
        confidence: float
    ) -> Dict[str, Any]:
        """Trigger fall detection alert"""
        alert = {
            "alert_id": secrets.token_urlsafe(12),
            "patient_id": patient_id,
            "alert_type": "fall_detected",
            "timestamp": impact_data.get("timestamp", datetime.now().isoformat()),
            "confidence": confidence,
            "impact_force": {
                "x": impact_data["x"],
                "y": impact_data["y"],
                "z": impact_data["z"]
            },
            "status": "active",
            "severity": "critical",
            "auto_emergency_call": confidence > 0.9
        }

        self.fall_history.append(alert)
        logger.critical(f"FALL DETECTED for patient {patient_id} with {confidence*100}% confidence")

        return alert


class ActivityMonitoringService:
    """
    Track daily activities for unusual pattern detection
    """

    def __init__(self):
        self.activity_patterns = {}
        self.baseline_patterns = {}

    def log_activity(
        self,
        patient_id: int,
        activity_type: str,
        duration_minutes: int,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Log patient activity"""
        if timestamp is None:
            timestamp = datetime.now()

        if patient_id not in self.activity_patterns:
            self.activity_patterns[patient_id] = []

        activity = {
            "activity_type": activity_type,  # 'walking', 'sleeping', 'eating', 'social', 'cognitive_task'
            "duration_minutes": duration_minutes,
            "timestamp": timestamp.isoformat(),
            "hour_of_day": timestamp.hour
        }

        self.activity_patterns[patient_id].append(activity)

        return {
            "activity_logged": True,
            "activity_type": activity_type,
            "timestamp": timestamp.isoformat()
        }

    def analyze_daily_patterns(
        self,
        patient_id: int,
        analysis_days: int = 7
    ) -> Dict[str, Any]:
        """Analyze activity patterns for anomalies"""
        if patient_id not in self.activity_patterns:
            return {"status": "insufficient_data"}

        activities = self.activity_patterns[patient_id]
        cutoff_date = datetime.now() - timedelta(days=analysis_days)

        # Filter recent activities
        recent_activities = [
            a for a in activities
            if datetime.fromisoformat(a["timestamp"]) > cutoff_date
        ]

        if not recent_activities:
            return {"status": "insufficient_data"}

        # Calculate activity metrics
        activity_types = {}
        hourly_distribution = np.zeros(24)

        for activity in recent_activities:
            activity_type = activity["activity_type"]
            activity_types[activity_type] = activity_types.get(activity_type, 0) + activity["duration_minutes"]
            hourly_distribution[activity["hour_of_day"]] += 1

        total_activity_minutes = sum(activity_types.values())
        daily_average = total_activity_minutes / analysis_days

        # Detect anomalies
        anomalies = []

        # Check for significantly reduced activity
        if patient_id in self.baseline_patterns:
            baseline_avg = self.baseline_patterns[patient_id]["daily_average"]
            if daily_average < baseline_avg * 0.6:  # 40% reduction
                anomalies.append({
                    "type": "reduced_activity",
                    "severity": "medium",
                    "description": f"Daily activity reduced by {((baseline_avg - daily_average) / baseline_avg * 100):.1f}%"
                })

        # Check for unusual sleep patterns
        sleep_minutes = activity_types.get("sleeping", 0)
        sleep_hours = sleep_minutes / 60
        if sleep_hours > 12:
            anomalies.append({
                "type": "excessive_sleep",
                "severity": "medium",
                "description": f"Sleeping {sleep_hours:.1f} hours per day (avg)"
            })
        elif sleep_hours < 5:
            anomalies.append({
                "type": "insufficient_sleep",
                "severity": "high",
                "description": f"Only sleeping {sleep_hours:.1f} hours per day (avg)"
            })

        # Check for social isolation
        social_minutes = activity_types.get("social", 0)
        if social_minutes < 30 * analysis_days:  # Less than 30 min/day
            anomalies.append({
                "type": "social_isolation",
                "severity": "medium",
                "description": "Limited social engagement detected"
            })

        return {
            "analysis_period_days": analysis_days,
            "daily_activity_average_minutes": daily_average,
            "activity_breakdown": activity_types,
            "anomalies_detected": len(anomalies),
            "anomalies": anomalies,
            "risk_score": len(anomalies) * 20  # 0-100 scale
        }

    def set_baseline(self, patient_id: int):
        """Set baseline activity pattern"""
        analysis = self.analyze_daily_patterns(patient_id, analysis_days=14)
        if analysis.get("status") != "insufficient_data":
            self.baseline_patterns[patient_id] = {
                "daily_average": analysis["daily_activity_average_minutes"],
                "activity_breakdown": analysis["activity_breakdown"],
                "set_at": datetime.now().isoformat()
            }


class MedicationComplianceService:
    """
    Photo verification of medication taking
    """

    def __init__(self):
        self.medication_schedules = {}
        self.compliance_records = {}

    def set_medication_schedule(
        self,
        patient_id: int,
        medications: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Set medication schedule for patient"""
        self.medication_schedules[patient_id] = {
            "patient_id": patient_id,
            "medications": medications,  # [{'name': 'Donepezil', 'dosage': '10mg', 'times': ['08:00', '20:00']}]
            "updated_at": datetime.now().isoformat()
        }

        return {
            "patient_id": patient_id,
            "medications_count": len(medications),
            "daily_doses": sum(len(med.get("times", [])) for med in medications)
        }

    def verify_medication_taken(
        self,
        patient_id: int,
        medication_name: str,
        photo_path: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Verify medication was taken (with optional photo verification)"""
        if timestamp is None:
            timestamp = datetime.now()

        if patient_id not in self.compliance_records:
            self.compliance_records[patient_id] = []

        # In production, use computer vision to verify medication from photo
        photo_verified = photo_path is not None

        record = {
            "medication_name": medication_name,
            "timestamp": timestamp.isoformat(),
            "photo_verified": photo_verified,
            "photo_path": photo_path,
            "verification_confidence": 0.95 if photo_verified else 0.70,
            "taken": True
        }

        self.compliance_records[patient_id].append(record)

        return {
            "verification_id": secrets.token_urlsafe(8),
            "medication": medication_name,
            "verified": photo_verified,
            "timestamp": timestamp.isoformat()
        }

    def get_compliance_report(
        self,
        patient_id: int,
        days: int = 7
    ) -> Dict[str, Any]:
        """Get medication compliance report"""
        if patient_id not in self.medication_schedules:
            return {"status": "no_schedule"}

        schedule = self.medication_schedules[patient_id]
        records = self.compliance_records.get(patient_id, [])

        cutoff_date = datetime.now() - timedelta(days=days)
        recent_records = [
            r for r in records
            if datetime.fromisoformat(r["timestamp"]) > cutoff_date
        ]

        # Calculate expected doses
        daily_doses = sum(len(med.get("times", [])) for med in schedule["medications"])
        expected_doses = daily_doses * days

        # Calculate actual doses taken
        actual_doses = len(recent_records)
        compliance_rate = (actual_doses / expected_doses * 100) if expected_doses > 0 else 0

        # Identify missed medications
        missed_count = expected_doses - actual_doses

        return {
            "period_days": days,
            "expected_doses": expected_doses,
            "actual_doses": actual_doses,
            "compliance_rate": compliance_rate,
            "missed_doses": missed_count,
            "status": "excellent" if compliance_rate >= 95 else "good" if compliance_rate >= 80 else "needs_improvement",
            "medications": schedule["medications"]
        }


class HomeSafetyChecklistService:
    """
    Assess home for dementia-friendly modifications
    """

    SAFETY_CHECKLIST = {
        "fall_prevention": [
            "Remove tripping hazards (rugs, cords)",
            "Install grab bars in bathroom",
            "Improve lighting in hallways and stairs",
            "Add non-slip mats in bathroom",
            "Secure loose carpets"
        ],
        "wandering_prevention": [
            "Install door alarms",
            "Use door locks that patient cannot operate",
            "Create safe outdoor space",
            "Remove car keys if not safe to drive"
        ],
        "fire_safety": [
            "Install smoke detectors",
            "Remove stove knobs when not in use",
            "Keep fire extinguisher accessible",
            "Create evacuation plan"
        ],
        "medication_safety": [
            "Lock up medications",
            "Use medication organizers",
            "Remove expired medications",
            "Keep emergency numbers visible"
        ],
        "general_safety": [
            "Label rooms and cabinets",
            "Remove dangerous items (sharp objects, chemicals)",
            "Ensure phone is easy to use",
            "Install night lights"
        ]
    }

    def __init__(self):
        self.assessments = {}

    def create_assessment(
        self,
        patient_id: int,
        home_type: str = "house"
    ) -> Dict[str, Any]:
        """Create home safety assessment"""
        assessment_id = secrets.token_urlsafe(12)

        assessment = {
            "assessment_id": assessment_id,
            "patient_id": patient_id,
            "home_type": home_type,
            "created_at": datetime.now().isoformat(),
            "checklist": self.SAFETY_CHECKLIST,
            "completed_items": {},
            "completion_percentage": 0,
            "risk_areas": []
        }

        self.assessments[assessment_id] = assessment

        return {
            "assessment_id": assessment_id,
            "total_items": sum(len(items) for items in self.SAFETY_CHECKLIST.values()),
            "categories": list(self.SAFETY_CHECKLIST.keys())
        }

    def update_assessment(
        self,
        assessment_id: str,
        category: str,
        item: str,
        completed: bool,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update assessment checklist item"""
        if assessment_id not in self.assessments:
            raise ValueError("Assessment not found")

        assessment = self.assessments[assessment_id]

        if category not in assessment["completed_items"]:
            assessment["completed_items"][category] = {}

        assessment["completed_items"][category][item] = {
            "completed": completed,
            "notes": notes,
            "timestamp": datetime.now().isoformat()
        }

        # Recalculate completion percentage
        total_items = sum(len(items) for items in self.SAFETY_CHECKLIST.values())
        completed_count = sum(
            1 for cat in assessment["completed_items"].values()
            for item_data in cat.values()
            if item_data["completed"]
        )
        assessment["completion_percentage"] = (completed_count / total_items * 100)

        return {
            "assessment_id": assessment_id,
            "completion_percentage": assessment["completion_percentage"],
            "item_updated": item
        }

    def get_assessment_report(self, assessment_id: str) -> Dict[str, Any]:
        """Get full assessment report with recommendations"""
        if assessment_id not in self.assessments:
            raise ValueError("Assessment not found")

        assessment = self.assessments[assessment_id]

        # Identify incomplete high-priority items
        recommendations = []
        for category, items in self.SAFETY_CHECKLIST.items():
            completed_in_category = assessment["completed_items"].get(category, {})
            for item in items:
                if item not in completed_in_category or not completed_in_category[item]["completed"]:
                    priority = "high" if category in ["fall_prevention", "fire_safety"] else "medium"
                    recommendations.append({
                        "category": category,
                        "item": item,
                        "priority": priority
                    })

        return {
            "assessment_id": assessment_id,
            "completion_percentage": assessment["completion_percentage"],
            "completed_items_count": sum(
                1 for cat in assessment["completed_items"].values()
                for item_data in cat.values()
                if item_data["completed"]
            ),
            "recommendations": recommendations[:10],  # Top 10 recommendations
            "safety_score": assessment["completion_percentage"]
        }


class CaregiverBurnoutService:
    """
    Track caregiver stress levels and suggest support
    """

    def __init__(self):
        self.caregiver_assessments = {}
        self.stress_history = {}

    def assess_burnout(
        self,
        caregiver_id: int,
        responses: Dict[str, int]
    ) -> Dict[str, Any]:
        """
        Assess caregiver burnout using standardized questions

        Args:
            responses: Dict with scores (1-5) for various stress indicators
        """
        # Zarit Burden Interview (simplified)
        stress_indicators = {
            "overwhelmed": responses.get("feel_overwhelmed", 3),
            "time_for_self": 5 - responses.get("time_for_self", 3),  # Inverted
            "emotional_strain": responses.get("emotional_strain", 3),
            "physical_exhaustion": responses.get("physical_exhaustion", 3),
            "sleep_quality": 5 - responses.get("sleep_quality", 3),  # Inverted
            "social_isolation": responses.get("social_isolation", 3),
            "financial_stress": responses.get("financial_stress", 3),
            "relationship_strain": responses.get("relationship_strain", 3)
        }

        # Calculate burnout score (0-100)
        total_score = sum(stress_indicators.values())
        max_possible = len(stress_indicators) * 5
        burnout_score = (total_score / max_possible) * 100

        # Determine risk level
        if burnout_score >= 70:
            risk_level = "critical"
            urgency = "immediate_action_needed"
        elif burnout_score >= 50:
            risk_level = "high"
            urgency = "seek_support_soon"
        elif burnout_score >= 30:
            risk_level = "moderate"
            urgency = "monitor_and_self_care"
        else:
            risk_level = "low"
            urgency = "maintain_current_practices"

        # Generate recommendations
        recommendations = self._generate_burnout_recommendations(
            burnout_score, risk_level, stress_indicators
        )

        assessment = {
            "caregiver_id": caregiver_id,
            "timestamp": datetime.now().isoformat(),
            "burnout_score": burnout_score,
            "risk_level": risk_level,
            "urgency": urgency,
            "stress_indicators": stress_indicators,
            "recommendations": recommendations
        }

        # Store assessment
        if caregiver_id not in self.stress_history:
            self.stress_history[caregiver_id] = []
        self.stress_history[caregiver_id].append(assessment)

        return assessment

    def _generate_burnout_recommendations(
        self,
        burnout_score: float,
        risk_level: str,
        stress_indicators: Dict[str, int]
    ) -> List[Dict[str, Any]]:
        """Generate personalized recommendations"""
        recommendations = []

        # Critical interventions
        if risk_level == "critical":
            recommendations.append({
                "priority": "urgent",
                "category": "professional_help",
                "title": "Seek Professional Support",
                "description": "Consider counseling or therapy for caregiver stress",
                "resources": ["National Caregiver Support Line: 1-800-XXX-XXXX"]
            })

        # Specific recommendations based on stress indicators
        if stress_indicators.get("time_for_self", 0) >= 4:
            recommendations.append({
                "priority": "high",
                "category": "respite_care",
                "title": "Arrange Respite Care",
                "description": "Take regular breaks - even 2-3 hours per week can help",
                "resources": ["Adult day care programs", "Respite care services"]
            })

        if stress_indicators.get("sleep_quality", 0) >= 4:
            recommendations.append({
                "priority": "high",
                "category": "sleep_hygiene",
                "title": "Improve Sleep Quality",
                "description": "Establish bedtime routine, consider sleep aids if needed",
                "resources": ["Sleep hygiene tips", "Consult doctor about sleep issues"]
            })

        if stress_indicators.get("social_isolation", 0) >= 4:
            recommendations.append({
                "priority": "medium",
                "category": "social_support",
                "title": "Join Support Group",
                "description": "Connect with other caregivers who understand your challenges",
                "resources": ["Local caregiver support groups", "Online caregiver communities"]
            })

        # General wellness recommendations
        recommendations.append({
            "priority": "medium",
            "category": "self_care",
            "title": "Practice Daily Self-Care",
            "description": "15-30 minutes daily for activities you enjoy",
            "resources": ["Meditation apps", "Exercise routines", "Hobbies"]
        })

        return recommendations

    def get_stress_trend(
        self,
        caregiver_id: int,
        days: int = 30
    ) -> Dict[str, Any]:
        """Get caregiver stress trend over time"""
        if caregiver_id not in self.stress_history:
            return {"status": "no_data"}

        history = self.stress_history[caregiver_id]
        cutoff_date = datetime.now() - timedelta(days=days)

        recent_assessments = [
            a for a in history
            if datetime.fromisoformat(a["timestamp"]) > cutoff_date
        ]

        if not recent_assessments:
            return {"status": "no_recent_data"}

        scores = [a["burnout_score"] for a in recent_assessments]
        timestamps = [a["timestamp"] for a in recent_assessments]

        # Calculate trend
        if len(scores) >= 2:
            trend = "increasing" if scores[-1] > scores[0] else "decreasing" if scores[-1] < scores[0] else "stable"
        else:
            trend = "insufficient_data"

        return {
            "caregiver_id": caregiver_id,
            "period_days": days,
            "assessments_count": len(recent_assessments),
            "current_score": scores[-1] if scores else None,
            "average_score": np.mean(scores) if scores else None,
            "trend": trend,
            "scores_over_time": list(zip(timestamps, scores))
        }


# Singleton instances
gps_wandering_service = GPSWanderingService()
fall_detection_service = FallDetectionService()
activity_monitoring_service = ActivityMonitoringService()
medication_compliance_service = MedicationComplianceService()
home_safety_service = HomeSafetyChecklistService()
caregiver_burnout_service = CaregiverBurnoutService()
