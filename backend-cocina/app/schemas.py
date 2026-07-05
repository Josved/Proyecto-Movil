from datetime import datetime
from pydantic import BaseModel

class ProductoOut(BaseModel):
    nombre: str
    cantidad: int
    observaciones: str | None = None

class PedidoResumenOut(BaseModel):
    id_pedido: int
    mesa: int
    mesero: str
    estado: str
    fecha: datetime
    total_productos: int

class PedidoDetalleOut(BaseModel):
    id_pedido: int
    mesa: int
    mesero: str
    estado: str
    fecha: datetime
    productos: list[ProductoOut]

class CambioEstadoOut(BaseModel):
    mensaje: str
    id_pedido: int
    estado: str