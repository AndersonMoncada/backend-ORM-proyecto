import uuid
from sqlalchemy import Column, DateTime, Float, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database.config import Base

class Entrada(Base):
    __tablename__="entrada"
    id_entrada=Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    codigo=Column(String(20), nullable=False, unique=True)
    precio=Column(Float, nullable=False)
    reingreso=Column(Boolean, nullable=False, default=False)
    fecha=Column(DateTime(timezone=True), server_default=func.now())

    id_titular = Column (
        UUID(as_uuid=True), ForeignKey("titular.id_titular"),nullable=False
    )
    titular=relationship("Titular")

    atracciones= relationship("Atraccion", secondary="accede", back_populates="entradas")