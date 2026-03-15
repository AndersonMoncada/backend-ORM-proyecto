import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Acuatica(Base):
    """Atracción de tipo acuático."""

    __tablename__ = "acuatica"

    id_acuatica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )
    profundidad = Column(Float, nullable=True)
    capacidad = Column(Integer, nullable=False)
    propulsion = Column(String(105), nullable=False)

    atraccion = relationship("Atraccion", back_populates="acuatica")


class Electronica(Base):
    """Atracción de tipo electrónico."""

    __tablename__ = "electronica"

    id_electronica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )
    experiencia = Column(String(130), nullable=False)
    equipamiento = Column(String(215), nullable=True)

    atraccion = relationship("Atraccion", back_populates="electronica")


class Mecanica(Base):
    """Atracción de tipo mecánico."""

    __tablename__ = "mecanica"

    id_mecanica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )

    atraccion = relationship("Atraccion", back_populates="mecanica")


class Fisica(Base):
    """Atracción de tipo físico."""

    __tablename__ = "fisica"

    id_fisica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )

    atraccion = relationship("Atraccion", back_populates="fisica")
