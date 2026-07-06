from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.detalle_pedido import (
    DetallePedidoCreate,
    DetallePedidoResponse,
)
from app.services.detalle_pedido import (
    obtener_detalles,
    obtener_detalle,
    crear_detalle,
    actualizar_detalle,
    eliminar_detalle,
)

router = APIRouter(
    prefix="/detalle-pedido",
    tags=["Detalle Pedido"]
)


@router.get("/", response_model=list[DetallePedidoResponse])
def listar_detalles(db: Session = Depends(get_db)):
    return obtener_detalles(db)


@router.get("/{detalle_id}", response_model=DetallePedidoResponse)
def obtener_un_detalle(detalle_id: int, db: Session = Depends(get_db)):
    return obtener_detalle(db, detalle_id)


@router.post("/", response_model=DetallePedidoResponse)
def crear_nuevo_detalle(
    detalle: DetallePedidoCreate,
    db: Session = Depends(get_db)
):
    return crear_detalle(db, detalle)


@router.put("/{detalle_id}", response_model=DetallePedidoResponse)
def editar_detalle(
    detalle_id: int,
    datos: DetallePedidoCreate,
    db: Session = Depends(get_db)
):
    return actualizar_detalle(db, detalle_id, datos)


@router.delete("/{detalle_id}")
def borrar_detalle(detalle_id: int, db: Session = Depends(get_db)):
    return eliminar_detalle(db, detalle_id)