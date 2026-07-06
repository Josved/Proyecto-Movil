from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.categorias import (
    CategoriaCreate,
    CategoriaResponse,
)
from app.services.categorias import (
    obtener_categorias,
    obtener_categoria,
    crear_categoria,
    actualizar_categoria,
    eliminar_categoria,
)

router = APIRouter(
    prefix="/categorias",
    tags=["Categorías"]
)


@router.get("/", response_model=list[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return obtener_categorias(db)


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def obtener_una_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return obtener_categoria(db, categoria_id)


@router.post("/", response_model=CategoriaResponse)
def crear_nueva_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    return crear_categoria(db, categoria)


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def editar_categoria(
    categoria_id: int,
    datos: CategoriaCreate,
    db: Session = Depends(get_db)
):
    return actualizar_categoria(db, categoria_id, datos)


@router.delete("/{categoria_id}")
def borrar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    return eliminar_categoria(db, categoria_id)