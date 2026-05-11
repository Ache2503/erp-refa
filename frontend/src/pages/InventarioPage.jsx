import { useState, useEffect } from 'react';
import { api } from '../hooks/useApi';

export default function InventarioPage() {
  const [rows,    setRows]    = useState([]);
  const [loading, setLoading] = useState(true);
  const [search,  setSearch]  = useState('');
  const [modal,   setModal]   = useState(false);
  const [form,    setForm]    = useState({ id_producto:'', id_almacen:'', cantidad:'' });
  const [saving,  setSaving]  = useState(false);
  const [err,     setErr]     = useState('');
  const [productos, setProductos] = useState([]);
  const [almacenes, setAlmacenes] = useState([]);
  const http = api();

  const prodMap = Object.fromEntries(productos.map(p => [p.id_producto, p.nombre]));
  const almMap  = Object.fromEntries(almacenes.map(a => [a.id_almacen, a.nombre]));

  const load = async () => {
    setLoading(true);
    try {
      const [d, p, a] = await Promise.allSettled([
        http.get('/inventario'),
        http.get('/productos'),
        http.get('/almacenes'),
      ]);
      if (d.status === 'fulfilled') setRows(Array.isArray(d.value) ? d.value : d.value?.data ?? []);
      if (p.status === 'fulfilled') setProductos(Array.isArray(p.value) ? p.value : p.value?.data ?? []);
      if (a.status === 'fulfilled') setAlmacenes(Array.isArray(a.value) ? a.value : a.value?.data ?? []);
    } catch { setRows([]); }
    finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const filtered = rows.filter(r =>
    JSON.stringify(r).toLowerCase().includes(search.toLowerCase())
  );

  const stockColor = q => q === 0 ? 'var(--danger)' : q < 10 ? 'var(--warning)' : 'var(--success)';
  const stockBadge = q => q === 0
    ? <span className="badge badge-red">Sin stock</span>
    : q < 10
      ? <span className="badge badge-yellow">Stock bajo</span>
      : <span className="badge badge-green">OK</span>;

  const save = async () => {
    setSaving(true); setErr('');
    try { await http.post('/inventario', {...form, cantidad:Number(form.cantidad)}); setModal(false); load(); }
    catch(e) { setErr(e.message); }
    finally { setSaving(false); }
  };

  return (
    <div>
      <div className="page-header anim-fade-up">
        <div>
          <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:3}}>
            <div style={{width:36,height:36,borderRadius:9,background:'#fef3c7',display:'flex',alignItems:'center',justifyContent:'center',fontSize:'1rem'}}>🗃</div>
            <h2 className="page-title">Inventario</h2>
          </div>
          <p className="page-sub">Stock de productos por almacén</p>
        </div>
        <button className="btn btn-primary" onClick={() => { setForm({id_producto:'',id_almacen:'',cantidad:''}); setErr(''); setModal(true); }}>
          + Agregar stock
        </button>
      </div>

      <div className="grid-3 anim-fade-up d2" style={{marginBottom:20}}>
        {[
          { label:'Total registros', value: rows.length, icon:'📊', color:'#6366f1', bg:'#e0e7ff' },
          { label:'Sin stock',       value: rows.filter(r=>r.cantidad===0).length, icon:'⚠',  color:'var(--danger)', bg:'var(--danger-bg)' },
          { label:'Stock bajo (<10)',value: rows.filter(r=>r.cantidad>0&&r.cantidad<10).length, icon:'📉', color:'var(--warning)', bg:'var(--warning-bg)' },
        ].map(({label,value,icon,color,bg}) => (
          <div key={label} className="stat-card">
            <div style={{display:'flex',alignItems:'center',gap:12}}>
              <div className="stat-icon" style={{background:bg}}><span>{icon}</span></div>
              <div>
                <div style={{fontSize:'1.6rem',fontWeight:800,fontFamily:'Syne,sans-serif',color,lineHeight:1}}>{loading?'…':value}</div>
                <div style={{fontSize:'.8rem',color:'var(--text-secondary)',marginTop:3}}>{label}</div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="card anim-fade-up d3" style={{padding:0,overflow:'hidden'}}>
        <div style={{display:'flex',alignItems:'center',gap:12,padding:'14px 18px',borderBottom:'1px solid var(--border)'}}>
          <div style={{position:'relative',flex:1,maxWidth:280}}>
            <input className="inp inp-sm" placeholder="Buscar producto o almacén…"
              value={search} onChange={e=>setSearch(e.target.value)} style={{paddingLeft:28}}/>
            <span style={{position:'absolute',left:9,top:'50%',transform:'translateY(-50%)',fontSize:'.8rem',color:'var(--text-tertiary)'}}>🔍</span>
          </div>
          <span style={{fontSize:'.8rem',color:'var(--text-secondary)',marginLeft:'auto'}}>{filtered.length} registros</span>
          <button className="btn btn-ghost btn-sm" onClick={load}>↻</button>
        </div>

        {loading ? (
          <div style={{padding:48,textAlign:'center',color:'var(--text-tertiary)'}}>Cargando…</div>
        ) : filtered.length === 0 ? (
          <div className="empty-state"><div className="es-icon">🗃</div><div className="es-title">Sin registros de inventario</div></div>
        ) : (
          <div style={{overflowX:'auto'}}>
            <table className="tbl">
              <thead>
                <tr>
                  <th>ID</th><th>Producto</th><th>Almacén</th>
                  <th>Cantidad</th><th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r,i) => (
                  <tr key={i}>
                    <td style={{color:'var(--text-tertiary)',fontSize:'.8rem'}}>#{r.id_inventario||r.id}</td>
                    <td style={{fontWeight:600}}>{prodMap[r.id_producto] || `Producto #${r.id_producto}`}</td>
                    <td>{almMap[r.id_almacen] || `Almacén #${r.id_almacen}`}</td>
                    <td>
                      <span style={{fontWeight:700,fontSize:'1rem',color:stockColor(r.cantidad)}}>
                        {r.cantidad}
                      </span>
                      <span style={{color:'var(--text-tertiary)',fontSize:'.78rem',marginLeft:4}}>uds</span>
                    </td>
                    <td>{stockBadge(r.cantidad)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {modal && (
        <div className="overlay" onClick={e=>e.target===e.currentTarget&&setModal(false)}>
          <div className="modal">
            <div className="modal-title">Agregar / Ajustar stock</div>
            <div style={{marginBottom:14}}>
              <label className="lbl">PRODUCTO</label>
              <select className="inp" value={form.id_producto} onChange={e=>setForm(p=>({...p,id_producto:e.target.value}))}>
                <option value="">Seleccionar producto…</option>
                {productos.map(p => <option key={p.id_producto} value={p.id_producto}>{p.nombre}</option>)}
              </select>
            </div>
            <div style={{marginBottom:14}}>
              <label className="lbl">ALMACÉN</label>
              <select className="inp" value={form.id_almacen} onChange={e=>setForm(p=>({...p,id_almacen:e.target.value}))}>
                <option value="">Seleccionar almacén…</option>
                {almacenes.map(a => <option key={a.id_almacen} value={a.id_almacen}>{a.nombre}</option>)}
              </select>
            </div>
            <div style={{marginBottom:14}}>
              <label className="lbl">CANTIDAD</label>
              <input className="inp" type="number" value={form.cantidad}
                onChange={e=>setForm(p=>({...p,cantidad:e.target.value}))}/>
            </div>
            {err&&<div style={{background:'var(--danger-bg)',border:'1px solid #fecaca',borderRadius:8,padding:'9px 12px',color:'var(--danger-text)',fontSize:'.83rem',marginBottom:14}}>⚠ {err}</div>}
            <div style={{display:'flex',gap:10,justifyContent:'flex-end',marginTop:8}}>
              <button className="btn btn-ghost" onClick={()=>setModal(false)}>Cancelar</button>
              <button className="btn btn-primary" onClick={save} disabled={saving}>{saving?'Guardando…':'Guardar'}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
