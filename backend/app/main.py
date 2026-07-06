from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine

# Importar modelos
from app.models import *

# Importar routers
from app.routers import (
    roles,
    usuarios,
    categorias,
    productos,
    mesas,
    pedidos,
    detalle_pedido,
    pagos,
    ventas,
)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Restaurant API",
    version="1.0.0"
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://localhost:8082",
        "http://127.0.0.1:8081",
        "http://127.0.0.1:8082",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(roles.router)
app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(mesas.router)
app.include_router(pedidos.router)
app.include_router(detalle_pedido.router)
app.include_router(pagos.router)
app.include_router(ventas.router)


@app.get("/")
def root():
    return {"message": "API funcionando correctamente"}