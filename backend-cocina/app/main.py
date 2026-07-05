from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine, SessionLocal
from app.models import Pedido, PedidoProducto
from app.routes.cocina import router as cocina_router

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Insertar datos de prueba
def insertar_datos_prueba():
    db = SessionLocal()

    try:
        total_pedidos = db.query(Pedido).count()

        if total_pedidos == 0:
            pedido1 = Pedido(
                mesa=4,
                mesero="Carlos Pérez",
                estado="Pendiente"
            )

            pedido1.productos = [
                PedidoProducto(
                    nombre="Hamburguesa",
                    cantidad=2,
                    observaciones="Sin cebolla"
                ),
                PedidoProducto(
                    nombre="Papas fritas",
                    cantidad=1,
                    observaciones="Extra queso"
                )
            ]

            pedido2 = Pedido(
                mesa=7,
                mesero="Ana López",
                estado="Pendiente"
            )

            pedido2.productos = [
                PedidoProducto(
                    nombre="Tacos",
                    cantidad=3,
                    observaciones="Con poca salsa"
                ),
                PedidoProducto(
                    nombre="Agua de limón",
                    cantidad=2,
                    observaciones="Sin hielo"
                )
            ]

            db.add_all([pedido1, pedido2])
            db.commit()

    finally:
        db.close()

insertar_datos_prueba()

app = FastAPI(
    title="API Restaurante - Módulo Cocina",
    description="API para gestionar pedidos del área de cocina",
    version="1.0.0"
)

# Permitir conexión desde app móvil y web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta principal
@app.get("/")
def inicio():
    return {
        "mensaje": "API de Cocina funcionando correctamente"
    }

# Agregar rutas del módulo cocina
app.include_router(cocina_router)