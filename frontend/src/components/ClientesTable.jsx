import DataTable from './DataTable';
import { useApi } from '../hooks/useApi';

const columnas = [
  { key: 'id_cliente', label: 'ID' },
  { key: 'nombre', label: 'Nombre', render: (row) => `${row.nombre} ${row.apellido}` },
  { key: 'email', label: 'Email' },
  { key: 'telefono', label: 'Teléfono' },
  { key: 'rfc', label: 'RFC' },
  { key: 'estatus', label: 'Estatus', render: (row) => (
    <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
      row.estatus === 'activo' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
    }`}>
      {row.estatus}
    </span>
  )},
  { key: 'fecha_registro', label: 'Fecha Registro' },
];

export default function ClientesTable() {
  const { data, loading, error, total, skip, limit, setSkip } = useApi('http://localhost:8000/clientes/');

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Listado de Clientes ({total})</h2>
      <DataTable
        columns={columnas}
        data={data}
        loading={loading}
        error={error}
        total={total}
        skip={skip}
        limit={limit}
        onPageChange={setSkip}
      />
    </div>
  );
}
