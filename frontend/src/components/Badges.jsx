export const estatusBadge = estatus => {
  const map = {
    activo:'badge-green', inactivo:'badge-red',
    pendiente:'badge-yellow', en_proceso:'badge-blue',
    completado:'badge-green', cancelado:'badge-red',
    aprobada:'badge-green', rechazada:'badge-red',
    en_transito:'badge-blue', entregado:'badge-green',
  };
  return <span className={`badge ${map[estatus?.toLowerCase()]||'badge-gray'}`}>{estatus||'—'}</span>;
};

export const priceFmt = v => v != null
  ? `$${Number(v).toLocaleString('es-MX',{minimumFractionDigits:2})}` : '—';

export const dateFmt = v => v ? new Date(v).toLocaleDateString('es-MX') : '—';
