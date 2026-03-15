import uuid
from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base


class Titular(Base):
    """Persona responsable del grupo de visitantes. Incluye trazabilidad completa."""

    __tablename__ = "titular"

    id_titular = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único del titular."""

    nombre = Column(String(150), nullable=False)
    """Nombre completo del titular."""

    cedula = Column(String(20), nullable=False, unique=True)
    """Cédula de identidad, debe ser única."""

    telefono = Column(String(20), nullable=True)
    """Teléfono de contacto, opcional."""

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    """Fecha en que se creó el registro."""

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    """Fecha de la última modificación."""

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    """ID del usuario que creó el registro."""

    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    """ID del usuario que realizó la última edición."""

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    visitantes = relationship("Visitante", back_populates="titular")
