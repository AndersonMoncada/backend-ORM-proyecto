from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Sede import Sede

db = SessionLocal()


def crear(nombre: str, ubicacion: str) -> Sede:
    sede = Sede(nombre=nombre.strip(), ubicacion=ubicacion.strip())
    db.add(sede)
    db.commit()
    db.refresh(sede)
    return sede


def obtener_por_id(id_sede: UUID) -> Optional[Sede]:
    return db.query(Sede).filter(Sede.id_sede == id_sede).first()


def obtener_todos() -> List[Sede]:
    return db.query(Sede).all()


def actualizar(id_sede: UUID, **kwargs) -> Optional[Sede]:
    sede = obtener_por_id(id_sede)
    if not sede:
        return None
    for key, value in kwargs.items():
        if hasattr(sede, key):
            setattr(sede, key, value)
    db.commit()
    db.refresh(sede)
    return sede


def eliminar(id_sede: UUID) -> bool:
    sede = obtener_por_id(id_sede)
    if not sede:
        return False
    db.delete(sede)
    db.commit()
    return True
