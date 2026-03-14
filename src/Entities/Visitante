import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base

class Visitante(Base):
    """Integrante del grupo registrado por un titular."""

    __tablename__ = "visitante"

    id_visitante = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre_visitante = Column(String(150), nullable=False)
    edad = Column(Integer, nullable=False)
    estatura = Column(Float, nullable=False)
    id_titular = Column(
        UUID(as_uuid=True), ForeignKey("titular.id_titular"), nullable=False
    )

    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())
    id_usuario_creacion = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("usuario.id_usuario"), nullable=True
    )

    titular = relationship("Titular", back_populates="visitantes")
    usuario_creacion = relationship("Usuario", foreign_keys=[id_usuario_creacion])
    usuario_edita = relationship("Usuario", foreign_keys=[id_usuario_edita])
