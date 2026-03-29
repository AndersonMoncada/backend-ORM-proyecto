from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from src.Api.deps import DbSession
import src.crud.VisitanteCrud as crud_visitante

router = APIRouter(prefix="/visitantes", tags=["Visitantes"])


class VisitanteCreate(BaseModel):
    nombre_visitante: str
    edad: int
    estatura: float
    id_titular: UUID
    id_usuario_creacion: UUID


class VisitanteUpdate(BaseModel):
    nombre_visitante: Optional[str] = None
    edad: Optional[int] = None
    estatura: Optional[float] = None
    id_usuario_edita: UUID


class VisitanteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_visitante: UUID
    nombre_visitante: str
    edad: int
    estatura: float
    id_titular: UUID
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None
    id_usuario_creacion: UUID
    id_usuario_edita: Optional[UUID] = None


@router.get("", response_model=List[VisitanteRead])
def listar_visitantes(db: DbSession) -> List[VisitanteRead]:
    """Retorna todos los visitantes que se hayan registrados"""
    return crud_visitante.obtener_todos(db)


@router.get("/{id_visitante}", response_model=VisitanteRead)
def obtener_visitante(db: DbSession, id_visitante: UUID) -> VisitanteRead:
    """Busca un visitante por su ID."""
    v = crud_visitante.obtener_por_id(db, id_visitante)
    if not v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Visitante no encontrado"
        )
    return v


@router.get("/titular/{id_titular}", response_model=List[VisitanteRead])
def listar_por_titular(db: DbSession, id_titular: UUID) -> List[VisitanteRead]:
    """Retorna todos los visitantes de un titular."""
    return crud_visitante.obtener_por_titular(db, id_titular)


@router.post("", response_model=VisitanteRead, status_code=status.HTTP_201_CREATED)
def crear_visitante(db: DbSession, body: VisitanteCreate) -> VisitanteRead:
    """Crea un nuevo visitante."""
    return crud_visitante.crear(
        db,
        body.nombre_visitante,
        body.edad,
        body.estatura,
        body.id_titular,
        body.id_usuario_creacion,
    )


@router.put("/{id_visitante}", response_model=VisitanteRead)
def actualizar_visitante(
    db: DbSession, id_visitante: UUID, body: VisitanteUpdate
) -> VisitanteRead:
    """Actualiza los datos de un visitante."""
    id_edita = body.id_usuario_edita
    data = body.model_dump(exclude_unset=True, exclude={"id_usuario_edita"})
    v = crud_visitante.actualizar(db, id_visitante, id_edita, **data)
    if not v:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Visitante no encontrado"
        )
    return v


@router.delete("/{id_usuario}")
def eliminar_usuario(db: DbSession, id_usuario: UUID):
    if not crud_visitante.eliminar(db, id_usuario):
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"msg": "Usuario eliminado correctamente"}
