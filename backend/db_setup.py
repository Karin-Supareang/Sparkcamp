from config.database import engine, Base
import database.models  # noqa: F401


def create_schema():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_schema()
    print("✅ Database schema created/updated successfully.")
