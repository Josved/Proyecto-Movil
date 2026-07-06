from pydantic import BaseModel


class MesaBase(BaseModel):
    numero: int
    capacidad: int
    estado: str


class MesaCreate(MesaBase):
    pass


class MesaResponse(MesaBase):
    id: int

    class Config:
        from_attributes = True