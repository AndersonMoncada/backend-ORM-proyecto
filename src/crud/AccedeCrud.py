from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Accede import Accede

db = SessionLocal()


def crear(id_entrada: UUID, id_atraccion: UUID) -> Accede:
    """Crea una relación entre una entrada y una atracción. Lanza error si ya existe."""
    accede = (
        db.query(Accede)
        .filter(Accede.id_entrada == id_entrada, Accede.id_atraccion == id_atraccion)
        .first()
    )
    if accede:
        raise ValueError("Ya existe")
    acceder = Accede(id_entrada=id_entrada, id_atraccion=id_atraccion)
    db.add(acceder)
    db.commit()
    db.refresh(acceder)
    return acceder


def obtener_por_entrada(id_entrada: UUID) -> List[Accede]:
    """Retorna todas las atracciones asociadas a una entrada."""
    return db.query(Accede).filter(Accede.id_entrada == id_entrada).all()


def obtener_por_atraccion(id_atraccion: UUID) -> List[Accede]:
    """Retorna todas las entradas asociadas a una atracción."""
    return db.query(Accede).filter(Accede.id_atraccion == id_atraccion).all()


def eliminar(id_entrada: UUID, id_atraccion: UUID) -> bool:
    """Elimina la relación entre una entrada y una atracción. Retorna True si se eliminó."""
    acceder = (
        db.query(Accede)
        .filter(Accede.id_entrada == id_entrada, Accede.id_atraccion == id_atraccion)
        .first()
    )
    if not acceder:
        return False
    db.delete(acceder)
    db.commit()
    return True
