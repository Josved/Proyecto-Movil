from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.productos import Producto
from app.models.categorias import Categoria
from app.schemas.productos import ProductoCreate


def obtener_productos(db: Session):
    return db.query(Producto).all()


def obtener_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(
        Producto.id == producto_id
    ).first()

    if not producto:
        raise HTTPException(
            status_code=404,
            detail="Producto no encontrado"
        )

    return producto


def crear_producto(db: Session, producto: ProductoCreate):

    categoria = db.query(Categoria).filter(
        Categoria.id == producto.categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    nuevo_producto = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock,
        disponible=producto.disponible,
        categoria_id=producto.categoria_id
    )

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return nuevo_producto


def actualizar_producto(
    db: Session,
    producto_id: int,
    datos: ProductoCreate
):

    producto = obtener_producto(db, producto_id)

    categoria = db.query(Categoria).filter(
        Categoria.id == datos.categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    producto.nombre = datos.nombre
    producto.descripcion = datos.descripcion
    producto.precio = datos.precio
    producto.stock = datos.stock
    producto.disponible = datos.disponible
    producto.categoria_id = datos.categoria_id

    db.commit()
    db.refresh(producto)

    return producto


def eliminar_producto(db: Session, producto_id: int):

    producto = obtener_producto(db, producto_id)

    db.delete(producto)
    db.commit()

    return {
        "message": "Producto eliminado correctamente"
    }