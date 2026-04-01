from fastapi import APIRouter
from app.db.session import SessionLocal
from app.models.temperature import Temperature

router = APIRouter()

@router.get("/temperatures/{trip_id}")
def get_temperatures(trip_id: int):
    db = SessionLocal()
    temps = db.query(Temperature).filter(Temperature.trip_id == trip_id).all()

    return [
        {
            "value": t.value,
            "timestamp": t.timestamp
        }
        for t in temps
    ]