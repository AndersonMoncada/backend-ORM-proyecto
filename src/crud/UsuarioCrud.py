import hashlib
from fastapi import HTTPException
from typing import List, Optional
from uuid import UUID
from src.Entities.Usuario import Usuario


def _hash_contrasena(contrasena: str) -> str:
    """Hashea la contraseña con SHA-256 para no guardarla en texto plano."""
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def crear(db, nombre_usuario: str, contrasena: str, rol: str = "usuario") -> Usuario:
    existente = (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip())
        .first()
    )

    if existente:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya existe")

    usuario = Usuario(
        nombre_usuario=nombre_usuario.strip(),
        contrasena=_hash_contrasena(contrasena),
        rol=rol.strip(),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def login(db, nombre_usuario: str, contrasena: str) -> Optional[Usuario]:

    usuario = obtener_por_nombre(db, nombre_usuario)

    if not usuario or not usuario.activo:
        return None
    if usuario.contrasena != _hash_contrasena(contrasena):
        return None

    return usuario


def obtener_por_id(db, id_usuario: UUID) -> Optional[Usuario]:
    """Busca un usuario por su ID. Retorna None si no existe."""
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_por_nombre(db, nombre_usuario: str) -> Optional[Usuario]:
    """Busca un usuario por su nombre. Retorna None si no existe."""
    return (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip())
        .first()
    )


def obtener_todos(db) -> List[Usuario]:
    """Retorna todos los usuarios registrados."""
    return db.query(Usuario).all()


def hay_usuarios(db) -> bool:
    """Indica si existe al menos un usuario en el sistema."""
    return db.query(Usuario).first() is not None


def actualizar(
    db, id_usuario: UUID, id_usuario_edita: UUID, **kwargs
) -> Optional[Usuario]:
    """Actualiza los campos indicados de un usuario. Hashea la contraseña si se actualiza."""
    usuario = obtener_por_id(db, id_usuario)
    if not usuario:
        return None
    if "contrasena" in kwargs:
        kwargs["contrasena"] = _hash_contrasena(kwargs["contrasena"])
    for key, value in kwargs.items():
        if hasattr(usuario, key):
            setattr(usuario, key, value)
    db.commit()
    db.refresh(usuario)
    return usuario


def eliminar(db, id_usuario: UUID) -> bool:
    """Elimina un usuario por su ID. Retorna True si se eliminó correctamente."""
    usuario = obtener_por_id(db, id_usuario)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True
