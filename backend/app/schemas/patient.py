"""
Pydantic schemas for patients
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from uuid import UUID


class PatientCreate(BaseModel):
    """Schema for creating a new patient"""
    full_name: str
    date_of_birth: date
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    diagnosis_date: Optional[date] = None
    current_stage: Optional[int] = Field(None, ge=0, le=7)
    mmse_score: Optional[int] = Field(None, ge=0, le=30)
    moca_score: Optional[int] = Field(None, ge=0, le=30)
    cdr_score: Optional[float] = Field(None, ge=0, le=3)


class PatientUpdate(BaseModel):
    """Schema for updating patient information"""
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    current_stage: Optional[int] = Field(None, ge=0, le=7)
    mmse_score: Optional[int] = Field(None, ge=0, le=30)
    moca_score: Optional[int] = Field(None, ge=0, le=30)
    cdr_score: Optional[float] = Field(None, ge=0, le=3)
    notes: Optional[str] = None


class PatientResponse(BaseModel):
    """Schema for patient response"""
    id: UUID
    full_name: str
    date_of_birth: date
    gender: Optional[str]
    current_stage: Optional[int]
    diagnosis_date: Optional[date]
    mmse_score: Optional[int]
    moca_score: Optional[int]
    cdr_score: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
