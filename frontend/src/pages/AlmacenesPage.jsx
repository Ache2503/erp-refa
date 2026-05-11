import CrudPage from '../components/CrudPage';

const columns = [
  { key:'id_almacen',      label:'ID' },
  { key:'nombre',          label:'Nombre' },
  { key:'direccion',       label:'Dirección' },
  { key:'id_tipo_almacen', label:'Tipo' },
];

const fields = [
  { name:'nombre',          label:'Nombre',   required:true },
  { name:'direccion',       label:'Dirección' },
  { name:'id_tipo_almacen', label:'ID Tipo',  type:'number' },
];

export default function AlmacenesPage() {
  return <CrudPage
    title="Almacenes" subtitle="Gestión de almacenes y bodegas"
    icon="🏬" endpoint="/almacenes"
    columns={columns} fields={fields}
    emptyIcon="🏬" emptyText="Sin almacenes registrados"
  />;
}
