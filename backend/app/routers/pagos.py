from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pagos import (
    PagoCreate,
    PagoResponse,
)
from app.services.pagos import (
    obtener_pagos,
    obtener_pago,
    crear_pago,
    actualizar_pago,
    eliminar_pago,
)

router = APIRouter(
    prefix="/pagos",
    tags=["Pagos"]
)


@router.get("/", response_model=list[PagoResponse])
def listar_pagos(db: Session = Depends(get_db)):
    return obtener_pagos(db)


@router.get("/{pago_id}", response_model=PagoResponse)
def obtener_un_pago(pago_id: int, db: Session = Depends(get_db)):
    return obtener_pago(db, pago_id)


@router.post("/", response_model=PagoResponse)
def crear_nuevo_pago(
    pago: PagoCreate,
    db: Session = Depends(get_db)
):
    return crear_pago(db, pago)


@router.put("/{pago_id}", response_model=PagoResponse)
def editar_pago(
    pago_id: int,
    datos: PagoCreate,
    db: Session = Depends(get_db)
):
    return actualizar_pago(db, pago_id, datos)


@router.delete("/{pago_id}")
def borrar_pago(pago_id: int, db: Session = Depends(get_db)):
    return eliminar_pago(db, pago_id)