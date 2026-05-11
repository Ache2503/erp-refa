import CrudPage from '../components/CrudPage';
import { estatusBadge } from '../components/Badges';

const columns = [
  { key:'id_vehiculo',      label:'ID' },
  { key:'placa',            label:'Placa' },
  { key:'marca',            label:'Marca' },
  { key:'modelo',           label:'Modelo' },
  { key:'id_tipo_vehiculo', label:'Tipo' },
  { key:'estatus',          label:'Estatus', render: v => estatusBadge(v) },
];

const fields = [
  { name:'placa',            label:'Placa',   required:true },
  { name:'marca',            label:'Marca' },
  { name:'modelo',           label:'Modelo' },
  { name:'anio',             label:'Año',     type:'number' },
  { name:'id_tipo_vehiculo', label:'ID Tipo', type:'number' },
  { name:'estatus', label:'Estatus', type:'select', options:[
    {value:'activo',label:'Activo'},{value:'inactivo',label:'Inactivo'},
    {value:'mantenimiento',label:'Mantenimiento'}
  ], default:'activo' },
];

export default function VehiculosPage() {
  return <CrudPage
    title="Vehículos" subtitle="Flota de vehículos de la empresa"
    icon="🚛" endpoint="/vehiculos"
    columns={columns} fields={fields}
    emptyIcon="🚛" emptyText="Sin vehículos registrados"
  />;
}
