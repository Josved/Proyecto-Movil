from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.usuarios import Usuario
from app.models.roles import Rol
from app.schemas.usuarios import UsuarioCreate, UsuarioUpdate


def obtener_usuarios(db: Session):
    return db.query(Usuario).all()


def obtener_usuario(db: Session, usuario_id: int):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


def crear_usuario(db: Session, usuario: UsuarioCreate):

    existe = db.query(Usuario).filter(
        Usuario.correo == usuario.correo
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    rol = db.query(Rol).filter(
        Rol.id == usuario.rol_id
    ).first()

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    nuevo_usuario = Usuario(
        nombre=usuario.nombre,
        correo=usuario.correo,
        password=usuario.password,
        rol_id=usuario.rol_id
    )

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)

    return nuevo_usuario


def actualizar_usuario(
    db: Session,
    usuario_id: int,
    datos: UsuarioUpdate
):

    usuario = obtener_usuario(db, usuario_id)

    existe = db.query(Usuario).filter(
        Usuario.correo == datos.correo,
        Usuario.id != usuario_id
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    rol = db.query(Rol).filter(
        Rol.id == datos.rol_id
    ).first()

    if not rol:
        raise HTTPException(
            status_code=404,
            detail="Rol no encontrado"
        )

    usuario.nombre = datos.nombre
    usuario.correo = datos.correo
    usuario.rol_id = datos.rol_id

    db.commit()
    db.refresh(usuario)

    return usuario


def eliminar_usuario(db: Session, usuario_id: int):

    usuario = obtener_usuario(db, usuario_id)

    db.delete(usuario)
    db.commit()

    return {
        "message": "Usuario eliminado correctamente"
    }