from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Visitante import Visitante

db = SessionLocal()


def crear(
    nombre_visitante: str,
    edad: int,
    estatura: float,
    id_titular: UUID,
    id_usuario_creacion: UUID,
) -> Visitante:
    """Crea un nuevo visitante asociado a un titular."""
    visitante = Visitante(
        nombre_visitante=nombre_visitante.strip(),
        edad=edad,
        estatura=estatura,
        id_titular=id_titular,
        id_usuario_creacion=id_usuario_creacion,
    )
    db.add(visitante)
    db.commit()
    db.refresh(visitante)
    return visitante


def obtener_por_id(id_visitante: UUID) -> Optional[Visitante]:
    """Busca un visitante por su ID. Retorna None si no existe."""
    return db.query(Visitante).filter(Visitante.id_visitante == id_visitante).first()


def obtener_todos() -> List[Visitante]:
    """Retorna todos los visitantes registrados."""
    return db.query(Visitante).all()


def obtener_por_titular(id_titular: UUID) -> List[Visitante]:
    """Retorna todos los visitantes asociados a un titular."""
    return db.query(Visitante).filter(Visitante.id_titular == id_titular).all()


def actualizar(
    id_visitante: UUID, id_usuario_edita: UUID, **kwargs: dict
) -> Optional[Visitante]:
    """Actualiza los campos indicados de un visitante. Retorna None si no existe."""
    visitante = obtener_por_id(id_visitante)
    if not visitante:
        return None
    for key, value in kwargs.items():
        setattr(visitante, key, value)
    visitante.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(visitante)
    return visitante


def eliminar(id_visitante: UUID) -> bool:
    """Elimina un visitante por su ID. Retorna True si se eliminó correctamente."""
    visitante = obtener_por_id(id_visitante)
    if not visitante:
        return False
    db.delete(visitante)
    db.commit()
    return True
