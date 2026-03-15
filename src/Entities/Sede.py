import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Sede(Base):
    __tablename__ = "sede"

    id_sede = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(30), nullable=False, unique=True)
    ubicacion = Column(String(100), nullable=False)

    atracciones = relationship("Atraccion", back_populates="sede")
