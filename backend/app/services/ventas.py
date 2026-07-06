from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.ventas import Venta
from app.models.pagos import Pago
from app.schemas.ventas import VentaCreate


def obtener_ventas(db: Session):
    return db.query(Venta).all()


def obtener_venta(db: Session, venta_id: int):
    venta = db.query(Venta).filter(
        Venta.id == venta_id
    ).first()

    if not venta:
        raise HTTPException(
            status_code=404,
            detail="Venta no encontrada"
        )

    return venta


def crear_venta(db: Session, venta: VentaCreate):

    pago = db.query(Pago).filter(
        Pago.id == venta.pago_id
    ).first()

    if not pago:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    existe_pago = db.query(Venta).filter(
        Venta.pago_id == venta.pago_id
    ).first()

    if existe_pago:
        raise HTTPException(
            status_code=400,
            detail="Ese pago ya tiene una venta registrada"
        )

    existe_folio = db.query(Venta).filter(
        Venta.folio == venta.folio
    ).first()

    if existe_folio:
        raise HTTPException(
            status_code=400,
            detail="El folio ya existe"
        )

    nueva_venta = Venta(
        pago_id=venta.pago_id,
        folio=venta.folio
    )

    db.add(nueva_venta)
    db.commit()
    db.refresh(nueva_venta)

    return nueva_venta


def actualizar_venta(
    db: Session,
    venta_id: int,
    datos: VentaCreate
):

    venta = obtener_venta(db, venta_id)

    pago = db.query(Pago).filter(
        Pago.id == datos.pago_id
    ).first()

    if not pago:
        raise HTTPException(
            status_code=404,
            detail="Pago no encontrado"
        )

    existe_folio = db.query(Venta).filter(
        Venta.folio == datos.folio,
        Venta.id != venta_id
    ).first()

    if existe_folio:
        raise HTTPException(
            status_code=400,
            detail="El folio ya existe"
        )

    venta.pago_id = datos.pago_id
    venta.folio = datos.folio

    db.commit()
    db.refresh(venta)

    return venta


def eliminar_venta(db: Session, venta_id: int):

    venta = obtener_venta(db, venta_id)

    db.delete(venta)
    db.commit()

    return {
        "message": "Venta eliminada correctamente"
    }