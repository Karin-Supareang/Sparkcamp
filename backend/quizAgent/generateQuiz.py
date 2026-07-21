import os
import json
import sys
from dotenv import load_dotenv
from pypdf import PdfReader
from jamaibase import JamAI

# โหลดค่าคอนฟิกจากไฟล์ .env
load_dotenv()

# สมมติการ Import ฟังก์ชันบันทึกข้อมูลจาก repository ของคุณ
# (ให้แก้ไข path นี้ให้ตรงกับโครงสร้างโปรเจกต์จริงของคุณ)
# from repositories.quiz_repository import insert_generated_questions

# จำลองฟังก์ชันบันทึกข้อมูลเพื่อไม่ให้โค้ดพังหากยังไม่มี repository จริง
def insert_generated_questions(data):
    # เปลี่ยนโค้ดตรงนี้เป็นการเรียกใช้ฐานข้อมูลจริงของคุณ
    print(f"[Repo] กำลังบันทึกชุดคำถามรหัส: {data.get('quiz_code')}")
    return {"status": "success", "inserted_count": len(data.get("questions", []))}

# สร้าง Instance ของ JamAI 
jamai = JamAI(
    api_key=os.getenv("JAMAI_API_KEY"),
    project_id=os.getenv("JAMAI_PROJECT_ID")
)

def extract_text_from_pdf(pdf_path: str) -> str:
    """ฟังก์ชันสำหรับอ่านและดึงข้อความทั้งหมดจากไฟล์ PDF"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text

def generate_quiz_with_jam_ai(context_text: str) -> dict:
    """ฟังก์ชันส่งข้อความไปประมวลผลกับ JamAI เพื่อสร้างข้อสอบแบบ JSON"""
    prompt = f"""คุณคือผู้เชี่ยวชาญด้านการสอบ จงสร้างข้อสอบปรนัยจำนวน 5 ข้อจากเนื้อหาต่อไปนี้
    
    เนื้อหา:
    {context_text}

    กรุณาส่งคืนผลลัพธ์เป็น JSON Object ในรูปแบบดังนี้เท่านั้น: {{
        "quiz_code": "QZ-101",
        "questions": [
            {{
                "question_number": 1,
                "question_text": "คำถามข้อที่ 1 คืออะไร?",
                "options_json": ["ตัวเลือก A", "ตัวเลือก B", "ตัวเลือก C", "ตัวเลือก D"],
                "correct_answer": "ตัวเลือก A",
                "topic_tag": "ชื่อหัวข้อเรื่อง"
            }}
        ]
    }}"""

    # เรียกใช้งาน Chat Completion ของ JamAI SDK
    response = jamai.chat.completions.create(
        model="meta/llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that strictly outputs JSON format."},
            {"role": "user", "content": prompt}
        ],
        # กำหนดรูปแบบการตอบกลับให้เป็น JSON Object (เหมือนใน Node.js)
        response_format={"type": "json_object"}
    )

    output_content = response.choices[0].message.content
    return json.loads(output_content)

def main():
    try:
        print("1. กำลังอ่านไฟล์ PDF...")
        pdf_text = extract_text_from_pdf("./document.pdf")

        print("2. กำลังส่งข้อมูลให้ JamAI ประมวลผล...")
        quiz_data = generate_quiz_with_jam_ai(pdf_text)

        print("3. ได้รับชุดข้อมูลคำถาม (Quiz Object) สำเร็จ:\n")
        print(json.dumps(quiz_data, indent=2, ensure_ascii=False))

        print("4. กำลังส่งข้อมูลไปยัง Repository เพื่อบันทึกลง Database...")
        lecture_id = 1

        result = insert_generated_questions({
            "quiz_code": quiz_data.get("quiz_code"),
            "lecture_id": lecture_id,
            "questions": quiz_data.get("questions")
        })

        print("✨ บันทึกข้อมูลควิซและคำถามลง Database สำเร็จเรียบร้อย!", result)
        return result
    except Exception as error:
        print(f"เกิดข้อผิดพลาดในการประมวลผล: {error}", file=sys.stderr)
        raise error

# ตรวจสอบการรันไฟล์โดยตรง (เหมือน `require.main === module` ใน Node.js)
if __name__ == "__main__":
    main()