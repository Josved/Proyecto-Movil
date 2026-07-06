from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.ventas import (
    VentaCreate,
    VentaResponse,
)
from app.services.ventas import (
    obtener_ventas,
    obtener_venta,
    crear_venta,
    actualizar_venta,
    eliminar_venta,
)

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"]
)


@router.get("/", response_model=list[VentaResponse])
def listar_ventas(db: Session = Depends(get_db)):
    return obtener_ventas(db)


@router.get("/{venta_id}", response_model=VentaResponse)
def obtener_una_venta(venta_id: int, db: Session = Depends(get_db)):
    return obtener_venta(db, venta_id)


@router.post("/", response_model=VentaResponse)
def crear_nueva_venta(
    venta: VentaCreate,
    db: Session = Depends(get_db)
):
    return crear_venta(db, venta)


@router.put("/{venta_id}", response_model=VentaResponse)
def editar_venta(
    venta_id: int,
    datos: VentaCreate,
    db: Session = Depends(get_db)
):
    return actualizar_venta(db, venta_id, datos)


@router.delete("/{venta_id}")
def borrar_venta(venta_id: int, db: Session = Depends(get_db)):
    return eliminar_venta(db, venta_id)