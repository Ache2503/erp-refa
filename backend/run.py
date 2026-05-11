# backend/run.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import engine, get_db, Base
from app.core.config import settings
from app.api.auth.controllers import router as auth_router
from app.api.ventas.controllers import router as ventas_router
from app.api.logistica.controllers import router as logistica_router
from app.api.productos.controllers import router as productos_router
from app.api.roles.controllers import router as roles_router
from app.api.empleados.controllers import router as empleados_router
from app.api.clientes.controllers import router as clientes_router
from app.api.proveedores.controllers import router as proveedores_router
from app.api.categorias.controllers import router as categorias_router
from app.api.marcas.controllers import router as marcas_router
from app.api.unidades_medida.controllers import router as unidades_medida_router
from app.api.tipos_almacen.controllers import router as tipos_almacen_router
from app.api.almacenes.controllers import router as almacenes_router
from app.api.tipos_vehiculos.controllers import router as tipos_vehiculo_router
from app.api.vehiculos.controllers import router as vehiculos_router
from app.api.compras.controllers import router as compras_router
from app.api.pedidos_clientes.controllers import router as pedidos_clientes_router
from app.api.inventario.controllers import router as inventario_router
from app.api.conductores.controllers import router as conductores_router
from app.api.guias_remision.controllers import router as guias_remision_router
from app.api.rutas.controllers import router as rutas_router
from app.api.asignaciones.controllers import router as asignaciones_router

app = FastAPI(
    title=settings.app_name,
    description="Sistema ERP — API REST",
    version=settings.app_version,
    openapi_tags=[
        {"name": "General"},
        {"name": "Autenticación"},
        {"name": "Roles & Permisos"},
        {"name": "Empleados"},
        {"name": "Clientes"},
        {"name": "Proveedores"},
        {"name": "Categorías"},
        {"name": "Marcas"},
        {"name": "Unidades de Medida"},
        {"name": "Almacenes"},
        {"name": "Transporte"},
        {"name": "Productos"},
        {"name": "Inventario"},
        {"name": "Compras"},
        {"name": "Ventas"},
        {"name": "Logística"},
        {"name": "Pedidos Clientes"},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(roles_router)
app.include_router(empleados_router)
app.include_router(clientes_router)
app.include_router(proveedores_router)
app.include_router(categorias_router)
app.include_router(marcas_router)
app.include_router(unidades_medida_router)
app.include_router(tipos_almacen_router)
app.include_router(almacenes_router)
app.include_router(tipos_vehiculo_router)
app.include_router(vehiculos_router)
app.include_router(productos_router)
app.include_router(ventas_router)
app.include_router(logistica_router)
app.include_router(compras_router)
app.include_router(pedidos_clientes_router)
app.include_router(inventario_router)
app.include_router(conductores_router)
app.include_router(guias_remision_router)
app.include_router(rutas_router)
app.include_router(asignaciones_router)


@app.get("/", tags=["General"])
def root():
    return {
        "message": "ERP API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health", tags=["General"])
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected", "environment": settings.environment}
    except Exception as e:
        return {"status": "error", "database": "disconnected", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "run:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info",
    )