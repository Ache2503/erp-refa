import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { api } from '../hooks/useApi';

const STATS = [
  { key:'empleados', label:'Empleados', icon:'👤', color:'#6366f1', bg:'#e0e7ff', path:'/empleados' },
  { key:'clientes',  label:'Clientes',  icon:'🏢', color:'#10b981', bg:'#d1fae5', path:'/clientes' },
  { key:'productos', label:'Productos', icon:'📦', color:'#f59e0b', bg:'#fef3c7', path:'/productos' },
  { key:'proveedores',label:'Proveedores',icon:'🏭',color:'#8b5cf6',bg:'#ede9fe',path:'/proveedores'},
];

const ACTIVIDAD = [
  { tipo:'Venta',     desc:'Pedido #1042 procesado',        tiempo:'Hace 5 min',  badge:'badge-green' },
  { tipo:'Envío',     desc:'Guía #8821 en tránsito',        tiempo:'Hace 18 min', badge:'badge-blue'  },
  { tipo:'Compra',    desc:'OC #305 recibida de proveedor', tiempo:'Hace 1h',     badge:'badge-yellow'},
  { tipo:'Traslado',  desc:'Traslado Almacén A → B',        tiempo:'Hace 2h',     badge:'badge-gray'  },
  { tipo:'Devolución',desc:'Devolución cliente #88',        tiempo:'Hace 3h',     badge:'badge-red'   },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [counts, setCounts] = useState({});
  const [loading, setLoading] = useState(true);
  const http = api();

  const cerrarSesion = () => { logout(); navigate('/login'); };

  useEffect(() => {
    const endpoints = [
      ['empleados', '/empleados'],
      ['clientes',  '/clientes'],
      ['productos', '/productos'],
      ['proveedores','/proveedores'],
    ];
    Promise.allSettled(endpoints.map(([k,p]) => http.get(p).then(d => [k, Array.isArray(d) ? d.length : d.total ?? '—'])))
      .then(res => {
        const c = {};
        res.forEach(r => { if (r.status==='fulfilled') c[r.value[0]] = r.value[1]; });
        setCounts(c);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div>
      {/* Header */}
      <div style={{marginBottom:26, display:'flex', justifyContent:'space-between', alignItems:'flex-start'}}>
        <div>
          <h2 style={{fontFamily:'Syne,sans-serif',fontWeight:800,fontSize:'1.55rem',letterSpacing:'-0.03em'}}>
            Buen día 👋
          </h2>
          <p style={{color:'var(--text-secondary)',fontSize:'.88rem',marginTop:3}}>
            Aquí está el resumen de operaciones del sistema
          </p>
        </div>
        <button className="btn btn-ghost btn-sm" onClick={cerrarSesion} style={{color:'rgba(255,90,90,.7)'}}>
          ⎋ Cerrar sesión
        </button>
      </div>

      {/* Stats */}
      <div className="grid-4" style={{marginBottom:24}}>
        {STATS.map(({key,label,icon,color,bg},i) => (
          <div key={key} className={`stat-card anim-fade-up d${i+1}`}>
            <div style={{display:'flex',alignItems:'flex-start',justifyContent:'space-between',marginBottom:14}}>
              <div className="stat-icon" style={{background:bg}}>
                <span style={{fontSize:'1.05rem'}}>{icon}</span>
              </div>
              <span style={{fontSize:'.72rem',fontWeight:600,color:'var(--success)',background:'var(--success-bg)',padding:'2px 8px',borderRadius:99}}>
                ↑ activos
              </span>
            </div>
            <div style={{fontSize:'1.9rem',fontWeight:800,fontFamily:'Syne,sans-serif',color,letterSpacing:'-0.04em',lineHeight:1}}>
              {loading ? '…' : (counts[key] ?? '—')}
            </div>
            <div style={{fontSize:'.82rem',color:'var(--text-secondary)',marginTop:5,fontWeight:500}}>{label}</div>
          </div>
        ))}
      </div>

      {/* Segunda fila */}
      <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:20,marginBottom:20}}>

        {/* Actividad reciente */}
        <div className="card anim-fade-up d3">
          <div style={{display:'flex',alignItems:'center',justifyContent:'space-between',marginBottom:18}}>
            <div>
              <div style={{fontWeight:700,fontSize:'.95rem'}}>Actividad reciente</div>
              <div style={{fontSize:'.78rem',color:'var(--text-secondary)',marginTop:2}}>Últimos movimientos del sistema</div>
            </div>
            <span style={{fontSize:'.75rem',color:'var(--accent)',fontWeight:600,cursor:'pointer'}}>Ver todo →</span>
          </div>
          {ACTIVIDAD.map((a,i) => (
            <div key={i} style={{
              display:'flex',alignItems:'center',gap:12,
              padding:'10px 0',
              borderBottom: i<ACTIVIDAD.length-1 ? '1px solid var(--border)' : 'none',
            }}>
              <span className={`badge ${a.badge}`}>{a.tipo}</span>
              <div style={{flex:1,fontSize:'.83rem'}}>{a.desc}</div>
              <div style={{fontSize:'.75rem',color:'var(--text-tertiary)',whiteSpace:'nowrap'}}>{a.tiempo}</div>
            </div>
          ))}
        </div>

        {/* Estado del sistema */}
        <div className="card anim-fade-up d4">
          <div style={{fontWeight:700,fontSize:'.95rem',marginBottom:4}}>Estado del sistema</div>
          <div style={{fontSize:'.78rem',color:'var(--text-secondary)',marginBottom:18}}>Módulos y su disponibilidad</div>
          {[
            {label:'API Backend',     ok:true,  detail:'FastAPI · puerto 8000'},
            {label:'Base de datos',   ok:true,  detail:'MySQL 8 · gestion'},
            {label:'Autenticación',   ok:true,  detail:'JWT · 30 min expiración'},
            {label:'Cola de tareas',  ok:false, detail:'Celery / Redis · pendiente'},
            {label:'Almacenamiento',  ok:true,  detail:'Local · Docker volume'},
          ].map(({label,ok,detail},i) => (
            <div key={i} style={{
              display:'flex',alignItems:'center',gap:12,
              padding:'10px 0',
              borderBottom:i<4?'1px solid var(--border)':'none',
            }}>
              <div style={{
                width:8,height:8,borderRadius:'50%',flexShrink:0,
                background: ok ? 'var(--success)' : 'var(--warning)',
                boxShadow: ok ? '0 0 6px rgba(16,185,129,.5)' : '0 0 6px rgba(245,158,11,.5)',
              }}/>
              <div style={{flex:1}}>
                <div style={{fontSize:'.85rem',fontWeight:600}}>{label}</div>
                <div style={{fontSize:'.75rem',color:'var(--text-tertiary)'}}>{detail}</div>
              </div>
              <span className={`badge ${ok?'badge-green':'badge-yellow'}`}>{ok?'Online':'Pendiente'}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Accesos rápidos */}
      <div className="card anim-fade-up d5">
        <div style={{fontWeight:700,fontSize:'.95rem',marginBottom:16}}>Accesos rápidos</div>
        <div style={{display:'flex',gap:10,flexWrap:'wrap'}}>
          {[
            {label:'Nuevo empleado',  icon:'👤', path:'/empleados'},
            {label:'Registrar venta', icon:'💳', path:'/ventas'},
            {label:'Nueva compra',    icon:'🛒', path:'/compras'},
            {label:'Ver inventario',  icon:'🗃', path:'/inventario'},
            {label:'Nuevo envío',     icon:'🚚', path:'/envios'},
            {label:'Traslado',        icon:'🔄', path:'/traslados'},
          ].map(({label,icon,path}) => (
            <a key={path} href={path} className="btn btn-ghost" style={{fontSize:'.82rem'}}>
              {icon} {label}
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
