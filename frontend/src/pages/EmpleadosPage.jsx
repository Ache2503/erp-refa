import CrudPage from '../components/CrudPage';
import { estatusBadge } from '../components/Badges';

const columns = [
  { key:'id_empleado', label:'ID' },
  { key:'nombre',      label:'Nombre', render:(v,r)=>`${r.nombre} ${r.apellido||''}` },
  { key:'email',       label:'Email' },
  { key:'telefono',    label:'Teléfono' },
  { key:'cargo',       label:'Cargo' },
  { key:'estatus',     label:'Estatus', render: v => estatusBadge(v) },
];

const fields = [
  { name:'nombre',   label:'Nombre',   required:true },
  { name:'apellido', label:'Apellido' },
  { name:'email',    label:'Email',    type:'email' },
  { name:'telefono', label:'Teléfono' },
  { name:'direccion',label:'Dirección' },
  { name:'rfc',      label:'RFC' },
  { name:'numero_seguridad_social', label:'NSS' },
  { name:'cargo',    label:'Cargo' },
  { name:'estatus',  label:'Estatus', type:'select', options:[
    {value:'activo',label:'Activo'},{value:'inactivo',label:'Inactivo'}
  ], default:'activo' },
];

export default function EmpleadosPage() {
  return <CrudPage
    title="Empleados" subtitle="Gestión del personal del sistema"
    icon="👤" endpoint="/empleados"
    columns={columns} fields={fields}
    emptyIcon="👥" emptyText="Sin empleados registrados"
  />;
}
