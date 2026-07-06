from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.categorias import Categoria
from app.schemas.categorias import CategoriaCreate


def obtener_categorias(db: Session):
    return db.query(Categoria).all()


def obtener_categoria(db: Session, categoria_id: int):
    categoria = db.query(Categoria).filter(
        Categoria.id == categoria_id
    ).first()

    if not categoria:
        raise HTTPException(
            status_code=404,
            detail="Categoría no encontrada"
        )

    return categoria


def crear_categoria(db: Session, categoria: CategoriaCreate):

    existe = db.query(Categoria).filter(
        Categoria.nombre == categoria.nombre
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="La categoría ya existe"
        )

    nueva_categoria = Categoria(
        nombre=categoria.nombre
    )

    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)

    return nueva_categoria


def actualizar_categoria(
    db: Session,
    categoria_id: int,
    datos: CategoriaCreate
):

    categoria = obtener_categoria(db, categoria_id)

    existe = db.query(Categoria).filter(
        Categoria.nombre == datos.nombre,
        Categoria.id != categoria_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="La categoría ya existe"
        )

    categoria.nombre = datos.nombre

    db.commit()
    db.refresh(categoria)

    return categoria


def eliminar_categoria(db: Session, categoria_id: int):

    categoria = obtener_categoria(db, categoria_id)

    db.delete(categoria)
    db.commit()

    return {
        "message": "Categoría eliminada correctamente"
    }