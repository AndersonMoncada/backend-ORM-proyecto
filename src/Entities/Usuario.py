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
    nombre_usuario = Column(String(150), nullable=False, unique=True)
    contrasena = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False, default="usuario")
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
