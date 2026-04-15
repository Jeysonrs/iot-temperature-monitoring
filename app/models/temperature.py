from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.base import Base

class Temperature(Base):
    __tablename__ = "temperatures"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)

    trip = relationship("Trip", back_populates="temperatures")