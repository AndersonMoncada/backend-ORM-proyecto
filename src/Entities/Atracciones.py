import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Atraccion(Base):
    """Atracción base del parque."""

    __tablename__ = "atraccion"

    id_atraccion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(150), nullable=False)
    edad_minima = Column(Integer, nullable=False)
    estatura_minima = Column(Float, nullable=False)
    id_sede = Column(UUID(as_uuid=True), ForeignKey("sede.id_sede"), nullable=False)

    sede = relationship("Sede", back_populates="atracciones")
    acuatica = relationship("Acuatica", back_populates="atraccion", uselist=False)
    electronica = relationship("Electronica", back_populates="atraccion", uselist=False)
    mecanica = relationship("Mecanica", back_populates="atraccion", uselist=False)
    fisica = relationship("Fisica", back_populates="atraccion", uselist=False)
