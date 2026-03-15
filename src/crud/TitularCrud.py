from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Titular import Titular

db = SessionLocal()


def crear(
    nombre: str, cedula: str, id_usuario_creacion: UUID, telefono: str = None
) -> Optional[Titular]:
    """Crea un nuevo titular. Lanza error si la cédula ya existe."""
    cedula_existente = db.query(Titular).filter(Titular.cedula == cedula).first()
    if cedula_existente:
        raise ValueError("La cédula ya existe")
    titular = Titular(
        nombre=nombre.strip(),
        cedula=cedula,
        telefono=telefono,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(titular)
    db.commit()
    db.refresh(titular)
    return titular


def obtener_por_id(id_titular: UUID) -> Optional[Titular]:
    """Busca un titular por su ID. Retorna None si no existe."""
    return db.query(Titular).filter(Titular.id_titular == id_titular).first()


def obtener_todos() -> List[Titular]:
    """Retorna todos los titulares registrados."""
    return db.query(Titular).all()


def actualizar(
    id_titular: UUID, id_usuario_edita: UUID, **kwargs: dict
) -> Optional[Titular]:
    """Actualiza los campos indicados de un titular. Retorna None si no existe."""
    titular = obtener_por_id(id_titular)
    if not titular:
        return None
    for key, value in kwargs.items():
        setattr(titular, key, value)
    titular.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(titular)
    return titular


def eliminar(id_titular: UUID) -> bool:
    """Elimina un titular por su ID. Retorna True si se eliminó correctamente."""
    titular = obtener_por_id(id_titular)
    if not titular:
        return False
    db.delete(titular)
    db.commit()
    return True
