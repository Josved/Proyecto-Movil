from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.usuarios import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
)
from app.services.usuarios import (
    obtener_usuarios,
    obtener_usuario,
    crear_usuario,
    actualizar_usuario,
    eliminar_usuario,
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.get("/", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return obtener_usuarios(db)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_un_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return obtener_usuario(db, usuario_id)


@router.post("/", response_model=UsuarioResponse)
def crear_nuevo_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    return crear_usuario(db, usuario)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def editar_usuario(
    usuario_id: int,
    datos: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    return actualizar_usuario(db, usuario_id, datos)


@router.delete("/{usuario_id}")
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    return eliminar_usuario(db, usuario_id)