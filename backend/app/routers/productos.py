from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.productos import (
    ProductoCreate,
    ProductoResponse,
)
from app.services.productos import (
    obtener_productos,
    obtener_producto,
    crear_producto,
    actualizar_producto,
    eliminar_producto,
)

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)


@router.get("/", response_model=list[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return obtener_productos(db)


@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_un_producto(producto_id: int, db: Session = Depends(get_db)):
    return obtener_producto(db, producto_id)


@router.post("/", response_model=ProductoResponse)
def crear_nuevo_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db)
):
    return crear_producto(db, producto)


@router.put("/{producto_id}", response_model=ProductoResponse)
def editar_producto(
    producto_id: int,
    datos: ProductoCreate,
    db: Session = Depends(get_db)
):
    return actualizar_producto(db, producto_id, datos)


@router.delete("/{producto_id}")
def borrar_producto(producto_id: int, db: Session = Depends(get_db)):
    return eliminar_producto(db, producto_id)