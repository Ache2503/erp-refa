import CrudPage from '../components/CrudPage';

const columns = [
  { key:'id_marca', label:'ID' },
  { key:'nombre',   label:'Marca' },
];

const fields = [
  { name:'nombre', label:'Nombre', required:true },
];

export default function MarcasPage() {
  return <CrudPage
    title="Marcas" subtitle="Marcas asociadas a productos"
    icon="✦" endpoint="/marcas"
    columns={columns} fields={fields}
    emptyIcon="✦" emptyText="Sin marcas"
  />;
}
