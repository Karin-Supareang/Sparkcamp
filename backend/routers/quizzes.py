from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config.database import get_db
from database import repository
import schemas

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("", response_model=schemas.QuizOut, status_code=201)
def create_quiz(payload: schemas.QuizCreate, db: Session = Depends(get_db)):
    if not repository.get_lecture_by_id(db, payload.lecture_id):
        raise HTTPException(status_code=404, detail="Lecture not found")
    try:
        return repository.create_quiz_session(db, payload.lecture_id, payload.quiz_code)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="quiz_code already exists")


@router.get("/{quiz_id}", response_model=schemas.QuizOut)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = repository.get_quiz_by_id(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.get("/by-code/{quiz_code}", response_model=schemas.QuizOut)
def get_quiz_by_code(quiz_code: str, db: Session = Depends(get_db)):
    quiz = repository.get_quiz_by_code(db, quiz_code)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


@router.patch("/{quiz_id}/close", response_model=schemas.QuizOut)
def close_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = repository.close_quiz_session(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
