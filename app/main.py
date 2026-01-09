from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqladmin import Admin, ModelView

app = FastAPI(title="API Sistema de Reservas Mejorada")

# --- Base de datos SQLite (se guarda en un archivo y no se borra) ---
DATABASE_URL = "sqlite:///./reservas.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo de la tabla en la base de datos
class ReservaDB(Base):
    __tablename__ = "reservas"
    id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String, index=True)
    service = Column(String)
    reservation_date = Column(DateTime)

# Crea la tabla si no existe
Base.metadata.create_all(bind=engine)

# Modelo para recibir datos al crear reserva
class ReservaCreate(BaseModel):
    client_name: str
    service: str
    reservation_date: datetime

# Para inyectar la base de datos en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Panel de Administrador ---
class ReservaAdmin(ModelView, model=ReservaDB):
    column_list = [ReservaDB.id, ReservaDB.client_name, ReservaDB.service, ReservaDB.reservation_date]
    column_searchable_list = [ReservaDB.client_name]
    column_sortable_list = [ReservaDB.reservation_date]
    page_size = 50
    can_create = True
    can_edit = True
    can_delete = True

admin = Admin(app, engine)
admin.add_view(ReservaAdmin)

# --- Endpoints de la API ---
@app.get("/")
def root():
    return {"message": "API de reservas mejorada funcionando"}

@app.get("/reservations")
def read_reservations(db: Session = Depends(get_db)):
    return db.query(ReservaDB).all()

@app.post("/reservations")
def create_reservation(reserva: ReservaCreate, db: Session = Depends(get_db)):
    # Detectar conflicto: misma fecha y hora exacta
    conflicto = db.query(ReservaDB).filter(
        ReservaDB.reservation_date == reserva.reservation_date
    ).first()
    
    if conflicto:
        raise HTTPException(
            status_code=409,
            detail="¡Conflicto! Ya existe una reserva en esa fecha y hora."
        )
    
    nueva_reserva = ReservaDB(**reserva.dict())
    db.add(nueva_reserva)
    db.commit()
    db.refresh(nueva_reserva)
    return nueva_reserva