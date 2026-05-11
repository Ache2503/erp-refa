import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';
import { priceFmt, estatusBadge } from '../components/Badges';

export default function AsignacionesPage() {
  const { user } = useAuth();
  const http = api();
  const [pendientes, setPendientes] = useState([]);
  const [conductores, setConductores] = useState([]);
  const [vehiculos, setVehiculos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [result, setResult] = useState(null);
  const [form, setForm] = useState({ id_pedido_cliente: '', id_vehiculo: '', id_conductor: '', origen: '', destino: '' });

  useEffect(() => {
    Promise.allSettled([
      http.get('/asignaciones/pendientes').then(d => setPendientes(Array.isArray(d) ? d : [])),
      http.get('/conductores').then(d => setConductores(Array.isArray(d) ? d : [])),
      http.get('/vehiculos').then(d => setVehiculos(Array.isArray(d) ? d : d?.data || [])),
    ]).finally(() => setLoading(false));
  }, []);

  const submit = async () => {
    setSaving(true); setResult(null);
    try {
      const res = await http.post('/asignaciones', {
        id_pedido_cliente: parseInt(form.id_pedido_cliente),
        id_vehiculo: parseInt(form.id_vehiculo),
        id_conductor: parseInt(form.id_conductor),
        origen: form.origen || null,
        destino: form.destino || null,
      });
      setResult(res);
      setForm({ id_pedido_cliente: '', id_vehiculo: '', id_conductor: '', origen: '', destino: '' });
      http.get('/asignaciones/pendientes').then(d => setPendientes(Array.isArray(d) ? d : []));
    } catch (e) { setResult({ error: e.message || 'Error al asignar' }); }
    finally { setSaving(false); }
  };

  if (loading) return <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-tertiary)' }}>Cargando…</div>;

  return (
    <div>
      <div className="page-header"><h2 className="page-title">Asignar Envíos a Transportistas</h2></div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        <div>
          <h3 style={{ marginBottom: 12, fontSize: '.95rem' }}>Pedidos pendientes de asignar</h3>
          {pendientes.length === 0 ? (
            <div className="card" style={{ textAlign: 'center', padding: 24, color: 'var(--text-tertiary)' }}>
              No hay pedidos pendientes de asignación
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
              {pendientes.map(p => (
                <div
                  key={p.id_pedido_cliente}
                  className="card"
                  style={{
                    padding: 12, cursor: 'pointer',
                    border: form.id_pedido_cliente === String(p.id_pedido_cliente) ? '2px solid var(--primary)' : '',
                    opacity: form.id_pedido_cliente && form.id_pedido_cliente !== String(p.id_pedido_cliente) ? 0.5 : 1,
                  }}
                  onClick={() => setForm(f => ({ ...f, id_pedido_cliente: String(p.id_pedido_cliente) }))}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div>
                      <div style={{ fontWeight: 600 }}>Pedido #{p.id_pedido_cliente}</div>
                      <div style={{ fontSize: '.82rem', color: 'var(--text-tertiary)' }}>{p.cliente} · {p.fecha}</div>
                      <div style={{ fontSize: '.82rem', color: 'var(--text-tertiary)' }}>Vendido por: {p.vendedor}</div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontWeight: 700 }}>{priceFmt(p.total)}</div>
                      {estatusBadge(p.estatus)}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div>
          <div className="card" style={{ padding: 20 }}>
            <h3 style={{ marginBottom: 16, fontSize: '.95rem' }}>Asignar transportista</h3>
            {!form.id_pedido_cliente && (
              <p style={{ color: 'var(--text-tertiary)', fontSize: '.85rem', marginBottom: 12 }}>
                Selecciona un pedido de la lista para asignarlo
              </p>
            )}
            <div style={{ display: 'grid', gap: 14 }}>
              <div>
                <label className="lbl">PEDIDO</label>
                <input className="inp" value={form.id_pedido_cliente ? `#${form.id_pedido_cliente}` : ''} disabled placeholder="Selecciona un pedido…" />
              </div>
              <div>
                <label className="lbl">CONDUCTOR</label>
                <select className="inp" value={form.id_conductor} onChange={e => setForm(p => ({ ...p, id_conductor: e.target.value }))}>
                  <option value="">Seleccionar conductor…</option>
                  {conductores.map(c => (
                    <option key={c.id_empleado} value={c.id_empleado}>
                      {c.nombre} {c.apellido} {c.email ? `(${c.email})` : ''}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="lbl">VEHÍCULO</label>
                <select className="inp" value={form.id_vehiculo} onChange={e => setForm(p => ({ ...p, id_vehiculo: e.target.value }))}>
                  <option value="">Seleccionar vehículo…</option>
                  {vehiculos.map(v => (
                    <option key={v.id_vehiculo} value={v.id_vehiculo}>
                      {v.marca} {v.modelo || ''} — {v.placa}
                    </option>
                  ))}
                </select>
              </div>
              <div style={{ display: 'flex', gap: 8 }}>
                <div style={{ flex: 1 }}>
                  <label className="lbl">ORIGEN (opcional)</label>
                  <input className="inp" placeholder="Ej: Almacén Central" value={form.origen} onChange={e => setForm(p => ({ ...p, origen: e.target.value }))} />
                </div>
                <div style={{ flex: 1 }}>
                  <label className="lbl">DESTINO (opcional)</label>
                  <input className="inp" placeholder="Ej: Zona Norte" value={form.destino} onChange={e => setForm(p => ({ ...p, destino: e.target.value }))} />
                </div>
              </div>

              <button
                className="btn btn-primary"
                onClick={submit}
                disabled={saving || !form.id_pedido_cliente || !form.id_conductor || !form.id_vehiculo}
                style={{ justifyContent: 'center', marginTop: 8 }}
              >
                {saving ? 'Asignando…' : 'Asignar Transportista'}
              </button>

              {result && (
                <div style={{
                  marginTop: 8, padding: 12, borderRadius: 8,
                  background: result.error ? 'var(--danger-bg)' : 'var(--success-bg)',
                  border: `1px solid ${result.error ? 'var(--danger)' : 'var(--success)'}`,
                  fontSize: '.88rem',
                }}>
                  {result.error ? (
                    <span style={{ color: 'var(--danger-text)' }}>⚠ {result.error}</span>
                  ) : (
                    <div style={{ color: 'var(--success-text)' }}>
                      <div style={{ fontWeight: 700, marginBottom: 4 }}>✅ {result.mensaje}</div>
                      {result.id_ruta && <div>Ruta #{result.id_ruta} creada</div>}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
