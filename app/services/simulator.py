import random
import time
from datetime import datetime
from app.db.session import SessionLocal
from app.models.temperature import Temperature

def generate_temperature(trip_id: int):
    db = SessionLocal()
    while True:
        temp = round(random.uniform(2.0, 8.0), 2)
        new_temp = Temperature(value=temp, trip_id=trip_id, timestamp=datetime.utcnow())
        db.add(new_temp)
        db.commit()
        print(f"Generated temp: {temp}")
        time.sleep(5)