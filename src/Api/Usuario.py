from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, ConfigDict
from src.Api.deps import DbSession
import src.crud.UsuarioCrud as crud_usuario

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


class UsuarioCreate(BaseModel):
    nombre_usuario: str
    contrasena: str
    rol: str = "usuario"


class UsuarioUpdate(BaseModel):
    nombre_usuario: Optional[str] = None
    contrasena: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_usuario: UUID
    nombre_usuario: str
    rol: str
    activo: bool
    fecha_creacion: Optional[datetime] = None
    fecha_edicion: Optional[datetime] = None


@router.get("", response_model=List[UsuarioRead])
def listar_usuarios(db: DbSession) -> List[UsuarioRead]:
    """
    Retorna todos los usuarios registrados

    """
    return crud_usuario.obtener_todos(db)


@router.get("/{id_usuario}", response_model=UsuarioRead)
def obtener_usuario(db: DbSession, id_usuario: UUID) -> UsuarioRead:
    """Busca un usuario por su ID."""
    u = crud_usuario.obtener_por_id(db, id_usuario)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return u


@router.post("", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(db: DbSession, body: UsuarioCreate) -> UsuarioRead:
    """Crea un nuevo usuario."""
    try:
        return crud_usuario.crear(db, body.nombre_usuario, body.contrasena, body.rol)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.put("/{id_usuario}", response_model=UsuarioRead)
def actualizar_usuario(
    db: DbSession, id_usuario: UUID, body: UsuarioUpdate
) -> UsuarioRead:
    """Actualiza los datos de un usuario."""
    data = body.model_dump(exclude_unset=True)
    u = crud_usuario.actualizar(db, id_usuario, **data)
    if not u:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado"
        )
    return u


@router.delete("/{id_usuario}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(db: DbSession, id_usuario: UUID) -> None:
    """Elimina un usuario por ID"""
    if not crud_usuario.eliminar(db, id_usuario):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuaro no encontrado"
        )
