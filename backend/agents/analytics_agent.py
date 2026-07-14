import os
# 1. เปลี่ยนไปใช้ MultiRowAddRequest ตามที่ตัวเตือนแนะนำ เพื่อไม่ให้เจอ FutureWarning
from jamaibase import JamAI, types as t 
from dotenv import load_dotenv

load_dotenv()

class AnalyticsAgent:
    def __init__(self):
        api_key = os.getenv("JAMAI_API_KEY")
        project_id = os.getenv("JAMAI_PROJECT_ID")
        
        if not api_key or not project_id:
            raise ValueError("❌ กรุณาตั้งค่า JAMAI_API_KEY และ JAMAI_PROJECT_ID ใน .env ก่อนรัน!")
            
        self.client = JamAI(token=api_key, project_id=project_id)

    def generate_analysis(self, raw_stats_json: str) -> str:
        """
        ส่งข้อมูล JSON เข้า Action Table ใน JamAI และดึงผลลัพธ์กลับมา
        """
        try:
            # 2. เปลี่ยนเป็น MultiRowAddRequest เพื่อลบ Warning กวนใจ
            response = self.client.table.add_table_rows(
                "action",
                t.MultiRowAddRequest(
                    table_id="Input",
                    data=[
                        {"AnalysisAgent": raw_stats_json}
                    ],
                    stream=False
                )
            )
            
            # 3. แกะคำตอบจากคอลัมน์ 'SumAgent' (แก้ไขจุดที่เกิด Error)
            if response.rows:
                result_row = response.rows[0]
                analysis_cell = result_row.columns.get("SumAgent")
                
                if analysis_cell:
                    # 💡 คีย์หลัก: ถ้าคำตอบมาจากคอลัมน์ LLM ตัว JamAI จะคืนค่าเป็น ChatCompletionResponse Object
                    # เราต้องดึงผ่านโครงสร้างเดี่ยวกับ OpenAI คือ .choices[0].message.content
                    if hasattr(analysis_cell, 'choices') and analysis_cell.choices:
                        return analysis_cell.choices[0].message.content
                    
                    # กันเหนียว: เผื่อบางเวอร์ชันคืนกลับมาเป็น text ตรงๆ หรือเป็น value
                    if hasattr(analysis_cell, 'value'):
                        return analysis_cell.value
                    
                    return str(analysis_cell)
            
            raise Exception("ไม่ได้รับผลลัพธ์การวิเคราะห์กลับมาจาก JamAI")
            
        except Exception as e:
            print(f"❌ Error ใน AnalyticsAgent: {e}")
            raise e