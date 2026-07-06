from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.mesas import Mesa
from app.schemas.mesas import MesaCreate


def obtener_mesas(db: Session):
    return db.query(Mesa).all()


def obtener_mesa(db: Session, mesa_id: int):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()

    if not mesa:
        raise HTTPException(
            status_code=404,
            detail="Mesa no encontrada"
        )

    return mesa


def crear_mesa(db: Session, mesa: MesaCreate):

    existe = db.query(Mesa).filter(
        Mesa.numero == mesa.numero
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una mesa con ese número"
        )

    nueva_mesa = Mesa(
        numero=mesa.numero,
        capacidad=mesa.capacidad,
        estado=mesa.estado
    )

    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)

    return nueva_mesa


def actualizar_mesa(
    db: Session,
    mesa_id: int,
    datos: MesaCreate
):

    mesa = obtener_mesa(db, mesa_id)

    existe = db.query(Mesa).filter(
        Mesa.numero == datos.numero,
        Mesa.id != mesa_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una mesa con ese número"
        )

    mesa.numero = datos.numero
    mesa.capacidad = datos.capacidad
    mesa.estado = datos.estado

    db.commit()
    db.refresh(mesa)

    return mesa


def eliminar_mesa(db: Session, mesa_id: int):

    mesa = obtener_mesa(db, mesa_id)

    db.delete(mesa)
    db.commit()

    return {
        "message": "Mesa eliminada correctamente"
    }