import CrudPage from '../components/CrudPage';

const columns = [
  { key:'id_categoria', label:'ID' },
  { key:'nombre',       label:'Nombre' },
  { key:'descripcion',  label:'Descripción', render:v=>v?v.slice(0,60)+'…':'—' },
];

const fields = [
  { name:'nombre',      label:'Nombre',      required:true },
  { name:'descripcion', label:'Descripción', type:'textarea' },
];

export default function CategoriasPage() {
  return <CrudPage
    title="Categorías" subtitle="Clasificación de productos"
    icon="🏷" endpoint="/categorias"
    columns={columns} fields={fields}
    emptyIcon="🏷" emptyText="Sin categorías"
  />;
}
