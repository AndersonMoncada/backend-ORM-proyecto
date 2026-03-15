import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Sede(Base):
    """Sede del parque de atracciones. Contiene múltiples atracciones."""

    __tablename__ = "sede"

    id_sede = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    """Identificador único de la sede."""

    nombre = Column(String(30), nullable=False, unique=True)
    """Nombre de la sede, debe ser único."""

    ubicacion = Column(String(100), nullable=False)
    """Ubicación o dirección de la sede."""

    atracciones = relationship("Atraccion", back_populates="sede")
    """Lista de atracciones que pertenecen a esta sede."""
