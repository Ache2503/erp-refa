import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import { estatusBadge } from '../components/Badges';

export default function LogisticaDashboard() {
  const http = api();
  const [kpis, setKpis] = useState(null);
  const [guias, setGuias] = useState([]);
  const [conductores, setConductores] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.allSettled([
      http.get('/guias-remision/estadisticas/kpis').then(d => setKpis(d)),
      http.get('/guias-remision/detalladas').then(d => setGuias(Array.isArray(d) ? d : [])),
      http.get('/conductores').then(d => setConductores(Array.isArray(d) ? d : [])),
      http.get('/vehiculos').then(d => {
        const arr = Array.isArray(d) ? d : d?.data || [];
        setVehiculos(arr);
      }),
    ]).finally(() => setLoading(false));
  }, []);

  const kpiItems = kpis ? [
    { label: 'Total Guías', value: kpis.total_guias, icon: '📋', color: '#6366f1', bg: '#e0e7ff' },
    { label: 'Pendientes', value: kpis.pendiente, icon: '⏳', color: '#f59e0b', bg: '#fef3c7' },
    { label: 'En Tránsito', value: kpis.en_transito, icon: '🚚', color: '#3b82f6', bg: '#dbeafe' },
    { label: 'Entregadas', value: kpis.entregado, icon: '✅', color: '#10b981', bg: '#d1fae5' },
    { label: 'Canceladas', value: kpis.cancelado, icon: '❌', color: '#ef4444', bg: '#fee2e2' },
  ] : [];

  const conductoresMap = Object.fromEntries(conductores.map(c => [c.id_empleado, c]));
  const badgeColors = { emitida: '#f59e0b', en_transito: '#3b82f6', entregado: '#10b981', cancelado: '#ef4444' };

  if (loading) return <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-tertiary)' }}>Cargando panel logístico…</div>;

  const activas = guias.filter(g => g.estatus !== 'cancelado' && g.estatus !== 'entregado');

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
          <div style={{ width: 36, height: 36, borderRadius: 9, background: '#dbeafe', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1rem' }}>📊</div>
          <h2 style={{ fontFamily: 'Syne,sans-serif', fontWeight: 800, fontSize: '1.3rem' }}>Dashboard Logístico</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '.88rem' }}>Monitoreo de guías, envíos y transporte</p>
      </div>

      {kpis && (
        <div className="grid-4" style={{ marginBottom: 24 }}>
          {kpiItems.map((k, i) => (
            <div key={k.label} className={`card anim-fade-up d${i + 1}`} style={{ padding: 20 }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: 14 }}>
                <div className="stat-icon" style={{ background: k.bg }}>
                  <span style={{ fontSize: '1.05rem' }}>{k.icon}</span>
                </div>
              </div>
              <div style={{ fontSize: '1.8rem', fontWeight: 800, fontFamily: 'Syne,sans-serif', color: k.color, letterSpacing: '-0.04em', lineHeight: 1 }}>
                {k.value}
              </div>
              <div style={{ fontSize: '.82rem', color: 'var(--text-secondary)', marginTop: 5, fontWeight: 500 }}>{k.label}</div>
            </div>
          ))}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
        <div className="card" style={{ padding: 16 }}>
          <h3 style={{ fontSize: '.95rem', marginBottom: 12 }}>🚚 Guías activas</h3>
          {guias.length === 0 ? (
            <div style={{ color: 'var(--text-tertiary)', fontSize: '.85rem', textAlign: 'center', padding: 16 }}>Sin guías registradas</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {guias.slice(0, 10).map(g => (
                <div key={g.id_guia} style={{
                  display: 'flex', alignItems: 'center', gap: 10, padding: '8px 10px',
                  borderRadius: 8, background: 'var(--surface-2)', fontSize: '.85rem',
                }}>
                  <span style={{ fontWeight: 600, minWidth: 70 }}>#{g.id_guia}</span>
                  <div style={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                    {g.cliente.nombre} {g.cliente.apellido}
                  </div>
                  <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                    <div style={{
                      width: 8, height: 8, borderRadius: '50%',
                      background: badgeColors[g.estatus] || '#999',
                    }} />
                    <span style={{ color: 'var(--text-tertiary)', fontSize: '.78rem' }}>
                      {g.estatus.replace('_', ' ')}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="card" style={{ padding: 16 }}>
          <h3 style={{ fontSize: '.95rem', marginBottom: 12 }}>👤 Conductores activos</h3>
          {conductores.length === 0 ? (
            <div style={{ color: 'var(--text-tertiary)', fontSize: '.85rem', textAlign: 'center', padding: 16 }}>Sin conductores registrados</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {conductores.map(c => {
                const guiasCond = guias.filter(g => g.id_conductor === c.id_empleado);
                const activasCond = guiasCond.filter(g => g.estatus === 'en_transito').length;
                return (
                  <div key={c.id_empleado} style={{
                    display: 'flex', alignItems: 'center', gap: 10, padding: '8px 10px',
                    borderRadius: 8, background: 'var(--surface-2)', fontSize: '.85rem',
                  }}>
                    <span style={{ fontSize: '1rem' }}>👤</span>
                    <div style={{ flex: 1 }}>{c.nombre} {c.apellido}</div>
                    <div style={{ color: 'var(--text-tertiary)', fontSize: '.78rem' }}>
                      {guiasCond.length} guías
                      {activasCond > 0 && <span style={{ color: '#3b82f6', marginLeft: 4 }}>· {activasCond} activas</span>}
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
