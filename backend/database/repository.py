from sqlalchemy import func, case
from sqlalchemy.orm import Session
from database.models import Lecture, Quiz, Question, StudentResponse, AIAnalysisReport
import json

# ==========================================
# 📊 SECTION 1: สำหรับงานของนาย (Agent 2 - Analytics)
# ==========================================

def get_quiz_aggregated_data(db: Session, quiz_id: int) -> dict:
    """
    ฟังก์ชันมหาเวทย์สำหรับย่อยข้อมูลดิบจาก MySQL ปรับปรุงเวอร์ชันส่งให้ AI วิเคราะห์
    ส่งทั้ง: 1. ภาพรวมสถิติ, 2. โจทย์+ชอยส์+เฉลย, 3. ตารางคำตอบแบบละเอียดรายคน
    """
    # --- 1. ดึงข้อมูลสถิติภาพรวมคลาส (Class Summary) ---
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

    if not class_stats or class_stats.total_students == 0:
        return {"error": "No responses found for this quiz"}

    # --- 2. ดึงข้อสอบ, ตัวเลือก (Options), เฉลย และ Topic (Question Breakdown) ---
    questions_data = (
        db.query(
            Question.id,
            Question.question_number,
            Question.topic_tag,
            Question.question_text,
            Question.options_json,  # 💡 ดึงตัวเลือกข้อสอบไปด้วย
            Question.correct_answer
        )
        .filter(Question.quiz_id == quiz_id)
        .order_by(Question.question_number.asc())
        .all()
    )

    question_analysis_list = []
    for q in questions_data:
        total_resp = db.query(func.count(StudentResponse.id)).filter(StudentResponse.question_id == q.id).scalar() or 1
        correct_resp = db.query(func.count(StudentResponse.id)).filter(
            StudentResponse.question_id == q.id, 
            StudentResponse.is_correct == True
        ).scalar() or 0
        
        correct_percentage = round((correct_resp / total_resp) * 100, 2)
        
        most_common_wrong = (
            db.query(StudentResponse.selected_answer)
            .filter(StudentResponse.question_id == q.id, StudentResponse.is_correct == False)
            .group_by(StudentResponse.selected_answer)
            .order_by(func.count(StudentResponse.selected_answer).desc())
            .first()
        )
        wrong_answer_key = most_common_wrong[0] if most_common_wrong else "None"

        # แปลงข้อความตัวเลือก (ถ้าเก็บเป็น string JSON) กลับเป็น python object
        options = q.options_json
        if isinstance(options, str):
            try:
                options = json.loads(options)
            except:
                pass

        question_analysis_list.append({
            "question_number": q.question_number,
            "topic_tag": q.topic_tag,
            "question_text": q.question_text,
            "options": options,       # 💡 เพิ่มให้ AI เห็นคำตอบลวงอื่นๆ
            "correct_answer": q.correct_answer,
            "correct_percentage": correct_percentage,
            "most_common_wrong_answer": wrong_answer_key
        })

    # --- 3. 🧩 ดึงตารางคำตอบแบบละเอียดของนักศึกษาแต่ละคน (Student Response Matrix) ---
    responses = (
        db.query(
            StudentResponse.student_id,
            Question.question_number,
            Question.topic_tag,
            StudentResponse.selected_answer,
            StudentResponse.is_correct
        )
        .join(Question, StudentResponse.question_id == Question.id)
        .filter(StudentResponse.quiz_id == quiz_id)
        .all()
    )

    student_matrix = {}
    for r in responses:
        if r.student_id not in student_matrix:
            student_matrix[r.student_id] = {
                "student_id": r.student_id,
                "responses": []
            }
        student_matrix[r.student_id]["responses"].append({
            "question_number": r.question_number,
            "topic_tag": r.topic_tag,
            "submitted_answer": r.selected_answer,
            "is_correct": r.is_correct
        })

    # --- 4. ประกอบร่างแพคเกจข้อมูลดิบยักษ์ใหญ่ส่งให้ AI ---
    aggregated_package = {
        "quiz_id": quiz_id,
        "class_summary": {
            "total_students_submitted": class_stats.total_students,
            "average_score": round(float(class_stats.average_score), 2) if class_stats.average_score else 0,
            "max_score": class_stats.max_score or 0,
            "min_score": class_stats.min_score or 0
        },
        "test_suite": question_analysis_list,  # ชุดข้อสอบพร้อมเฉลยและสถิติรายข้อ
        "student_responses_matrix": list(student_matrix.values())  # ตารางคำตอบนศ. รายคน
    }
    
    return aggregated_package

def get_detailed_quiz_response_matrix(db: Session, quiz_id: int):
    # ดึงข้อมูลการตอบกลับของนักเรียนทั้งหมดในควิซนี้
    responses = db.query(StudentResponse).filter(StudentResponse.quiz_id == quiz_id).all()
    
    # หรือดึงข้อมูลแบบ Join เพื่อเอาโจทย์ไปด้วย
    # (ขึ้นอยู่กับว่า AI ของนายต้องการโครงสร้างข้อมูลแบบไหน)
    return responses


def save_ai_analysis_report(db: Session, quiz_id: int, jamai_data: dict) -> AIAnalysisReport:
    """
    ฟังก์ชันสำหรับรับ Data JSON ที่ได้มาจาก JamAI แล้วแตกแยกฟิลด์ลงตารางใหม่
    jamai_data คาดหวัง Format: 
    {
       "overall_summary": "...", 
       "critical_review": "...", 
       "mastery_achieved": "..."
    }
    """
    # ตรวจสอบก่อนว่าเคยมีผลวิเคราะห์ของควิซนี้บันทึกอยู่แล้วหรือไม่
    db_report = db.query(AIAnalysisReport).filter(AIAnalysisReport.quiz_id == quiz_id).first()
    
    if db_report:
        # ถ้ามีอยู่แล้วให้ทำการอัปเดตข้อมูล (Update)
        db_report.overall_summary = jamai_data.get("overall_summary", db_report.overall_summary)
        db_report.critical_review = jamai_data.get("critical_review", db_report.critical_review)
        db_report.mastery_achieved = jamai_data.get("mastery_achieved", db_report.mastery_achieved)
    else:
        # ถ้ายังไม่มีให้สร้างแถวข้อมูลใหม่ (Insert)
        db_report = AIAnalysisReport(
            quiz_id=quiz_id,
            overall_summary=jamai_data.get("overall_summary", ""),
            critical_review=jamai_data.get("critical_review", ""),
            mastery_achieved=jamai_data.get("mastery_achieved", "")
        )
        db.add(db_report)
        
    db.commit()
    db.refresh(db_report)
    return db_report


def save_analysis_result(db: Session, quiz_id: int, analysis_text_or_data) -> AIAnalysisReport:
    """
    Compatibility shim for older analytics workflows that pass plain text analysis.
    If a dict is provided, it is stored as a full AI analysis report.
    """
    if isinstance(analysis_text_or_data, dict):
        return save_ai_analysis_report(db, quiz_id, analysis_text_or_data)

    return save_ai_analysis_report(db, quiz_id, {
        "overall_summary": analysis_text_or_data,
        "critical_review": "",
        "mastery_achieved": ""
    })


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


# ==========================================
# 📖 SECTION 3: Read helpers for the API layer
# ==========================================

def get_lecture_by_id(db: Session, lecture_id: int) -> Lecture | None:
    return db.query(Lecture).filter(Lecture.id == lecture_id).first()

def get_quiz_by_id(db: Session, quiz_id: int) -> Quiz | None:
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()

def get_quiz_by_code(db: Session, quiz_code: str) -> Quiz | None:
    return db.query(Quiz).filter(Quiz.quiz_code == quiz_code).first()

def get_questions_by_quiz(db: Session, quiz_id: int) -> list[Question]:
    return (
        db.query(Question)
        .filter(Question.quiz_id == quiz_id)
        .order_by(Question.question_number.asc())
        .all()
    )

def get_question_by_id(db: Session, question_id: int) -> Question | None:
    return db.query(Question).filter(Question.id == question_id).first()

def get_analysis_result(db: Session, quiz_id: int) -> AIAnalysisReport | None:
    return db.query(AIAnalysisReport).filter(AIAnalysisReport.quiz_id == quiz_id).first()