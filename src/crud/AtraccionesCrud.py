from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Atracciones import Atraccion

db = SessionLocal()


def crear(
    nombre: str, edad_minima: int, estatura_minima: float, id_sede: UUID
) -> Atraccion:
    Atraccion = Atraccion(
        nombre=nombre.strip(),
        edad_minima=edad_minima,
        estatura_minima=estatura_minima,
        id_sede=id_sede,
    )
    db.add(atraccion)
    db.commit()
    db.refresh(Atraccion)
    return Atraccion


def obtener_por_id(id_atraccion: UUID) -> Optional[Atraccion]:
    return db.query(Atraccion).filter(Atraccion.id_atraccion == id_atraccion).first()


def obtener_todos() -> List[Atraccion]:
    return db.query(Atraccion).all()


def obtener_por_sede(id_sede: UUID) -> List[Atraccion]:
    return db.query(Atraccion).filter(Atraccion.id_sede == id_sede).all()


def actualizar(id_atraccion: UUID, **kwargs) -> Optional[Atraccion]:

    Atraccion = obtener_por_id(id_atraccion)
    if not Atraccion:
        return None
    for key, value in kwargs.items():
        if hasattr(atraccion, key):
            setattr(Atraccion, key, value)
    db.commit
    db.refresh(Atraccion)
    return Atraccion


def eliminar(id_atraccion: UUID) -> bool:
    Atraccion = obtener_por_id(id_atraccion)
    if not Atraccion:
        return False
    db.delete(Atraccion)
    db.commit()
    return True
