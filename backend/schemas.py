from datetime import datetime
from pydantic import BaseModel, ConfigDict


# ---------- Lectures ----------

class LectureCreate(BaseModel):
    teacher_id: str
    title: str
    slide_text_content: str
    slide_file_path: str | None = None


class LectureOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    teacher_id: str
    title: str
    slide_file_path: str | None
    slide_text_content: str
    created_at: datetime | None


# ---------- Quizzes ----------

class QuizCreate(BaseModel):
    lecture_id: int
    quiz_code: str


class QuizOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lecture_id: int
    quiz_code: str
    is_closed: bool
    created_at: datetime | None


# ---------- Questions ----------

class QuestionCreate(BaseModel):
    question_number: int
    question_text: str
    options_json: dict
    correct_answer: str
    topic_tag: str


class QuestionsCreateRequest(BaseModel):
    questions: list[QuestionCreate]


class QuestionOut(BaseModel):
    """Student-facing view — correct_answer is intentionally omitted."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_id: int
    question_number: int
    question_text: str
    options_json: dict
    topic_tag: str


# ---------- Student responses ----------

class ResponseCreate(BaseModel):
    quiz_id: int
    question_id: int
    student_id: str
    selected_answer: str


class ResponseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    quiz_id: int
    question_id: int
    student_id: str
    selected_answer: str
    is_correct: bool
    submitted_at: datetime | None


# ---------- Analytics ----------

class AnalysisOut(BaseModel):
    quiz_id: int
    status: str
    analysis_result: str


class SavedAnalysisOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    quiz_id: int
    overall_summary: str
    critical_review: str
    mastery_achieved: str
    analyzed_at: datetime | None
