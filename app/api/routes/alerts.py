from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.alert import Alert
from app.models.trip import Trip
from app.models.user import User
from app.schemas.alert import AlertRead

router = APIRouter(prefix="/alerts", tags=["Alerts"])


def validate_trip_access(trip_id: int, current_user: User, db: Session):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    if trip.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to view this trip")


@router.get("/{trip_id}", response_model=List[AlertRead])
def get_alerts_by_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_trip_access(trip_id, current_user, db)

    alerts = (
        db.query(Alert)
        .filter(Alert.trip_id == trip_id)
        .order_by(Alert.created_at.desc())
        .all()
    )
    return alerts