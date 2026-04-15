from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.temperature import Temperature
from app.models.trip import Trip
from app.models.user import User
from app.schemas.temperature import TemperatureRead

router = APIRouter(prefix="/temperatures", tags=["Temperatures"])


def validate_trip_access(trip_id: int, current_user: User, db: Session):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to view this trip")


@router.get("/{trip_id}", response_model=List[TemperatureRead])
def get_temperatures(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_trip_access(trip_id, current_user, db)

    temps = (
        db.query(Temperature)
        .filter(Temperature.trip_id == trip_id)
        .order_by(Temperature.timestamp.asc())
        .all()
    )

    return temps


@router.get("/{trip_id}/latest", response_model=TemperatureRead)
def get_latest_temperature(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_trip_access(trip_id, current_user, db)

    temp = (
        db.query(Temperature)
        .filter(Temperature.trip_id == trip_id)
        .order_by(Temperature.timestamp.desc())
        .first()
    )

    if not temp:
        raise HTTPException(status_code=404, detail="No temperatures found for this trip")

    return temp