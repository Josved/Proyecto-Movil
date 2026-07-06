from pydantic import BaseModel


class DetallePedidoBase(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
    subtotal: float


class DetallePedidoCreate(DetallePedidoBase):
    pass


class DetallePedidoResponse(DetallePedidoBase):
    id: int

    class Config:
        from_attributes = True