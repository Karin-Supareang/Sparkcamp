import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@localhost:3306/quiz_agent_db")
    JAMAI_API_KEY: str = os.getenv("JAMAI_API_KEY", "")
    JAMAI_PROJECT_ID: str = os.getenv("JAMAI_PROJECT_ID", "")

settings = Settings()