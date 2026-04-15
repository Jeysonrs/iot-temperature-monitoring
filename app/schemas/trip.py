from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TripCreate(BaseModel):
    product_type: str


class TripStartResponse(BaseModel):
    message: str
    trip_id: int
    user_id: int
    product_type: str
    min_temp: float
    max_temp: float


class TripEndResponse(BaseModel):
    message: str
    trip_id: int
    active: bool
    end_time: Optional[datetime] = None


class TripStatusResponse(BaseModel):
    id: int
    user_id: int
    product_type: str
    min_temp: float
    max_temp: float
    active: bool
    start_time: datetime
    end_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)