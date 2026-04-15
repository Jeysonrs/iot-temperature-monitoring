from datetime import datetime
from pydantic import BaseModel, ConfigDict

class AlertRead(BaseModel):
    id: int
    trip_id: int
    temperature_value: float
    min_temp: float
    max_temp: float
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)