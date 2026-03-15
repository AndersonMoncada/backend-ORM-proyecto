import hashlib
from typing import List, Optional
from uuid import UUID
from src.database.config import SessionLocal
from src.Entities.Usuario import Usuario

db = SessionLocal()


def _hash_contrasena(contrasena: str) -> str:
    """Hashea la contraseña con SHA-256 para no guardarla en texto plano."""
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


def crear(nombre_usuario: str, contrasena: str, rol: str = "usuario") -> Usuario:
    """Crea un nuevo usuario. Lanza error si el nombre de usuario ya existe."""
    existente = (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip())
        .first()
    )
    if existente:
        raise ValueError("El nombre de usuario ya existe")
    usuario = Usuario(
        nombre_usuario=nombre_usuario.strip(),
        contrasena=_hash_contrasena(contrasena),
        rol=rol.strip(),
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def login(nombre_usuario: str, contrasena: str) -> Optional[Usuario]:
    """Verifica credenciales. Retorna el usuario si son correctas, None si no."""
    usuario = obtener_por_nombre(nombre_usuario)
    if not usuario or not usuario.activo:
        return None
    if usuario.contrasena != _hash_contrasena(contrasena):
        return None
    return usuario


def obtener_por_id(id_usuario: UUID) -> Optional[Usuario]:
    """Busca un usuario por su ID. Retorna None si no existe."""
    return db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()


def obtener_por_nombre(nombre_usuario: str) -> Optional[Usuario]:
    """Busca un usuario por su nombre. Retorna None si no existe."""
    return (
        db.query(Usuario)
        .filter(Usuario.nombre_usuario == nombre_usuario.strip())
        .first()
    )


def obtener_todos() -> List[Usuario]:
    """Retorna todos los usuarios registrados."""
    return db.query(Usuario).all()


def hay_usuarios() -> bool:
    """Indica si existe al menos un usuario en el sistema."""
    return db.query(Usuario).first() is not None


def actualizar(id_usuario: UUID, id_usuario_edita: UUID, **kwargs) -> Optional[Usuario]:
    """Actualiza los campos indicados de un usuario. Hashea la contraseña si se actualiza."""
    usuario = obtener_por_id(id_usuario)
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


def eliminar(id_usuario: UUID) -> bool:
    """Elimina un usuario por su ID. Retorna True si se eliminó correctamente."""
    usuario = obtener_por_id(id_usuario)
    if not usuario:
        return False
    db.delete(usuario)
    db.commit()
    return True
