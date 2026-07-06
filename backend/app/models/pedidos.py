from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"))
    mesero_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    estado = Column(String(30), default="Pendiente")

    mesa = relationship("Mesa")
    mesero = relationship("Usuario")
    detalles = relationship("DetallePedido", back_populates="pedido")
    pago = relationship("Pago", back_populates="pedido", uselist=False)