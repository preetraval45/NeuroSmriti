"""
Behavioral Analysis Service
Eye tracking, gait analysis, sleep patterns, and sentiment analysis
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger


class EyeTrackingAnalyzer:
    """Analyze eye movement patterns during cognitive tests"""

    def analyze_gaze_data(
        self,
        fixations: List[Dict[str, Any]],
        saccades: List[Dict[str, Any]],
        test_duration: float
    ) -> Dict[str, Any]:
        """
        Analyze eye tracking data

        Args:
            fixations: List of fixation events {x, y, duration, timestamp}
            saccades: List of saccade events {start_x, start_y, end_x, end_y, duration, velocity}
            test_duration: Total test duration in seconds

        Returns:
            Eye tracking metrics
        """
        try:
            # Fixation metrics
            fixation_durations = [f['duration'] for f in fixations]
            avg_fixation_duration = np.mean(fixation_durations) if fixation_durations else 0

            # Saccade metrics
            saccade_velocities = [s['velocity'] for s in saccades]
            avg_saccade_velocity = np.mean(saccade_velocities) if saccade_velocities else 0

            # Calculate saccade amplitudes
            amplitudes = []
            for s in saccades:
                dx = s['end_x'] - s['start_x']
                dy = s['end_y'] - s['start_y']
                amplitude = np.sqrt(dx**2 + dy**2)
                amplitudes.append(amplitude)

            avg_amplitude = np.mean(amplitudes) if amplitudes else 0

            # Gaze dispersion (measure of focus)
            fixation_coords = [(f['x'], f['y']) for f in fixations]
            dispersion = self._calculate_dispersion(fixation_coords)

            # Smooth pursuit (following moving objects)
            pursuit_quality = self._assess_smooth_pursuit(saccades)

            # Cognitive load indicators
            fixation_rate = len(fixations) / test_duration if test_duration > 0 else 0
            saccade_rate = len(saccades) / test_duration if test_duration > 0 else 0

            # Risk assessment
            risk_score = self._calculate_eye_tracking_risk({
                'fixation_duration': avg_fixation_duration,
                'saccade_velocity': avg_saccade_velocity,
                'dispersion': dispersion,
                'pursuit_quality': pursuit_quality
            })

            return {
                "fixation_metrics": {
                    "count": len(fixations),
                    "average_duration_ms": avg_fixation_duration,
                    "rate_per_second": fixation_rate
                },
                "saccade_metrics": {
                    "count": len(saccades),
                    "average_velocity_deg_per_sec": avg_saccade_velocity,
                    "average_amplitude_deg": avg_amplitude,
                    "rate_per_second": saccade_rate
                },
                "gaze_dispersion": dispersion,
                "smooth_pursuit_quality": pursuit_quality,
                "cognitive_load_estimate": min((fixation_rate + saccade_rate) / 10, 1.0),
                "risk_score": risk_score,
                "abnormalities": self._detect_abnormalities({
                    'fixation_duration': avg_fixation_duration,
                    'saccade_velocity': avg_saccade_velocity
                })
            }

        except Exception as e:
            logger.error(f"Error analyzing eye tracking data: {e}")
            raise

    def _calculate_dispersion(self, coords: List[Tuple[float, float]]) -> float:
        """Calculate gaze dispersion (lower = more focused)"""
        if len(coords) < 2:
            return 0.0

        coords_array = np.array(coords)
        centroid = coords_array.mean(axis=0)
        distances = np.linalg.norm(coords_array - centroid, axis=1)
        return float(distances.mean())

    def _assess_smooth_pursuit(self, saccades: List[Dict]) -> float:
        """Assess smooth pursuit eye movement quality (0-1)"""
        if not saccades:
            return 0.5

        # Good pursuit = consistent velocities
        velocities = [s['velocity'] for s in saccades]
        velocity_std = np.std(velocities)
        velocity_mean = np.mean(velocities)

        # Lower coefficient of variation = better pursuit
        cv = velocity_std / velocity_mean if velocity_mean > 0 else 1.0
        quality = 1.0 - min(cv, 1.0)

        return quality

    def _calculate_eye_tracking_risk(self, metrics: Dict[str, float]) -> float:
        """Calculate risk score from eye tracking metrics"""
        # Normal ranges: fixation 200-400ms, saccade velocity 200-500 deg/s
        fixation_abnormal = abs(metrics['fixation_duration'] - 300) / 300
        saccade_abnormal = abs(metrics['saccade_velocity'] - 350) / 350

        risk = (fixation_abnormal + saccade_abnormal + (1 - metrics['pursuit_quality'])) / 3
        return min(risk, 1.0)

    def _detect_abnormalities(self, metrics: Dict[str, float]) -> List[str]:
        """Detect specific abnormalities"""
        abnormalities = []

        if metrics['fixation_duration'] > 500:
            abnormalities.append("Prolonged fixations (may indicate processing difficulty)")
        elif metrics['fixation_duration'] < 150:
            abnormalities.append("Brief fixations (may indicate attention deficit)")

        if metrics['saccade_velocity'] < 200:
            abnormalities.append("Slow saccades (potential motor control issue)")
        elif metrics['saccade_velocity'] > 600:
            abnormalities.append("Hyperactive saccades")

        return abnormalities


class GaitAnalyzer:
    """Analyze gait patterns using accelerometer data"""

    def analyze_gait_data(
        self,
        accelerometer_data: List[Dict[str, Any]],
        gyroscope_data: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Analyze gait from smartphone accelerometer/gyroscope

        Args:
            accelerometer_data: List of {timestamp, x, y, z} readings
            gyroscope_data: Optional gyroscope data

        Returns:
            Gait analysis metrics
        """
        try:
            # Extract acceleration values
            timestamps = [d['timestamp'] for d in accelerometer_data]
            acc_x = np.array([d['x'] for d in accelerometer_data])
            acc_y = np.array([d['y'] for d in accelerometer_data])
            acc_z = np.array([d['z'] for d in accelerometer_data])

            # Calculate magnitude
            magnitude = np.sqrt(acc_x**2 + acc_y**2 + acc_z**2)

            # Detect steps
            steps = self._detect_steps(magnitude, timestamps)

            # Gait speed
            gait_speed = self._calculate_gait_speed(steps, timestamps)

            # Stride variability
            stride_variability = self._calculate_stride_variability(steps)

            # Balance/symmetry
            balance_score = self._assess_balance(acc_x, acc_y, acc_z)

            # Fall risk
            fall_risk = self._calculate_fall_risk({
                'gait_speed': gait_speed,
                'stride_variability': stride_variability,
                'balance': balance_score
            })

            return {
                "step_count": len(steps),
                "gait_speed_m_per_s": gait_speed,
                "stride_variability": stride_variability,
                "balance_score": balance_score,
                "cadence_steps_per_min": len(steps) / ((timestamps[-1] - timestamps[0]) / 60) if len(timestamps) > 1 else 0,
                "fall_risk_score": fall_risk,
                "risk_level": "high" if fall_risk > 0.7 else "moderate" if fall_risk > 0.4 else "low",
                "recommendations": self._generate_gait_recommendations(gait_speed, stride_variability, fall_risk)
            }

        except Exception as e:
            logger.error(f"Error analyzing gait data: {e}")
            raise

    def _detect_steps(self, magnitude: np.ndarray, timestamps: List[float]) -> List[int]:
        """Detect steps from acceleration magnitude"""
        # Simple peak detection
        threshold = magnitude.mean() + magnitude.std()
        peaks = []

        for i in range(1, len(magnitude) - 1):
            if magnitude[i] > threshold and magnitude[i] > magnitude[i-1] and magnitude[i] > magnitude[i+1]:
                peaks.append(i)

        return peaks

    def _calculate_gait_speed(self, steps: List[int], timestamps: List[float]) -> float:
        """Estimate gait speed"""
        if len(steps) < 2:
            return 0.0

        # Assume average stride length of 0.7m
        stride_length = 0.7
        duration = timestamps[-1] - timestamps[0]

        if duration == 0:
            return 0.0

        speed = (len(steps) * stride_length) / duration
        return speed

    def _calculate_stride_variability(self, steps: List[int]) -> float:
        """Calculate stride-to-stride variability"""
        if len(steps) < 3:
            return 0.0

        stride_intervals = np.diff(steps)
        variability = np.std(stride_intervals) / np.mean(stride_intervals) if np.mean(stride_intervals) > 0 else 0

        return float(variability)

    def _assess_balance(self, acc_x: np.ndarray, acc_y: np.ndarray, acc_z: np.ndarray) -> float:
        """Assess balance from acceleration patterns (0-1, higher is better)"""
        # Lower variability in lateral (x) and vertical (z) = better balance
        lateral_std = np.std(acc_x)
        vertical_std = np.std(acc_z)

        # Normalize (typical std ~2-4 m/s^2)
        balance = 1.0 - min((lateral_std + vertical_std) / 8, 1.0)

        return balance

    def _calculate_fall_risk(self, metrics: Dict[str, float]) -> float:
        """Calculate fall risk (0-1)"""
        # Slow gait = higher risk
        speed_risk = 1.0 - min(metrics['gait_speed'] / 1.2, 1.0)

        # High variability = higher risk
        variability_risk = min(metrics['stride_variability'] * 10, 1.0)

        # Poor balance = higher risk
        balance_risk = 1.0 - metrics['balance']

        risk = (speed_risk * 0.4 + variability_risk * 0.3 + balance_risk * 0.3)
        return risk

    def _generate_gait_recommendations(self, speed: float, variability: float, risk: float) -> List[str]:
        """Generate gait improvement recommendations"""
        recommendations = []

        if speed < 0.8:
            recommendations.append("Practice walking exercises to improve gait speed")

        if variability > 0.15:
            recommendations.append("Work on stride consistency with a physical therapist")

        if risk > 0.6:
            recommendations.append("Consider fall prevention strategies and home safety assessment")
            recommendations.append("Use assistive devices if needed")

        return recommendations if recommendations else ["Continue regular walking and exercise"]


class SleepAnalyzer:
    """Analyze sleep patterns for cognitive decline markers"""

    def analyze_sleep_data(
        self,
        sleep_sessions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze sleep patterns from multiple nights

        Args:
            sleep_sessions: List of sleep data {date, total_sleep_min, rem_min, deep_min, light_min, awakenings, efficiency}

        Returns:
            Sleep analysis metrics
        """
        try:
            if not sleep_sessions:
                return {"error": "No sleep data provided"}

            # Calculate averages
            avg_total_sleep = np.mean([s['total_sleep_min'] for s in sleep_sessions])
            avg_rem = np.mean([s['rem_min'] for s in sleep_sessions])
            avg_deep = np.mean([s['deep_min'] for s in sleep_sessions])
            avg_awakenings = np.mean([s['awakenings'] for s in sleep_sessions])
            avg_efficiency = np.mean([s['efficiency'] for s in sleep_sessions])

            # REM percentage
            rem_percentage = (avg_rem / avg_total_sleep * 100) if avg_total_sleep > 0 else 0

            # Sleep variability
            sleep_durations = [s['total_sleep_min'] for s in sleep_sessions]
            sleep_variability = np.std(sleep_durations) / np.mean(sleep_durations) if np.mean(sleep_durations) > 0 else 0

            # Cognitive risk factors
            risk_factors = []
            if avg_total_sleep < 360:  # < 6 hours
                risk_factors.append("Insufficient sleep duration")
            if rem_percentage < 15:  # < 15% REM
                risk_factors.append("Reduced REM sleep")
            if avg_awakenings > 5:
                risk_factors.append("Frequent awakenings")
            if avg_efficiency < 0.85:
                risk_factors.append("Poor sleep efficiency")

            # Overall sleep quality score
            sleep_quality = self._calculate_sleep_quality({
                'duration': avg_total_sleep,
                'rem_percentage': rem_percentage,
                'efficiency': avg_efficiency,
                'awakenings': avg_awakenings
            })

            return {
                "analysis_period_days": len(sleep_sessions),
                "average_metrics": {
                    "total_sleep_hours": avg_total_sleep / 60,
                    "rem_sleep_minutes": avg_rem,
                    "deep_sleep_minutes": avg_deep,
                    "rem_percentage": rem_percentage,
                    "awakenings_per_night": avg_awakenings,
                    "sleep_efficiency": avg_efficiency
                },
                "sleep_variability": sleep_variability,
                "sleep_quality_score": sleep_quality,
                "risk_factors": risk_factors,
                "cognitive_impact": "high" if len(risk_factors) >= 3 else "moderate" if len(risk_factors) >= 2 else "low",
                "recommendations": self._generate_sleep_recommendations(avg_total_sleep, rem_percentage, avg_efficiency)
            }

        except Exception as e:
            logger.error(f"Error analyzing sleep data: {e}")
            raise

    def _calculate_sleep_quality(self, metrics: Dict[str, float]) -> float:
        """Calculate overall sleep quality score (0-100)"""
        # Duration score (optimal 7-9 hours)
        optimal_duration = 480  # 8 hours
        duration_score = 1.0 - min(abs(metrics['duration'] - optimal_duration) / optimal_duration, 1.0)

        # REM score (optimal 20-25%)
        rem_score = min(metrics['rem_percentage'] / 25, 1.0)

        # Efficiency score
        efficiency_score = metrics['efficiency']

        # Awakenings (fewer is better)
        awakening_score = 1.0 - min(metrics['awakenings'] / 10, 1.0)

        quality = (duration_score * 0.3 + rem_score * 0.3 + efficiency_score * 0.25 + awakening_score * 0.15) * 100

        return quality

    def _generate_sleep_recommendations(self, duration: float, rem_pct: float, efficiency: float) -> List[str]:
        """Generate sleep improvement recommendations"""
        recommendations = []

        if duration < 360:
            recommendations.append("Aim for 7-9 hours of sleep per night")

        if rem_pct < 15:
            recommendations.append("Avoid alcohol before bed (reduces REM sleep)")
            recommendations.append("Maintain consistent sleep schedule")

        if efficiency < 0.85:
            recommendations.append("Improve sleep hygiene: dark room, comfortable temperature, no screens before bed")

        return recommendations if recommendations else ["Maintain current healthy sleep patterns"]


class SentimentAnalyzer:
    """Analyze sentiment and emotional patterns in conversation"""

    def analyze_sentiment(
        self,
        text: str,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Analyze sentiment in text

        Args:
            text: Text to analyze
            conversation_history: Optional list of {timestamp, text, sentiment} for trend analysis

        Returns:
            Sentiment analysis results
        """
        # Simple rule-based sentiment (can be replaced with ML model)
        positive_words = {
            'good', 'great', 'happy', 'wonderful', 'excellent', 'love', 'joy',
            'pleased', 'delighted', 'fantastic', 'amazing', 'beautiful'
        }

        negative_words = {
            'bad', 'sad', 'angry', 'terrible', 'awful', 'hate', 'pain',
            'upset', 'worried', 'anxious', 'depressed', 'frustrated', 'confused'
        }

        words = text.lower().split()

        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)

        # Sentiment score (-1 to 1)
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words > 0:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
        else:
            sentiment_score = 0.0

        # Emotional stability (if history available)
        stability_score = 1.0
        if conversation_history and len(conversation_history) > 1:
            sentiment_values = [h.get('sentiment', 0) for h in conversation_history]
            stability_score = 1.0 - min(np.std(sentiment_values), 1.0)

        return {
            "sentiment_score": sentiment_score,
            "sentiment_label": "positive" if sentiment_score > 0.2 else "negative" if sentiment_score < -0.2 else "neutral",
            "positive_words_count": positive_count,
            "negative_words_count": negative_count,
            "emotional_stability": stability_score,
            "cognitive_indicators": self._detect_emotional_cognitive_markers(text, sentiment_score)
        }

    def _detect_emotional_cognitive_markers(self, text: str, sentiment: float) -> List[str]:
        """Detect cognitive decline markers in emotional expression"""
        markers = []

        # Apathy markers
        apathy_words = ['don\'t care', 'doesn\'t matter', 'whatever', 'don\'t know']
        if any(phrase in text.lower() for phrase in apathy_words):
            markers.append("Possible apathy")

        # Confusion markers
        if 'confused' in text.lower() or 'don\'t understand' in text.lower():
            markers.append("Expressed confusion")

        # Extreme sentiment swings
        if abs(sentiment) > 0.8:
            markers.append("Intense emotional expression")

        return markers


# Service instances
eye_tracking_service = EyeTrackingAnalyzer()
gait_service = GaitAnalyzer()
sleep_service = SleepAnalyzer()
sentiment_service = SentimentAnalyzer()
