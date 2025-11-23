"""
Prediction models for AI-generated insights
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

from app.core.database import Base


class Prediction(Base):
    """
    Alzheimer's stage prediction and risk assessment
    """

    __tablename__ = "predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)

    # Prediction Results
    predicted_stage = Column(Integer, nullable=False)  # 0-7
    confidence = Column(Float, nullable=False)  # 0-1
    stage_probabilities = Column(JSON, nullable=True)  # Probability distribution across stages

    # Risk Assessment
    progression_risk = Column(String(20), nullable=True)  # "low", "medium", "high"
    estimated_progression_months = Column(Integer, nullable=True)  # Months to next stage

    # Input Data Used
    mri_scan_id = Column(String, nullable=True)
    cognitive_scores = Column(JSON, nullable=True)
    speech_analysis_id = Column(String, nullable=True)
    behavioral_data = Column(JSON, nullable=True)

    # Explanation
    explanation = Column(JSON, nullable=True)  # Feature importance, SHAP values
    top_contributing_factors = Column(JSON, nullable=True)  # Top 3-5 factors

    # Model Information
    model_version = Column(String, nullable=False)
    model_type = Column(String, nullable=False)  # "multimodal_transformer", "memory_gnn"

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    patient = relationship("Patient", back_populates="predictions")

    def __repr__(self):
        return f"<Prediction Patient:{self.patient_id} Stage:{self.predicted_stage} ({self.confidence:.2f})>"


class MemoryDecayPrediction(Base):
    """
    Memory-specific decay predictions
    Predicts which memories will fade and when
    """

    __tablename__ = "memory_decay_predictions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    memory_id = Column(UUID(as_uuid=True), ForeignKey("memories.id"), nullable=False)
    prediction_id = Column(UUID(as_uuid=True), ForeignKey("predictions.id"), nullable=True)

    # Decay Predictions
    decay_30_days = Column(Float, nullable=False)  # Predicted strength in 30 days
    decay_90_days = Column(Float, nullable=False)  # Predicted strength in 90 days
    decay_180_days = Column(Float, nullable=False)  # Predicted strength in 180 days

    # Risk Assessment
    risk_score = Column(Float, nullable=False)  # 0-1, probability of significant decay
    risk_level = Column(String(20), nullable=False)  # "low", "medium", "high", "critical"
    days_until_critical = Column(Integer, nullable=True)  # Days until recall_strength < 30

    # Recommendations
    intervention_recommended = Column(Float, default=False, nullable=False)
    recommended_intervention_type = Column(String, nullable=True)

    # Model Information
    model_version = Column(String, nullable=False)
    explanation = Column(JSON, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    memory = relationship("Memory")
    prediction = relationship("Prediction")

    def __repr__(self):
        return f"<MemoryDecayPrediction Memory:{self.memory_id} Risk:{self.risk_level}>"
