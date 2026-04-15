import io

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.alert import Alert
from app.models.temperature import Temperature
from app.models.trip import Trip
from app.models.user import User
from app.services.report_service import generate_trip_report_pdf

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/{trip_id}/pdf")
def download_trip_report(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    if trip.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not allowed to view this trip report")

    if trip.active:
        raise HTTPException(
            status_code=400,
            detail="Trip must be ended before generating the report",
        )

    temperatures = (
        db.query(Temperature)
        .filter(Temperature.trip_id == trip_id)
        .order_by(Temperature.timestamp.asc())
        .all()
    )

    alerts = (
        db.query(Alert)
        .filter(Alert.trip_id == trip_id)
        .order_by(Alert.created_at.asc())
        .all()
    )

    pdf_bytes = generate_trip_report_pdf(trip, temperatures, alerts)

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="trip_{trip_id}_report.pdf"'
        },
    )