from sqlalchemy import Column, Integer, Boolean, DateTime
from datetime import datetime
from app.db.base import Base
from fastapi import APIRouter
from threading import Thread
from app.db.session import SessionLocal

from app.services.simulator import generate_temperature


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    active = Column(Boolean, default=True)
    start_time = Column(DateTime, default=datetime.utcnow)


router = APIRouter()

@router.post("/start-trip")
def start_trip():
    db = SessionLocal()
    trip = Trip(active=True)
    db.add(trip)
    db.commit()
    db.refresh(trip)

    thread = Thread(target=generate_temperature, args=(trip.id,))
    thread.start()

    return {"message": "Trip started", "trip_id": trip.id}