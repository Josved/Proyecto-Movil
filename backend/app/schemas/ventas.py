from pydantic import BaseModel
from datetime import datetime


class VentaBase(BaseModel):
    pago_id: int
    folio: str


class VentaCreate(VentaBase):
    pass


class VentaResponse(VentaBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True