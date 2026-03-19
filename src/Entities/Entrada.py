import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base


class Entrada(Base):
    """Registro de compra de entrada al parque. Incluye trazabilidad completa."""

    __tablename__ = "entrada"

    id_entrada = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    """Identificador único de la entrada."""

    codigo = Column(String(20), nullable=False, unique=True)
    """Código único de la entrada."""

    precio = Column(Float, nullable=False)
    """Precio pagado por la entrada."""

    reingreso = Column(Boolean, nullable=False, default=False)
    """Indica si la entrada permite reingreso al parque."""

    fecha = Column(DateTime(timezone=True), server_default=func.now())
    """Fecha de compra de la entrada."""

    id_titular = Column(
        UUID(as_uuid=True), ForeignKey("titular.id_titular"), nullable=False
    )
    """ID del titular que compró la entrada."""

    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    """ID del usuario que creó el registro."""

    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )
    """ID del usuario que realizó la última edición."""

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    """Fecha en que se creó el registro."""

    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    """Fecha de la última modificación."""

    titular = relationship("Titular", foreign_keys=[id_titular])
    """Titular asociado a la entrada."""

    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    """Usuario que creó el registro."""

    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
    """Usuario que realizó la última edición."""
