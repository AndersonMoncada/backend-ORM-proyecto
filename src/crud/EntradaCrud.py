from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Entrada import Entrada

db = SessionLocal()


def crear(codigo: str, precio: float, reingreso: bool, id_titular: UUID) -> Entrada:
    """Crea una nueva entrada. Lanza error si el código ya existe."""
    nombre_entrada = db.query(Entrada).filter(Entrada.codigo == codigo).first()
    if nombre_entrada:
        raise ValueError("La entrada ya existe")
    entrada = Entrada(
        codigo=codigo.strip(), precio=precio, reingreso=reingreso, id_titular=id_titular
    )
    db.add(entrada)
    db.commit()
    db.refresh(entrada)
    return entrada


def obtener_por_id(id_entrada: UUID) -> Optional[Entrada]:
    """Busca una entrada por su ID. Retorna None si no existe."""
    return db.query(Entrada).filter(Entrada.id_entrada == id_entrada).first()


def obtener_todos() -> List[Entrada]:
    """Retorna todas las entradas registradas."""
    return db.query(Entrada).all()


def actualizar(id_entrada: UUID, **kwargs: dict) -> Optional[Entrada]:
    """Actualiza los campos indicados de una entrada. Retorna None si no existe."""
    entrada = obtener_por_id(id_entrada)
    if not entrada:
        return None
    for key, value in kwargs.items():
        setattr(entrada, key, value)
    db.commit()
    db.refresh(entrada)
    return entrada


def eliminar(id_entrada: UUID) -> bool:
    """Elimina una entrada por su ID. Retorna True si se eliminó correctamente."""
    entrada = obtener_por_id(id_entrada)
    if not entrada:
        return False
    db.delete(entrada)
    db.commit()
    return True
