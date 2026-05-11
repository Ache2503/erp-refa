import CrudPage from '../components/CrudPage';
import { priceFmt } from '../components/Badges';

const columns = [
  { key:'id_producto',  label:'ID' },
  { key:'nombre',       label:'Producto' },
  { key:'descripcion',  label:'Descripción', render:v=>v?v.slice(0,40)+(v.length>40?'…':''):'—' },
  { key:'precio',       label:'Precio', render:v=>priceFmt(v) },
  { key:'id_categoria', label:'Categoría' },
  { key:'id_marca',     label:'Marca' },
];

const fields = [
  { name:'nombre',      label:'Nombre',      required:true },
  { name:'descripcion', label:'Descripción', type:'textarea' },
  { name:'precio',      label:'Precio',      type:'number', placeholder:'0.00' },
  { name:'id_categoria',label:'ID Categoría',type:'number' },
  { name:'id_marca',    label:'ID Marca',    type:'number' },
];

export default function ProductosPage() {
  return <CrudPage
    title="Productos" subtitle="Catálogo de productos disponibles"
    icon="📦" endpoint="/productos"
    columns={columns} fields={fields}
    emptyIcon="📦" emptyText="Sin productos registrados"
  />;
}
