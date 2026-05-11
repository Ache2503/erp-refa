from datetime import date
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories.pedido_cliente_repository import PedidoClienteRepository
from app.repositories.cliente_repository import ClienteRepository
from app.repositories.empleado_repository import EmpleadoRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.envio_repository import EnvioRepository
from app.repositories.conductores_repository import ConductorRepository
from app.repositories.guias_remision_repository import GuiaRemisionRepository
from app.repositories.rutas_repository import RutaRepository
from app.models.pedido_cliente_detalle import PedidoClienteDetalle
from app.models.productos_almacen import ProductosAlmacen
from app.schemas.venta_completa import VentaCompletaRequest, VentaCompletaResponse
from app.schemas.guias_remision import GuiaRemisionCreate, GuiaDetalleCreate as GuiaRemisionDetalle

TAX_RATE = Decimal("0.16")

class VentaCompletaService:
    def __init__(self, db: Session):
        self.db = db
        self.pedido_repo = PedidoClienteRepository(db)
        self.cliente_repo = ClienteRepository(db)
        self.empleado_repo = EmpleadoRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.envio_repo = EnvioRepository(db)

    def ejecutar(self, data: VentaCompletaRequest) -> VentaCompletaResponse:
        cliente = self.cliente_repo.get_by_id(data.id_cliente)
        if not cliente:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no existe")
        empleado = self.empleado_repo.get_by_id(data.id_empleado)
        if not empleado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no existe")

        subtotal = Decimal("0.00")
        for d in data.detalles:
            prod = self.producto_repo.get_by_id(d.id_producto)
            if not prod:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Producto {d.id_producto} no existe")
            subtotal += d.cantidad * d.precio_unitario

        impuesto = (subtotal * TAX_RATE).quantize(Decimal("0.01"))
        total = (subtotal + impuesto).quantize(Decimal("0.01"))

        pedido = self.pedido_repo.create(
            type("obj", (), {
                "id_cliente": data.id_cliente,
                "id_empleado": data.id_empleado,
                "id_almacen": data.id_almacen,
                "estatus": "pendiente",
            })()
        )
        pedido.subtotal = subtotal
        pedido.impuesto = impuesto
        pedido.total = total

        for d in data.detalles:
            det = PedidoClienteDetalle(
                id_pedido_cliente=pedido.id_pedido_cliente,
                id_producto=d.id_producto,
                cantidad=d.cantidad,
                precio_unitario=d.precio_unitario,
                subtotal=(d.cantidad * d.precio_unitario).quantize(Decimal("0.01")),
            )
            self.db.add(det)
            self._descontar_stock(d.id_producto, data.id_almacen, d.cantidad)

        self.db.commit()
        self.db.refresh(pedido)

        id_envio = None
        id_guia = None

        if data.envio.requiere_envio and data.envio.id_vehiculo:
            envio_data = type("obj", (), {
                "id_pedido_cliente": pedido.id_pedido_cliente,
                "id_vehiculo": data.envio.id_vehiculo,
                "id_empleado": data.id_empleado,
                "estatus": "pendiente",
            })()
            envio_response = self.envio_repo.create(envio_data)
            id_envio = envio_response.id_envio

            if data.envio.id_conductor:
                guia_data = GuiaRemisionCreate(
                    id_pedido_cliente=pedido.id_pedido_cliente,
                    id_vehiculo=data.envio.id_vehiculo,
                    id_conductor=data.envio.id_conductor,
                    estatus="emitida",
                    detalles=[
                        GuiaRemisionDetalle(id_producto=d.id_producto, cantidad=d.cantidad)
                        for d in data.detalles
                    ],
                )
                guia_repo = GuiaRemisionRepository(self.db)
                guia = guia_repo.create(guia_data)
                id_guia = guia.id_guia

                if data.envio.origen and data.envio.destino:
                    ruta_repo = RutaRepository(self.db)
                    ruta = ruta_repo.create(
                        origen=data.envio.origen,
                        destino=data.envio.destino,
                    )
                    ruta_repo.asignar_envio(ruta.id_ruta, id_envio)

        ticket = self._generar_ticket(pedido, data)

        return VentaCompletaResponse(
            id_pedido=pedido.id_pedido_cliente,
            total=total,
            estatus=pedido.estatus,
            id_envio=id_envio,
            id_guia=id_guia,
            ticket=ticket,
        )

    def ticket(self, id_pedido: int) -> dict:
        pedido = self.pedido_repo.get_by_id(id_pedido)
        if not pedido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")
        detalles = self.pedido_repo.get_detalles(id_pedido)
        cliente = self.cliente_repo.get_by_id(pedido.id_cliente)
        empleado = self.empleado_repo.get_by_id(pedido.id_empleado)
        return self._build_ticket(pedido, detalles, cliente, empleado)

    def _descontar_stock(self, id_producto: int, id_almacen: int, cantidad: int):
        pa = self.db.query(ProductosAlmacen).filter(
            ProductosAlmacen.id_producto == id_producto,
            ProductosAlmacen.id_almacen == id_almacen,
        ).first()
        if pa:
            pa.stock = max(0, pa.stock - cantidad)

    def _generar_ticket(self, pedido, data: VentaCompletaRequest) -> dict:
        cliente = self.cliente_repo.get_by_id(data.id_cliente)
        empleado = self.empleado_repo.get_by_id(data.id_empleado)
        articulos = []
        for d in data.detalles:
            prod = self.producto_repo.get_by_id(d.id_producto)
            articulos.append({
                "producto": prod.nombre if prod else f"ID {d.id_producto}",
                "cantidad": d.cantidad,
                "precio_unitario": float(d.precio_unitario),
                "subtotal": float((d.cantidad * d.precio_unitario).quantize(Decimal("0.01"))),
            })
        return {
            "folio": f"P-{pedido.id_pedido_cliente:05d}",
            "fecha": str(date.today()),
            "cliente": f"{cliente.nombre} {cliente.apellido}" if cliente else f"ID {pedido.id_cliente}",
            "vendedor": f"{empleado.nombre} {empleado.apellido}" if empleado else f"ID {pedido.id_empleado}",
            "subtotal": float(pedido.subtotal),
            "impuesto": float(pedido.impuesto),
            "total": float(pedido.total),
            "estatus": pedido.estatus,
            "articulos": articulos,
        }

    def _build_ticket(self, pedido, detalles, cliente, empleado) -> dict:
        articulos = []
        for d in detalles:
            prod = self.producto_repo.get_by_id(d.id_producto)
            articulos.append({
                "producto": prod.nombre if prod else f"ID {d.id_producto}",
                "cantidad": d.cantidad,
                "precio_unitario": float(d.precio_unitario),
                "subtotal": float(d.subtotal),
            })
        return {
            "folio": f"P-{pedido.id_pedido_cliente:05d}",
            "fecha": str(pedido.fecha),
            "cliente": f"{cliente.nombre} {cliente.apellido}" if cliente else f"ID {pedido.id_cliente}",
            "vendedor": f"{empleado.nombre} {empleado.apellido}" if empleado else f"ID {pedido.id_empleado}",
            "subtotal": float(pedido.subtotal),
            "impuesto": float(pedido.impuesto),
            "total": float(pedido.total),
            "estatus": pedido.estatus,
            "articulos": articulos,
        }
