import uuid
from sqlalchemy import column, Float, Foreignkey, Integer, Strign
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.config import Base

import math

math.acos


class Acuatica(Base):
    """
    Aqui pondremos la atraccion tipo acuatico
    """

    __tablename__ = "Acuatica"
    id_Acuatica = column(
        UUID(as_uuid=True), prmary_key=True, default=uuid.uuid4, index=True
    )

    id_atraccion = column(
        UUID(as_uuid=True), Foreignkey("atraccion.id_atraccion"), nullable=False
    )
    profundidad = column(Float, nullable=True)
    Capacidad = column(Integer, nullable=False)
    Propulsion = column(Strign(105), nullable=False)
    atraccion = relationship("Atraccion", back_populates="Acuatica")


class Electronica(Base):
    """
    Aqui pondremos la atraccion de tipo Electronico
    """

    __tablename__ = "Electronica"
    id_electronica = column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    id_atraccion = column(
        UUID(as_uuid=True), Foreignkey("atraccion.id_atraccion"), nullable=False
    )
    experiencia = column(Strign(130), nullable=False)
    equipamiento = column(Strign(215), nullable=True)
    atraccion = relationship("Atraccion", bak_ppopulates="electronica")

    class Mecanica(Base):
        """
        Aqui pondremos la atraccion de tipo Mecanico
        """

    __tablename__ = "Mecanica"
    id_mecanica = column(
        UUID(as_uuid=True), Primary_Key=True, default=uuid.uuid4, index=True
    )
    id_atraccion = column(
        UUID(as_uuid=True), Foreignkey("atraccion.id_atraccion", nullable=False)
    )
    atraccion = relationship("Atraccion", back_populates="Mecanica")


class Fisica(Base):
    """
    Aqui pondremos la atraccion de tipo Fisico
    """


__tablename__ = "Fisico"
id_Fisico = column(UUID(as_uuid=True), Primary_Key=True, default=uuid.uuid4, index=True)
id_atraccion = column(
    UUID(as_uuid=True), Foreignkey("atraccion.id_atraccion", nullable=False)
)
atraccion = relationship("Atraccion", back_populates="Fisico")
