from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    nombre: str
    correo: EmailStr
    rol_id: int


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdate(UsuarioBase):
    pass


class UsuarioLogin(BaseModel):
    correo: EmailStr
    password: str


class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True