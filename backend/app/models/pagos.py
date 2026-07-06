from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), unique=True)
    metodo_pago = Column(String(30))
    total = Column(Numeric(10, 2))
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    pedido = relationship("Pedido", back_populates="pago")
    venta = relationship("Venta", back_populates="pago", uselist=False)