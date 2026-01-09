from sqlalchemy.orm import Session
from . import models, schemas


def get_reservations(db: Session):
    return db.query(models.Reservation).all()


def create_reservation(db: Session, reservation: schemas.ReservationCreate):
    existing = db.query(models.Reservation).filter(
        models.Reservation.reservation_date == reservation.reservation_date
    ).first()

    if existing:
        return None

    new_reservation = models.Reservation(**reservation.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation
