from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import join
from typing import List

from app.core.database import get_db
from app.services.producto_service import ProductoService
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.models.productos_almacen import ProductosAlmacen
from app.models.almacenes import Almacenes
from app.models.productos import Productos
from app.api.deps import require_roles
from pydantic import BaseModel, ConfigDict
from decimal import Decimal
from typing import Optional


class ProductoConStock(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id_producto: int
    nombre: str
    codigo: str
    precio: Decimal
    id_almacen: int
    almacen: str
    stock: int
    stock_minimo: int
    stock_maximo: int

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db), _=Depends(require_roles("Administrador"))):
    service = ProductoService(db)
    return service.crear_producto(producto)

@router.get("/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    service = ProductoService(db)
    return service.obtener_producto(producto_id)

@router.get("/", response_model=List[ProductoResponse])
def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    service = ProductoService(db)
    return service.listar_productos(skip, limit)

@router.put("/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(producto_id: int, producto: ProductoUpdate, db: Session = Depends(get_db), _=Depends(require_roles("Administrador"))):
    service = ProductoService(db)
    return service.actualizar_producto(producto_id, producto)

@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db), _=Depends(require_roles("Administrador"))):
    service = ProductoService(db)
    service.eliminar_producto(producto_id)
    return None


@router.get("/con-stock/listar", response_model=List[ProductoConStock])
def listar_con_stock(
    almacen_id: int = Query(None, ge=1),
    db: Session = Depends(get_db)
):
    q = (
        db.query(Productos, ProductosAlmacen, Almacenes)
        .join(ProductosAlmacen, ProductosAlmacen.id_producto == Productos.id_producto)
        .join(Almacenes, Almacenes.id_almacen == ProductosAlmacen.id_almacen)
        .filter(Productos.estatus == "activo")
    )
    if almacen_id:
        q = q.filter(ProductosAlmacen.id_almacen == almacen_id)
    rows = q.all()
    return [
        ProductoConStock(
            id_producto=p.id_producto,
            nombre=p.nombre,
            codigo=p.codigo,
            precio=p.precio,
            id_almacen=pa.id_almacen,
            almacen=a.nombre,
            stock=pa.stock,
            stock_minimo=pa.stock_minimo,
            stock_maximo=pa.stock_maximo,
        )
        for p, pa, a in rows
    ]