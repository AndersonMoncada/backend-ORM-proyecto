from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

import src.crud.EntradaCrud as crud_entrada

router = APIRouter(prefix="/entradas", tags=["entradas"])

class EntradaCreate(BaseModel):
    codigo: str
    precio: float
    fecha: Optional[datetime] = None
    id_titular: UUID
    id_usuario_creacion: UUID
    reingreso: bool = False

class EntradaUpdate(BaseModel):
    codigo: Optional[str] = None
    precio: Optional[float] = None
    reingreso: Optional[bool] = None

class EntradaRead(BaseModel):
     model_config = ConfigDict(from_attributes=True)
     id_entrada: UUID
     codigo: str
     precio: float
     fecha: datetime
     id_titular: UUID
     id_usuario_creacion: UUID

@router.get("", response_model=List[EntradaRead])
def listar_entradas() -> List[EntradaRead]:
    return crud_entrada.obtener_todos()

@router.get("/titular/{id_titular}", response_model=List[EntradaRead])
def obtener_por_titular(id_titular: UUID) -> List[EntradaRead]:
    return crud_entrada.obtener_por_titular(id_titular)

@router.get("/{id_entrada}", response_model=EntradaRead)
def obtener_entrada(id_entrada: UUID) -> EntradaRead:
    e = crud_entrada.obtener_por_id(id_entrada)
    if not e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrada no encontrada")
    return e

@router.post("", response_model=EntradaRead, status_code=status.HTTP_201_CREATED)
def crear_entrada(body:EntradaCreate) -> EntradaRead:
    c = crud_entrada.crear(
        codigo=body.codigo,
        precio=body.precio,
        fecha=body.fecha,
        id_titular=body.id_titular,
        id_usuario_creacion=body.id_usuario_creacion,
        reingreso=body.reingreso
    )
    return c

@router.put("/{id_entrada}", response_model=EntradaRead)
def actualizar_entrada(id_entrada: UUID, body: EntradaUpdate) -> EntradaRead:
    data = body.model_dump(exclude_unset=True)
    e = crud_entrada.actualizar(id_entrada, **data)
    if not e:
        raise HTTPException(status_code=404, detail="Entrada no encontrada")
    return e

@router.delete("/{id_entrada}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_entrada(id_entrada: UUID) -> None:
    if not crud_entrada.eliminar(id_entrada):
        raise HTTPException(status_code=404, detail="Entrada no encontrada")