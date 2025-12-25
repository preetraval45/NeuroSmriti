"""
Advanced Cognitive Analysis Service
Handwriting analysis, facial recognition, and temporal modeling
"""

import numpy as np
import torch
import torch.nn as nn
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from loguru import logger
from PIL import Image
import cv2


class HandwritingAnalyzer:
    """Analyze handwriting patterns for cognitive decline detection"""

    def analyze_handwriting_sample(
        self,
        image_path: str,
        writing_duration: Optional[float] = None,
        pressure_data: Optional[List[float]] = None
    ) -> Dict[str, Any]:
        """
        Analyze handwriting sample

        Args:
            image_path: Path to handwriting image
            writing_duration: Time taken to write (seconds)
            pressure_data: Pen pressure data if available

        Returns:
            Handwriting analysis metrics
        """
        try:
            # Load image
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                raise ValueError(f"Could not load image from {image_path}")

            # Analyze stroke characteristics
            stroke_metrics = self._analyze_strokes(img)

            # Analyze letter formation
            letter_metrics = self._analyze_letter_formation(img)

            # Analyze spacing and alignment
            spatial_metrics = self._analyze_spatial_characteristics(img)

            # Tremor detection
            tremor_score = self._detect_tremor(img, pressure_data)

            # Micrographia detection (small handwriting)
            micrographia_score = self._detect_micrographia(stroke_metrics)

            # Overall cognitive score
            cognitive_score = self._calculate_handwriting_cognitive_score({
                'stroke_quality': stroke_metrics['quality_score'],
                'letter_formation': letter_metrics['formation_score'],
                'spatial_organization': spatial_metrics['organization_score'],
                'tremor': tremor_score,
                'micrographia': micrographia_score
            })

            return {
                "timestamp": datetime.now().isoformat(),
                "stroke_characteristics": stroke_metrics,
                "letter_formation": letter_metrics,
                "spatial_characteristics": spatial_metrics,
                "tremor_score": tremor_score,
                "micrographia_detected": micrographia_score > 0.5,
                "cognitive_score": cognitive_score,
                "risk_level": "high" if cognitive_score < 50 else "moderate" if cognitive_score < 70 else "low",
                "abnormalities": self._detect_handwriting_abnormalities({
                    'tremor': tremor_score,
                    'micrographia': micrographia_score,
                    'stroke_quality': stroke_metrics['quality_score']
                })
            }

        except Exception as e:
            logger.error(f"Error analyzing handwriting: {e}")
            raise

    def _analyze_strokes(self, img: np.ndarray) -> Dict[str, Any]:
        """Analyze stroke characteristics"""
        # Detect edges (strokes)
        edges = cv2.Canny(img, 50, 150)

        # Calculate stroke density
        stroke_density = np.sum(edges > 0) / edges.size

        # Stroke thickness variability
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        thicknesses = [cv2.contourArea(c) / (cv2.arcLength(c, False) + 1) for c in contours if cv2.arcLength(c, False) > 0]

        thickness_std = np.std(thicknesses) if thicknesses else 0
        thickness_mean = np.mean(thicknesses) if thicknesses else 0

        # Quality score (consistent thickness = higher quality)
        quality = 1.0 - min(thickness_std / (thickness_mean + 1), 1.0)

        return {
            "stroke_density": float(stroke_density),
            "average_thickness": float(thickness_mean),
            "thickness_variability": float(thickness_std),
            "quality_score": quality
        }

    def _analyze_letter_formation(self, img: np.ndarray) -> Dict[str, Any]:
        """Analyze letter formation quality"""
        # Simplified: analyze vertical and horizontal components
        sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

        # Orientation consistency
        orientations = np.arctan2(sobel_y, sobel_x)
        orientation_std = np.std(orientations[np.abs(orientations) > 0.1])

        # Formation score (lower variability = better formation)
        formation_score = 1.0 - min(orientation_std / np.pi, 1.0)

        return {
            "orientation_consistency": float(orientation_std),
            "formation_score": formation_score
        }

    def _analyze_spatial_characteristics(self, img: np.ndarray) -> Dict[str, Any]:
        """Analyze spacing and alignment"""
        # Find horizontal projections (rows with writing)
        horizontal_proj = np.sum(255 - img, axis=1)

        # Find lines of text
        threshold = np.mean(horizontal_proj)
        line_positions = np.where(horizontal_proj > threshold)[0]

        if len(line_positions) < 2:
            return {
                "line_count": 0,
                "line_spacing_variability": 0,
                "organization_score": 0.5
            }

        # Calculate line spacing
        line_groups = []
        current_group = [line_positions[0]]

        for i in range(1, len(line_positions)):
            if line_positions[i] - line_positions[i-1] > 5:  # Gap between lines
                line_groups.append(current_group)
                current_group = []
            current_group.append(line_positions[i])

        if current_group:
            line_groups.append(current_group)

        # Calculate spacing between line centers
        line_centers = [np.mean(group) for group in line_groups if len(group) > 0]

        if len(line_centers) > 1:
            spacings = np.diff(line_centers)
            spacing_std = np.std(spacings)
            spacing_mean = np.mean(spacings)

            # Organization score (consistent spacing = better organization)
            organization = 1.0 - min(spacing_std / (spacing_mean + 1), 1.0)
        else:
            spacing_std = 0
            organization = 0.5

        return {
            "line_count": len(line_groups),
            "line_spacing_variability": float(spacing_std),
            "organization_score": organization
        }

    def _detect_tremor(self, img: np.ndarray, pressure_data: Optional[List[float]]) -> float:
        """Detect tremor in handwriting (0-1)"""
        # Analyze edge roughness
        edges = cv2.Canny(img, 50, 150)

        # Calculate local curvature variations
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        curvatures = []
        for contour in contours:
            if len(contour) > 10:
                # Approximate curvature from angle changes
                for i in range(2, len(contour) - 2):
                    vec1 = contour[i][0] - contour[i-2][0]
                    vec2 = contour[i+2][0] - contour[i][0]
                    if np.linalg.norm(vec1) > 0 and np.linalg.norm(vec2) > 0:
                        angle_change = np.arccos(np.clip(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)), -1, 1))
                        curvatures.append(abs(angle_change))

        if curvatures:
            # High curvature variability = more tremor
            tremor = min(np.std(curvatures) * 5, 1.0)
        else:
            tremor = 0.0

        return float(tremor)

    def _detect_micrographia(self, stroke_metrics: Dict) -> float:
        """Detect micrographia (abnormally small writing)"""
        # Small strokes + low density = micrographia
        avg_thickness = stroke_metrics['average_thickness']
        density = stroke_metrics['stroke_density']

        # Threshold: average thickness < 2 pixels and low density
        if avg_thickness < 2 and density < 0.15:
            return 0.8
        elif avg_thickness < 3 and density < 0.20:
            return 0.5
        else:
            return 0.2

    def _calculate_handwriting_cognitive_score(self, metrics: Dict[str, float]) -> float:
        """Calculate overall cognitive score from handwriting (0-100)"""
        stroke_score = metrics.get('stroke_quality', 0.5) * 100
        formation_score = metrics.get('letter_formation', 0.5) * 100
        spatial_score = metrics.get('spatial_organization', 0.5) * 100

        # Penalties for tremor and micrographia
        tremor_penalty = metrics.get('tremor', 0) * 30
        micrographia_penalty = metrics.get('micrographia', 0) * 20

        score = (stroke_score * 0.3 + formation_score * 0.3 + spatial_score * 0.2) - tremor_penalty - micrographia_penalty

        return max(0, min(100, score))

    def _detect_handwriting_abnormalities(self, metrics: Dict) -> List[str]:
        """Detect specific handwriting abnormalities"""
        abnormalities = []

        if metrics['tremor'] > 0.5:
            abnormalities.append("Tremor detected in handwriting")

        if metrics['micrographia'] > 0.5:
            abnormalities.append("Micrographia (abnormally small writing)")

        if metrics['stroke_quality'] < 0.4:
            abnormalities.append("Poor stroke control and consistency")

        return abnormalities


class FacialRecognitionAnalyzer:
    """Analyze facial recognition abilities for prosopagnosia detection"""

    def __init__(self):
        # In production, would load a pre-trained face recognition model
        self.recognition_threshold = 0.6

    def analyze_recognition_test(
        self,
        test_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Analyze facial recognition test results

        Args:
            test_results: List of {shown_face_id, recognized_correctly, response_time, confidence}

        Returns:
            Recognition analysis
        """
        try:
            if not test_results:
                return {"error": "No test results provided"}

            # Calculate accuracy
            correct = sum(1 for r in test_results if r['recognized_correctly'])
            accuracy = correct / len(test_results)

            # Average response time
            avg_response_time = np.mean([r['response_time'] for r in test_results])

            # Confidence in correct vs incorrect
            correct_confidence = np.mean([r['confidence'] for r in test_results if r['recognized_correctly']]) if correct > 0 else 0
            incorrect_confidence = np.mean([r['confidence'] for r in test_results if not r['recognized_correctly']]) if (len(test_results) - correct) > 0 else 0

            # Familiar vs unfamiliar faces
            familiar_results = [r for r in test_results if r.get('familiar', False)]
            unfamiliar_results = [r for r in test_results if not r.get('familiar', False)]

            familiar_accuracy = sum(1 for r in familiar_results if r['recognized_correctly']) / len(familiar_results) if familiar_results else 0
            unfamiliar_accuracy = sum(1 for r in unfamiliar_results if r['recognized_correctly']) / len(unfamiliar_results) if unfamiliar_results else 0

            # Risk assessment
            risk_level = self._assess_recognition_risk(accuracy, familiar_accuracy, avg_response_time)

            return {
                "total_faces_tested": len(test_results),
                "overall_accuracy": accuracy,
                "familiar_face_accuracy": familiar_accuracy,
                "unfamiliar_face_accuracy": unfamiliar_accuracy,
                "average_response_time_seconds": avg_response_time,
                "confidence_when_correct": correct_confidence,
                "confidence_when_incorrect": incorrect_confidence,
                "risk_level": risk_level,
                "possible_prosopagnosia": accuracy < 0.5 or familiar_accuracy < 0.6,
                "recommendations": self._generate_recognition_recommendations(accuracy, familiar_accuracy)
            }

        except Exception as e:
            logger.error(f"Error analyzing facial recognition: {e}")
            raise

    def _assess_recognition_risk(self, overall_acc: float, familiar_acc: float, response_time: float) -> str:
        """Assess cognitive risk from recognition performance"""
        if familiar_acc < 0.5 or overall_acc < 0.4:
            return "high"
        elif familiar_acc < 0.7 or overall_acc < 0.6 or response_time > 5:
            return "moderate"
        else:
            return "low"

    def _generate_recognition_recommendations(self, overall_acc: float, familiar_acc: float) -> List[str]:
        """Generate recommendations based on recognition performance"""
        recommendations = []

        if familiar_acc < 0.6:
            recommendations.append("Consider comprehensive neurological evaluation for facial recognition deficit")

        if overall_acc < 0.5:
            recommendations.append("Practice facial recognition exercises with family photos")

        if not recommendations:
            recommendations.append("Facial recognition ability is within normal range")

        return recommendations


class TemporalModelingService:
    """LSTM/Transformer models for longitudinal patient tracking"""

    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = None

    def create_lstm_model(self, input_dim: int, hidden_dim: int = 128, num_layers: int = 2):
        """Create LSTM model for temporal sequence modeling"""

        class LSTMCognitiveModel(nn.Module):
            def __init__(self, input_dim, hidden_dim, num_layers):
                super(LSTMCognitiveModel, self).__init__()

                self.lstm = nn.LSTM(
                    input_size=input_dim,
                    hidden_size=hidden_dim,
                    num_layers=num_layers,
                    batch_first=True,
                    dropout=0.2 if num_layers > 1 else 0
                )

                self.fc1 = nn.Linear(hidden_dim, hidden_dim // 2)
                self.fc2 = nn.Linear(hidden_dim // 2, 5)  # 5 stages
                self.relu = nn.ReLU()
                self.dropout = nn.Dropout(0.3)

            def forward(self, x):
                # x shape: (batch, sequence_length, input_dim)
                lstm_out, (hidden, cell) = self.lstm(x)

                # Use last hidden state
                last_hidden = hidden[-1]  # (batch, hidden_dim)

                out = self.relu(self.fc1(last_hidden))
                out = self.dropout(out)
                out = self.fc2(out)

                return out

        self.model = LSTMCognitiveModel(input_dim, hidden_dim, num_layers).to(self.device)
        return self.model

    def predict_trajectory(
        self,
        patient_history: List[Dict[str, Any]],
        forecast_horizon: int = 6
    ) -> Dict[str, Any]:
        """
        Predict future cognitive trajectory

        Args:
            patient_history: List of historical assessments with timestamps and features
            forecast_horizon: Months to forecast

        Returns:
            Trajectory predictions
        """
        try:
            if len(patient_history) < 3:
                return {
                    "error": "Insufficient history for temporal modeling",
                    "min_required": 3,
                    "provided": len(patient_history)
                }

            # Extract temporal features
            sequence = self._prepare_temporal_sequence(patient_history)

            # Simple trend analysis (without ML for now)
            trajectory = self._analyze_trend(sequence, forecast_horizon)

            return {
                "historical_datapoints": len(patient_history),
                "forecast_horizon_months": forecast_horizon,
                "current_trend": trajectory['trend'],
                "projected_trajectory": trajectory['projections'],
                "confidence_intervals": trajectory['confidence_intervals'],
                "risk_assessment": trajectory['risk_assessment'],
                "recommendations": self._generate_trajectory_recommendations(trajectory)
            }

        except Exception as e:
            logger.error(f"Error predicting trajectory: {e}")
            raise

    def _prepare_temporal_sequence(self, history: List[Dict]) -> np.ndarray:
        """Prepare temporal sequence from patient history"""
        # Extract key features from each assessment
        sequence = []

        for assessment in sorted(history, key=lambda x: x['timestamp']):
            features = [
                assessment.get('mmse_score', 24),
                assessment.get('moca_score', 22),
                assessment.get('cdr_score', 0),
                assessment.get('adas_cog_score', 10),
                assessment.get('functional_score', 100)
            ]
            sequence.append(features)

        return np.array(sequence)

    def _analyze_trend(self, sequence: np.ndarray, horizon: int) -> Dict[str, Any]:
        """Analyze cognitive trend and make projections"""
        # Calculate rate of change for each metric
        rates_of_change = []

        for i in range(sequence.shape[1]):  # For each feature
            metric_values = sequence[:, i]

            # Linear regression to find trend
            x = np.arange(len(metric_values))
            slope = np.polyfit(x, metric_values, 1)[0]

            rates_of_change.append(slope)

        # Overall trend (average rate)
        avg_rate = np.mean(rates_of_change)

        # Project future values
        projections = []
        for month in range(1, horizon + 1):
            projected = sequence[-1] + (avg_rate * month)
            projections.append({
                "month": month,
                "projected_mmse": max(0, min(30, float(projected[0]))),
                "projected_moca": max(0, min(30, float(projected[1]))),
                "projected_cdr": max(0, min(3, float(projected[2])))
            })

        # Confidence intervals (simplified)
        std_dev = np.std(sequence, axis=0).mean()
        confidence_intervals = {
            "lower_bound": avg_rate - 2 * std_dev,
            "upper_bound": avg_rate + 2 * std_dev
        }

        # Risk assessment
        if avg_rate < -0.5:
            risk = "rapid_decline"
        elif avg_rate < -0.2:
            risk = "moderate_decline"
        elif avg_rate < 0:
            risk = "slow_decline"
        else:
            risk = "stable"

        return {
            "trend": "declining" if avg_rate < 0 else "stable",
            "rate_of_change": float(avg_rate),
            "projections": projections,
            "confidence_intervals": confidence_intervals,
            "risk_assessment": risk
        }

    def _generate_trajectory_recommendations(self, trajectory: Dict) -> List[str]:
        """Generate recommendations based on projected trajectory"""
        recommendations = []

        risk = trajectory['risk_assessment']

        if risk == "rapid_decline":
            recommendations.append("Immediate consultation with neurologist recommended")
            recommendations.append("Consider adjusting treatment plan")
            recommendations.append("Increase frequency of cognitive assessments")

        elif risk == "moderate_decline":
            recommendations.append("Monitor closely with monthly assessments")
            recommendations.append("Discuss treatment options with healthcare provider")

        elif risk == "slow_decline":
            recommendations.append("Continue current treatment and monitoring")
            recommendations.append("Engage in cognitive stimulation activities")

        else:
            recommendations.append("Maintain current health practices")

        return recommendations


# Service instances
handwriting_service = HandwritingAnalyzer()
facial_recognition_service = FacialRecognitionAnalyzer()
temporal_modeling_service = TemporalModelingService()
