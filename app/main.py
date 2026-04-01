from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api.routes.trips import router as trips_router
from app.api.routes.temperature import router as temp_router



app = FastAPI(title="IoT Temperature Monitoring API")
app.include_router(trips_router)
app.include_router(temp_router)

# Crear tablas apenas levanta
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "IoT Monitoring API running"}