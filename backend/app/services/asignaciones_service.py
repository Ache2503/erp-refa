from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status
from app.schemas.asignaciones import AsignacionCreate, AsignacionResponse
from app.repositories.envio_repository import EnvioRepository
from app.repositories.guias_remision_repository import GuiaRemisionRepository
from app.repositories.rutas_repository import RutaRepository
from app.repositories.pedido_cliente_repository import PedidoClienteRepository
from app.schemas.guias_remision import GuiaRemisionCreate, GuiaDetalleCreate
from app.models.envios import Envios
from app.models.pedidos_clientes import PedidosClientes
from app.models.guia_remision import GuiaRemision


class AsignacionService:
    def __init__(self, db: Session):
        self.db = db
        self.envio_repo = EnvioRepository(db)
        self.guia_repo = GuiaRemisionRepository(db)
        self.ruta_repo = RutaRepository(db)
        self.pedido_repo = PedidoClienteRepository(db)

    def asignar(self, data: AsignacionCreate, id_empleado: int) -> AsignacionResponse:
        pedido = self.pedido_repo.get_by_id(data.id_pedido_cliente)
        if not pedido:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido no encontrado")

        existing = self.db.query(Envios).filter(Envios.id_pedido_cliente == data.id_pedido_cliente).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El pedido ya tiene un envío asignado")

        envio_data = type("obj", (), {
            "id_pedido_cliente": data.id_pedido_cliente,
            "id_vehiculo": data.id_vehiculo,
            "id_empleado": id_empleado,
            "estatus": "pendiente",
        })()
        envio = self.envio_repo.create(envio_data)

        detalles = self.pedido_repo.get_detalles(data.id_pedido_cliente)
        guia_data = GuiaRemisionCreate(
            id_pedido_cliente=data.id_pedido_cliente,
            id_vehiculo=data.id_vehiculo,
            id_conductor=data.id_conductor,
            estatus="emitida",
            detalles=[
                GuiaDetalleCreate(id_producto=d.id_producto, cantidad=d.cantidad)
                for d in detalles
            ],
        )
        guia = self.guia_repo.create(guia_data)

        id_ruta = None
        if data.origen and data.destino:
            ruta = self.ruta_repo.create(
                origen=data.origen,
                destino=data.destino,
            )
            self.ruta_repo.asignar_envio(ruta.id_ruta, envio.id_envio)
            id_ruta = ruta.id_ruta

        return AsignacionResponse(
            id_pedido_cliente=data.id_pedido_cliente,
            id_envio=envio.id_envio,
            id_guia=guia.id_guia,
            id_ruta=id_ruta,
            estatus="asignado",
            mensaje=f"Transportista asignado correctamente. Envío #{envio.id_envio}, Guía #{guia.id_guia}",
        )

    def listar_pendientes(self, skip: int = 0, limit: int = 100) -> list:
        subquery = self.db.query(Envios.id_pedido_cliente).subquery()
        pedidos = (
            self.db.query(PedidosClientes)
            .options(
                joinedload(PedidosClientes.clientes),
                joinedload(PedidosClientes.empleados),
            )
            .filter(PedidosClientes.id_pedido_cliente.notin_(subquery))
            .filter(PedidosClientes.estatus.in_(["pendiente", "aprobado"]))
            .offset(skip).limit(limit)
            .all()
        )
        return [
            {
                "id_pedido_cliente": p.id_pedido_cliente,
                "fecha": str(p.fecha),
                "cliente": f"{p.clientes.nombre} {p.clientes.apellido}" if p.clientes else f"ID {p.id_cliente}",
                "vendedor": f"{p.empleados.nombre} {p.empleados.apellido}" if p.empleados else f"ID {p.id_empleado}",
                "total": float(p.total),
                "estatus": p.estatus,
            }
            for p in pedidos
        ]
