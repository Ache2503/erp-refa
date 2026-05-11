import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';

export default function AlmacenistaDashboard() {
  const { user } = useAuth();
  const http = api();
  const [stats, setStats] = useState({ productos: 0, almacenes: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      http.get('/productos').then(d => setStats(p => ({ ...p, productos: Array.isArray(d) ? d.length : 0 }))),
      http.get('/almacenes').then(d => setStats(p => ({ ...p, almacenes: Array.isArray(d) ? d.length : d?.data?.length || 0 }))),
    ]).finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-tertiary)' }}>Cargando panel…</div>;

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontFamily: 'Syne,sans-serif', fontWeight: 800, fontSize: '1.3rem' }}>Panel de Almacenista</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '.88rem' }}>Bienvenido, {user?.nombre_empleado}</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(200px,1fr))', gap: 16 }}>
        <div className="card" style={{ textAlign: 'center', padding: 24 }}>
          <div style={{ fontSize: '2rem', marginBottom: 4 }}>📦</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{stats.productos}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>Productos</div>
        </div>
        <div className="card" style={{ textAlign: 'center', padding: 24 }}>
          <div style={{ fontSize: '2rem', marginBottom: 4 }}>🏬</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{stats.almacenes}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>Almacenes</div>
        </div>
      </div>
    </div>
  );
}
