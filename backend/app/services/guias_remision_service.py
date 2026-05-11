from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.repositories.guias_remision_repository import GuiaRemisionRepository
from app.schemas.guias_remision import GuiaRemisionCreate, GuiaRemisionResponse, GuiaRemisionFullResponse
from app.schemas.guias_remision import GuiaRemisionDetalleFull, GuiaVehiculoInfo, GuiaVendedorInfo, GuiaClienteInfo, GuiaAlmacenInfo
from app.models.guia_remision import GuiaRemision
from app.models.pedidos_clientes import PedidosClientes
from app.models.empleados import Empleados
from app.models.clientes import Clientes
from app.models.almacenes import Almacenes
from app.models.guia_remision_detalle import GuiaRemisionDetalle
from app.models.productos import Productos
from app.models.vehiculo import Vehiculo


class GuiaRemisionService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = GuiaRemisionRepository(db)

    def listar(self, skip: int = 0, limit: int = 100) -> list[GuiaRemisionResponse]:
        return [GuiaRemisionResponse.model_validate(g) for g in self.repo.get_all(skip, limit)]

    def listar_full(self, skip: int = 0, limit: int = 100) -> list[GuiaRemisionFullResponse]:
        guias = (
            self.db.query(GuiaRemision)
            .options(
                joinedload(GuiaRemision.pedidos_clientes)
                .joinedload(PedidosClientes.empleados),
                joinedload(GuiaRemision.pedidos_clientes)
                .joinedload(PedidosClientes.clientes),
                joinedload(GuiaRemision.pedidos_clientes)
                .joinedload(PedidosClientes.almacenes),
                joinedload(GuiaRemision.vehiculo),
                joinedload(GuiaRemision.guia_remision_detalle)
                .joinedload(GuiaRemisionDetalle.productos),
            )
            .offset(skip).limit(limit)
            .all()
        )
        return [self._to_full(g) for g in guias]

    def obtener(self, id_guia: int) -> GuiaRemisionResponse:
        guia = self.repo.get_by_id(id_guia)
        if not guia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guía no encontrada")
        return GuiaRemisionResponse.model_validate(guia)

    def obtener_full(self, id_guia: int) -> GuiaRemisionFullResponse:
        guia = (
            self.db.query(GuiaRemision)
            .options(
                joinedload(GuiaRemision.pedidos_clientes)
                .joinedload(PedidosClientes.empleados),
                joinedload(GuiaRemision.pedidos_clientes)
                .joinedload(PedidosClientes.clientes),
                joinedload(GuiaRemision.pedidos_clientes)
                .joinedload(PedidosClientes.almacenes),
                joinedload(GuiaRemision.vehiculo),
                joinedload(GuiaRemision.guia_remision_detalle)
                .joinedload(GuiaRemisionDetalle.productos),
            )
            .filter(GuiaRemision.id_guia == id_guia)
            .first()
        )
        if not guia:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guía no encontrada")
        return self._to_full(guia)

    def _to_full(self, guia: GuiaRemision) -> GuiaRemisionFullResponse:
        pedido = guia.pedidos_clientes
        emp = pedido.empleados if pedido else None
        cli = pedido.clientes if pedido else None
        alm = pedido.almacenes if pedido else None
        veh = guia.vehiculo

        return GuiaRemisionFullResponse(
            id_guia=guia.id_guia,
            id_pedido_cliente=guia.id_pedido_cliente,
            id_conductor=guia.id_conductor,
            fecha_guia=guia.fecha_guia,
            estatus=guia.estatus,
            vendedor=GuiaVendedorInfo(
                id_empleado=emp.id_empleado if emp else 0,
                nombre=emp.nombre if emp else "—",
                apellido=emp.apellido if emp else "",
            ),
            cliente=GuiaClienteInfo(
                id_cliente=cli.id_cliente if cli else 0,
                nombre=cli.nombre if cli else "—",
                apellido=cli.apellido if cli else "",
            ),
            almacen=GuiaAlmacenInfo(
                id_almacen=alm.id_almacen if alm else 0,
                nombre=alm.nombre if alm else "—",
            ),
            vehiculo=GuiaVehiculoInfo(
                id_vehiculo=veh.id_vehiculo if veh else 0,
                placa=veh.placa if veh else "—",
                marca=veh.marca if veh else "—",
                modelo=veh.modelo if veh else None,
                capacidad_carga=float(veh.capacidad_carga) if veh and veh.capacidad_carga else None,
            ),
            detalles=[
                GuiaRemisionDetalleFull(
                    id_producto=d.id_producto,
                    producto=d.productos.nombre if d.productos else f"ID {d.id_producto}",
                    codigo=d.productos.codigo if d.productos else "—",
                    cantidad=d.cantidad,
                )
                for d in (guia.guia_remision_detalle or [])
            ],
        )

    def crear(self, data: GuiaRemisionCreate) -> GuiaRemisionResponse:
        return GuiaRemisionResponse.model_validate(self.repo.create(data))
