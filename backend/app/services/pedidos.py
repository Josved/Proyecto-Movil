from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.pedidos import Pedido
from app.models.mesas import Mesa
from app.models.usuarios import Usuario
from app.schemas.pedidos import PedidoCreate


def obtener_pedidos(db: Session):
    return db.query(Pedido).all()


def obtener_pedido(db: Session, pedido_id: int):
    pedido = db.query(Pedido).filter(
        Pedido.id == pedido_id
    ).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido no encontrado"
        )

    return pedido


def crear_pedido(db: Session, pedido: PedidoCreate):

    mesa = db.query(Mesa).filter(
        Mesa.id == pedido.mesa_id
    ).first()

    if not mesa:
        raise HTTPException(
            status_code=404,
            detail="Mesa no encontrada"
        )

    mesero = db.query(Usuario).filter(
        Usuario.id == pedido.mesero_id
    ).first()

    if not mesero:
        raise HTTPException(
            status_code=404,
            detail="Mesero no encontrado"
        )

    nuevo_pedido = Pedido(
        mesa_id=pedido.mesa_id,
        mesero_id=pedido.mesero_id,
        estado=pedido.estado
    )

    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)

    return nuevo_pedido


def actualizar_pedido(
    db: Session,
    pedido_id: int,
    datos: PedidoCreate
):

    pedido = obtener_pedido(db, pedido_id)

    mesa = db.query(Mesa).filter(
        Mesa.id == datos.mesa_id
    ).first()

    if not mesa:
        raise HTTPException(
            status_code=404,
            detail="Mesa no encontrada"
        )

    mesero = db.query(Usuario).filter(
        Usuario.id == datos.mesero_id
    ).first()

    if not mesero:
        raise HTTPException(
            status_code=404,
            detail="Mesero no encontrado"
        )

    pedido.mesa_id = datos.mesa_id
    pedido.mesero_id = datos.mesero_id
    pedido.estado = datos.estado

    db.commit()
    db.refresh(pedido)

    return pedido


def eliminar_pedido(db: Session, pedido_id: int):

    pedido = obtener_pedido(db, pedido_id)

    db.delete(pedido)
    db.commit()

    return {
        "message": "Pedido eliminado correctamente"
    }