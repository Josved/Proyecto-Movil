from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.mesas import (
    MesaCreate,
    MesaResponse,
)
from app.services.mesas import (
    obtener_mesas,
    obtener_mesa,
    crear_mesa,
    actualizar_mesa,
    eliminar_mesa,
)

router = APIRouter(
    prefix="/mesas",
    tags=["Mesas"]
)


@router.get("/", response_model=list[MesaResponse])
def listar_mesas(db: Session = Depends(get_db)):
    return obtener_mesas(db)


@router.get("/{mesa_id}", response_model=MesaResponse)
def obtener_una_mesa(mesa_id: int, db: Session = Depends(get_db)):
    return obtener_mesa(db, mesa_id)


@router.post("/", response_model=MesaResponse)
def crear_nueva_mesa(
    mesa: MesaCreate,
    db: Session = Depends(get_db)
):
    return crear_mesa(db, mesa)


@router.put("/{mesa_id}", response_model=MesaResponse)
def editar_mesa(
    mesa_id: int,
    datos: MesaCreate,
    db: Session = Depends(get_db)
):
    return actualizar_mesa(db, mesa_id, datos)


@router.delete("/{mesa_id}")
def borrar_mesa(mesa_id: int, db: Session = Depends(get_db)):
    return eliminar_mesa(db, mesa_id)