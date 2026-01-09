from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, nullable=False)
    service = Column(String, nullable=False)
    reservation_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
