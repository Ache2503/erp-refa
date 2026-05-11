import CrudPage from '../components/CrudPage';
import { estatusBadge } from '../components/Badges';

const columns = [
  { key:'id_proveedor', label:'ID' },
  { key:'nombre',       label:'Nombre' },
  { key:'email',        label:'Email' },
  { key:'telefono',     label:'Teléfono' },
  { key:'rfc',          label:'RFC' },
  { key:'estatus',      label:'Estatus', render: v => estatusBadge(v) },
];

const fields = [
  { name:'nombre',    label:'Nombre',   required:true },
  { name:'email',     label:'Email',    type:'email' },
  { name:'telefono',  label:'Teléfono' },
  { name:'direccion', label:'Dirección' },
  { name:'rfc',       label:'RFC' },
  { name:'estatus',   label:'Estatus', type:'select', options:[
    {value:'activo',label:'Activo'},{value:'inactivo',label:'Inactivo'}
  ], default:'activo' },
];

export default function ProveedoresPage() {
  return <CrudPage
    title="Proveedores" subtitle="Gestión de proveedores y suministros"
    icon="🏭" endpoint="/proveedores"
    columns={columns} fields={fields}
    emptyIcon="🏭" emptyText="Sin proveedores registrados"
  />;
}
