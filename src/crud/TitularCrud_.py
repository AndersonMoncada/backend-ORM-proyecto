from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.entities.titular import Titular
db = SessionLocal()

def crear(
        nombre: str,
        cedula: str,
        telefono: str,
        id_usuario_creacion: UUID
) -> Optional[Titular]:

    cedula_existente= db.query(Titular).filter(Titular.cedula == cedula).first()
    if cedula_existente:
        raise ValueError("La cédula ya existe")
    titular=Titular(
        nombre=nombre.strip(),
        cedula=cedula,
        telefono=telefono,
        id_usuario_creacion=id_usuario_creacion
    )
    db.add(titular)
    db.commit()
    db.refresh(titular)
    return titular

def obtener_por_id(id_titular: UUID) -> Optional[Titular]:
    return db.query(Titular).filter(Titular.id_titular==id_titular).first()

def obtener_todos() -> List[Titular]:
    return db.query(Titular).all()

def actualizar(id_titular: UUID, id_usuario_edita: UUID, **kwargs:dict) -> Optional[Titular]:
    titular=obtener_por_id(id_titular)
    if not titular:
        return None
    for key, value in kwargs.items():
        setattr(titular, key, value)
    titular.id_usuario_edita=id_usuario_edita
    db.commit()
    db.refresh(titular)

    return titular

def delete(id_titular: UUID) -> bool:
    titular=obtener_por_id(id_titular)
    if not titular:
        return False
    db.delete(titular)
    db.commit()
    return True

    