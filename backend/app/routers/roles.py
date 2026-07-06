from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.roles import RolCreate, RolResponse
from app.services.roles import (
    obtener_roles,
    obtener_rol,
    crear_rol,
    actualizar_rol,
    eliminar_rol,
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.get("/", response_model=list[RolResponse])
def listar_roles(db: Session = Depends(get_db)):
    return obtener_roles(db)


@router.get("/{rol_id}", response_model=RolResponse)
def obtener_un_rol(rol_id: int, db: Session = Depends(get_db)):
    return obtener_rol(db, rol_id)


@router.post("/", response_model=RolResponse)
def crear_nuevo_rol(rol: RolCreate, db: Session = Depends(get_db)):
    return crear_rol(db, rol)


@router.put("/{rol_id}", response_model=RolResponse)
def editar_rol(rol_id: int, datos: RolCreate, db: Session = Depends(get_db)):
    return actualizar_rol(db, rol_id, datos)


@router.delete("/{rol_id}")
def borrar_rol(rol_id: int, db: Session = Depends(get_db)):
    return eliminar_rol(db, rol_id)