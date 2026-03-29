from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from src.Api.deps import DbSession
import src.crud.TitularCrud as crud_titular

router = APIRouter(prefix="/titulares", tags=["Titulares"])


class TitularCreate(BaseModel):
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    id_usuario_creacion: UUID


class TitularUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    id_usuario_edita: UUID


class TitularRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_titular: UUID
    nombre: str
    cedula: str
    telefono: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[TitularRead])
def listar_titualres(db: DbSession) -> List[TitularRead]:
    """Retornara todos los titulares registrados."""
    return crud_titular.obtener_todos(db)


@router.get("/{id_titular}", response_model=TitularRead)
def obtener_titular(db: DbSession, id_titular: UUID) -> TitularRead:
    """Busca un titular por si ID"""
    t = crud_titular.obtener_por_id(db, id_titular)
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details="Titular No encontrado :("
        )
    return t


@router.post("", response_model=TitularRead, status_code=status.HTTP_201_CREATED)
def crear_titular(db: DbSession, body: TitularCreate) -> TitularRead:
    """Crea un nuevo titular"""
    try:
        return crud_titular.crear(
            db, body.nombre, body.cedula, body.id_usuario_creacion, body.telefono
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_titular}", response_model=TitularRead)
def actualizar_titular(
    db: DbSession, id_titular: UUID, body: TitularUpdate
) -> TitularRead:
    """Actualiza los datos de un titular."""
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    t = crud_titular.actualizar(db, id_titular, id_edita, **data)
    if not t:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Titular no encontrado X"
        )
    return t


@router.delete("/{id_titular}")
def eliminar_titular(id_titular: UUID, db: DbSession):
    """Elimina un titular por su ID."""
    if not crud_titular.eliminar(db, id_titular):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Titular no encontrado X"
        )
    return {"Message": "Titular eliminado correctamente!! :D"}
