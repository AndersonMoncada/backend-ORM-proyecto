import uuid

from database.config import Base
from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Categoria(Base):

    __Tablename = "Categorias"

    id_categoria = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True
    )
    nombre = Column(String(100), nullable=False, unique=True)
    descripcion = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())
    fecha_edicion = Column(DateTime(timezone=True), onupdate=func.now())

    id_usuario_crea = Column(
        UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=False
    )
    id_usuario_edita = Column(
        UUID(as_uuid=True), ForeignKey("tbl_usuarios.id"), nullable=True
    )

    productos = relationship("Producto", back_populates="categoria")

    def __repr__(self):
        return f"<Categoria(id_categoria={self.id_categoria}, nombre='{self.nombre}')>"
