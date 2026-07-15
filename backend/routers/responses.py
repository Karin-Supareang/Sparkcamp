from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from database import repository
import schemas

router = APIRouter(prefix="/responses", tags=["responses"])


@router.post("", response_model=schemas.ResponseOut, status_code=201)
def submit_response(payload: schemas.ResponseCreate, db: Session = Depends(get_db)):
    quiz = repository.get_quiz_by_id(db, payload.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    if quiz.is_closed:
        raise HTTPException(status_code=400, detail="Quiz is closed")

    question = repository.get_question_by_id(db, payload.question_id)
    if not question or question.quiz_id != payload.quiz_id:
        raise HTTPException(status_code=404, detail="Question not found for this quiz")

    return repository.submit_student_response(
        db,
        quiz_id=payload.quiz_id,
        question_id=payload.question_id,
        student_id=payload.student_id,
        selected_answer=payload.selected_answer,
    )
