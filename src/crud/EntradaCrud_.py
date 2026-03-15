from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Entrada import Entrada
db = SessionLocal()

def crear(
        codigo: str, precio: float, reingreso: bool, id_titular: UUID
)-> Entrada:
    nombre_entrada = (
        db.query(Entrada).filter(Entrada.codigo==codigo).first()
    )
    if nombre_entrada:
        raise ValueError("La entrada ya existe")
    entrada=Entrada(
        codigo=codigo.strip(),
        precio=precio,
        reingreso=reingreso,
        id_titular=id_titular
    )
    db.add(entrada)
    db.commit()
    db.refresh(entrada)
    return entrada

def obtener_por_id(id_entrada:UUID) -> Optional[Entrada]:
    return db.query(Entrada).filter(Entrada.id_entrada==id_entrada).first()

def obtener_todos() -> List[Entrada]:
    return db.query(Entrada).all()

def actualizar(
        id_entrada:UUID, **kwargs:dict
) ->Optional[Entrada]:
    entrada= obtener_por_id(id_entrada)
    if not entrada:
        return None
    for key, value in kwargs.items():
        setattr(entrada, key, value)
    db.commit()
    db.refresh(entrada)
    return entrada
def eliminar(
        id_entrada:UUID
) -> bool:
    entrada=obtener_por_id(id_entrada)
    if not entrada:
        return False
    db.delete(entrada)
    db.commit()
    return True