import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base


class Sede(Base):
    __tablename__ = "sede"
    id_sede = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(30), nullable=False, unique=True)
    ubicacion = Column(String(100), nullable=False)

    id_atraccion = Column(UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False)
    atraccion=relationship("Atraccion")