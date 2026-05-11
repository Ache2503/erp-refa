import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import CrudPage from '../components/CrudPage';
import { priceFmt, estatusBadge, dateFmt } from '../components/Badges';

export default function PedidosPage() {
  const http = api();
  const [clientes, setClientes] = useState([]);
  const [empleados, setEmpleados] = useState([]);

  useEffect(() => {
    Promise.allSettled([
      http.get('/clientes').then(d => setClientes(Array.isArray(d) ? d : d?.data || [])),
      http.get('/empleados').then(d => setEmpleados(Array.isArray(d) ? d : d?.data || [])),
    ]);
  }, []);

  const cliMap = Object.fromEntries(clientes.map(c => [c.id_cliente, `${c.nombre} ${c.apellido}`]));
  const empMap = Object.fromEntries(empleados.map(e => [e.id_empleado, `${e.nombre} ${e.apellido}`]));

  return <CrudPage
    title="Pedidos" subtitle="Órdenes de pedido de clientes"
    icon="📋" endpoint="/pedidos-clientes"
    columns={[
      { key:'id_pedido_cliente', label:'#' },
      { key:'id_cliente', label:'Cliente', render: (v, row) => cliMap[v] || `ID ${v}` },
      { key:'id_empleado', label:'Vendedor', render: (v, row) => empMap[v] || `ID ${v}` },
      { key:'total', label:'Total', render: v => priceFmt(v) },
      { key:'estatus', label:'Estatus', render: v => estatusBadge(v) },
      { key:'fecha', label:'Fecha', render: v => dateFmt(v) },
    ]}
    fields={[
      { name:'id_cliente',  label:'ID Cliente',  type:'number', required:true },
      { name:'id_empleado', label:'ID Empleado', type:'number', required:true },
      { name:'estatus', label:'Estatus', type:'select', options:[
        {value:'pendiente',label:'Pendiente'},{value:'aprobado',label:'Aprobado'},
        {value:'completado',label:'Completado'},{value:'cancelado',label:'Cancelado'},
      ], default:'pendiente' },
    ]}
    emptyIcon="📋" emptyText="Sin pedidos registrados"
  />;
}
