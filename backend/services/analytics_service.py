import json
from agents.analytics_agent import AnalyticsAgent

class AnalyticsService:
    def __init__(self, quiz_repo, analysis_repo):
        self.quiz_repo = quiz_repo
        self.analysis_repo = analysis_repo
        self.agent = AnalyticsAgent()

    def run_quiz_analytics_workflow(self, quiz_id: int) -> dict:
        print(f"⏳ [Workflow] เริ่มดึงข้อมูล Detailed Matrix ของควิซ ID: {quiz_id}...")
        
        # 💡 เรียกใช้ฟังก์ชันตัวใหม่ที่เราจัดโครงสร้าง JSON ไว้สวยงาม
        raw_detailed_data = self.quiz_repo.get_detailed_quiz_response_matrix(quiz_id)
        
        if not raw_detailed_data:
            raise ValueError(f"ไม่พบข้อมูลสำหรับควิซ ID: {quiz_id}")
            
        # แปลงโครงสร้าง Matrix เป็น JSON string ส่งให้ AI 
        stats_json = json.dumps(raw_detailed_data, default=str, ensure_ascii=False)
        
        print("🤖 [Workflow] กำลังส่งข้อมูล Matrix ข้อสอบ + คำตอบนักศึกษา ไปให้ JamAI Base...")
        ai_response = self.agent.generate_analysis(stats_json)
        
        print("💾 [Workflow] บันทึกวิเคราะห์เสร็จสิ้น!")
        # (ฟังก์ชันเซฟผลลัพธ์ของนาย)
        self.analysis_repo.save_analysis_result(quiz_id=quiz_id, analysis_text=ai_response)
        
        return {
            "quiz_id": quiz_id,
            "status": "success",
            "analysis_result": ai_response
        }