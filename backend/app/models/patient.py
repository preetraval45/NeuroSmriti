"""
Patient model for storing patient information
"""

from sqlalchemy import Column, String, Integer, Date, DateTime, Float, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, date

from app.core.database import Base


class Patient(Base):
    """Patient model"""

    __tablename__ = "patients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caregiver_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    # Personal Information
    full_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(10), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String, nullable=True)

    # Medical Information
    diagnosis_date = Column(Date, nullable=True)
    current_stage = Column(Integer, nullable=True)  # 0-7 Alzheimer's stage
    medical_history = Column(JSON, nullable=True)  # Store as JSON
    medications = Column(JSON, nullable=True)  # Current medications

    # Baseline Cognitive Scores
    mmse_score = Column(Integer, nullable=True)  # Mini-Mental State Examination (0-30)
    moca_score = Column(Integer, nullable=True)  # Montreal Cognitive Assessment (0-30)
    cdr_score = Column(Float, nullable=True)  # Clinical Dementia Rating (0-3)

    # Additional Information
    notes = Column(Text, nullable=True)
    emergency_contact = Column(JSON, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    caregiver = relationship("User", back_populates="patients")
    memories = relationship("Memory", back_populates="patient", cascade="all, delete-orphan")
    predictions = relationship("Prediction", back_populates="patient", cascade="all, delete-orphan")
    interventions = relationship("Intervention", back_populates="patient", cascade="all, delete-orphan")

    @property
    def age(self) -> int:
        """Calculate patient's current age"""
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    def __repr__(self):
        return f"<Patient {self.full_name} (Stage {self.current_stage})>"
