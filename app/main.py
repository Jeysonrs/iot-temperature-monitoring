from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base

from app.api.routes.auth import router as auth_router
from app.api.routes.trips import router as trips_router
from app.api.routes.temperature import router as temperature_router
from app.api.routes.alerts import router as alerts_router
from app.api.routes.reports import router as reports_router



app = FastAPI(
    title="IoT Cold-Chain Temperature Monitoring API",
    version="1.3.0",
    description="Trip-based monitoring system for refrigerated truck temperature simulation, alerts, users, and PDF reports.",

)

# Crear tablas apenas levanta
Base.metadata.create_all(bind=engine)

app.include_router(trips_router)
app.include_router(temperature_router)
app.include_router(alerts_router)
app.include_router(auth_router)
app.include_router(reports_router)

@app.get("/")
def root():
    return {"message": "IoT Monitoring API running"}