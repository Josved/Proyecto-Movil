from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.pagos import Pago
from app.models.pedidos import Pedido
from app.models.ventas import Venta
from app.schemas.pagos import PagoCreate


def obtener_pagos(db: Session):
    return db.query(Pago).all()


def obtener_pago(db: Session, pago_id: int):
    pago = db.query(Pago).filter(
        Pago.id == pago_id
    ).first()

    if not pago:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    return pago


def crear_pago(db: Session, pago: PagoCreate):

    pedido = db.query(Pedido).filter(
        Pedido.id == pago.pedido_id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    existe = db.query(Pago).filter(
        Pago.pedido_id == pago.pedido_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ese pedido ya tiene un pago registrado"
        )

    # Crear pago
    nuevo_pago = Pago(
        pedido_id=pago.pedido_id,
        metodo_pago=pago.metodo_pago,
        total=pago.total
    )

    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)

    # Crear venta automáticamente
    try:
        nueva_venta = Venta(
            pago_id=nuevo_pago.id,
            folio=f"V-{nuevo_pago.id}"
        )

        db.add(nueva_venta)
        db.commit()
        db.refresh(nueva_venta)

        print("VENTA CREADA:", nueva_venta.id)

    except Exception as e:
        db.rollback()
        print("ERROR AL CREAR VENTA:", e)

    return nuevo_pago


def actualizar_pago(
    db: Session,
    pago_id: int,
    datos: PagoCreate
):

    pago = obtener_pago(db, pago_id)

    pedido = db.query(Pedido).filter(
        Pedido.id == datos.pedido_id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    pago.pedido_id = datos.pedido_id
    pago.metodo_pago = datos.metodo_pago
    pago.total = datos.total

    db.commit()
    db.refresh(pago)

    return pago


def eliminar_pago(db: Session, pago_id: int):

    pago = obtener_pago(db, pago_id)

    db.delete(pago)
    db.commit()

    return {
        "message": "Pago eliminado correctamente"
    }