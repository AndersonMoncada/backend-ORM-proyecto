from typing import List, Optional
from uuid import UUID
from src.Entities.Titular import Titular


def crear(db, nombre, cedula, id_usuario_creacion, telefono=None):
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


def obtener_todos(db) -> List[Titular]:
    return db.query(Titular).all()


def obtener_por_id(db, id_titular: UUID) -> Optional[Titular]:
    return db.query(Titular).filter(Titular.id_titular == id_titular).first()


def actualizar(db, id_titular: UUID, id_usuario_edita: UUID, **kwargs):
    titular = obtener_por_id(db, id_titular)
    if not titular:
        return None

    for key, value in kwargs.items():
        setattr(titular, key, value)

    titular.id_usuario_edita = id_usuario_edita
    db.commit()
    db.refresh(titular)
    return titular


def eliminar(db, id_titular: UUID) -> bool:
    titular = obtener_por_id(db, id_titular)
    if not titular:
        return False

    db.delete(titular)
    db.commit()
    return True
