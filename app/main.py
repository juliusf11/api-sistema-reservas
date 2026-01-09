from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Sistema de Reservas")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "API de reservas funcionando"}


@app.get(
    "/reservations",
    response_model=list[schemas.Reservation],
    status_code=status.HTTP_200_OK
)
def read_reservations(db: Session = Depends(get_db)):
    return crud.get_reservations(db)


@app.post(
    "/reservations",
    response_model=schemas.Reservation,
    status_code=status.HTTP_201_CREATED
)
def create_reservation(
    reservation: schemas.ReservationCreate,
    db: Session = Depends(get_db)
):
    result = crud.create_reservation(db, reservation)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe una reserva en ese horario"
        )

    return result
