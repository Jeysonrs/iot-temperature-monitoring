import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL


def wait_for_db():
    while True:
        try:
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            with engine.connect():
                print("Database is ready!")
            return engine
        except Exception as e:
            print(f"Waiting for database... {e}")
            time.sleep(2)


engine = wait_for_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()