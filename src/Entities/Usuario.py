import uuid
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from src.database.config import Base


class Usuario(Base):
    """Usuario del sistema. Base de trazabilidad para las demás entidades."""

    __tablename__ = "usuario"

    id_usuario = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único del usuario."""

    nombre_usuario = Column(String(150), nullable=False, unique=True)
    """Nombre de usuario para iniciar sesión, debe ser único."""

    contrasena = Column(String(255), nullable=False)
    """Contraseña hasheada con SHA-256."""

    rol = Column(String(50), nullable=False, default="usuario")
    """Rol del usuario en el sistema: admin o usuario."""

    activo = Column(Boolean, default=True)
    """Indica si el usuario está activo en el sistema."""

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    """Fecha en que se creó el registro."""

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    """Fecha de la última modificación."""
