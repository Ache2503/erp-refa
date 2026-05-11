/**
 * Componente genérico para páginas CRUD con tabla, búsqueda y modal de formulario.
 * Props:
 *   title, subtitle, icon, endpoint, columns, fields, emptyIcon, emptyText
 */
import { useState, useEffect, useCallback } from 'react';
import { api } from '../hooks/useApi';

export default function CrudPage({
  title, subtitle, icon, endpoint,
  columns, fields,
  emptyIcon = '📭', emptyText = 'No hay registros',
  idKey = null, // si null se auto-detecta
  deletable = true,
  refs = {},  // { key: { data: [{id, nombre}], idKey: 'id', labelKey: 'nombre' } }
}) {
  const [rows,    setRows]    = useState([]);
  const [loading, setLoading] = useState(true);
  const [search,  setSearch]  = useState('');
  const [modal,   setModal]   = useState(null); // null | 'create' | row (edit)
  const [form,    setForm]    = useState({});
  const [saving,  setSaving]  = useState(false);
  const [err,     setErr]     = useState('');
  const http = api();

  const lookupMaps = {};
  for (const [key, ref] of Object.entries(refs)) {
    const arr = Array.isArray(ref.data) ? ref.data : [];
    lookupMaps[key] = Object.fromEntries(
      arr.map(item => [item[ref.idKey || 'id'], item[ref.labelKey || 'nombre'] || item.nombre])
    );
  }

  const resolveVal = (col, val, row) => {
    if (col.render) return col.render(val, row);
    if (col.ref && lookupMaps[col.ref]) return lookupMaps[col.ref][val] ?? val;
    return val ?? '—';
  };

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const d = await http.get(endpoint);
      setRows(Array.isArray(d) ? d : d.data ?? []);
    } catch { setRows([]); }
    finally { setLoading(false); }
  }, [endpoint]);

  useEffect(() => { load(); }, [load]);

  const detectId = row => {
    if (idKey) return row[idKey];
    const k = Object.keys(row).find(k => k.startsWith('id_'));
    return k ? row[k] : row.id;
  };

  const openCreate = () => {
    const defaults = {};
    fields.forEach(f => { defaults[f.name] = f.default ?? ''; });
    setForm(defaults); setErr(''); setModal('create');
  };

  const openEdit = row => {
    const vals = {};
    fields.forEach(f => { vals[f.name] = row[f.name] ?? f.default ?? ''; });
    setForm(vals); setErr(''); setModal(row);
  };

  const save = async () => {
    setSaving(true); setErr('');
    try {
      if (modal === 'create') {
        await http.post(endpoint, form);
      } else {
        const id = detectId(modal);
        await http.put(`${endpoint}/${id}`, form);
      }
      setModal(null); load();
    } catch(e) { setErr(e.message); }
    finally { setSaving(false); }
  };

  const remove = async row => {
    if (!confirm('¿Eliminar este registro?')) return;
    const id = detectId(row);
    try { await http.del(`${endpoint}/${id}`); load(); }
    catch(e) { alert(e.message); }
  };

  const filtered = rows.filter(r =>
    JSON.stringify(r).toLowerCase().includes(search.toLowerCase())
  );

  const setF = k => e => setForm(p => ({...p, [k]: e.target.value}));

  return (
    <div>
      {/* Header */}
      <div className="page-header anim-fade-up">
        <div>
          <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:3}}>
            <div style={{
              width:36,height:36,borderRadius:9,
              background:'var(--info-bg)',
              display:'flex',alignItems:'center',justifyContent:'center',fontSize:'1rem',
            }}>{icon}</div>
            <h2 className="page-title">{title}</h2>
          </div>
          {subtitle && <p className="page-sub">{subtitle}</p>}
        </div>
        <button className="btn btn-primary" onClick={openCreate}>
          + Nuevo
        </button>
      </div>

      {/* Tabla */}
      <div className="card anim-fade-up d2" style={{padding:0,overflow:'hidden'}}>
        {/* Toolbar */}
        <div style={{
          display:'flex',alignItems:'center',gap:12,
          padding:'14px 18px',borderBottom:'1px solid var(--border)',
        }}>
          <div style={{position:'relative',flex:1,maxWidth:280}}>
            <input className="inp inp-sm" placeholder={`Buscar en ${title.toLowerCase()}…`}
              value={search} onChange={e=>setSearch(e.target.value)}
              style={{paddingLeft:28}}/>
            <span style={{position:'absolute',left:9,top:'50%',transform:'translateY(-50%)',fontSize:'.8rem',color:'var(--text-tertiary)'}}>🔍</span>
          </div>
          <span style={{fontSize:'.8rem',color:'var(--text-secondary)',marginLeft:'auto'}}>
            {filtered.length} registros
          </span>
          <button className="btn btn-ghost btn-sm" onClick={load}>↻ Actualizar</button>
        </div>

        {/* Contenido */}
        {loading ? (
          <div style={{padding:48,textAlign:'center',color:'var(--text-tertiary)',fontSize:'.9rem'}}>
            Cargando…
          </div>
        ) : filtered.length === 0 ? (
          <div className="empty-state">
            <div className="es-icon">{emptyIcon}</div>
            <div className="es-title">{emptyText}</div>
            <div className="es-sub">Haz clic en "+ Nuevo" para agregar el primero</div>
          </div>
        ) : (
          <div style={{overflowX:'auto'}}>
            <table className="tbl">
              <thead>
                <tr>
                  {columns.map(c => <th key={c.key}>{c.label}</th>)}
                  <th style={{textAlign:'right'}}>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((row, i) => (
                  <tr key={i}>
                    {columns.map(c => (
                      <td key={c.key}>
                        {resolveVal(c, row[c.key], row)}
                      </td>
                    ))}
                    <td style={{textAlign:'right'}}>
                      <div style={{display:'flex',gap:6,justifyContent:'flex-end'}}>
                        <button className="btn btn-ghost btn-sm" onClick={() => openEdit(row)}>✏ Editar</button>
                        {deletable && (
                          <button className="btn btn-danger btn-sm" onClick={() => remove(row)}>🗑</button>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Modal */}
      {modal && (
        <div className="overlay" onClick={e => e.target===e.currentTarget && setModal(null)}>
          <div className="modal">
            <div className="modal-title">
              {modal === 'create' ? `Nuevo ${title.slice(0,-1)||title}` : `Editar registro`}
            </div>
            <div style={{display:'grid',gap:14}}>
              {fields.map(f => (
                <div key={f.name}>
                  <label className="lbl">{f.label.toUpperCase()}</label>
                  {f.type === 'select' ? (
                    <select className="inp" value={form[f.name]} onChange={setF(f.name)}>
                      {f.options.map(o => (
                        <option key={o.value} value={o.value}>{o.label}</option>
                      ))}
                    </select>
                  ) : f.type === 'textarea' ? (
                    <textarea className="inp" rows={3} value={form[f.name]}
                      onChange={setF(f.name)} placeholder={f.placeholder||''} />
                  ) : (
                    <input className="inp" type={f.type||'text'}
                      value={form[f.name]} onChange={setF(f.name)}
                      placeholder={f.placeholder||''} required={f.required}/>
                  )}
                </div>
              ))}
            </div>
            {err && (
              <div style={{marginTop:14,background:'var(--danger-bg)',border:'1px solid #fecaca',
                borderRadius:8,padding:'9px 12px',color:'var(--danger-text)',fontSize:'.83rem'}}>
                ⚠ {err}
              </div>
            )}
            <div style={{display:'flex',gap:10,justifyContent:'flex-end',marginTop:22}}>
              <button className="btn btn-ghost" onClick={() => setModal(null)}>Cancelar</button>
              <button className="btn btn-primary" onClick={save} disabled={saving}>
                {saving ? 'Guardando…' : modal==='create' ? 'Crear' : 'Guardar cambios'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
