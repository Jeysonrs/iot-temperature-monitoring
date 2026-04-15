import random
import time
from datetime import datetime
from sqlalchemy import text

from app.db.session import SessionLocal
from app.models.temperature import Temperature
from app.models.alert import Alert


def get_trip_data(db, trip_id: int):
    result = db.execute(
        text("""
            SELECT active, min_temp, max_temp, product_type
            FROM trips
            WHERE id = :trip_id
        """),
        {"trip_id": trip_id},
    ).mappings().first()

    return result


def generate_temperature_value(min_temp: float, max_temp: float) -> float:
    # 80% dentro del rango, 20% fuera del rango para simular alertas reales
    if random.random() < 0.8:
        return round(random.uniform(min_temp, max_temp), 2)

    deviation = random.uniform(0.5, 4.0)

    if random.choice([True, False]):
        return round(max_temp + deviation, 2)
    return round(min_temp - deviation, 2)


def build_alert_message(product_type: str, temperature_value: float, min_temp: float, max_temp: float) -> str:
    if temperature_value > max_temp:
        return (
            f"High temperature alert for {product_type}: "
            f"{temperature_value}°C exceeds maximum allowed {max_temp}°C"
        )

    return (
        f"Low temperature alert for {product_type}: "
        f"{temperature_value}°C is below minimum allowed {min_temp}°C"
    )


def generate_temperature(trip_id: int) -> None:
    while True:
        db = SessionLocal()
        try:
            trip_data = get_trip_data(db, trip_id)

            if not trip_data:
                print(f"Trip {trip_id} not found. Stopping simulator.")
                break

            if not trip_data["active"]:
                print(f"Trip {trip_id} finished. Stopping simulator.")
                break

            min_temp = float(trip_data["min_temp"])
            max_temp = float(trip_data["max_temp"])
            product_type = trip_data["product_type"]

            temp = generate_temperature_value(min_temp, max_temp)

            new_temp = Temperature(
                value=temp,
                trip_id=trip_id,
                timestamp=datetime.utcnow(),
            )
            db.add(new_temp)

            if temp < min_temp or temp > max_temp:
                alert = Alert(
                    trip_id=trip_id,
                    temperature_value=temp,
                    min_temp=min_temp,
                    max_temp=max_temp,
                    message=build_alert_message(product_type, temp, min_temp, max_temp),
                    created_at=datetime.utcnow(),
                )
                db.add(alert)

            db.commit()

            print(f"Generated temp for trip {trip_id}: {temp}")

        except Exception as e:
            db.rollback()
            print(f"Simulator error for trip {trip_id}: {e}")
        finally:
            db.close()

        time.sleep(5)