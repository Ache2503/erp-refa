import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';
import { priceFmt } from '../components/Badges';

export default function GerenteDashboard() {
  const { user } = useAuth();
  const http = api();
  const [stats, setStats] = useState({ empleados: 0, clientes: 0, productos: 0, proveedores: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      http.get('/empleados').then(d => setStats(p => ({ ...p, empleados: Array.isArray(d) ? d.length : d?.data?.length || 0 }))),
      http.get('/clientes').then(d => setStats(p => ({ ...p, clientes: Array.isArray(d) ? d.length : d?.data?.length || 0 }))),
      http.get('/productos').then(d => setStats(p => ({ ...p, productos: Array.isArray(d) ? d.length : 0 }))),
      http.get('/proveedores').then(d => setStats(p => ({ ...p, proveedores: Array.isArray(d) ? d.length : d?.data?.length || 0 }))),
    ]).finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-tertiary)' }}>Cargando panel…</div>;

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontFamily: 'Syne,sans-serif', fontWeight: 800, fontSize: '1.3rem' }}>Panel de Gerente</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '.88rem' }}>Bienvenido, {user?.nombre_empleado}</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(200px,1fr))', gap: 16 }}>
        {[
          ['👤', stats.empleados, 'Empleados'],
          ['🏢', stats.clientes, 'Clientes'],
          ['📦', stats.productos, 'Productos'],
          ['🏭', stats.proveedores, 'Proveedores'],
        ].map(([ic, n, lb]) => (
          <div key={lb} className="card" style={{ textAlign: 'center', padding: 24 }}>
            <div style={{ fontSize: '2rem', marginBottom: 4 }}>{ic}</div>
            <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{n}</div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>{lb}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
