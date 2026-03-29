from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict

import src.crud.AccedeCrud as crud_accede

router = APIRouter(prefix="/accede", tags=["accede"])

class AccedeCreate(BaseModel):
    id_entrada: UUID
    id_atraccion: UUID

class AccedeRead(BaseModel):
     model_config = ConfigDict(from_attributes=True)
     id_entrada: UUID
     id_atraccion: UUID

@router.get("/entrada/{id_entrada}", response_model=List[AccedeRead])
def obtener_por_entrada(id_entrada: UUID) -> List[AccedeRead]:
    c = crud_accede.obtener_por_entrada(id_entrada)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrada no encontrada")
    return c

@router.get("/atraccion/{id_atraccion}", response_model=List[AccedeRead])
def obtener_por_atraccion(id_atraccion: UUID) -> List[AccedeRead]:
    c =crud_accede.obtener_por_atraccion(id_atraccion)
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Atraccion no encontrada")
    return c

@router.post("", response_model=AccedeRead, status_code=status.HTTP_201_CREATED)
def crear_accede(body: AccedeCreate) -> AccedeRead:
    try:
        c = crud_accede.crear(
            id_entrada=body.id_entrada,
            id_atraccion=body.id_atraccion
        )
        return c
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id_entrada}/{id_atraccion}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_accede(id_entrada: UUID, id_atraccion: UUID) -> None:
    """Elimina la relación entre una entrada y una atracción."""
    if not crud_accede.eliminar(id_entrada, id_atraccion):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="no existe"
        )