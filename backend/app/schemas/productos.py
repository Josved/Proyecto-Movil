from pydantic import BaseModel


class ProductoBase(BaseModel):
    nombre: str
    descripcion: str | None = None
    precio: float
    stock: int
    disponible: bool
    categoria_id: int


class ProductoCreate(ProductoBase):
    pass


class ProductoResponse(ProductoBase):
    id: int

    class Config:
        from_attributes = True