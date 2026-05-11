import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import CrudPage from '../components/CrudPage';
import { estatusBadge, dateFmt } from '../components/Badges';

export default function TrasladosPage() {
  const http = api();
  const [almacenes, setAlmacenes] = useState([]);
  const [empleados, setEmpleados] = useState([]);

  useEffect(() => {
    Promise.allSettled([
      http.get('/almacenes').then(d => setAlmacenes(Array.isArray(d) ? d : d?.data || [])),
      http.get('/empleados').then(d => setEmpleados(Array.isArray(d) ? d : d?.data || [])),
    ]);
  }, []);

  const almMap = Object.fromEntries(almacenes.map(a => [a.id_almacen, a.nombre]));
  const empMap = Object.fromEntries(empleados.map(e => [e.id_empleado, `${e.nombre} ${e.apellido}`]));

  return <CrudPage
    title="Traslados Internos" subtitle="Movimiento de mercancía entre almacenes"
    icon="🔄" endpoint="/traslados"
    columns={[
      { key:'id_traslado',        label:'#' },
      { key:'id_almacen_origen',  label:'Origen', render: (v, row) => almMap[v] || `ID ${v}` },
      { key:'id_almacen_destino', label:'Destino', render: (v, row) => almMap[v] || `ID ${v}` },
      { key:'id_empleado',        label:'Empleado', render: (v, row) => empMap[v] || `ID ${v}` },
      { key:'estatus',            label:'Estatus', render: v => estatusBadge(v) },
      { key:'fecha_traslado',     label:'Fecha', render: v => dateFmt(v) },
    ]}
    fields={[
      { name:'id_almacen_origen',  label:'Almacén Origen',  type:'number', required:true },
      { name:'id_almacen_destino', label:'Almacén Destino', type:'number', required:true },
      { name:'id_empleado',        label:'ID Empleado',     type:'number', required:true },
      { name:'estatus', label:'Estatus', type:'select', options:[
        {value:'pendiente',label:'Pendiente'},{value:'en_proceso',label:'En proceso'},
        {value:'completado',label:'Completado'},{value:'cancelado',label:'Cancelado'}
      ], default:'pendiente' },
    ]}
    emptyIcon="🔄" emptyText="Sin traslados registrados"
  />;
}
