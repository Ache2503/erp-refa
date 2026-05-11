import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import CrudPage from '../components/CrudPage';
import { priceFmt, estatusBadge, dateFmt } from '../components/Badges';

export default function ComprasPage() {
  const http = api();
  const [empleados, setEmpleados] = useState([]);

  useEffect(() => {
    http.get('/empleados').then(d => setEmpleados(Array.isArray(d) ? d : d?.data || [])).catch(() => {});
  }, []);

  const empMap = Object.fromEntries(empleados.map(e => [e.id_empleado, `${e.nombre} ${e.apellido}`]));

  return <CrudPage
    title="Compras" subtitle="Órdenes de compra a proveedores"
    icon="🛒" endpoint="/compras"
    columns={[
      { key:'id_compra', label:'#' },
      { key:'id_empleado', label:'Comprador', render: (v, row) => empMap[v] || `ID ${v}` },
      { key:'total', label:'Total', render: v => priceFmt(v) },
      { key:'estatus', label:'Estatus', render: v => estatusBadge(v) },
      { key:'fecha_compra', label:'Fecha', render: v => dateFmt(v) },
    ]}
    fields={[
      { name:'id_empleado',  label:'ID Empleado',  type:'number', required:true },
      { name:'id_proveedor',  label:'ID Proveedor',  type:'number', required:true },
      { name:'estatus', label:'Estatus', type:'select', options:[
        {value:'pendiente',label:'Pendiente'},{value:'recibido',label:'Recibido'},
        {value:'cancelado',label:'Cancelado'},
      ], default:'pendiente' },
    ]}
    emptyIcon="🛒" emptyText="Sin compras registradas"
  />;
}
