export default function DataTable({ columns, data, loading, error, total, skip, limit, onPageChange }) {
  if (loading) return <p className="text-center py-4">Cargando...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;
  if (!data || data.length === 0) return <p>No hay registros.</p>;

  return (
    <div>
      <div className="overflow-x-auto bg-white shadow rounded">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {columns.map(col => (
                <th key={col.key} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                  {col.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {data.map((row, i) => (
              <tr key={row.id_cliente || row.id_empleado || i} className="hover:bg-gray-50">
                {columns.map(col => (
                  <td key={col.key} className="px-6 py-4 whitespace-nowrap text-sm">
                    {col.render ? col.render(row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between mt-4">
        <button
          onClick={() => onPageChange(Math.max(0, skip - limit))}
          disabled={skip === 0}
          className="px-4 py-2 bg-white border rounded shadow disabled:opacity-50"
        >
          Anterior
        </button>
        <span className="text-sm text-gray-600">Página {Math.floor(skip/limit)+1} de {Math.ceil(total/limit)}</span>
        <button
          onClick={() => onPageChange(skip + limit)}
          disabled={skip + limit >= total}
          className="px-4 py-2 bg-white border rounded shadow disabled:opacity-50"
        >
          Siguiente
        </button>
      </div>
    </div>
  );
}
