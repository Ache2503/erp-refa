import { useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const TITLES = {
  '/':'/Dashboard','//':'Dashboard','/empleados':'Empleados','/clientes':'Clientes',
  '/proveedores':'Proveedores','/productos':'Productos','/categorias':'Categorías',
  '/marcas':'Marcas','/inventario':'Inventario','/compras':'Compras',
  '/ventas':'Ventas','/pedidos':'Pedidos','/envios':'Envíos',
  '/traslados':'Traslados Internos','/vehiculos':'Vehículos',
  '/almacenes':'Almacenes','/roles':'Roles y Permisos',
  '/vendedor':'Panel Vendedor','/conductor':'Panel Conductor',
};

export default function Topbar() {
  const { pathname } = useLocation();
  const { user } = useAuth();
  const title = TITLES[pathname] || 'ERP';

  return (
    <div className="topbar">
      <div style={{flex:1}}>
        <h1 style={{fontFamily:'Syne,sans-serif',fontWeight:800,fontSize:'1.05rem',letterSpacing:'-0.02em'}}>
          {title}
        </h1>
      </div>
      <div style={{position:'relative'}}>
        <input className="inp inp-sm" placeholder="Buscar…"
          style={{width:190,paddingLeft:30,background:'var(--surface-2)'}}/>
        <span style={{position:'absolute',left:9,top:'50%',transform:'translateY(-50%)',fontSize:'.82rem',color:'var(--text-tertiary)'}}>🔍</span>
      </div>
      <div style={{
        display:'flex',alignItems:'center',gap:8,
        padding:'5px 11px',borderRadius:8,
        background:'var(--surface-2)',border:'1px solid var(--border)',
      }}>
        <div style={{
          width:24,height:24,borderRadius:'50%',
          background:'linear-gradient(135deg,#6366f1,#a78bfa)',
          display:'flex',alignItems:'center',justifyContent:'center',
          fontSize:'.7rem',fontWeight:700,color:'#fff',
        }}>{user?.username?.[0]?.toUpperCase()||'U'}</div>
        <span style={{fontSize:'.82rem',fontWeight:500,color:'var(--text-secondary)'}}>
          {user?.username}
        </span>
      </div>
    </div>
  );
}
