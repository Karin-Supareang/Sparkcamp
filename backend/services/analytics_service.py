import os
import json
import httpx
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) if obj % 1 else int(obj)
        return super(DecimalEncoder, self).default(obj)

class AnalyticsService:
    def __init__(self, quiz_repo, analysis_repo):
        self.quiz_repo = quiz_repo
        self.analysis_repo = analysis_repo
        self.api_key = os.getenv("JAMAI_API_KEY")
        self.project_id = os.getenv("JAMAI_PROJECT_ID")
        self.table_id = "Input"  # ชื่อ Table ID บนหน้าเว็บ JamAI

    def run_quiz_analytics_workflow(self, quiz_id: int):
        # 1. ดึงก้อนข้อมูลสถิตินักเรียนจาก Adapter
        quiz_metrics = self.quiz_repo.get_detailed_quiz_response_matrix(quiz_id)
        input_context_string = json.dumps(quiz_metrics, cls=DecimalEncoder, ensure_ascii=False)

        # 2. ยิงเชื่อมต่อไปยัง JamAI API พิกัดใหม่ของแท้
        url = "https://api.jamaibase.com/api/v1/gen_tables/action/rows/add"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "X-Project-ID": self.project_id,
            "Content-Type": "application/json"
        }
        
        payload = {
            "table_id": self.table_id,
            "data": [{"AnalysisAgent": input_context_string}], # ใช้ชื่อคอลัมน์รับข้อมูลบนเว็บ
            "stream": False
        }

        with httpx.Client(timeout=60.0, follow_redirects=True) as client:
            response = client.post(url, headers=headers, json=payload)
            if response.status_code not in [200, 201]:
                raise Exception(f"JamAI API Error ({response.status_code}): {response.text}")
            
            result_json = response.json()
            rows_data = result_json.get("rows", result_json.get("value", []))
            if not rows_data:
                raise Exception("JamAI did not return row data.")
            
            generated_columns = rows_data[0].get("columns", rows_data[0])

            # ฟังก์ชันแกะโครงสร้างลึกของคอลัมน์ เอาเฉพาะเนื้อหา text ข้างใน
            def extract_clean_text(column_key):
                column_obj = generated_columns.get(column_key, {})
                if isinstance(column_obj, str):
                    try: column_obj = json.loads(column_obj)
                    except: return column_obj
                if isinstance(column_obj, dict):
                    choices = column_obj.get("choices", [])
                    if choices and isinstance(choices, list):
                        msg = choices[0].get("message", {})
                        if "content" in msg: return msg["content"]
                    if "value" in column_obj:
                        val = column_obj["value"]
                        if isinstance(val, dict) and "choices" in val:
                            choices = val.get("choices", [])
                            if choices: return choices[0].get("message", {}).get("content", str(val))
                        return str(val)
                return str(column_obj) if column_obj is not None else ""

            # 3. จัดกลุ่มข้อมูล 3 กล่องส่งไปเซฟ
            # (มั่นใจว่าคีย์ "SumAgent", "critical_review", "mastery_achieved" ตรงกับคอลัมน์บนเว็บ)
            jamai_extracted_data = {
                "overall_summary": extract_clean_text("SumAgent"),
                "critical_review": extract_clean_text("critical_review"),
                "mastery_achieved": extract_clean_text("mastery_achieved")
            }

            # 4. ส่งกลับให้ Adapter ไปบันทึกลงตาราง ai_analysis_reports ของ MySQL
            return self.analysis_repo.save_analysis_result(quiz_id, jamai_extracted_data)