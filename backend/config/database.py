from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import settings

# สร้าง Engine สำหรับต่อ DB
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

# สร้าง Session สำหรับให้คลาสอื่นเรียกไป Query/Insert
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Class สำหรับคลาสใน models.py เอาไปสืบทอด
Base = declarative_base()

# ฟังก์ชันสารพัดประโยชน์สำหรับเรียกใช้เปิด-ปิด Session ใน API หรือ Service
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()