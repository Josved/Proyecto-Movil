from pydantic import BaseModel
from datetime import datetime


class PagoBase(BaseModel):
    pedido_id: int
    metodo_pago: str
    total: float


class PagoCreate(PagoBase):
    pass


class PagoResponse(PagoBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True