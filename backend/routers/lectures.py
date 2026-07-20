from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from database import repository
import schemas

router = APIRouter(prefix="/lectures", tags=["lectures"])


@router.post("", response_model=schemas.LectureOut, status_code=201)
def create_lecture(payload: schemas.LectureCreate, db: Session = Depends(get_db)):
    return repository.create_lecture(
        db,
        teacher_id=payload.teacher_id,
        title=payload.title,
        slide_text=payload.slide_text_content,
        file_path=payload.slide_file_path,
    )


@router.get("/{lecture_id}", response_model=schemas.LectureOut)
def get_lecture(lecture_id: int, db: Session = Depends(get_db)):
    lecture = repository.get_lecture_by_id(db, lecture_id)
    if not lecture:
        raise HTTPException(status_code=404, detail="Lecture not found")
    return lecture


@router.get("", response_model=list[schemas.LectureOut])
def list_lectures(db: Session = Depends(get_db)):
    return db.query(repository.Lecture).order_by(repository.Lecture.id.desc()).all()
