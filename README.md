# IoT Cold-Chain Temperature Monitoring API

Backend system for monitoring refrigerated truck temperature by trip, with user authentication, protected endpoints, automatic temperature simulation, alert generation, and trip-based storage.

## Features

- User registration and login with JWT authentication
- Protected endpoints by authenticated user
- Trip-based monitoring flow
- Background temperature simulation using threads
- Temperature history stored in PostgreSQL
- Automatic alerts when temperature goes out of allowed range
- Product-based temperature rules
- Dockerized setup with FastAPI + PostgreSQL

## Tech Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker / Docker Compose
- JWT Authentication
- Python Threads

## Supported Products

- `vaccines` → 2°C to 8°C
- `dairy` → 1°C to 4°C
- `fresh_food` → 0°C to 5°C
- `frozen_food` → -18°C to -15°C

## Project Structure

```bash
app/
 ├── api/
 │    ├── deps.py
 │    └── routes/
 │         ├── auth.py
 │         ├── trips.py
 │         ├── temperature.py
 │         └── alerts.py
 ├── core/
 │    ├── config.py
 │    ├── product_rules.py
 │    └── security.py
 ├── db/
 │    ├── base.py
 │    └── session.py
 ├── models/
 │    ├── user.py
 │    ├── trip.py
 │    ├── temperature.py
 │    └── alert.py
 ├── schemas/
 │    ├── user.py
 │    ├── trip.py
 │    ├── temperature.py
 │    └── alert.py
 ├── services/
 │    └── simulator.py
 └── main.py