"""
Memory models for Personal Memory Knowledge Graph
"""

from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Text, JSON, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum

from app.core.database import Base


class MemoryType(str, enum.Enum):
    """Types of memories in the knowledge graph"""
    PERSON = "person"
    PLACE = "place"
    EVENT = "event"
    SKILL = "skill"
    ROUTINE = "routine"
    OBJECT = "object"


class Memory(Base):
    """
    Individual memory node in the knowledge graph
    Represents people, places, events, skills, etc.
    """

    __tablename__ = "memories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    patient_id = Column(UUID(as_uuid=True), ForeignKey("patients.id"), nullable=False)

    # Memory Content
    type = Column(Enum(MemoryType), nullable=False)
    name = Column(String, nullable=False)  # e.g., "Daughter Alice", "Home Address"
    description = Column(Text, nullable=True)
    memory_metadata = Column(JSON, nullable=True)  # Additional structured data

    # Memory Strength & Status
    recall_strength = Column(Float, default=100.0, nullable=False)  # 0-100 scale
    emotional_weight = Column(Float, default=0.5, nullable=False)  # 0-1 scale
    importance = Column(Integer, default=5, nullable=False)  # 1-10 scale

    # Temporal Information
    memory_date = Column(DateTime, nullable=True)  # When the memory is from
    last_accessed = Column(DateTime, default=datetime.utcnow, nullable=False)
    access_count = Column(Integer, default=0, nullable=False)

    # Decay Prediction
    predicted_decay_rate = Column(Float, nullable=True)  # Percentage per month
    high_risk = Column(Float, default=False, nullable=False)  # Flagged for intervention

    # Media attachments
    image_url = Column(String, nullable=True)
    audio_url = Column(String, nullable=True)
    video_url = Column(String, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    patient = relationship("Patient", back_populates="memories")
    outgoing_connections = relationship(
        "MemoryConnection",
        foreign_keys="MemoryConnection.source_id",
        back_populates="source",
        cascade="all, delete-orphan"
    )
    incoming_connections = relationship(
        "MemoryConnection",
        foreign_keys="MemoryConnection.target_id",
        back_populates="target",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Memory {self.type.value}: {self.name} (Strength: {self.recall_strength})>"


class ConnectionType(str, enum.Enum):
    """Types of connections between memories"""
    FAMILY = "family"
    FRIEND = "friend"
    ASSOCIATED_WITH = "associated_with"
    LOCATED_AT = "located_at"
    TEMPORAL = "temporal"  # Happened around same time
    EMOTIONAL = "emotional"  # Emotionally linked


class MemoryConnection(Base):
    """
    Edges in the memory knowledge graph
    Represents relationships between memories
    """

    __tablename__ = "memory_connections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id = Column(UUID(as_uuid=True), ForeignKey("memories.id"), nullable=False)
    target_id = Column(UUID(as_uuid=True), ForeignKey("memories.id"), nullable=False)

    # Connection Properties
    connection_type = Column(Enum(ConnectionType), nullable=False)
    strength = Column(Float, default=1.0, nullable=False)  # 0-1 scale
    description = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    source = relationship("Memory", foreign_keys=[source_id], back_populates="outgoing_connections")
    target = relationship("Memory", foreign_keys=[target_id], back_populates="incoming_connections")

    def __repr__(self):
        return f"<MemoryConnection {self.connection_type.value}: {self.source_id} -> {self.target_id}>"
