"""
Memory Intervention endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.core.security import get_current_active_user

router = APIRouter()


@router.get("/{patient_id}")
async def get_interventions(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get recommended interventions for patient"""
    return {
        "patient_id": str(patient_id),
        "interventions": [
            {
                "id": "intervention-1",
                "type": "spaced_repetition",
                "title": "Remember Alex's Baseball Game",
                "description": "Help strengthen memory of grandson's weekly activity",
                "scheduled_for": "2024-01-21T09:00:00Z",
                "status": "scheduled"
            }
        ]
    }


@router.post("/{intervention_id}/complete")
async def complete_intervention(
    intervention_id: UUID,
    success: bool,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Mark intervention as completed with result"""
    pass
