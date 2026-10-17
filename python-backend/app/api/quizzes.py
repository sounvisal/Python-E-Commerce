import json
from typing import Optional, Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.database import get_db
from app.models.quiz import Quiz

router = APIRouter(prefix="/quizzes", tags=["Skin Diagnostic Quizzes"])

class QuizCompletionPayload(BaseModel):
    answers: Dict[str, Any]
    skin_type_result: Optional[str] = "Combination"
    recommended_product_ids: Optional[List[int]] = []

@router.get("/active")
def get_active_quiz(db: Session = Depends(get_db)):
    """
    Public endpoint: Get the active Skin Diagnostic Quiz with parsed question steps.
    Used by Storefront /quiz and /quiz/questions.
    """
    quiz = db.query(Quiz).filter(Quiz.status == "active").order_by(Quiz.id.asc()).first()
    if not quiz:
        # Fallback to first quiz
        quiz = db.query(Quiz).first()

    if not quiz:
        raise HTTPException(status_code=404, detail="No active diagnostic quizzes found.")

    questions = []
    if quiz.questions_data:
        if isinstance(quiz.questions_data, list):
            questions = quiz.questions_data
        elif isinstance(quiz.questions_data, str):
            try:
                questions = json.loads(quiz.questions_data)
            except Exception:
                questions = []

    settings = {}
    if quiz.settings:
        if isinstance(quiz.settings, dict):
            settings = quiz.settings
        elif isinstance(quiz.settings, str):
            try:
                settings = json.loads(quiz.settings)
            except Exception:
                settings = {}

    return {
        "status": "success",
        "data": {
            "id": quiz.id,
            "title": quiz.title,
            "slug": quiz.slug,
            "description": quiz.description,
            "badge": quiz.badge,
            "level": quiz.level,
            "cover_image": quiz.cover_image,
            "questions_count": quiz.questions_count,
            "questions": questions,
            "settings": settings
        }
    }

@router.get("/{quiz_id_or_slug}")
def get_quiz_by_id_or_slug(quiz_id_or_slug: str, db: Session = Depends(get_db)):
    """
    Public endpoint: Get details of a specific quiz.
    """
    clean = quiz_id_or_slug.strip()
    quiz = db.query(Quiz).filter(
        (Quiz.slug == clean) |
        (Quiz.id == int(clean) if clean.isdigit() else False)
    ).first()

    if not quiz:
        raise HTTPException(status_code=404, detail=f"Quiz '{quiz_id_or_slug}' not found.")

    questions = []
    if quiz.questions_data:
        if isinstance(quiz.questions_data, list):
            questions = quiz.questions_data
        elif isinstance(quiz.questions_data, str):
            try:
                questions = json.loads(quiz.questions_data)
            except Exception:
                questions = []

    return {
        "status": "success",
        "data": {
            "id": quiz.id,
            "title": quiz.title,
            "slug": quiz.slug,
            "description": quiz.description,
            "cover_image": quiz.cover_image,
            "questions": questions
        }
    }

@router.post("/{quiz_id}/complete")
def record_quiz_completion(quiz_id: int, payload: QuizCompletionPayload, db: Session = Depends(get_db)):
    """
    Record quiz completion, increment statistics, and return recommendation guidance.
    """
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz.completions = (quiz.completions or 0) + 1
    db.commit()

    return {
        "status": "success",
        "message": "Diagnostic completion recorded successfully",
        "result": {
            "skin_type": payload.skin_type_result,
            "completions": quiz.completions
        }
    }
