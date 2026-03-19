import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Accede(Base):
    """Tabla intermedia que relaciona una Entrada con una Atracción."""

    __tablename__ = "accede"

    id_entrada = Column(
        UUID(as_uuid=True), ForeignKey("entrada.id_entrada"), primary_key=True
    )
    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), primary_key=True
    )

    entrada = relationship("Entrada")
    atraccion = relationship("Atraccion")
