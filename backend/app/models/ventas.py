from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    pago_id = Column(Integer, ForeignKey("pagos.id"), unique=True)
    folio = Column(String(40), unique=True)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    pago = relationship("Pago", back_populates="venta")