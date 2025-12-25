"""
Advanced AI Features API Endpoints
Speech analysis, eye tracking, gait, sleep, sentiment, handwriting, facial recognition, temporal modeling
"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.speech_analysis_service import speech_analysis_service
from app.services.behavioral_analysis_service import (
    eye_tracking_service, gait_service, sleep_service, sentiment_service
)
from app.services.advanced_cognitive_service import (
    handwriting_service, facial_recognition_service, temporal_modeling_service
)
from loguru import logger

router = APIRouter(prefix="/advanced", tags=["Advanced AI Features"])


# Request/Response Models
class SpeechAnalysisRequest(BaseModel):
    transcript: str
    audio_duration: float
    pause_timestamps: Optional[List[List[float]]] = None
    word_timestamps: Optional[List[List]] = None


class EyeTrackingRequest(BaseModel):
    fixations: List[Dict[str, Any]]
    saccades: List[Dict[str, Any]]
    test_duration: float


class GaitAnalysisRequest(BaseModel):
    accelerometer_data: List[Dict[str, Any]]
    gyroscope_data: Optional[List[Dict[str, Any]]] = None


class SleepAnalysisRequest(BaseModel):
    sleep_sessions: List[Dict[str, Any]]


class SentimentAnalysisRequest(BaseModel):
    text: str
    conversation_history: Optional[List[Dict[str, str]]] = None


class FacialRecognitionRequest(BaseModel):
    test_results: List[Dict[str, Any]]


class TemporalModelingRequest(BaseModel):
    patient_history: List[Dict[str, Any]]
    forecast_horizon: int = 6


# Speech Analysis Endpoint
@router.post("/speech/analyze")
async def analyze_speech(request: SpeechAnalysisRequest):
    """
    Analyze speech patterns for cognitive markers

    Returns linguistic markers, pause patterns, word-finding difficulty, etc.
    """
    try:
        # Convert pause timestamps to tuples
        pause_timestamps = [(p[0], p[1]) for p in request.pause_timestamps] if request.pause_timestamps else None

        result = speech_analysis_service.analyze_speech_recording(
            transcript=request.transcript,
            audio_duration=request.audio_duration,
            pause_timestamps=pause_timestamps,
            word_timestamps=request.word_timestamps
        )

        return result

    except Exception as e:
        logger.error(f"Error in speech analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Eye Tracking Endpoint
@router.post("/eye-tracking/analyze")
async def analyze_eye_tracking(request: EyeTrackingRequest):
    """
    Analyze eye tracking data from cognitive tests

    Returns fixation patterns, saccade metrics, gaze dispersion, etc.
    """
    try:
        result = eye_tracking_service.analyze_gaze_data(
            fixations=request.fixations,
            saccades=request.saccades,
            test_duration=request.test_duration
        )

        return result

    except Exception as e:
        logger.error(f"Error in eye tracking analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Gait Analysis Endpoint
@router.post("/gait/analyze")
async def analyze_gait(request: GaitAnalysisRequest):
    """
    Analyze gait patterns from accelerometer data

    Returns gait speed, stride variability, balance, fall risk, etc.
    """
    try:
        result = gait_service.analyze_gait_data(
            accelerometer_data=request.accelerometer_data,
            gyroscope_data=request.gyroscope_data
        )

        return result

    except Exception as e:
        logger.error(f"Error in gait analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Sleep Analysis Endpoint
@router.post("/sleep/analyze")
async def analyze_sleep(request: SleepAnalysisRequest):
    """
    Analyze sleep patterns for cognitive decline markers

    Returns sleep quality, REM percentage, disruptions, cognitive impact, etc.
    """
    try:
        result = sleep_service.analyze_sleep_data(
            sleep_sessions=request.sleep_sessions
        )

        return result

    except Exception as e:
        logger.error(f"Error in sleep analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Sentiment Analysis Endpoint
@router.post("/sentiment/analyze")
async def analyze_sentiment(request: SentimentAnalysisRequest):
    """
    Analyze sentiment and emotional patterns

    Returns sentiment score, emotional stability, cognitive indicators, etc.
    """
    try:
        result = sentiment_service.analyze_sentiment(
            text=request.text,
            conversation_history=request.conversation_history
        )

        return result

    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Handwriting Analysis Endpoint
@router.post("/handwriting/analyze")
async def analyze_handwriting(
    image: UploadFile = File(...),
    writing_duration: Optional[float] = None
):
    """
    Analyze handwriting for tremor, micrographia, and cognitive markers

    Upload a handwriting sample image for analysis
    """
    try:
        import tempfile
        import os

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            content = await image.read()
            tmp.write(content)
            image_path = tmp.name

        # Analyze handwriting
        result = handwriting_service.analyze_handwriting_sample(
            image_path=image_path,
            writing_duration=writing_duration
        )

        # Clean up
        os.unlink(image_path)

        return result

    except Exception as e:
        logger.error(f"Error in handwriting analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Facial Recognition Endpoint
@router.post("/facial-recognition/analyze")
async def analyze_facial_recognition(request: FacialRecognitionRequest):
    """
    Analyze facial recognition test results for prosopagnosia detection

    Returns recognition accuracy, familiar vs unfamiliar performance, etc.
    """
    try:
        result = facial_recognition_service.analyze_recognition_test(
            test_results=request.test_results
        )

        return result

    except Exception as e:
        logger.error(f"Error in facial recognition analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Temporal Modeling Endpoint
@router.post("/temporal/predict-trajectory")
async def predict_cognitive_trajectory(request: TemporalModelingRequest):
    """
    Predict future cognitive trajectory using temporal modeling

    Uses LSTM/Transformer models to forecast cognitive decline
    """
    try:
        result = temporal_modeling_service.predict_trajectory(
            patient_history=request.patient_history,
            forecast_horizon=request.forecast_horizon
        )

        return result

    except Exception as e:
        logger.error(f"Error in temporal modeling: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Comprehensive Assessment Endpoint
@router.post("/comprehensive-assessment")
async def comprehensive_cognitive_assessment(
    patient_id: int,
    speech_data: Optional[SpeechAnalysisRequest] = None,
    eye_tracking_data: Optional[EyeTrackingRequest] = None,
    gait_data: Optional[GaitAnalysisRequest] = None,
    sleep_data: Optional[SleepAnalysisRequest] = None,
    sentiment_data: Optional[SentimentAnalysisRequest] = None
):
    """
    Perform comprehensive cognitive assessment using multiple modalities

    Combines all available data sources for holistic evaluation
    """
    try:
        results = {
            "patient_id": patient_id,
            "assessments": {}
        }

        # Run each analysis if data provided
        if speech_data:
            results["assessments"]["speech"] = speech_analysis_service.analyze_speech_recording(
                speech_data.transcript,
                speech_data.audio_duration,
                [(p[0], p[1]) for p in speech_data.pause_timestamps] if speech_data.pause_timestamps else None,
                speech_data.word_timestamps
            )

        if eye_tracking_data:
            results["assessments"]["eye_tracking"] = eye_tracking_service.analyze_gaze_data(
                eye_tracking_data.fixations,
                eye_tracking_data.saccades,
                eye_tracking_data.test_duration
            )

        if gait_data:
            results["assessments"]["gait"] = gait_service.analyze_gait_data(
                gait_data.accelerometer_data,
                gait_data.gyroscope_data
            )

        if sleep_data:
            results["assessments"]["sleep"] = sleep_service.analyze_sleep_data(
                sleep_data.sleep_sessions
            )

        if sentiment_data:
            results["assessments"]["sentiment"] = sentiment_service.analyze_sentiment(
                sentiment_data.text,
                sentiment_data.conversation_history
            )

        # Calculate overall risk score
        risk_scores = []
        if "speech" in results["assessments"]:
            speech_risk = 1 - (results["assessments"]["speech"]["cognitive_score"] / 100)
            risk_scores.append(speech_risk)

        if "eye_tracking" in results["assessments"]:
            risk_scores.append(results["assessments"]["eye_tracking"]["risk_score"])

        if "gait" in results["assessments"]:
            risk_scores.append(results["assessments"]["gait"]["fall_risk_score"])

        overall_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0

        results["overall_risk_score"] = overall_risk
        results["risk_level"] = "high" if overall_risk > 0.7 else "moderate" if overall_risk > 0.4 else "low"

        return results

    except Exception as e:
        logger.error(f"Error in comprehensive assessment: {e}")
        raise HTTPException(status_code=500, detail=str(e))
