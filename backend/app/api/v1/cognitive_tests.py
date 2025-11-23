"""
Cognitive Assessment Tests API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel
import random

from app.core.database import get_db
from app.core.security import get_current_active_user

router = APIRouter()


# Schemas
class TestStart(BaseModel):
    test_type: str  # memory, attention, language, spatial, executive
    patient_id: Optional[str] = None


class TestAnswer(BaseModel):
    question_id: str
    answer: str
    time_taken_ms: int


class QuestionResponse(BaseModel):
    question_id: str
    question_type: str
    content: dict
    options: Optional[List[str]] = None


class TestSession(BaseModel):
    test_id: str
    test_type: str
    total_questions: int
    current_question: int
    question: QuestionResponse


class TestResult(BaseModel):
    test_id: str
    test_type: str
    score: int
    max_score: int
    percentage: float
    time_spent_seconds: int
    performance_summary: dict
    recommendations: List[str]


# In-memory test sessions (in production, use Redis or database)
active_tests = {}


# Test question generators
def generate_memory_questions():
    """Generate memory test questions."""
    questions = [
        {
            "question_id": str(uuid4()),
            "question_type": "sequence_recall",
            "content": {
                "instruction": "Remember this sequence of numbers",
                "sequence": [random.randint(1, 9) for _ in range(4 + i)],
                "display_time_ms": 3000
            }
        }
        for i in range(5)
    ]
    return questions


def generate_attention_questions():
    """Generate attention test questions."""
    questions = []
    for i in range(5):
        grid = ['O'] * 9
        odd_idx = random.randint(0, 8)
        grid[odd_idx] = random.choice(['Q', 'D', 'C'])
        questions.append({
            "question_id": str(uuid4()),
            "question_type": "odd_one_out",
            "content": {
                "instruction": "Find the different symbol",
                "grid": grid,
                "correct_index": odd_idx
            }
        })
    return questions


def generate_language_questions():
    """Generate language test questions."""
    word_sets = [
        ["APPLE", "BANANA", "ORANGE"],
        ["CAT", "DOG", "BIRD", "FISH"],
        ["HAPPY", "SAD", "ANGRY", "CALM", "EXCITED"],
        ["CHAIR", "TABLE", "LAMP", "SOFA"],
        ["MOUNTAIN", "OCEAN", "FOREST", "DESERT", "RIVER"]
    ]
    questions = [
        {
            "question_id": str(uuid4()),
            "question_type": "word_recall",
            "content": {
                "instruction": "Remember these words",
                "words": words,
                "display_time_ms": len(words) * 1500
            }
        }
        for words in word_sets
    ]
    return questions


def generate_spatial_questions():
    """Generate spatial reasoning questions."""
    shapes = ['▲', '►', '▼', '◄']
    questions = []
    for _ in range(5):
        target = random.randint(0, 3)
        start = (target + random.randint(1, 3)) % 4
        questions.append({
            "question_id": str(uuid4()),
            "question_type": "rotation",
            "content": {
                "instruction": "Rotate the shape to match the target",
                "shapes": shapes,
                "target_index": target,
                "start_index": start
            }
        })
    return questions


def generate_executive_questions():
    """Generate executive function questions."""
    patterns = [
        {"sequence": [2, 4, 6, 8], "answer": 10, "rule": "add 2"},
        {"sequence": [1, 3, 6, 10], "answer": 15, "rule": "add increasing"},
        {"sequence": [3, 6, 12, 24], "answer": 48, "rule": "multiply by 2"},
        {"sequence": [1, 1, 2, 3, 5], "answer": 8, "rule": "fibonacci"},
        {"sequence": [100, 50, 25], "answer": 12.5, "rule": "divide by 2"}
    ]
    questions = [
        {
            "question_id": str(uuid4()),
            "question_type": "pattern_completion",
            "content": {
                "instruction": "What comes next in the pattern?",
                "sequence": p["sequence"],
                "correct_answer": p["answer"]
            }
        }
        for p in patterns
    ]
    return questions


@router.post("/start", response_model=TestSession)
async def start_test(
    test_data: TestStart,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Start a new cognitive assessment test."""
    test_type = test_data.test_type.lower()

    # Generate questions based on test type
    if test_type == "memory":
        questions = generate_memory_questions()
    elif test_type == "attention":
        questions = generate_attention_questions()
    elif test_type == "language":
        questions = generate_language_questions()
    elif test_type == "spatial":
        questions = generate_spatial_questions()
    elif test_type == "executive":
        questions = generate_executive_questions()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown test type: {test_type}"
        )

    test_id = str(uuid4())

    # Store test session
    active_tests[test_id] = {
        "test_id": test_id,
        "test_type": test_type,
        "patient_id": test_data.patient_id,
        "user_id": current_user["user_id"],
        "questions": questions,
        "answers": [],
        "current_index": 0,
        "started_at": datetime.utcnow(),
        "score": 0
    }

    return TestSession(
        test_id=test_id,
        test_type=test_type,
        total_questions=len(questions),
        current_question=1,
        question=QuestionResponse(
            question_id=questions[0]["question_id"],
            question_type=questions[0]["question_type"],
            content=questions[0]["content"]
        )
    )


@router.post("/{test_id}/answer")
async def submit_answer(
    test_id: str,
    answer_data: TestAnswer,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Submit an answer for the current question."""
    if test_id not in active_tests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test session not found"
        )

    test = active_tests[test_id]

    if test["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this test"
        )

    # Record answer
    current_q = test["questions"][test["current_index"]]

    # Check if answer is correct
    correct = False
    if current_q["question_type"] == "sequence_recall":
        correct = answer_data.answer == "".join(map(str, current_q["content"]["sequence"]))
    elif current_q["question_type"] == "odd_one_out":
        correct = int(answer_data.answer) == current_q["content"]["correct_index"]
    elif current_q["question_type"] == "word_recall":
        submitted_words = set(answer_data.answer.upper().split(","))
        correct_words = set(current_q["content"]["words"])
        correct = len(submitted_words & correct_words) >= len(correct_words) * 0.8
    elif current_q["question_type"] == "rotation":
        correct = int(answer_data.answer) == current_q["content"]["target_index"]
    elif current_q["question_type"] == "pattern_completion":
        try:
            correct = float(answer_data.answer) == current_q["content"]["correct_answer"]
        except:
            correct = False

    if correct:
        test["score"] += 1

    test["answers"].append({
        "question_id": answer_data.question_id,
        "answer": answer_data.answer,
        "time_taken_ms": answer_data.time_taken_ms,
        "correct": correct
    })

    test["current_index"] += 1

    # Check if test is complete
    if test["current_index"] >= len(test["questions"]):
        return {
            "status": "complete",
            "message": "Test completed. Get results at /results endpoint.",
            "test_id": test_id
        }

    # Return next question
    next_q = test["questions"][test["current_index"]]
    return {
        "status": "next_question",
        "current_question": test["current_index"] + 1,
        "total_questions": len(test["questions"]),
        "previous_correct": correct,
        "question": QuestionResponse(
            question_id=next_q["question_id"],
            question_type=next_q["question_type"],
            content=next_q["content"]
        )
    }


@router.get("/{test_id}/results", response_model=TestResult)
async def get_test_results(
    test_id: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get results for a completed test."""
    if test_id not in active_tests:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Test session not found"
        )

    test = active_tests[test_id]

    if test["user_id"] != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this test"
        )

    # Calculate metrics
    total_time = sum(a["time_taken_ms"] for a in test["answers"]) / 1000
    correct_count = sum(1 for a in test["answers"] if a["correct"])
    total_questions = len(test["questions"])
    percentage = (correct_count / total_questions) * 100

    # Generate performance summary
    avg_time = total_time / total_questions if total_questions > 0 else 0

    performance = {
        "correct_answers": correct_count,
        "total_questions": total_questions,
        "average_response_time": round(avg_time, 2),
        "fastest_response": min((a["time_taken_ms"] for a in test["answers"]), default=0) / 1000,
        "slowest_response": max((a["time_taken_ms"] for a in test["answers"]), default=0) / 1000,
        "accuracy_trend": "stable"  # Could calculate trend over questions
    }

    # Generate recommendations
    recommendations = []
    if percentage < 60:
        recommendations.append("Consider scheduling a follow-up assessment with a specialist")
        recommendations.append("Try daily memory exercises to improve cognitive function")
    elif percentage < 80:
        recommendations.append("Good performance! Continue with regular cognitive exercises")
        recommendations.append("Consider using memory aids for daily tasks")
    else:
        recommendations.append("Excellent cognitive performance!")
        recommendations.append("Maintain current lifestyle and mental engagement")

    if avg_time > 5:
        recommendations.append("Practice timed exercises to improve processing speed")

    test_names = {
        "memory": "Memory Assessment",
        "attention": "Attention Assessment",
        "language": "Language Assessment",
        "spatial": "Spatial Reasoning Assessment",
        "executive": "Executive Function Assessment"
    }

    return TestResult(
        test_id=test_id,
        test_type=test_names.get(test["test_type"], test["test_type"]),
        score=correct_count,
        max_score=total_questions,
        percentage=round(percentage, 1),
        time_spent_seconds=int(total_time),
        performance_summary=performance,
        recommendations=recommendations
    )


@router.get("/history")
async def get_test_history(
    patient_id: Optional[str] = None,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_active_user)
):
    """Get test history for current user or patient."""
    # Filter tests by user/patient
    user_tests = [
        {
            "test_id": tid,
            "test_type": t["test_type"],
            "score": t["score"],
            "total": len(t["questions"]),
            "started_at": t["started_at"].isoformat(),
            "completed": t["current_index"] >= len(t["questions"])
        }
        for tid, t in active_tests.items()
        if t["user_id"] == current_user["user_id"]
    ]

    return user_tests[:limit]
