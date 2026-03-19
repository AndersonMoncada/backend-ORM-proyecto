import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Atraccion(Base):
    """Atracción base del parque. Todas las subentidades se relacionan con esta tabla."""

    __tablename__ = "atraccion"

    id_atraccion = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único de la atracción."""

    nombre = Column(String(150), nullable=False)
    """Nombre de la atracción."""

    edad_minima = Column(Integer, nullable=False)
    """Edad mínima requerida para acceder a la atracción."""

    estatura_minima = Column(Float, nullable=False)
    """Estatura mínima en metros requerida para acceder a la atracción."""

    id_sede = Column(UUID(as_uuid=True), ForeignKey("sede.id_sede"), nullable=False)
    """ID de la sede a la que pertenece esta atracción."""

    sede = relationship("Sede", back_populates="atracciones")
    """Sede a la que pertenece la atracción."""

    acuatica = relationship("Acuatica", back_populates="atraccion", uselist=False)
    """Detalle acuático de la atracción, si aplica."""

    electronica = relationship("Electronica", back_populates="atraccion", uselist=False)
    """Detalle electrónico de la atracción, si aplica."""

    mecanica = relationship("Mecanica", back_populates="atraccion", uselist=False)
    """Detalle mecánico de la atracción, si aplica."""

    fisica = relationship("Fisica", back_populates="atraccion", uselist=False)
    """Detalle físico de la atracción, si aplica."""
