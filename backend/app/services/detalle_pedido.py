from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.detalle_pedido import DetallePedido
from app.models.pedidos import Pedido
from app.models.productos import Producto
from app.schemas.detalle_pedido import DetallePedidoCreate


def obtener_detalles(db: Session):
    return db.query(DetallePedido).all()


def obtener_detalle(db: Session, detalle_id: int):
    detalle = db.query(DetallePedido).filter(
        DetallePedido.id == detalle_id
    ).first()

    if not detalle:
        raise HTTPException(
            status_code=404,
            detail="Detalle de pedido no encontrado"
        )

    return detalle


def crear_detalle(db: Session, detalle: DetallePedidoCreate):

    pedido = db.query(Pedido).filter(
        Pedido.id == detalle.pedido_id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    producto = db.query(Producto).filter(
        Producto.id == detalle.producto_id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    nuevo_detalle = DetallePedido(
        pedido_id=detalle.pedido_id,
        producto_id=detalle.producto_id,
        cantidad=detalle.cantidad,
        precio_unitario=detalle.precio_unitario,
        subtotal=detalle.subtotal
    )

    db.add(nuevo_detalle)
    db.commit()
    db.refresh(nuevo_detalle)

    return nuevo_detalle


def actualizar_detalle(
    db: Session,
    detalle_id: int,
    datos: DetallePedidoCreate
):

    detalle = obtener_detalle(db, detalle_id)

    detalle.pedido_id = datos.pedido_id
    detalle.producto_id = datos.producto_id
    detalle.cantidad = datos.cantidad
    detalle.precio_unitario = datos.precio_unitario
    detalle.subtotal = datos.subtotal

    db.commit()
    db.refresh(detalle)

    return detalle


def eliminar_detalle(db: Session, detalle_id: int):

    detalle = obtener_detalle(db, detalle_id)

    db.delete(detalle)
    db.commit()

    return {
        "message": "Detalle eliminado correctamente"
    }