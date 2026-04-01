import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

def wait_for_db():
    while True:
        try:
            engine = create_engine(DATABASE_URL)
            engine.connect()
            print("Database is ready!")
            return engine
        except Exception:
            print("Waiting for database...")
            time.sleep(2)

engine = wait_for_db()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)