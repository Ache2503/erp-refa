import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';
import { estatusBadge } from '../components/Badges';

const TABS = [
  { key: 'inicio', label: 'Inicio', icon: '⊞' },
  { key: 'guias', label: 'Mis Guías', icon: '📋' },
  { key: 'rutas', label: 'Rutas', icon: '🗺' },
];

function printGuia(g) {
  const w = window.open('', '_blank');
  w.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>Guía #${g.id_guia}</title>
<style>body{font-family:sans-serif;padding:40px;max-width:700px;margin:auto}
h1{text-align:center;border-bottom:2px solid #333;padding-bottom:10px}
table{width:100%;border-collapse:collapse;margin:16px 0}
th,td{padding:8px 10px;text-align:left;border-bottom:1px solid #ddd}
th{background:#f5f5f5}.info{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.label{color:#666;font-size:.8rem;text-transform:uppercase;margin-bottom:2px}
.footer{text-align:center;margin-top:30px;color:#999;font-size:.8rem;border-top:1px solid #ddd;padding-top:15px}
</style></head><body>
<h1>GUÍA DE REMISIÓN #${g.id_guia}</h1>
<p style="text-align:center;color:#666">Pedido #${g.id_pedido_cliente} · ${g.fecha_guia}</p>
<div class="info">
<div><div class="label">Vendedor</div><b>${g.vendedor.nombre} ${g.vendedor.apellido}</b></div>
<div><div class="label">Cliente</div><b>${g.cliente.nombre} ${g.cliente.apellido}</b></div>
<div><div class="label">Almacén</div><b>${g.almacen.nombre}</b></div>
<div><div class="label">Vehículo</div><b>${g.vehiculo.marca} ${g.vehiculo.modelo||''} · ${g.vehiculo.placa}</b></div>
</div>
<h3>Productos</h3>
<table><thead><tr><th>Producto</th><th>Código</th><th style="text-align:right">Cantidad</th></tr></thead><tbody>
${g.detalles.map(d => `<tr><td>${d.producto}</td><td>${d.codigo}</td><td style="text-align:right">${d.cantidad}</td></tr>`).join('')}
</tbody></table>
<div class="footer">Documento generado por ERP Logístico · Fecha: ${new Date().toLocaleDateString()}</div>
</body></html>`);
  w.document.close();
  w.print();
}

const ESTATUS_FLUJO = ['emitida', 'en_transito', 'entregado'];

export default function ConductorDashboard() {
  const { user } = useAuth();
  const http = api();
  const [tab, setTab] = useState('inicio');
  const [guias, setGuias] = useState([]);
  const [rutas, setRutas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedGuia, setExpandedGuia] = useState(null);
  const [tracking, setTracking] = useState({});
  const [cambiando, setCambiando] = useState(null);

  const loadGuias = () =>
    http.get('/guias-remision/detalladas').then(d => setGuias(Array.isArray(d) ? d : []));

  useEffect(() => {
    Promise.allSettled([
      loadGuias(),
      http.get('/rutas').then(d => setRutas(Array.isArray(d) ? d : [])),
    ]).finally(() => setLoading(false));
  }, []);

  const loadTracking = async idGuia => {
    if (tracking[idGuia]) return;
    try {
      const data = await http.get(`/guias-remision/${idGuia}/tracking`);
      setTracking(p => ({ ...p, [idGuia]: Array.isArray(data) ? data : [] }));
    } catch { setTracking(p => ({ ...p, [idGuia]: [] })); }
  };

  const cambiarEstatus = async (guia, nuevoEstatus) => {
    setCambiando(guia.id_guia);
    try {
      await http.patch(`/guias-remision/${guia.id_guia}/estatus`, { estatus: nuevoEstatus });
      await loadGuias();
      setTracking(p => ({ ...p, [guia.id_guia]: undefined }));
      if (expandedGuia === guia.id_guia) loadTracking(guia.id_guia);
    } catch (e) { alert('Error al cambiar estatus: ' + (e.message || '')); }
    finally { setCambiando(null); }
  };

  const handleExpandir = idGuia => {
    const next = expandedGuia === idGuia ? null : idGuia;
    setExpandedGuia(next);
    if (next) loadTracking(next);
  };

  const misGuias = guias.filter(g => g.id_conductor === user?.id_empleado);
  const pendientes = misGuias.filter(g => g.estatus === 'emitida' || g.estatus === 'pendiente').length;
  const totalProductos = misGuias.reduce((s, g) => s + g.detalles.reduce((a, d) => a + d.cantidad, 0), 0);

  if (loading) return <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-tertiary)' }}>Cargando panel de conductor…</div>;

  const estatusIcono = { emitida: '📄', en_transito: '🚚', entregado: '✅', cancelado: '❌' };

  const TabContent = () => {
    switch (tab) {
      case 'inicio':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Panel de Conductor</h2></div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(240px,1fr))', gap: 16, marginBottom: 24 }}>
              <div className="card" style={{ textAlign: 'center', padding: 24 }}>
                <div style={{ fontSize: '2rem', marginBottom: 4 }}>📋</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{misGuias.length}</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>Guías asignadas</div>
              </div>
              <div className="card" style={{ textAlign: 'center', padding: 24 }}>
                <div style={{ fontSize: '2rem', marginBottom: 4 }}>⏳</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{pendientes}</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>Pendientes</div>
              </div>
              <div className="card" style={{ textAlign: 'center', padding: 24 }}>
                <div style={{ fontSize: '2rem', marginBottom: 4 }}>📦</div>
                <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{totalProductos}</div>
                <div style={{ color: 'var(--text-secondary)', fontSize: '.85rem' }}>Productos a transportar</div>
              </div>
            </div>
            <div className="card" style={{ padding: 16 }}>
              <h3 style={{ marginBottom: 12 }}>Información del Conductor</h3>
              <div style={{ display: 'grid', gap: 8, fontSize: '.9rem' }}>
                <div><strong>Nombre:</strong> {user?.nombre_empleado}</div>
                <div><strong>Email:</strong> {user?.username}</div>
                <div><strong>Cargo:</strong> {user?.cargo || 'Transportista'}</div>
                <div><strong>ID Empleado:</strong> {user?.id_empleado}</div>
              </div>
            </div>
          </div>
        );

      case 'guias':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Mis Guías de Remisión</h2></div>
            {misGuias.length === 0 && (
              <div className="card" style={{ textAlign: 'center', padding: 32, color: 'var(--text-tertiary)' }}>
                No tienes guías asignadas
              </div>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              {misGuias.map(g => {
                const idxActual = ESTATUS_FLUJO.indexOf(g.estatus);
                const proxEstatus = idxActual < ESTATUS_FLUJO.length - 1 ? ESTATUS_FLUJO[idxActual + 1] : null;
                const badgeColors = { emitida: '#f59e0b', en_transito: '#3b82f6', entregado: '#10b981', cancelado: '#ef4444' };

                return (
                  <div key={g.id_guia} className="card" style={{ padding: 0, overflow: 'hidden' }}>
                    <div
                      style={{
                        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                        padding: '14px 18px', cursor: 'pointer',
                        background: expandedGuia === g.id_guia ? 'var(--surface-2)' : 'transparent',
                        borderBottom: expandedGuia === g.id_guia ? '1px solid var(--border)' : 'none',
                      }}
                      onClick={() => handleExpandir(g.id_guia)}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                        <span style={{ fontSize: '1.1rem' }}>📋</span>
                        <div>
                          <div style={{ fontWeight: 700 }}>Guía #{g.id_guia} — Pedido #{g.id_pedido_cliente}</div>
                          <div style={{ fontSize: '.8rem', color: 'var(--text-tertiary)' }}>
                            {g.fecha_guia} · {g.cliente.nombre} {g.cliente.apellido}
                          </div>
                        </div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        {estatusBadge(g.estatus)}
                        <span style={{ fontSize: '.8rem', color: 'var(--text-tertiary)', transition: 'transform .2s', transform: expandedGuia === g.id_guia ? 'rotate(180deg)' : '' }}>▼</span>
                      </div>
                    </div>

                    {expandedGuia === g.id_guia && (
                      <div style={{ padding: '16px 18px' }}>
                        <div style={{ display: 'flex', gap: 8, marginBottom: 16, flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between' }}>
                          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                            {proxEstatus && (
                              <button
                                className="btn btn-primary btn-sm"
                                onClick={() => cambiarEstatus(g, proxEstatus)}
                                disabled={cambiando === g.id_guia}
                                style={{ background: badgeColors[proxEstatus], border: 'none' }}
                              >
                                {cambiando === g.id_guia ? '⋯' : `${estatusIcono[proxEstatus] || ''} Marcar como ${proxEstatus === 'en_transito' ? 'En Tránsito' : proxEstatus.charAt(0).toUpperCase() + proxEstatus.slice(1)}`}
                              </button>
                            )}
                            {g.estatus !== 'cancelado' && (
                              <button className="btn btn-danger btn-sm" onClick={() => cambiarEstatus(g, 'cancelado')} disabled={cambiando === g.id_guia}>
                                {cambiando === g.id_guia ? '⋯' : '❌ Cancelar guía'}
                              </button>
                            )}
                          </div>
                          <button className="btn btn-ghost btn-sm" onClick={() => printGuia(g)}>🖨 Imprimir</button>
                        </div>

                        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
                          <div>
                            <h4 style={{ fontSize: '.8rem', textTransform: 'uppercase', color: 'var(--text-tertiary)', marginBottom: 8, letterSpacing: '.5px' }}>Vendedor</h4>
                            <div style={{ background: 'var(--surface-2)', borderRadius: 8, padding: 12 }}>
                              <div style={{ fontWeight: 600 }}>{g.vendedor.nombre} {g.vendedor.apellido}</div>
                            </div>
                          </div>
                          <div>
                            <h4 style={{ fontSize: '.8rem', textTransform: 'uppercase', color: 'var(--text-tertiary)', marginBottom: 8, letterSpacing: '.5px' }}>Cliente</h4>
                            <div style={{ background: 'var(--surface-2)', borderRadius: 8, padding: 12 }}>
                              <div style={{ fontWeight: 600 }}>{g.cliente.nombre} {g.cliente.apellido}</div>
                            </div>
                          </div>
                          <div>
                            <h4 style={{ fontSize: '.8rem', textTransform: 'uppercase', color: 'var(--text-tertiary)', marginBottom: 8, letterSpacing: '.5px' }}>Almacén</h4>
                            <div style={{ background: 'var(--surface-2)', borderRadius: 8, padding: 12 }}>
                              <div style={{ fontWeight: 600 }}>{g.almacen.nombre}</div>
                            </div>
                          </div>
                          <div>
                            <h4 style={{ fontSize: '.8rem', textTransform: 'uppercase', color: 'var(--text-tertiary)', marginBottom: 8, letterSpacing: '.5px' }}>Vehículo</h4>
                            <div style={{ background: 'var(--surface-2)', borderRadius: 8, padding: 12 }}>
                              <div style={{ fontWeight: 600 }}>{g.vehiculo.marca} {g.vehiculo.modelo || ''}</div>
                              <div style={{ fontSize: '.8rem', color: 'var(--text-tertiary)' }}>
                                Placa: {g.vehiculo.placa}
                                {g.vehiculo.capacidad_carga && ` · Cap. carga: ${g.vehiculo.capacidad_carga} kg`}
                              </div>
                            </div>
                          </div>
                        </div>

                        <h4 style={{ fontSize: '.8rem', textTransform: 'uppercase', color: 'var(--text-tertiary)', marginBottom: 8, letterSpacing: '.5px' }}>
                          Productos ({g.detalles.length} ítems)
                        </h4>
                        <div style={{ border: '1px solid var(--border)', borderRadius: 8, overflow: 'hidden', marginBottom: 16 }}>
                          <table className="tbl" style={{ margin: 0 }}>
                            <thead>
                              <tr>
                                <th>Producto</th>
                                <th>Código</th>
                                <th style={{ textAlign: 'right' }}>Cantidad</th>
                              </tr>
                            </thead>
                            <tbody>
                              {g.detalles.map((d, i) => (
                                <tr key={i}>
                                  <td style={{ fontWeight: 500 }}>{d.producto}</td>
                                  <td style={{ color: 'var(--text-tertiary)', fontSize: '.85rem' }}>{d.codigo}</td>
                                  <td style={{ textAlign: 'right', fontWeight: 700 }}>{d.cantidad}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        </div>

                        {/* Tracking Timeline */}
                        <h4 style={{ fontSize: '.8rem', textTransform: 'uppercase', color: 'var(--text-tertiary)', marginBottom: 12, letterSpacing: '.5px' }}>
                          📍 Historial de seguimiento
                        </h4>
                        {!tracking[g.id_guia] ? (
                          <div style={{ textAlign: 'center', padding: 12, color: 'var(--text-tertiary)', fontSize: '.85rem' }}>Cargando…</div>
                        ) : tracking[g.id_guia].length === 0 ? (
                          <div style={{ textAlign: 'center', padding: 12, color: 'var(--text-tertiary)', fontSize: '.85rem' }}>Sin registros de seguimiento</div>
                        ) : (
                          <div style={{ position: 'relative', paddingLeft: 28 }}>
                            {tracking[g.id_guia].map((t, i) => (
                              <div key={t.id_tracking} style={{ position: 'relative', paddingBottom: i < tracking[g.id_guia].length - 1 ? 16 : 0 }}>
                                <div style={{
                                  position: 'absolute', left: -28, top: 4, width: 14, height: 14, borderRadius: '50%',
                                  background: badgeColors[t.estatus_nuevo] || '#666',
                                  border: '2px solid #fff', boxShadow: '0 0 0 2px ' + (badgeColors[t.estatus_nuevo] || '#666'),
                                }} />
                                {i < tracking[g.id_guia].length - 1 && (
                                  <div style={{
                                    position: 'absolute', left: -22, top: 18, width: 2, height: 'calc(100% - 4px)',
                                    background: '#ddd',
                                  }} />
                                )}
                                <div style={{ fontSize: '.88rem' }}>
                                  <span style={{ fontWeight: 600 }}>{estatusIcono[t.estatus_nuevo] || ''} {t.estatus_nuevo.replace('_', ' ')}</span>
                                  {t.estatus_anterior && <span style={{ color: 'var(--text-tertiary)', fontSize: '.8rem' }}> (desde {t.estatus_anterior.replace('_', ' ')})</span>}
                                </div>
                                <div style={{ fontSize: '.78rem', color: 'var(--text-tertiary)', marginTop: 2 }}>
                                  {new Date(t.fecha).toLocaleString('es-MX')}
                                  {t.ubicacion && ` · ${t.ubicacion}`}
                                </div>
                                {t.comentario && <div style={{ fontSize: '.82rem', color: '#666', marginTop: 2 }}>📝 {t.comentario}</div>}
                              </div>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        );

      case 'rutas':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Rutas</h2></div>
            {rutas.length === 0 && (
              <div className="card" style={{ textAlign: 'center', padding: 32, color: 'var(--text-tertiary)' }}>
                Sin rutas registradas
              </div>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {rutas.map(r => (
                <div key={r.id_ruta} className="card" style={{ display: 'flex', alignItems: 'center', gap: 16, padding: '14px 18px' }}>
                  <span style={{ fontSize: '1.2rem' }}>🗺</span>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600 }}>Ruta #{r.id_ruta}</div>
                    <div style={{ fontSize: '.85rem', color: 'var(--text-secondary)' }}>
                      {r.origen} → {r.destino}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right', fontSize: '.85rem', color: 'var(--text-tertiary)' }}>
                    <div>{r.distancia} km</div>
                    <div>{r.tiempo_estimado}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        );

      default: return null;
    }
  };

  return (
    <div>
      <div style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
          <div style={{ width: 36, height: 36, borderRadius: 9, background: 'var(--info-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1rem' }}>🚚</div>
          <h2 style={{ fontFamily: 'Syne,sans-serif', fontWeight: 800, fontSize: '1.3rem' }}>Panel de Conductor</h2>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: '.88rem' }}>Bienvenido, {user?.nombre_empleado || user?.username}</p>
      </div>

      <div style={{ display: 'flex', gap: 6, marginBottom: 20, flexWrap: 'wrap' }}>
        {TABS.map(t => (
          <button key={t.key} className={`btn ${tab === t.key ? 'btn-primary' : 'btn-ghost'}`} onClick={() => setTab(t.key)}>
            {t.icon} {t.label}
          </button>
        ))}
      </div>

      <div className="anim-fade-up"><TabContent /></div>
    </div>
  );
}
