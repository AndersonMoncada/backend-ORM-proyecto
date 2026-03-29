from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

import src.crud.AtraccionesCrud as crud_atraccion

router = APIRouter(prefix="/atracciones", tags=["atraccion"])

class AtraccionCreate(BaseModel):
    nombre: str
    edad_minima: int
    estatura_minima: float
    id_sede: UUID

class AtraccionUpdate(BaseModel):
    nombre: Optional[str] = None
    edad_minima: Optional[int] = None
    estatura_minima: Optional[float] = None

class AtraccionRead(BaseModel):
     model_config = ConfigDict(from_attributes=True)
     id_atraccion: UUID
     nombre: str
     edad_minima: int
     estatura_minima: float
     id_sede: UUID

@router.get("", response_model=List[AtraccionRead])
def listar_Atraccion() -> List[AtraccionRead]:
    return crud_atraccion.obtener_todos()

@router.get("/{id_atraccion}", response_model=AtraccionRead)
def obtener_por_id(id_atraccion: UUID) -> AtraccionRead:
    e = crud_atraccion.obtener_por_id(id_atraccion)
    if not e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atraccion no encontrada")
    return e

@router.get("/{id_sede}", response_model=List[AtraccionRead])
def obtener_por_sede(id_sede: UUID) -> AtraccionRead:
    e = crud_atraccion.obtener_por_sede(id_sede)
    if not e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sede no encontrada")
    return e

@router.post("", response_model=AtraccionRead, status_code=status.HTTP_201_CREATED)
def crear_Atraccion(body:AtraccionCreate) -> AtraccionRead:
    c = crud_atraccion.crear(
        nombre=body.nombre,
        edad_minima=body.edad_minima,
        estatura_minima=body.estatura_minima,
        id_sede=body.id_sede
    )
    return c

@router.put("/{id_atraccion}", response_model=AtraccionRead)
def actualizar_atraccion(id_atraccion: UUID, body: AtraccionUpdate) -> AtraccionRead:
    data = body.model_dump(exclude_unset=True)
    e = crud_atraccion.actualizar(id_atraccion, **data)
    if not e:
        raise HTTPException(status_code=404, detail="Atraccion no encontrada")
    return e

@router.delete("/{id_atraccion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_atraccion(id_atraccion: UUID) -> None:
    if not crud_atraccion.eliminar(id_atraccion):
        raise HTTPException(status_code=404, detail="Atraccion no encontrada")