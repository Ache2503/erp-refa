"""
Controllers — Pedidos Clientes
Órdenes de venta a clientes
"""
from fastapi import APIRouter, Depends, Query, status, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.pedido_cliente_service import PedidoClienteService
from app.schemas.pedidos_clientes import (
    PedidoClienteCreate, PedidoClienteUpdate,
    PedidoClienteResponse, PedidoClienteConDetalles,
    PedidoClienteListResponse, PedidoClienteDetalleResponse,
)

router = APIRouter(prefix="/pedidos-clientes", tags=["Pedidos Clientes"])


@router.get("", response_model=PedidoClienteListResponse, summary="Listar pedidos")
def listar(
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar(skip, limit)


@router.post("", response_model=PedidoClienteResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Crear pedido")
def crear(data: PedidoClienteCreate, db: Session = Depends(get_db)):
    return PedidoClienteService(db).crear(data)


@router.get("/{id_pedido}", response_model=PedidoClienteConDetalles,
            summary="Obtener pedido con detalles")
def obtener(id_pedido: int, db: Session = Depends(get_db)):
    return PedidoClienteService(db).obtener(id_pedido)


@router.put("/{id_pedido}", response_model=PedidoClienteResponse,
            summary="Actualizar pedido")
def actualizar(id_pedido: int, data: PedidoClienteUpdate,
               db: Session = Depends(get_db)):
    return PedidoClienteService(db).actualizar(id_pedido, data)


@router.delete("/{id_pedido}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar pedido")
def eliminar(id_pedido: int, db: Session = Depends(get_db)):
    PedidoClienteService(db).eliminar(id_pedido)


@router.get("/cliente/{id_cliente}", response_model=list[PedidoClienteResponse],
            summary="Listar pedidos de un cliente")
def listar_por_cliente(
    id_cliente: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar_por_cliente(id_cliente, skip, limit)


@router.get("/estado/{estado}", response_model=list[PedidoClienteResponse],
            summary="Listar pedidos por estado")
def listar_por_estado(
    estado: str = Path(..., description="pendiente/confirmado/despachado/entregado/cancelado"),
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar_por_estado(estado, skip, limit)


@router.get("/empleado/{id_empleado}", response_model=list[PedidoClienteResponse],
            summary="Listar pedidos de un empleado (vendedor)")
def listar_por_empleado(
    id_empleado: int,
    skip: int  = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return PedidoClienteService(db).listar_por_empleado(id_empleado, skip, limit)


@router.get("/{id_pedido}/detalles", response_model=list[PedidoClienteDetalleResponse],
            summary="Listar detalles de un pedido")
def listar_detalles(id_pedido: int, db: Session = Depends(get_db)):
    return PedidoClienteService(db).listar_detalles(id_pedido)


@router.get("/detalles/{id_detalle}", response_model=PedidoClienteDetalleResponse,
            summary="Obtener detalle por ID")
def obtener_detalle(id_detalle: int, db: Session = Depends(get_db)):
    return PedidoClienteService(db).obtener_detalle(id_detalle)


@router.delete("/detalles/{id_detalle}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Eliminar detalle")
def eliminar_detalle(id_detalle: int, db: Session = Depends(get_db)):
    PedidoClienteService(db).eliminar_detalle(id_detalle)