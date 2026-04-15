from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.user import User  # noqa: F401, E402
from app.models.trip import Trip  # noqa: F401, E402
from app.models.temperature import Temperature  # noqa: F401, E402
from app.models.alert import Alert  # noqa: F401, E402