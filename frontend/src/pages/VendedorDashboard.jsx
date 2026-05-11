import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';
import { useAuth } from '../context/AuthContext';
import { priceFmt, estatusBadge } from '../components/Badges';

function printTicket(t) {
  const w = window.open('', '_blank');
  w.document.write(`<!DOCTYPE html><html><head><meta charset="utf-8"><title>Ticket ${t.folio}</title>
<style>body{font-family:sans-serif;padding:40px;max-width:400px;margin:auto}
h1{text-align:center;font-size:1.3rem}h2{text-align:center;font-size:.9rem;color:#666;margin-top:-8px}
table{width:100%;border-collapse:collapse;margin:16px 0}
th,td{padding:6px 8px;text-align:left;border-bottom:1px solid #ddd}
.total{font-size:1.2rem;font-weight:700;text-align:right;border-top:2px solid #333;padding-top:8px;margin-top:8px}
.footer{text-align:center;margin-top:20px;color:#999;font-size:.75rem;border-top:1px solid #ddd;padding-top:10px}
</style></head><body>
<h1>🧾 TICKET</h1>
<h2>${t.folio}</h2>
<p><b>Cliente:</b> ${t.cliente}<br><b>Vendedor:</b> ${t.vendedor}<br><b>Fecha:</b> ${t.fecha}</p>
<table><thead><tr><th>Producto</th><th>Cant</th><th style="text-align:right">Subtotal</th></tr></thead><tbody>
${(t.articulos||[]).map(a => `<tr><td>${a.producto}</td><td>${a.cantidad}</td><td style="text-align:right">$${parseFloat(a.subtotal).toFixed(2)}</td></tr>`).join('')}
</tbody></table>
<p style="text-align:right"><b>Subtotal:</b> $${parseFloat(t.subtotal).toFixed(2)}<br><b>IVA (16%):</b> $${parseFloat(t.impuesto).toFixed(2)}</p>
<p class="total">TOTAL: $${parseFloat(t.total).toFixed(2)}</p>
<div class="footer">ERP Logístico · ${new Date().toLocaleDateString()}</div>
</body></html>`);
  w.document.close();
  w.print();
}

const TABS = [
  { key: 'inicio', label: 'Inicio', icon: '⊞' },
  { key: 'productos', label: 'Productos', icon: '📦' },
  { key: 'venta', label: 'Nueva Venta', icon: '➕' },
  { key: 'ventas', label: 'Mis Ventas', icon: '💳' },
  { key: 'clientes', label: 'Clientes', icon: '🏢' },
  { key: 'guias', label: 'Guías', icon: '📋' },
];

export default function VendedorDashboard() {
  const { user } = useAuth();
  const http = api();
  const [tab, setTab] = useState('inicio');
  const [productos, setProductos] = useState([]);
  const [ventas, setVentas] = useState([]);
  const [clientes, setClientes] = useState([]);
  const [conductores, setConductores] = useState([]);
  const [guias, setGuias] = useState([]);
  const [almacenes, setAlmacenes] = useState([]);
  const [productoFilter, setProductoFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [selectedAlmacen, setSelectedAlmacen] = useState('');
  const [saving, setSaving] = useState(false);
  const [result, setResult] = useState(null);

  const [form, setForm] = useState({
    id_cliente: '', id_almacen: '3',
    requiere_envio: false, id_vehiculo: '', id_conductor: '',
    origen: '', destino: '',
    items: [{ id_producto: '', cantidad: 1, precio_unitario: '' }],
  });

  useEffect(() => {
    Promise.allSettled([
      http.get('/productos/con-stock/listar').then(d => setProductos(Array.isArray(d) ? d : [])),
      http.get('/ventas').then(d => setVentas(d?.data || [])),
      http.get('/clientes').then(d => setClientes(Array.isArray(d) ? d : d?.data || [])),
      http.get('/conductores').then(d => setConductores(Array.isArray(d) ? d : [])),
      http.get('/guias-remision/detalladas').then(d => setGuias(Array.isArray(d) ? d : [])),
      http.get('/almacenes').then(d => setAlmacenes(Array.isArray(d) ? d : d?.data || [])),
    ]).finally(() => setLoading(false));
  }, []);

  const clientesMap = Object.fromEntries(clientes.map(c => [c.id_cliente, c]));

  const prodFiltrados = productos.filter(p =>
    JSON.stringify(p).toLowerCase().includes(productoFilter.toLowerCase())
  );

  const prodUnicos = [...new Map(productos.map(p => [p.id_producto, p])).values()];

  const prodPorAlmacen = selectedAlmacen
    ? productos.filter(p => p.id_almacen === parseInt(selectedAlmacen))
    : productos;

  const addItem = () => setForm(p => ({ ...p, items: [...p.items, { id_producto: '', cantidad: 1, precio_unitario: '' }] }));
  const rmItem = i => setForm(p => ({ ...p, items: p.items.filter((_, idx) => idx !== i) }));
  const setItem = (i, k, v) => {
    const items = [...form.items];
    items[i] = { ...items[i], [k]: v };
    if (k === 'id_producto') {
      const prod = productos.find(p => p.id_producto === parseInt(v));
      if (prod) items[i].precio_unitario = prod.precio;
    }
    setForm(p => ({ ...p, items }));
  };

  const submitVenta = async () => {
    setSaving(true); setResult(null);
    try {
      const payload = {
        id_cliente: parseInt(form.id_cliente),
        id_empleado: user.id_empleado,
        id_almacen: parseInt(form.id_almacen),
        detalles: form.items.filter(i => i.id_producto).map(i => ({
          id_producto: parseInt(i.id_producto),
          cantidad: parseInt(i.cantidad),
          precio_unitario: parseFloat(i.precio_unitario),
        })),
        envio: {
          requiere_envio: form.requiere_envio,
          id_vehiculo: form.id_vehiculo ? parseInt(form.id_vehiculo) : null,
          id_conductor: form.id_conductor ? parseInt(form.id_conductor) : null,
          origen: form.origen || null,
          destino: form.destino || null,
        },
      };
      const res = await http.post('/ventas/completa', payload);
      setResult(res);
      setForm({
        id_cliente: '', id_almacen: '3', requiere_envio: false,
        id_vehiculo: '', id_conductor: '', origen: '', destino: '',
        items: [{ id_producto: '', cantidad: 1, precio_unitario: '' }],
      });
      http.get('/ventas').then(d => setVentas(d?.data || []));
    } catch (e) { setResult({ error: e.message }); }
    finally { setSaving(false); }
  };

  if (loading) return <div style={{ padding: 48, textAlign: 'center', color: 'var(--text-tertiary)' }}>Cargando módulo de ventas…</div>;

  const misVentas = ventas.filter(v => v.id_empleado === user.id_empleado);

  const TabContent = () => {
    switch (tab) {
      case 'inicio':
        return (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill,minmax(200px,1fr))', gap: 16 }}>
            {TABS.filter(t => t.key !== 'inicio').map(t => (
              <div key={t.key} className="card" style={{ cursor: 'pointer', textAlign: 'center', padding: 24 }} onClick={() => setTab(t.key)}>
                <div style={{ fontSize: '2rem', marginBottom: 8 }}>{t.icon}</div>
                <div style={{ fontWeight: 600 }}>{t.label}</div>
              </div>
            ))}
          </div>
        );

      case 'productos':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Catálogo de Productos</h2></div>
            <div style={{ display: 'flex', gap: 12, marginBottom: 16 }}>
              <input className="inp" placeholder="Buscar producto…" value={productoFilter} onChange={e => setProductoFilter(e.target.value)} style={{ flex: 1, maxWidth: 300 }} />
              <select className="inp" value={selectedAlmacen} onChange={e => setSelectedAlmacen(e.target.value)} style={{ maxWidth: 200 }}>
                <option value="">Todos los almacenes</option>
                {almacenes.map(a => <option key={a.id_almacen} value={a.id_almacen}>{a.nombre}</option>)}
              </select>
            </div>
            <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
              <table className="tbl">
                <thead><tr><th>Producto</th><th>Código</th><th>Precio</th><th>Almacén</th><th>Stock</th><th>Stock Mín</th></tr></thead>
                <tbody>
                  {prodPorAlmacen.filter(p => JSON.stringify(p).toLowerCase().includes(productoFilter.toLowerCase())).map((p, i) => (
                    <tr key={i}>
                      <td>{p.nombre}</td>
                      <td>{p.codigo}</td>
                      <td>{priceFmt(p.precio)}</td>
                      <td>{p.almacen}</td>
                      <td><span className={`badge ${p.stock <= p.stock_minimo ? 'badge-red' : 'badge-green'}`}>{p.stock}</span></td>
                      <td>{p.stock_minimo}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );

      case 'venta':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Nueva Venta</h2></div>
            <div className="card" style={{ maxWidth: 700 }}>
              <div style={{ display: 'grid', gap: 14 }}>
                <div>
                  <label className="lbl">CLIENTE</label>
                  <select className="inp" value={form.id_cliente} onChange={e => setForm(p => ({ ...p, id_cliente: e.target.value }))}>
                    <option value="">Seleccionar cliente…</option>
                    {clientes.map(c => <option key={c.id_cliente} value={c.id_cliente}>{c.nombre} {c.apellido}</option>)}
                  </select>
                </div>
                <div>
                  <label className="lbl">ALMACÉN</label>
                  <select className="inp" value={form.id_almacen} onChange={e => setForm(p => ({ ...p, id_almacen: e.target.value }))}>
                    {almacenes.map(a => <option key={a.id_almacen} value={a.id_almacen}>{a.nombre}</option>)}
                  </select>
                </div>
                <div><label className="lbl">PRODUCTOS</label></div>
                {form.items.map((item, i) => (
                  <div key={i} style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <select className="inp" value={item.id_producto} onChange={e => setItem(i, 'id_producto', e.target.value)} style={{ flex: 1 }}>
                      <option value="">Seleccionar…</option>
                      {prodUnicos.map(p => <option key={p.id_producto} value={p.id_producto}>{p.nombre} - {priceFmt(p.precio)}</option>)}
                    </select>
                    <input className="inp" type="number" min="1" value={item.cantidad} onChange={e => setItem(i, 'cantidad', e.target.value)} style={{ width: 80 }} placeholder="Cant" />
                    <input className="inp" type="number" step="0.01" value={item.precio_unitario} onChange={e => setItem(i, 'precio_unitario', e.target.value)} style={{ width: 120 }} placeholder="Precio" />
                    {form.items.length > 1 && <button className="btn btn-danger btn-sm" onClick={() => rmItem(i)}>✕</button>}
                  </div>
                ))}
                <button className="btn btn-ghost btn-sm" onClick={addItem}>+ Agregar producto</button>

                <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginTop: 8 }}>
                  <input type="checkbox" checked={form.requiere_envio} onChange={e => setForm(p => ({ ...p, requiere_envio: e.target.checked }))} />
                  <label>Requiere envío</label>
                </div>

                {form.requiere_envio && (
                  <div style={{ display: 'grid', gap: 12, padding: 12, background: 'var(--surface-2)', borderRadius: 8 }}>
                    <div style={{ display: 'flex', gap: 8 }}>
                      <div style={{ flex: 1 }}>
                        <label className="lbl">VEHÍCULO</label>
                        <select className="inp" value={form.id_vehiculo} onChange={e => setForm(p => ({ ...p, id_vehiculo: e.target.value }))}>
                          <option value="">Seleccionar…</option>
                          <option value="5">Vehículo 5</option>
                          <option value="6">Vehículo 6</option>
                        </select>
                      </div>
                      <div style={{ flex: 1 }}>
                        <label className="lbl">CONDUCTOR</label>
                        <select className="inp" value={form.id_conductor} onChange={e => setForm(p => ({ ...p, id_conductor: e.target.value }))}>
                          <option value="">Seleccionar…</option>
                          {conductores.map(c => <option key={c.id_empleado} value={c.id_empleado}>{c.nombre} {c.apellido}</option>)}
                        </select>
                      </div>
                    </div>
                    <div style={{ display: 'flex', gap: 8 }}>
                      <input className="inp" placeholder="Origen" value={form.origen} onChange={e => setForm(p => ({ ...p, origen: e.target.value }))} style={{ flex: 1 }} />
                      <input className="inp" placeholder="Destino" value={form.destino} onChange={e => setForm(p => ({ ...p, destino: e.target.value }))} style={{ flex: 1 }} />
                    </div>
                  </div>
                )}

                <button className="btn btn-primary" onClick={submitVenta} disabled={saving} style={{ justifyContent: 'center', marginTop: 8 }}>
                  {saving ? 'Procesando…' : 'Realizar Venta'}
                </button>

                {result && (
                  <div style={{
                    marginTop: 16, padding: 16, borderRadius: 8,
                    background: result.error ? 'var(--danger-bg)' : 'var(--success-bg)',
                    border: `1px solid ${result.error ? 'var(--danger)' : 'var(--success)'}`,
                  }}>
                    {result.error ? (
                      <div style={{ color: 'var(--danger-text)' }}>⚠ {result.error}</div>
                    ) : (
                      <div>
                        <div style={{ fontWeight: 700, marginBottom: 8, color: 'var(--success-text)' }}>✅ Venta realizada</div>
                        <div style={{ fontSize: '.9rem' }}>Pedido: <strong>#{result.id_pedido}</strong></div>
                        <div style={{ fontSize: '.9rem' }}>Total: <strong>{priceFmt(result.total)}</strong></div>
                        {result.id_envio && <div style={{ fontSize: '.9rem' }}>Envío: #{result.id_envio}</div>}
                        {result.id_guia && <div style={{ fontSize: '.9rem' }}>Guía: #{result.id_guia}</div>}
                        {result.ticket && (
                          <div style={{ marginTop: 8, padding: 12, background: '#fff', borderRadius: 8, border: '1px solid #ddd', fontSize: '.85rem' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
                              <div style={{ fontWeight: 700 }}>🧾 TICKET</div>
                              <button className="btn btn-ghost btn-sm" onClick={() => printTicket(result.ticket)}>🖨</button>
                            </div>
                            <div>Folio: {result.ticket.folio}</div>
                            <div>Cliente: {result.ticket.cliente}</div>
                            <div>Vendedor: {result.ticket.vendedor}</div>
                            <div style={{ borderTop: '1px solid #eee', margin: '6px 0', paddingTop: 4 }}>
                              <div style={{ fontWeight: 600, marginBottom: 4 }}>Artículos:</div>
                              {Array.isArray(result.ticket.articulos) && result.ticket.articulos.map((a, i) => (
                                <div key={i} style={{ display: 'flex', justifyContent: 'space-between', paddingLeft: 8 }}>
                                  <span>{a.producto} x{a.cantidad}</span>
                                  <span>{priceFmt(a.subtotal)}</span>
                                </div>
                              ))}
                            </div>
                            <div>Subtotal: {priceFmt(result.ticket.subtotal)}</div>
                            <div>IVA (16%): {priceFmt(result.ticket.impuesto)}</div>
                            <div style={{ fontWeight: 700, borderTop: '1px solid #ddd', paddingTop: 4, marginTop: 4 }}>Total: {priceFmt(result.ticket.total)}</div>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>
        );

      case 'ventas':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Mis Ventas</h2></div>
            <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
              <table className="tbl">
                <thead><tr><th>ID</th><th>Fecha</th><th>Cliente</th><th>Subtotal</th><th>Total</th><th>Estatus</th></tr></thead>
                <tbody>
                  {misVentas.map(v => (
                    <tr key={v.id_pedido_cliente}>
                      <td>#{v.id_pedido_cliente}</td>
                      <td>{v.fecha}</td>
                      <td>{clientesMap[v.id_cliente] ? `${clientesMap[v.id_cliente].nombre} ${clientesMap[v.id_cliente].apellido}` : `ID ${v.id_cliente}`}</td>
                      <td>{priceFmt(v.subtotal)}</td>
                      <td>{priceFmt(v.total)}</td>
                      <td>{estatusBadge(v.estatus)}</td>
                    </tr>
                  ))}
                  {misVentas.length === 0 && <tr><td colSpan={6} style={{ textAlign: 'center', padding: 24 }}>Sin ventas registradas</td></tr>}
                </tbody>
              </table>
            </div>
          </div>
        );

      case 'clientes':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Clientes</h2></div>
            <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
              <table className="tbl">
                <thead><tr><th>ID</th><th>Nombre</th><th>Email</th><th>Teléfono</th><th>RFC</th><th>Estatus</th></tr></thead>
                <tbody>
                  {clientes.map(c => (
                    <tr key={c.id_cliente}>
                      <td>{c.id_cliente}</td>
                      <td>{c.nombre} {c.apellido}</td>
                      <td>{c.email || '—'}</td>
                      <td>{c.telefono || '—'}</td>
                      <td>{c.rfc || '—'}</td>
                      <td>{estatusBadge(c.estatus)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        );

      case 'guias':
        return (
          <div>
            <div className="page-header"><h2 className="page-title">Guías de Remisión</h2></div>
            {guias.length === 0 && (
              <div className="card" style={{ textAlign: 'center', padding: 32, color: 'var(--text-tertiary)' }}>Sin guías registradas</div>
            )}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
              {guias.map(g => (
                <div key={g.id_guia} className="card" style={{ padding: 16 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 12 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                      <span style={{ fontSize: '1.2rem' }}>📋</span>
                      <div>
                        <div style={{ fontWeight: 700 }}>Guía #{g.id_guia} — Pedido #{g.id_pedido_cliente}</div>
                        <div style={{ fontSize: '.82rem', color: 'var(--text-tertiary)' }}>{g.fecha_guia}</div>
                      </div>
                    </div>
                    {estatusBadge(g.estatus)}
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(180px, 1fr))', gap: 10, fontSize: '.88rem' }}>
                    <div>
                      <span style={{ color: 'var(--text-tertiary)', fontSize: '.75rem', textTransform: 'uppercase' }}>Vendedor</span>
                      <div style={{ fontWeight: 500 }}>{g.vendedor?.nombre} {g.vendedor?.apellido}</div>
                    </div>
                    <div>
                      <span style={{ color: 'var(--text-tertiary)', fontSize: '.75rem', textTransform: 'uppercase' }}>Cliente</span>
                      <div style={{ fontWeight: 500 }}>{g.cliente?.nombre} {g.cliente?.apellido}</div>
                    </div>
                    <div>
                      <span style={{ color: 'var(--text-tertiary)', fontSize: '.75rem', textTransform: 'uppercase' }}>Conductor</span>
                      <div style={{ fontWeight: 500 }}>{g.vendedor?.nombre || `ID ${g.id_conductor}`}</div>
                    </div>
                    <div>
                      <span style={{ color: 'var(--text-tertiary)', fontSize: '.75rem', textTransform: 'uppercase' }}>Vehículo</span>
                      <div style={{ fontWeight: 500 }}>{g.vehiculo?.marca} {g.vehiculo?.placa}</div>
                    </div>
                    <div>
                      <span style={{ color: 'var(--text-tertiary)', fontSize: '.75rem', textTransform: 'uppercase' }}>Almacén</span>
                      <div style={{ fontWeight: 500 }}>{g.almacen?.nombre}</div>
                    </div>
                  </div>
                  {g.detalles?.length > 0 && (
                    <div style={{ marginTop: 12, borderTop: '1px solid var(--border)', paddingTop: 10 }}>
                      <span style={{ color: 'var(--text-tertiary)', fontSize: '.75rem', textTransform: 'uppercase', marginBottom: 6, display: 'block' }}>Productos</span>
                      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                        {g.detalles.map((d, i) => (
                          <span key={i} style={{ background: 'var(--surface-2)', padding: '4px 10px', borderRadius: 6, fontSize: '.85rem' }}>
                            {d.producto} <strong>x{d.cantidad}</strong>
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
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
          <div style={{ width: 36, height: 36, borderRadius: 9, background: 'var(--info-bg)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '1rem' }}>👤</div>
          <h2 style={{ fontFamily: 'Syne,sans-serif', fontWeight: 800, fontSize: '1.3rem' }}>Panel de Vendedor</h2>
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
