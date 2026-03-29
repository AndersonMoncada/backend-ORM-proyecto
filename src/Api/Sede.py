from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

import src.crud.SedeCrud as crud_sede

router = APIRouter(prefix="/sedes", tags=["sedes"])

class SedeCreate(BaseModel):
    nombre: str
    ubicacion: str

class SedeUpdate(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    
class SedeRead(BaseModel):
     model_config = ConfigDict(from_attributes=True)
     id_sede: UUID
     nombre: str
     ubicacion: str

@router.get("", response_model=List[SedeRead])
def listar_sedes() -> List[SedeRead]:
    return crud_sede.obtener_todos()

@router.get("/sede/{id_sede}", response_model=SedeRead)
def obtener_por_id(id_sede: UUID) -> SedeRead:
    s = crud_sede.obtener_por_id(id_sede)
    if not s:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return s


@router.post("", response_model=SedeRead, status_code=status.HTTP_201_CREATED)
def crear_sede(body:SedeCreate) -> SedeRead:
    c = crud_sede.crear(
        nombre=body.nombre,
        ubicacion=body.ubicacion
    )
    return c

@router.put("/{id_sede}", response_model=SedeRead)
def actualizar_Sede(id_sede: UUID, body: SedeUpdate) -> SedeRead:
    data = body.model_dump(exclude_unset=True)
    e = crud_sede.actualizar(id_sede, **data)
    if not e:
        raise HTTPException(status_code=404, detail="Sede no encontrada")
    return e

@router.delete("/{id_sede}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_sede(id_sede: UUID) -> None:
    if not crud_sede.eliminar(id_sede):
        raise HTTPException(status_code=404, detail="Sede no encontrada")