"""
Social Support & Gamification API Endpoints
Support groups, forums, education, brain games, achievements, VR therapy
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.services.social_support_service import (
    support_group_service,
    forum_service,
    education_service,
    expert_qa_service,
    peer_matching_service
)
from app.services.gamification_service import (
    brain_games_service,
    achievement_service,
    progress_tracking_service,
    vr_therapy_service
)
from loguru import logger

router = APIRouter(prefix="/social-gamification", tags=["Social & Gamification"])


# ===== Pydantic Models =====

class SupportGroupSearchRequest(BaseModel):
    location: str
    radius_km: int = 50
    group_type: str = "all"  # all, patient, caregiver, mixed


class ForumPostRequest(BaseModel):
    user_id: int
    category: str
    title: str
    content: str
    is_anonymous: bool = False


class ForumReplyRequest(BaseModel):
    user_id: int
    post_id: str
    content: str
    is_anonymous: bool = False


class EducationSearchRequest(BaseModel):
    topic: str
    content_type: Optional[str] = None  # article, video, guide
    difficulty_level: Optional[str] = None  # beginner, intermediate, advanced


class QuestionSubmissionRequest(BaseModel):
    user_id: int
    patient_id: int
    question: str
    category: str
    is_urgent: bool = False


class PeerMatchRequest(BaseModel):
    caregiver_id: int
    patient_diagnosis_stage: str
    caregiver_role: str  # spouse, child, professional
    preferred_language: Optional[str] = "en"


class BrainGameSessionRequest(BaseModel):
    patient_id: int
    game_type: str  # memory, attention, processing_speed, executive_function
    difficulty: str = "adaptive"  # easy, medium, hard, adaptive


class GameResultRequest(BaseModel):
    patient_id: int
    game_session_id: str
    score: int
    time_seconds: int
    mistakes: int


class VRTherapySessionRequest(BaseModel):
    patient_id: int
    therapy_type: str  # reminiscence, relaxation, cognitive_stimulation
    duration_minutes: int = 15


# ===== Social & Support Endpoints =====

@router.post("/support-groups/search")
async def search_support_groups(request: SupportGroupSearchRequest):
    """
    Find local Alzheimer's support groups

    Group types:
    - patient: For individuals with Alzheimer's
    - caregiver: For family caregivers
    - mixed: Combined patient and caregiver groups
    """
    try:
        groups = support_group_service.search_groups(
            location=request.location,
            radius_km=request.radius_km,
            group_type=request.group_type
        )
        return {"groups": groups}
    except Exception as e:
        logger.error(f"Error searching support groups: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/support-groups/online")
async def get_online_support_groups():
    """Get list of online/virtual support groups"""
    try:
        groups = support_group_service.get_online_groups()
        return {"groups": groups}
    except Exception as e:
        logger.error(f"Error getting online support groups: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forum/post")
async def create_forum_post(request: ForumPostRequest):
    """
    Create discussion post in caregiver forums

    Categories: advice, venting, success_stories, resources, questions
    """
    try:
        post = forum_service.create_post(
            user_id=request.user_id,
            category=request.category,
            title=request.title,
            content=request.content,
            is_anonymous=request.is_anonymous
        )
        return post
    except Exception as e:
        logger.error(f"Error creating forum post: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forum/reply")
async def reply_to_post(request: ForumReplyRequest):
    """Reply to forum post"""
    try:
        reply = forum_service.create_reply(
            user_id=request.user_id,
            post_id=request.post_id,
            content=request.content,
            is_anonymous=request.is_anonymous
        )
        return reply
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error replying to post: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/forum/posts")
async def get_forum_posts(
    category: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
):
    """Get forum posts with optional category filter"""
    try:
        posts = forum_service.get_posts(
            category=category,
            limit=limit,
            offset=offset
        )
        return {"posts": posts}
    except Exception as e:
        logger.error(f"Error getting forum posts: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/education/search")
async def search_educational_resources(request: EducationSearchRequest):
    """
    Search curated educational resources

    Topics: symptoms, diagnosis, treatments, caregiving, legal, financial, etc.
    """
    try:
        resources = education_service.search_resources(
            topic=request.topic,
            content_type=request.content_type,
            difficulty_level=request.difficulty_level
        )
        return {"resources": resources}
    except Exception as e:
        logger.error(f"Error searching educational resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/education/recommended/{patient_id}")
async def get_recommended_resources(patient_id: int):
    """Get AI-curated resources based on patient's stage and needs"""
    try:
        resources = education_service.get_personalized_recommendations(patient_id)
        return {"resources": resources}
    except Exception as e:
        logger.error(f"Error getting recommended resources: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/expert-qa/submit")
async def submit_question_to_expert(request: QuestionSubmissionRequest):
    """
    Submit question to dementia care specialists

    Experts respond within 24-48 hours
    Urgent questions prioritized
    """
    try:
        submission = expert_qa_service.submit_question(
            user_id=request.user_id,
            patient_id=request.patient_id,
            question=request.question,
            category=request.category,
            is_urgent=request.is_urgent
        )
        return submission
    except Exception as e:
        logger.error(f"Error submitting question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/expert-qa/answers/{user_id}")
async def get_expert_answers(user_id: int):
    """Get answers to user's questions"""
    try:
        answers = expert_qa_service.get_user_answers(user_id)
        return {"answers": answers}
    except Exception as e:
        logger.error(f"Error getting expert answers: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/peer-matching/find")
async def find_peer_caregivers(request: PeerMatchRequest):
    """
    Match with peer caregivers in similar situations

    Matching factors:
    - Diagnosis stage
    - Caregiver role
    - Geographic proximity
    - Language preference
    """
    try:
        matches = peer_matching_service.find_matches(
            caregiver_id=request.caregiver_id,
            patient_diagnosis_stage=request.patient_diagnosis_stage,
            caregiver_role=request.caregiver_role,
            preferred_language=request.preferred_language
        )
        return {"matches": matches}
    except Exception as e:
        logger.error(f"Error finding peer matches: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===== Gamification Endpoints =====

@router.post("/brain-games/start-session")
async def start_brain_game(request: BrainGameSessionRequest):
    """
    Start evidence-based cognitive exercise session

    Game types:
    - memory: Working memory, episodic memory
    - attention: Sustained attention, selective attention
    - processing_speed: Reaction time, processing speed
    - executive_function: Planning, problem-solving
    """
    try:
        session = brain_games_service.start_game_session(
            patient_id=request.patient_id,
            game_type=request.game_type,
            difficulty=request.difficulty
        )
        return session
    except Exception as e:
        logger.error(f"Error starting brain game: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/brain-games/submit-result")
async def submit_game_result(request: GameResultRequest):
    """
    Submit game results and get feedback

    Updates difficulty for adaptive games
    Awards achievements for milestones
    """
    try:
        result = brain_games_service.submit_result(
            patient_id=request.patient_id,
            game_session_id=request.game_session_id,
            score=request.score,
            time_seconds=request.time_seconds,
            mistakes=request.mistakes
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting game result: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/brain-games/progress/{patient_id}")
async def get_game_progress(patient_id: int, days: int = 30):
    """Get cognitive gaming progress over time"""
    try:
        progress = brain_games_service.get_progress(patient_id, days)
        return progress
    except Exception as e:
        logger.error(f"Error getting game progress: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/achievements/{patient_id}")
async def get_achievements(patient_id: int):
    """
    Get patient achievements and badges

    Achievement categories:
    - Consistency: Daily/weekly streaks
    - Performance: High scores, improvements
    - Milestones: Tests completed, days tracked
    - Social: Forum participation, helping others
    """
    try:
        achievements = achievement_service.get_patient_achievements(patient_id)
        return achievements
    except Exception as e:
        logger.error(f"Error getting achievements: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progress/milestones/{patient_id}")
async def get_milestones(patient_id: int):
    """
    Get progress milestones

    Celebrates:
    - Maintaining cognitive function
    - Medication adherence
    - Lifestyle improvements
    - Engagement consistency
    """
    try:
        milestones = progress_tracking_service.get_milestones(patient_id)
        return milestones
    except Exception as e:
        logger.error(f"Error getting milestones: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/leaderboard")
async def get_leaderboard(
    game_type: Optional[str] = None,
    timeframe: str = "weekly"  # daily, weekly, monthly, all_time
):
    """
    Get anonymized leaderboard for friendly competition

    All patient data is anonymized for privacy
    """
    try:
        leaderboard = brain_games_service.get_leaderboard(
            game_type=game_type,
            timeframe=timeframe
        )
        return leaderboard
    except Exception as e:
        logger.error(f"Error getting leaderboard: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vr-therapy/start-session")
async def start_vr_therapy(request: VRTherapySessionRequest):
    """
    Start VR therapy session for cognitive stimulation

    Therapy types:
    - reminiscence: Virtual visits to familiar places
    - relaxation: Calming environments
    - cognitive_stimulation: Interactive puzzles in VR
    - social: Virtual group activities
    """
    try:
        session = vr_therapy_service.start_session(
            patient_id=request.patient_id,
            therapy_type=request.therapy_type,
            duration_minutes=request.duration_minutes
        )
        return session
    except Exception as e:
        logger.error(f"Error starting VR therapy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/vr-therapy/end-session/{session_id}")
async def end_vr_therapy(session_id: str, patient_feedback: Optional[Dict[str, Any]] = None):
    """End VR therapy session and record feedback"""
    try:
        summary = vr_therapy_service.end_session(
            session_id=session_id,
            patient_feedback=patient_feedback
        )
        return summary
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error ending VR therapy: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/vr-therapy/history/{patient_id}")
async def get_vr_therapy_history(patient_id: int):
    """Get VR therapy session history and effectiveness"""
    try:
        history = vr_therapy_service.get_session_history(patient_id)
        return {"patient_id": patient_id, "sessions": history}
    except Exception as e:
        logger.error(f"Error getting VR therapy history: {e}")
        raise HTTPException(status_code=500, detail=str(e))
