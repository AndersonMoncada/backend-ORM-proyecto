import uuid
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base


class Acuatica(Base):
    """Atracción de tipo acuático. Extiende la atracción base con datos del agua."""

    __tablename__ = "acuatica"

    id_acuatica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único de la atracción acuática."""

    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )
    """ID de la atracción base a la que pertenece."""

    profundidad = Column(Float, nullable=True)
    """Profundidad del agua en metros."""

    capacidad = Column(Integer, nullable=False)
    """Número máximo de personas simultáneas."""

    propulsion = Column(String(105), nullable=False)
    """Tipo de propulsión: corriente natural, motor eléctrico, etc."""

    atraccion = relationship("Atraccion", back_populates="acuatica")
    """Atracción base asociada."""


class Electronica(Base):
    """Atracción de tipo electrónico. Extiende la atracción base con datos del juego."""

    __tablename__ = "electronica"

    id_electronica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único de la atracción electrónica."""

    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )
    """ID de la atracción base a la que pertenece."""

    experiencia = Column(String(130), nullable=False)
    """Tipo de experiencia: VR, Arcade, Shooter FPS, etc."""

    equipamiento = Column(String(215), nullable=True)
    """Equipamiento necesario para la atracción, opcional."""

    atraccion = relationship("Atraccion", back_populates="electronica")
    """Atracción base asociada."""


class Mecanica(Base):
    """Atracción de tipo mecánico. Extiende la atracción base."""

    __tablename__ = "mecanica"

    id_mecanica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único de la atracción mecánica."""

    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )
    """ID de la atracción base a la que pertenece."""

    atraccion = relationship("Atraccion", back_populates="mecanica")
    """Atracción base asociada."""


class Fisica(Base):
    """Atracción de tipo físico. Extiende la atracción base."""

    __tablename__ = "fisica"

    id_fisica = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    """Identificador único de la atracción física."""

    id_atraccion = Column(
        UUID(as_uuid=True), ForeignKey("atraccion.id_atraccion"), nullable=False
    )
    """ID de la atracción base a la que pertenece."""

    atraccion = relationship("Atraccion", back_populates="fisica")
    """Atracción base asociada."""
