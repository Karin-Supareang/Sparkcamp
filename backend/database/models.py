from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP, JSON, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.database import Base

class Lecture(Base):
    __tablename__ = "lectures"

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    slide_file_path = Column(String(555), nullable=True)
    slide_text_content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    quizzes = relationship("Quiz", back_populates="lecture", cascade="all, delete-orphan")

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    lecture_id = Column(Integer, ForeignKey("lectures.id", ondelete="CASCADE"), nullable=False)
    quiz_code = Column(String(10), unique=True, nullable=False)
    is_closed = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    lecture = relationship("Lecture", back_populates="quizzes")
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    responses = relationship("StudentResponse", back_populates="quiz", cascade="all, delete-orphan")
    analysis = relationship("AIAnalysisReport", back_populates="quiz", uselist=False, cascade="all, delete-orphan")

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    options_json = Column(JSON, nullable=False)
    correct_answer = Column(String(5), nullable=False)
    topic_tag = Column(String(100), nullable=False)

    quiz = relationship("Quiz", back_populates="questions")
    responses = relationship("StudentResponse", back_populates="question", cascade="all, delete-orphan")

class StudentResponse(Base):
    __tablename__ = "student_responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(String(50), nullable=False)
    selected_answer = Column(String(5), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    submitted_at = Column(TIMESTAMP, server_default=func.now())

    quiz = relationship("Quiz", back_populates="responses")
    question = relationship("Question", back_populates="responses")

class AIAnalysisReport(Base):
    __tablename__ = "ai_analysis_reports"

    # ใช้ quiz_id เป็นทั้ง Primary Key และ Foreign Key ผูกกับตาราง quizzes ไปเลย (1 ควิซ มี 1 ผลวิเคราะห์)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), primary_key=True)
    
    # 3 คอลัมน์ใหม่ที่ดึงแยกมาจาก 3 คอลัมน์ของ JamAI ตรงตามหน้า Web UI เป๊ะๆ
    overall_summary = Column(Text, nullable=False)   # กล่องสีเหลือง
    critical_review = Column(Text, nullable=False)    # กล่องสีแดง
    mastery_achieved = Column(Text, nullable=False)   # กล่องสีเขียว
    
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    quiz = relationship("Quiz", back_populates="analysis")

    def to_dict(self):
        return {
            "quiz_id": self.quiz_id,
            "overall_summary": self.overall_summary,
            "critical_review": self.critical_review,
            "mastery_achieved": self.mastery_achieved,
            "analyzed_at": self.analyzed_at.isoformat() if self.analyzed_at else None
        }