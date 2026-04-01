from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    trip_id = Column(Integer, ForeignKey("trips.id"))