"""
Intervention models for memory preservation activities
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, JSON, Text, Enum, Float, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base


class InterventionType(str, enum.Enum):
    """Types of memory interventions"""
    SPACED_REPETITION = "spaced_repetition"
    CONTEXTUAL_ANCHORING = "contextual_anchoring"
    MULTIMEDIA_REINFORCEMENT = "multimedia_reinforcement"
    EMOTIONAL_PRESERVATION = "emotional_preservation"
    ROUTINE_REMINDER = "routine_reminder"
    NAVIGATION_ASSIST = "navigation_assist"


class InterventionStatus(str, enum.Enum):
    """Status of intervention"""
    SCHEDULED = "scheduled"
    DELIVERED = "delivered"
    COMPLETED = "completed"
    SKIPPED = "skipped"
    FAILED = "failed"


class Intervention(Base):
    """
    Memory preservation interventions
    Tracks what interventions are delivered to patients
    """

    __tablename__ = "interventions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)
    memory_id = Column(UUID(as_uuid=True), ForeignKey("memories.id"), nullable=True)

    # Intervention Details
    type = Column(Enum(InterventionType), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    content = Column(JSON, nullable=True)  # Intervention-specific content

    # Timing
    scheduled_for = Column(DateTime, nullable=False)
    delivered_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Status & Results
    status = Column(Enum(InterventionStatus), default=InterventionStatus.SCHEDULED, nullable=False)
    success = Column(Boolean, nullable=True)  # Did patient complete it successfully?

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="interventions")
    memory = relationship("Memory")
    results = relationship("InterventionResult", back_populates="intervention", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Intervention {self.type.value} for Patient:{self.patient_id}>"


class InterventionResult(Base):
    """
    Results and effectiveness tracking for interventions
    """

    __tablename__ = "intervention_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    intervention_id = Column(UUID(as_uuid=True), ForeignKey("interventions.id"), nullable=False)

    # Performance Metrics
    recall_before = Column(Float, nullable=True)  # Memory strength before intervention
    recall_after = Column(Float, nullable=True)  # Memory strength after intervention
    improvement = Column(Float, nullable=True)  # Calculated improvement percentage

    # User Interaction
    time_spent_seconds = Column(Integer, nullable=True)
    attempts = Column(Integer, default=1, nullable=False)
    hints_used = Column(Integer, default=0, nullable=False)

    # Qualitative Data
    patient_feedback = Column(Text, nullable=True)
    caregiver_notes = Column(Text, nullable=True)
    emotional_response = Column(String(50), nullable=True)  # "positive", "neutral", "negative", "frustrated"

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    intervention = relationship("Intervention", back_populates="results")

    def __repr__(self):
        return f"<InterventionResult {self.intervention_id} (Improvement: {self.improvement})>"
