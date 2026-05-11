"""
Service — Compras
Maneja órdenes de compra, validaciones y flujo de estados
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from decimal import Decimal

from app.repositories.compra_repository import CompraRepository, CompraDetalleRepository
from app.repositories.proveedor_repository import ProveedorRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.almacen_repository import AlmacenRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.schemas.compras import (
    CompraCreate, CompraUpdate,
    CompraResponse, CompraConDetalles, CompraConRelaciones, CompraListResponse,
    CompraDetalleResponse, CompraDetalleConProducto,
)


class CompraService:

    def __init__(self, db: Session):
        self.db = db
        self.repo = CompraRepository(db)
        self.detalle_repo = CompraDetalleRepository(db)
        self.proveedor_repo = ProveedorRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.almacen_repo = AlmacenRepository(db)
        self.empleado_repo = EmpleadoRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> CompraListResponse:
        data = self.repo.get_all(skip, limit)
        total = self.repo.get_total()
        return CompraListResponse(
            total=total, skip=skip, limit=limit,
            data=[CompraResponse.model_validate(c) for c in data],
        )

    def buscar(self, q: str, skip: int = 0,
               limit: int = 100) -> list[CompraResponse]:
        return [
            CompraResponse.model_validate(c)
            for c in self.repo.buscar(q, skip, limit)
        ]

    def obtener(self, id_compra: int) -> CompraConRelaciones:
        c = self.repo.get_by_id(id_compra)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra {id_compra} no encontrada",
            )
        return CompraConRelaciones.model_validate(c)

    def listar_por_proveedor(self, id_proveedor: int,
                            skip: int = 0,
                            limit: int = 100) -> list[CompraResponse]:
        if not self.proveedor_repo.get_by_id(id_proveedor):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {id_proveedor} no existe",
            )
        compras = self.repo.get_by_proveedor(id_proveedor, skip, limit)
        return [CompraResponse.model_validate(c) for c in compras]

    def listar_por_estado(self, estado: str,
                         skip: int = 0,
                         limit: int = 100) -> list[CompraResponse]:
        estados_validos = ["pendiente", "confirmada", "entregada", "cancelada"]
        if estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado debe ser uno de: {', '.join(estados_validos)}",
            )
        compras = self.repo.get_by_estado(estado, skip, limit)
        return [CompraResponse.model_validate(c) for c in compras]

    def listar_por_empleado(self, id_empleado: int,
                           skip: int = 0,
                           limit: int = 100) -> list[CompraResponse]:
        if not self.empleado_repo.get_by_id(id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {id_empleado} no existe",
            )
        compras = self.repo.get_by_empleado(id_empleado, skip, limit)
        return [CompraResponse.model_validate(c) for c in compras]

    def crear(self, data: CompraCreate) -> CompraConDetalles:
        # Validar número de orden único
        if self.repo.get_by_numero_orden(data.numero_orden):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe una compra con número '{data.numero_orden}'",
            )
        # Validar existencia de proveedor
        if not self.proveedor_repo.get_by_id(data.id_proveedor):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Proveedor {data.id_proveedor} no existe",
            )
        # Validar existencia de almacén
        if not self.almacen_repo.get_by_id(data.id_almacen):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Almacén {data.id_almacen} no existe",
            )
        # Validar existencia de empleado
        if not self.empleado_repo.get_by_id(data.id_empleado):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Empleado {data.id_empleado} no existe",
            )
        # Validar estado
        estados_validos = ["pendiente", "confirmada", "entregada", "cancelada"]
        if data.estado not in estados_validos:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estado debe ser uno de: {', '.join(estados_validos)}",
            )
        # Validar detalles
        if not data.detalles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Compra debe tener al menos un detalle",
            )
        for detalle in data.detalles:
            if not self.producto_repo.get_by_id(detalle.id_producto):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto {detalle.id_producto} no existe",
                )
        
        compra = self.repo.create(data)
        return CompraConDetalles.model_validate(compra)

    def actualizar(self, id_compra: int,
                   data: CompraUpdate) -> CompraResponse:
        c = self.repo.get_by_id(id_compra)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra {id_compra} no encontrada",
            )
        # Validar nuevo número de orden si cambió
        if data.numero_orden and data.numero_orden != c.numero_orden:
            if self.repo.get_by_numero_orden(data.numero_orden):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe una compra con número '{data.numero_orden}'",
                )
        # Validar nuevo proveedor si cambió
        if data.id_proveedor and data.id_proveedor != c.id_proveedor:
            if not self.proveedor_repo.get_by_id(data.id_proveedor):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Proveedor {data.id_proveedor} no existe",
                )
        # Validar nuevo almacén si cambió
        if data.id_almacen and data.id_almacen != c.id_almacen:
            if not self.almacen_repo.get_by_id(data.id_almacen):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Almacén {data.id_almacen} no existe",
                )
        # Validar nuevo empleado si cambió
        if data.id_empleado and data.id_empleado != c.id_empleado:
            if not self.empleado_repo.get_by_id(data.id_empleado):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Empleado {data.id_empleado} no existe",
                )
        # Validar nuevo estado si cambió
        if data.estado:
            estados_validos = ["pendiente", "confirmada", "entregada", "cancelada"]
            if data.estado not in estados_validos:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Estado debe ser uno de: {', '.join(estados_validos)}",
                )
        
        return CompraResponse.model_validate(self.repo.update(c, data))

    def eliminar(self, id_compra: int) -> None:
        c = self.repo.get_by_id(id_compra)
        if not c:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra {id_compra} no encontrada",
            )
        # Solo permitir eliminar si está en estado pendiente o cancelada
        if c.estado not in ["pendiente", "cancelada"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar compra en estado '{c.estado}'",
            )
        self.repo.delete(c)

    # ── DETALLES ──────────────────────────────────────────────

    def obtener_detalle(self, id_compra_detalle: int) -> CompraDetalleConProducto:
        cd = self.detalle_repo.get_by_id(id_compra_detalle)
        if not cd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detalle {id_compra_detalle} no encontrado",
            )
        return CompraDetalleConProducto.model_validate(cd)

    def listar_detalles(self, id_compra: int) -> list[CompraDetalleConProducto]:
        if not self.repo.get_by_id(id_compra):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Compra {id_compra} no encontrada",
            )
        detalles = self.detalle_repo.get_by_compra(id_compra)
        return [CompraDetalleConProducto.model_validate(d) for d in detalles]

    def eliminar_detalle(self, id_compra_detalle: int) -> None:
        cd = self.detalle_repo.get_by_id(id_compra_detalle)
        if not cd:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detalle {id_compra_detalle} no encontrado",
            )
        # Validar que la compra esté en estado pendiente
        if cd.compra.estado != "pendiente":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar detalle de compra en estado '{cd.compra.estado}'",
            )
        
        # Recalcular total de la compra
        compra = cd.compra
        self.detalle_repo.delete(cd)
        
        # Recalcular total
        detalles = self.detalle_repo.get_by_compra(compra.id_compra)
        nuevo_total = Decimal("0")
        for d in detalles:
            subtotal = d.cantidad * d.precio_unitario
            descuento = subtotal * (d.descuento_porcentaje / 100)
            nuevo_total += (subtotal - descuento)
        
        compra.total = nuevo_total
        self.db.commit()