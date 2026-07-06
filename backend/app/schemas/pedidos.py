from pydantic import BaseModel
from datetime import datetime


class PedidoBase(BaseModel):
    mesa_id: int
    mesero_id: int
    estado: str


class PedidoCreate(PedidoBase):
    pass


class PedidoResponse(PedidoBase):
    id: int
    fecha: datetime

    class Config:
        from_attributes = True