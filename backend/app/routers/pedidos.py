from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.pedidos import (
    PedidoCreate,
    PedidoResponse,
)
from app.services.pedidos import (
    obtener_pedidos,
    obtener_pedido,
    crear_pedido,
    actualizar_pedido,
    eliminar_pedido,
)

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)


@router.get("/", response_model=list[PedidoResponse])
def listar_pedidos(db: Session = Depends(get_db)):
    return obtener_pedidos(db)


@router.get("/{pedido_id}", response_model=PedidoResponse)
def obtener_un_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return obtener_pedido(db, pedido_id)


@router.post("/", response_model=PedidoResponse)
def crear_nuevo_pedido(
    pedido: PedidoCreate,
    db: Session = Depends(get_db)
):
    return crear_pedido(db, pedido)


@router.put("/{pedido_id}", response_model=PedidoResponse)
def editar_pedido(
    pedido_id: int,
    datos: PedidoCreate,
    db: Session = Depends(get_db)
):
    return actualizar_pedido(db, pedido_id, datos)


@router.delete("/{pedido_id}")
def borrar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return eliminar_pedido(db, pedido_id)