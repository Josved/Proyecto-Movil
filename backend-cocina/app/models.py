from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    mesa = Column(Integer, nullable=False)
    mesero = Column(String, nullable=False)
    estado = Column(String, default="Pendiente")
    fecha = Column(DateTime, default=datetime.now)

    productos = relationship(
        "PedidoProducto",
        back_populates="pedido",
        cascade="all, delete-orphan"
    )

class PedidoProducto(Base):
    __tablename__ = "pedido_productos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    nombre = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    observaciones = Column(String, nullable=True)

    pedido = relationship("Pedido", back_populates="productos")