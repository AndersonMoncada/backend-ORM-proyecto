from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Atracciones import Atraccion

db = SessionLocal()


def crear(
    nombre: str, edad_minima: int, estatura_minima: float, id_sede: UUID
) -> Atraccion:
    """Crea una nueva atracción asociada a una sede."""
    atraccion = Atraccion(
        nombre=nombre.strip(),
        edad_minima=edad_minima,
        estatura_minima=estatura_minima,
        id_sede=id_sede,
    )
    db.add(atraccion)
    db.commit()
    db.refresh(atraccion)
    return atraccion


def obtener_por_id(id_atraccion: UUID) -> Optional[Atraccion]:
    """Busca una atracción por su ID. Retorna None si no existe."""
    return db.query(Atraccion).filter(Atraccion.id_atraccion == id_atraccion).first()


def obtener_todos() -> List[Atraccion]:
    """Retorna todas las atracciones registradas."""
    return db.query(Atraccion).all()


def obtener_por_sede(id_sede: UUID) -> List[Atraccion]:
    """Retorna todas las atracciones de una sede específica."""
    return db.query(Atraccion).filter(Atraccion.id_sede == id_sede).all()


def actualizar(id_atraccion: UUID, **kwargs) -> Optional[Atraccion]:
    """Actualiza los campos indicados de una atracción. Retorna None si no existe."""
    atraccion = obtener_por_id(id_atraccion)
    if not atraccion:
        return None
    for key, value in kwargs.items():
        if hasattr(atraccion, key):
            setattr(atraccion, key, value)
    db.commit()
    db.refresh(atraccion)
    return atraccion


def eliminar(id_atraccion: UUID) -> bool:
    """Elimina una atracción por su ID. Retorna True si se eliminó correctamente."""
    atraccion = obtener_por_id(id_atraccion)
    if not atraccion:
        return False
    db.delete(atraccion)
    db.commit()
    return True
