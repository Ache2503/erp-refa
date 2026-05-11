import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';
import { priceFmt } from '../components/Badges';

export default function ContadorDashboard() {
  const { user } = useAuth();
  const http = api();
  const [stats, setStats] = useState({ ventas: 0, totalVentas: 0 });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      http.get('/ventas').then(d => {
        const data = d?.data || [];
        setStats(p => ({
          ...p,
          ventas: data.length,
          totalVentas: data.reduce((s, v) => s + (parseFloat(v.total) || 0), 0),
        }));
      }),
    ]).finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-tertiary)' }}>Cargando panel…</div>;

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <h2 style={{ fontFamily: 'Syne,sans-serif', fontWeight: 800, fontSize: '1.3rem' }}>Panel de Contador</h2>
        <p style={{ color: 'var(--text-secondary)', fontSize: '.88rem' }}>Bienvenido, {user?.nombre_empleado}</p>
      </div>
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(240px,1fr))', gap: 16 }}>
        <div className="card" style={{ textAlign: 'center', padding: 24 }}>
          <div style={{ fontSize: '2rem', marginBottom: 4 }}>💳</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{stats.ventas}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>Ventas registradas</div>
        </div>
        <div className="card" style={{ textAlign: 'center', padding: 24 }}>
          <div style={{ fontSize: '2rem', marginBottom: 4 }}>💰</div>
          <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{priceFmt(stats.totalVentas)}</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>Total en ventas</div>
        </div>
      </div>
    </div>
  );
}
