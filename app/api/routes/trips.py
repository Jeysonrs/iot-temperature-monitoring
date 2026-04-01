from fastapi import APIRouter
from threading import Thread
from app.db.session import SessionLocal
from app.models.trip import Trip
from app.services.simulator import generate_temperature

router = APIRouter()

@router.post("/start-trip")
def start_trip():
    db = SessionLocal()
    trip = Trip(active=True)
    db.add(trip)
    db.commit()
    db.refresh(trip)

    # Arranca el simulador en un hilo
    thread = Thread(target=generate_temperature, args=(trip.id,))
    thread.start()

    return {"message": "Trip started", "trip_id": trip.id}