from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.MicroEntidades import Acuatica, Electronica, Mecanica, Fisica

db = SessionLocal()


def crear_acuatica(
    id_atraccion: UUID, profundidad: float, capacidad: int, propulsion: str
) -> Acuatica:
    Acuatica = Acuatica(
        id_atraccion=id_atraccion,
        profundidad=profundidad,
        capacidad=capacidad,
        propulsion=propulsion.strip(),
    )
    db.add(Acuatica)
    db.commit()
    db.refresh(Acuatica)
    return Acuatica


def obtener_acuatica_por_id(id_acuatica: UUID) -> Optional[Acuatica]:
    return db.query(Acuatica).filter(Acuatica.id_acuatica == id_acuatica).first()


def obtener_todas_acuaticas() -> List[Acuatica]:
    return db.query(Acuatica).all()


def actualizar_acuatica(id_acuatica: UUID, **kwargs) -> Optional[Acuatica]:
    acuatica = obtener_acuatica_por_id(id_acuatica)
    if not acuatica:
        return None
    for key, value in kwargs.items():
        if hasattr(acuatica, key):
            setattr(acuatica, key, value)
    db.commit()
    db.refresh(acuatica)
    return acuatica


def eliminar_acuatica(id_acuatica: UUID) -> bool:
    acuatica = obtener_acuatica_por_id(id_acuatica)
    if not acuatica:
        return False
    db.delete(acuatica)
    db.commit()
    return True


def crear_electronica(
    id_atraccion: UUID, experiencia: str, equipamiento: Optional[str] = None
) -> Electronica:
    electronica = Electronica(
        id_atraccion=id_atraccion,
        experiencia=experiencia.strip(),
        equipamiento=equipamiento.strip() if equipamiento else None,
    )
    db.add(electronica)
    db.commit()
    db.refresh(electronica)
    return electronica


def obtener_electronica_por_id(id_electronica: UUID) -> Optional[Electronica]:
    return (
        db.query(Electronica)
        .filter(Electronica.id_electronica == id_electronica)
        .first()
    )


def obtener_todas_electronicas() -> List[Electronica]:
    return db.query(Electronica).all()


def actualizar_electronica(id_electronica: UUID, **kwargs) -> Optional[Electronica]:
    electronica = obtener_electronica_por_id(id_electronica)
    if not electronica:
        return None
    for key, value in kwargs.items():
        if hasattr(electronica, key):
            setattr(electronica, key, value)
    db.commit()
    db.refresh(electronica)
    return electronica


def eliminar_electronica(id_electronica: UUID) -> bool:
    electronica = obtener_electronica_por_id(id_electronica)
    if not electronica:
        return False
    db.delete(electronica)
    db.commit()
    return True


def crear_mecanica(id_atraccion: UUID) -> Mecanica:
    mecanica = Mecanica(id_atraccion=id_atraccion)
    db.add(mecanica)
    db.commit()
    db.refresh(mecanica)
    return mecanica


def obtener_mecanica_por_id(id_mecanica: UUID) -> Optional[Mecanica]:
    return db.query(Mecanica).filter(Mecanica.id_mecanica == id_mecanica).first()


def obtener_todas_mecanicas() -> List[Mecanica]:
    return db.query(Mecanica).all()


def eliminar_mecanica(id_mecanica: UUID) -> bool:
    mecanica = obtener_mecanica_por_id(id_mecanica)
    if not mecanica:
        return False
    db.delete(mecanica)
    db.commit()
    return True


def crear_fisica(id_atraccion: UUID) -> Fisica:
    fisica = Fisica(id_atraccion=id_atraccion)
    db.add(fisica)
    db.commit()
    db.refresh(fisica)
    return fisica


def obtener_fisica_por_id(id_fisica: UUID) -> Optional[Fisica]:
    return db.query(Fisica).filter(Fisica.id_fisica == id_fisica).first()


def obtener_todas_fisicas() -> List[Fisica]:
    return db.query(Fisica).all()


def eliminar_fisica(id_fisica: UUID) -> bool:
    fisica = obtener_fisica_por_id(id_fisica)
    if not fisica:
        return False
    db.delete(fisica)
    db.commit()
    return True
