from pydantic import BaseModel
from datetime import datetime


class ReservationCreate(BaseModel):
    client_name: str
    service: str
    reservation_date: datetime


class Reservation(BaseModel):
    id: int
    client_name: str
    service: str
    reservation_date: datetime

    class Config:
        orm_mode = True
