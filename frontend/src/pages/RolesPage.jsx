import CrudPage from '../components/CrudPage';

const columns = [
  { key:'id_rol',      label:'ID' },
  { key:'nombre',      label:'Rol' },
  { key:'descripcion', label:'Descripción' },
];

const fields = [
  { name:'nombre',      label:'Nombre',      required:true },
  { name:'descripcion', label:'Descripción', type:'textarea' },
];

export default function RolesPage() {
  return <CrudPage
    title="Roles" subtitle="Roles y permisos del sistema"
    icon="🔑" endpoint="/roles"
    columns={columns} fields={fields}
    emptyIcon="🔑" emptyText="Sin roles configurados"
  />;
}
