import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base


class Visitante(Base):
    """Integrante del grupo registrado por un titular. Incluye trazabilidad completa."""

    __tablename__ = "visitante"

    id_visitante = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único del visitante."""

    nombre_visitante = Column(String(150), nullable=False)
    """Nombre completo del visitante."""

    edad = Column(Integer, nullable=False)
    """Edad del visitante en años."""

    estatura = Column(Float, nullable=False)
    """Estatura del visitante en metros."""

    id_titular = Column(
        UUID(as_uuid=True), ForeignKey("titular.id_titular"), nullable=False
    )
    """ID del titular responsable de este visitante."""

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

    titular = relationship("Titular", back_populates="visitantes")
    """Titular responsable del visitante."""

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    """Usuario que creó el registro."""

    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    """Usuario que realizó la última edición."""
