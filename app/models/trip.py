from sqlalchemy import Column, Integer, Boolean, DateTime, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from fastapi import APIRouter
from threading import Thread
from app.db.session import SessionLocal

from app.services.simulator import generate_temperature


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    product_type = Column(String, nullable=False)
    min_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    active = Column(Boolean, default=True, nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="trips")

    temperatures = relationship(
        "Temperature",
        back_populates="trip",
        cascade="all, delete-orphan",
    )

    alerts = relationship(
        "Alert",
        back_populates="trip",
        cascade="all, delete-orphan",
    )

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