from datetime import datetime
from threading import Thread
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.product_rules import PRODUCT_TEMPERATURE_RANGES, get_product_range
from app.db.session import get_db
from app.models.trip import Trip
from app.models.user import User
from app.schemas.trip import (
    TripCreate,
    TripStartResponse,
    TripEndResponse,
    TripStatusResponse,
)
from app.services.simulator import generate_temperature

router = APIRouter(prefix="/trips", tags=["Trips"])

@router.get("/products")
def get_supported_products():
    return PRODUCT_TEMPERATURE_RANGES


@router.post("/start", response_model=TripStartResponse)
def start_trip(
    payload: TripCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user),
    ):

    product_range = get_product_range(payload.product_type)

    if not product_range:
        raise HTTPException(
            status_code=400,
            detail="Unsupported product type. Use one of: vaccines, dairy, fresh_food, frozen_food",
        )

    trip = Trip(
        product_type=payload.product_type.lower(),
        min_temp=product_range["min_temp"],
        max_temp=product_range["max_temp"],
        active=True,
        user_id=current_user.id,
    )

    db.add(trip)
    db.commit()
    db.refresh(trip)

    thread = Thread(target=generate_temperature, args=(trip.id,), daemon=True)
    thread.start()

    return {
        "message": "Trip started successfully",
        "trip_id": trip.id,
        "user_id": trip.user_id,
        "product_type": trip.product_type,
        "min_temp": trip.min_temp,
        "max_temp": trip.max_temp,
    }


@router.post("/{trip_id}/end", response_model=TripEndResponse)
def end_trip(
    trip_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    if trip.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to end this trip")


    if not trip.active:
        return {
            "message": "Trip already ended",
            "trip_id": trip.id,
            "active": trip.active,
            "end_time": trip.end_time,
        }

    trip.active = False
    trip.end_time = datetime.utcnow()

    db.commit()
    db.refresh(trip)

    return {
        "message": "Trip ended successfully",
        "trip_id": trip.id,
        "active": trip.active,
        "end_time": trip.end_time,
    }


@router.get("/{trip_id}", response_model=TripStatusResponse)
def get_trip(
    trip_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    ):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    if trip.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to view this trip")


    return trip