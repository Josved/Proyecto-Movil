from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.roles import Rol
from app.schemas.roles import RolCreate


def obtener_roles(db: Session):
    return db.query(Rol).all()


def obtener_rol(db: Session, rol_id: int):
    rol = db.query(Rol).filter(Rol.id == rol_id).first()

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    return rol


def crear_rol(db: Session, rol: RolCreate):

    rol_existente = (
        db.query(Rol)
        .filter(Rol.nombre == rol.nombre)
        .first()
    )

    if rol_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un rol con ese nombre"
        )

    nuevo_rol = Rol(
        nombre=rol.nombre
    )

    db.add(nuevo_rol)
    db.commit()
    db.refresh(nuevo_rol)

    return nuevo_rol


def actualizar_rol(
    db: Session,
    rol_id: int,
    datos: RolCreate
):

    rol = obtener_rol(db, rol_id)

    existe = (
        db.query(Rol)
        .filter(
            Rol.nombre == datos.nombre,
            Rol.id != rol_id
        )
        .first()
    )

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un rol con ese nombre"
        )

    rol.nombre = datos.nombre

    db.commit()
    db.refresh(rol)

    return rol


def eliminar_rol(
    db: Session,
    rol_id: int
):

    rol = obtener_rol(db, rol_id)

    db.delete(rol)
    db.commit()

    return {
        "message": "Rol eliminado correctamente"
    }