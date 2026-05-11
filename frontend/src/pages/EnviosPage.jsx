import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import CrudPage from '../components/CrudPage';
import { estatusBadge, dateFmt } from '../components/Badges';

export default function EnviosPage() {
  const http = api();
  const [vehiculos, setVehiculos] = useState([]);
  const [empleados, setEmpleados] = useState([]);

  useEffect(() => {
    Promise.allSettled([
      http.get('/vehiculos').then(d => setVehiculos(Array.isArray(d) ? d : d?.data || [])),
      http.get('/empleados').then(d => setEmpleados(Array.isArray(d) ? d : d?.data || [])),
    ]);
  }, []);

  const empMap = Object.fromEntries(empleados.map(e => [e.id_empleado, `${e.nombre} ${e.apellido}`]));

  return <CrudPage
    title="Envíos" subtitle="Gestión y seguimiento de envíos"
    icon="🚚" endpoint="/logistica"
    columns={[
      { key:'id_envio',          label:'#' },
      { key:'id_pedido_cliente', label:'Pedido' },
      { key:'id_vehiculo',       label:'Vehículo', ref:'vehiculos' },
      { key:'id_empleado',       label:'Empleado', render: (v, row) => empMap[v] || `ID ${v}` },
      { key:'estatus',           label:'Estatus', render: v => estatusBadge(v) },
      { key:'fecha_envio',       label:'Fecha', render: v => dateFmt(v) },
    ]}
    fields={[
      { name:'id_pedido_cliente', label:'ID Pedido',   type:'number', required:true },
      { name:'id_vehiculo',       label:'ID Vehículo', type:'number' },
      { name:'id_empleado',       label:'ID Empleado', type:'number' },
      { name:'estatus', label:'Estatus', type:'select', options:[
        {value:'pendiente',label:'Pendiente'},{value:'en_transito',label:'En tránsito'},
        {value:'entregado',label:'Entregado'},{value:'cancelado',label:'Cancelado'}
      ], default:'pendiente' },
    ]}
    refs={{
      vehiculos: { data: vehiculos, idKey: 'id_vehiculo', labelKey: 'placa' },
    }}
    emptyIcon="🚚" emptyText="Sin envíos registrados"
  />;
}
