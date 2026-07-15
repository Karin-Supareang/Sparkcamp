from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from database import repository
import schemas

router = APIRouter(prefix="/quizzes", tags=["questions"])


@router.post("/{quiz_id}/questions", response_model=list[schemas.QuestionOut], status_code=201)
def add_questions(quiz_id: int, payload: schemas.QuestionsCreateRequest, db: Session = Depends(get_db)):
    if not repository.get_quiz_by_id(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    questions = [q.model_dump() for q in payload.questions]
    return repository.insert_generated_questions(db, quiz_id, questions)


@router.get("/{quiz_id}/questions", response_model=list[schemas.QuestionOut])
def list_questions(quiz_id: int, db: Session = Depends(get_db)):
    if not repository.get_quiz_by_id(db, quiz_id):
        raise HTTPException(status_code=404, detail="Quiz not found")
    return repository.get_questions_by_quiz(db, quiz_id)
