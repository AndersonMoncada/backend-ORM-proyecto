from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from src.Api.deps import DbSession
from src.crud.MicroEntidadesCrud import (
    crear_acuatica,
    obtener_todas_acuaticas,
    obtener_acuatica_por_id,
    actualizar_acuatica,
    eliminar_acuatica,
    crear_electronica,
    obtener_todas_electronicas,
    obtener_electronica_por_id,
    actualizar_electronica,
    eliminar_electronica,
    crear_mecanica,
    obtener_todas_mecanicas,
    obtener_mecanica_por_id,
    eliminar_mecanica,
    crear_fisica,
    obtener_todas_fisicas,
    obtener_fisica_por_id,
    eliminar_fisica,
)

router_acuatica = APIRouter(prefix="/acuaticas", tags=["Acuaticas"])


class AcuaticaCreate(BaseModel):
    id_atraccion: UUID
    profundidad: float
    capacidad: int
    propulsion: str


class AcuaticaUpdate(BaseModel):
    profundidad: Optional[float] = None
    capacidad: Optional[int] = None
    propulsion: Optional[str] = None


class AcuaticaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_acuatica: UUID
    id_atraccion: UUID
    profundidad: Optional[float] = None
    capacidad: int
    propulsion: str


@router_acuatica.get("", response_model=List[AcuaticaRead])
def listar_acuaticas(db: DbSession):
    return obtener_todas_acuaticas(db)


@router_acuatica.get("/{id_acuatica}", response_model=AcuaticaRead)
def obtener_acuatica(db: DbSession, id_acuatica: UUID):
    a = obtener_acuatica_por_id(db, id_acuatica)
    if not a:
        raise HTTPException(status_code=404, detail="Acuática no encontrada")
    return a


@router_acuatica.post("", response_model=AcuaticaRead, status_code=201)
def crear_acuatica_endpoint(db: DbSession, body: AcuaticaCreate):
    return crear_acuatica(
        db, body.id_atraccion, body.profundidad, body.capacidad, body.propulsion
    )


@router_acuatica.put("/{id_acuatica}", response_model=AcuaticaRead)
def actualizar_acuatica_endpoint(
    db: DbSession, id_acuatica: UUID, body: AcuaticaUpdate
):
    a = actualizar_acuatica(db, id_acuatica, **body.model_dump(exclude_unset=True))
    if not a:
        raise HTTPException(status_code=404, detail="Acuática no encontrada")
    return a


@router_acuatica.delete("/{id_acuatica}")
def eliminar_acuatica_endpoint(db: DbSession, id_acuatica: UUID):
    if not eliminar_acuatica(db, id_acuatica):
        raise HTTPException(status_code=404, detail="Acuática no encontrada")

    return {"msg": "Acuática eliminada correctamente"}


router_electronica = APIRouter(prefix="/electronicas", tags=["Electrónicas"])


class ElectronicaCreate(BaseModel):
    id_atraccion: UUID
    experiencia: str
    equipamiento: Optional[str] = None


class ElectronicaUpdate(BaseModel):
    experiencia: Optional[str] = None
    equipamiento: Optional[str] = None


class ElectronicaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_electronica: UUID
    id_atraccion: UUID
    experiencia: str
    equipamiento: Optional[str] = None


@router_electronica.get("", response_model=List[ElectronicaRead])
def listar_electronicas(db: DbSession):
    return obtener_todas_electronicas(db)


@router_electronica.get("/{id_electronica}", response_model=ElectronicaRead)
def obtener_electronica(db: DbSession, id_electronica: UUID):
    e = obtener_electronica_por_id(db, id_electronica)
    if not e:
        raise HTTPException(status_code=404, detail="Electrónica no encontrada")
    return e


@router_electronica.post("", response_model=ElectronicaRead, status_code=201)
def crear_electronica_endpoint(db: DbSession, body: ElectronicaCreate):
    return crear_electronica(db, body.id_atraccion, body.experiencia, body.equipamiento)


@router_electronica.put("/{id_electronica}", response_model=ElectronicaRead)
def actualizar_electronica_endpoint(
    db: DbSession, id_electronica: UUID, body: ElectronicaUpdate
):
    e = actualizar_electronica(
        db, id_electronica, **body.model_dump(exclude_unset=True)
    )
    if not e:
        raise HTTPException(status_code=404, detail="Electrónica no encontrada")
    return e


@router_electronica.delete("/{id_electronica}", status_code=204)
def eliminar_electronica_endpoint(db: DbSession, id_electronica: UUID):
    if not eliminar_electronica(db, id_electronica):
        raise HTTPException(status_code=404, detail="Electrónica no encontrada")


router_mecanica = APIRouter(prefix="/mecanicas", tags=["Mecánicas"])


class MecanicaCreate(BaseModel):
    id_atraccion: UUID


class MecanicaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_mecanica: UUID
    id_atraccion: UUID


@router_mecanica.get("", response_model=List[MecanicaRead])
def listar_mecanicas(db: DbSession):
    return obtener_todas_mecanicas(db)


@router_mecanica.get("/{id_mecanica}", response_model=MecanicaRead)
def obtener_mecanica(db: DbSession, id_mecanica: UUID):
    m = obtener_mecanica_por_id(db, id_mecanica)
    if not m:
        raise HTTPException(status_code=404, detail="Mecánica no encontrada")
    return m


@router_mecanica.post("", response_model=MecanicaRead, status_code=201)
def crear_mecanica_endpoint(db: DbSession, body: MecanicaCreate):
    return crear_mecanica(db, body.id_atraccion)


@router_mecanica.delete("/{id_mecanica}", status_code=204)
def eliminar_mecanica_endpoint(db: DbSession, id_mecanica: UUID):
    if not eliminar_mecanica(db, id_mecanica):
        raise HTTPException(status_code=404, detail="Mecánica no encontrada")


router_fisica = APIRouter(prefix="/fisicas", tags=["Físicas"])


class FisicaCreate(BaseModel):
    id_atraccion: UUID


class FisicaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_fisica: UUID
    id_atraccion: UUID


@router_fisica.get("", response_model=List[FisicaRead])
def listar_fisicas(db: DbSession):
    return obtener_todas_fisicas(db)


@router_fisica.get("/{id_fisica}", response_model=FisicaRead)
def obtener_fisica(db: DbSession, id_fisica: UUID):
    f = obtener_fisica_por_id(db, id_fisica)
    if not f:
        raise HTTPException(status_code=404, detail="Física no encontrada")
    return f


@router_fisica.post("", response_model=FisicaRead, status_code=201)
def crear_fisica_endpoint(db: DbSession, body: FisicaCreate):
    return crear_fisica(db, body.id_atraccion)


@router_fisica.delete("/{id_fisica}", status_code=204)
def eliminar_fisica_endpoint(db: DbSession, id_fisica: UUID):
    if not eliminar_fisica(db, id_fisica):
        raise HTTPException(status_code=404, detail="Física no encontrada")
