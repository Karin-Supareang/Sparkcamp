from sqlalchemy import func, case
from sqlalchemy.orm import Session
from database.models import Lecture, Quiz, Question, StudentResponse, AnalysisResult
import json

# ==========================================
# 📊 SECTION 1: สำหรับงานของนาย (Agent 2 - Analytics)
# ==========================================

def get_quiz_aggregated_data(db: Session, quiz_id: int) -> dict:
    """
    ฟังก์ชันมหาเวทย์สำหรับย่อยข้อมูลดิบจาก MySQL 
    มันจะทำการกรุ๊ปรวมผลลัพธ์ของนักศึกษาทุกคนในควิซนั้นๆ ออกมาเป็นสถิติสรุป
    เพื่อให้นายพร้อมเอาไปยิงเข้า JamAI (Agent 2) ได้ทันที
    """
    
    # 1. ดึงข้อมูลสถิติภาพรวมของคลาส (Class Summary)
    # หาจำนวนคนทำ, คะแนนเฉลี่ย, คะแนนสูงสุด, คะแนนต่ำสุด
    # (คิดคะแนนโดยนับจำนวนข้อที่ student_responses.is_correct = 1 แยกตามรายคนก่อน แล้วหาค่าทางสถิติ)
    student_scores_subquery = (
        db.query(
            StudentResponse.student_id,
            func.sum(case((StudentResponse.is_correct == 1, 1), else_=0)).label("total_score")
        )
        .filter(StudentResponse.quiz_id == quiz_id)
        .group_by(StudentResponse.student_id)
        .subquery()
    )
    
    class_stats = db.query(
        func.count(student_scores_subquery.c.student_id).label("total_students"),
        func.avg(student_scores_subquery.c.total_score).label("average_score"),
        func.max(student_scores_subquery.c.total_score).label("max_score"),
        func.min(student_scores_subquery.c.total_score).label("min_score")
    ).first()

    # ถ้ายังไม่มีเด็กเข้ามาทำควิซเลย ให้ส่งข้อมูลว่างกลับไป
    if not class_stats or class_stats.total_students == 0:
        return {"error": "No responses found for this quiz"}

    # 2. ดึงข้อมูลวิเคราะห์รายข้อ (Question-by-Question Analysis)
    # หาว่าแต่ละข้อมีหัวข้อ (Topic Tag) อะไร คนตอบถูกกี่เปอร์เซ็นต์ และชอยส์ไหนที่คนตอบผิดเยอะที่สุด
    questions_data = (
        db.query(
            Question.id,
            Question.question_number,
            Question.topic_tag,
            Question.question_text,
            Question.correct_answer
        )
        .filter(Question.quiz_id == quiz_id)
        .order_by(Question.question_number.asc())
        .all()
    )

    question_analysis_list = []
    
    for q in questions_data:
        # นับจำนวนคนตอบข้อนี้ทั้งหมด
        total_resp = db.query(func.count(StudentResponse.id)).filter(StudentResponse.question_id == q.id).scalar() or 1
        
        # นับจำนวนคนตอบถูก
        correct_resp = db.query(func.count(StudentResponse.id)).filter(
            StudentResponse.question_id == q.id, 
            StudentResponse.is_correct == True
        ).scalar() or 0
        
        # คำนวณเปอร์เซ็นต์คนตอบถูก
        correct_percentage = round((correct_resp / total_resp) * 100, 2)
        
        # หาชอยส์ที่เด็กตอบผิดบ่อยที่สุด (Most Common Wrong Answer)
        most_common_wrong = (
            db.query(StudentResponse.selected_answer)
            .filter(StudentResponse.question_id == q.id, StudentResponse.is_correct == False)
            .group_by(StudentResponse.selected_answer)
            .order_by(func.count(StudentResponse.selected_answer).desc())
            .first()
        )
        wrong_answer_key = most_common_wrong[0] if most_common_wrong else "None"

        question_analysis_list.append({
            "question_number": q.question_number,
            "topic_tag": q.topic_tag,
            "question_text": q.question_text,
            "correct_answer": q.correct_answer,
            "correct_percentage": correct_percentage,
            "most_common_wrong_answer": wrong_answer_key
        })

    # 3. ประกอบร่างร่างชุดข้อมูลดิบที่ย่อยแล้ว (Aggregated Package Data)
    aggregated_package = {
        "quiz_id": quiz_id,
        "class_summary": {
            "total_students_submitted": class_stats.total_students,
            "average_score": round(float(class_stats.average_score), 2) if class_stats.average_score else 0,
            "max_score": class_stats.max_score or 0,
            "min_score": class_stats.min_score or 0
        },
        "question_breakdown": question_analysis_list
    }
    
    return aggregated_package


def save_analysis_result(db: Session, quiz_id: int, summary_json_data: dict) -> AnalysisResult:
    """
    บันทึกผลลัพธ์ JSON ที่ได้มาจาก JamAI ลงตาราง analysis_results
    หากเคยบันทึกไปแล้ว จะทำการอัปเดตข้อมูลให้ล่าสุด (Upsert)
    """
    db_result = db.query(AnalysisResult).filter(AnalysisResult.quiz_id == quiz_id).first()
    
    if db_result:
        db_result.summary_json = summary_json_data
    else:
        db_result = AnalysisResult(quiz_id=quiz_id, summary_json=summary_json_data)
        db_prefix = db.add(db_result)
        
    db.commit()
    db.refresh(db_result)
    return db_result


# ==========================================
# 📝 SECTION 2: สำหรับงานของเพื่อน (Agent 1 & หน้าบ้าน)
# ==========================================

def create_lecture(db: Session, teacher_id: str, title: str, slide_text: str, file_path: str = None) -> Lecture:
    """เมื่ออาจารย์อัปโหลดสไลด์ บันทึกข้อความและสร้างไอดีบทเรียน"""
    db_lecture = Lecture(teacher_id=teacher_id, title=title, slide_text_content=slide_text, slide_file_path=file_path)
    db.add(db_lecture)
    db.commit()
    db.refresh(db_lecture)
    return db_lecture

def create_quiz_session(db: Session, lecture_id: int, quiz_code: str) -> Quiz:
    """สร้างเซสชันควิซใหม่เพื่อเอาไปทำ QR Code"""
    db_quiz = Quiz(lecture_id=lecture_id, quiz_code=quiz_code)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def insert_generated_questions(db: Session, quiz_id: int, questions: list) -> list:
    """ให้ Agent 1 เรียกใช้ เพื่อเซฟข้อสอบที่เจนได้ลง DB"""
    inserted_questions = []
    for item in questions:
        db_q = Question(
            quiz_id=quiz_id,
            question_number=item["question_number"],
            question_text=item["question_text"],
            options_json=item["options_json"],
            correct_answer=item["correct_answer"],
            topic_tag=item["topic_tag"]
        )
        db.add(db_q)
        inserted_questions.append(db_q)
    db.commit()
    return inserted_questions

def submit_student_response(db: Session, quiz_id: int, question_id: int, student_id: str, selected_answer: str) -> StudentResponse:
    """หน้าบ้านเรียกใช้เมื่อนักศึกษากดส่งคำตอบ (เช็คคำตอบให้ทันที)"""
    question = db.query(Question).filter(Question.id == question_id).first()
    is_correct = (question.correct_answer.strip().upper() == selected_answer.strip().upper())
    
    db_response = StudentResponse(
        quiz_id=quiz_id,
        question_id=question_id,
        student_id=student_id,
        selected_answer=selected_answer,
        is_correct=is_correct
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response

def close_quiz_session(db: Session, quiz_id: int):
    """อาจารย์สั่งปิดควิซเพื่อสิ้นสุดการทำควิซ"""
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if quiz:
        quiz.is_closed = True
        db.commit()
    return quiz