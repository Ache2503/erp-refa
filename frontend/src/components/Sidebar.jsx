import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ALL_MENU = [
  { group:'General',    items:[{to:'/',label:'Dashboard',ic:'⊞',end:true}] },
  { group:'Personas',   items:[{to:'/empleados',label:'Empleados',ic:'👤'},{to:'/clientes',label:'Clientes',ic:'🏢'},{to:'/proveedores',label:'Proveedores',ic:'🏭'}] },
  { group:'Catálogo',   items:[{to:'/productos',label:'Productos',ic:'📦'},{to:'/categorias',label:'Categorías',ic:'🏷'},{to:'/marcas',label:'Marcas',ic:'✦'}] },
  { group:'Operaciones',items:[{to:'/inventario',label:'Inventario',ic:'🗃'},{to:'/compras',label:'Compras',ic:'🛒'},{to:'/ventas',label:'Ventas',ic:'💳'},{to:'/pedidos',label:'Pedidos',ic:'📋'}] },
  { group:'Logística',  items:[{to:'/logistica',label:'Dashboard Log.',ic:'📊',end:true},{to:'/envios',label:'Envíos',ic:'🚚'},{to:'/asignaciones',label:'Asignar Envíos',ic:'📋'},{to:'/traslados',label:'Traslados',ic:'🔄'},{to:'/vehiculos',label:'Vehículos',ic:'🚛'},{to:'/almacenes',label:'Almacenes',ic:'🏬'}] },
  { group:'Ventas',     items:[{to:'/vendedor',label:'Vendedor',ic:'👤'},{to:'/conductor',label:'Conductor',ic:'🚚'}] },
  { group:'Sistema',    items:[{to:'/roles',label:'Roles',ic:'🔑'}] },
];

const ROLE_MENU = {
  Administrador: ALL_MENU,
  Vendedor: [
    { group:'Ventas',     items:[{to:'/vendedor',label:'Panel Vendedor',ic:'👤',end:true}] },
    { group:'Personas',   items:[{to:'/clientes',label:'Clientes',ic:'🏢'}] },
    { group:'Catálogo',   items:[{to:'/productos',label:'Productos',ic:'📦'}] },
    { group:'Logística',  items:[{to:'/asignaciones',label:'Asignar Envíos',ic:'📋'}] },
  ],
  Transportista: [
    { group:'General',    items:[{to:'/conductor',label:'Panel Conductor',ic:'⊞',end:true}] },
    { group:'Logística',  items:[{to:'/envios',label:'Envíos',ic:'🚚'}] },
  ],
  Almacenista: [
    { group:'General',    items:[{to:'/',label:'Dashboard',ic:'⊞',end:true}] },
    { group:'Catálogo',   items:[{to:'/productos',label:'Productos',ic:'📦'}] },
    { group:'Operaciones',items:[{to:'/inventario',label:'Inventario',ic:'🗃'},{to:'/compras',label:'Compras',ic:'🛒'}] },
    { group:'Logística',  items:[{to:'/traslados',label:'Traslados',ic:'🔄'},{to:'/almacenes',label:'Almacenes',ic:'🏬'}] },
  ],
  Contador: [
    { group:'General',    items:[{to:'/',label:'Dashboard',ic:'⊞',end:true}] },
    { group:'Operaciones',items:[{to:'/ventas',label:'Ventas',ic:'💳'},{to:'/compras',label:'Compras',ic:'🛒'}] },
  ],
  Gerente: ALL_MENU,
};

export default function Sidebar() {
  const { user, logout } = useAuth();
  const initials = user?.username?.[0]?.toUpperCase() || 'U';
  const role = user?.roles?.[0];
  const menu = ROLE_MENU[role] || ALL_MENU;

  return (
    <aside className="sidebar">
      <div style={{padding:'18px 14px 14px',borderBottom:'1px solid rgba(255,255,255,.05)'}}>
        <div style={{display:'flex',alignItems:'center',gap:9}}>
          <div style={{
            width:30,height:30,borderRadius:7,flexShrink:0,
            background:'linear-gradient(135deg,#6366f1,#818cf8)',
            display:'flex',alignItems:'center',justifyContent:'center',fontSize:'.85rem',
          }}>⬡</div>
          <span className="sidebar-logo-text">ERP Logístico</span>
        </div>
      </div>

      <nav style={{flex:1,overflowY:'auto',padding:'6px 8px'}}>
        {menu.map(({group,items})=>(
          <div key={group}>
            <div className="nav-group-label">{group}</div>
            {items.map(({to,label,ic,end})=>(
              <NavLink key={to} to={to} end={end}
                className={({isActive})=>`nav-item${isActive?' active':''}`}>
                <span className="nav-ic" style={{fontSize:'.88rem',width:16,textAlign:'center'}}>{ic}</span>
                <span>{label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </nav>

      <div style={{padding:'10px 12px',borderTop:'1px solid rgba(255,255,255,.05)'}}>
        <div style={{display:'flex',alignItems:'center',gap:9,marginBottom:8}}>
          <div style={{
            width:30,height:30,borderRadius:'50%',flexShrink:0,
            background:'linear-gradient(135deg,#6366f1,#a78bfa)',
            display:'flex',alignItems:'center',justifyContent:'center',
            fontSize:'.75rem',fontWeight:700,color:'#fff',
          }}>{initials}</div>
          <div style={{overflow:'hidden'}}>
            <div style={{fontSize:'.8rem',fontWeight:600,color:'#fff',whiteSpace:'nowrap',overflow:'hidden',textOverflow:'ellipsis'}}>
              {user?.nombre_empleado || user?.username}
            </div>
            <div style={{fontSize:'.7rem',color:'rgba(255,255,255,.3)'}}>
              {user?.cargo || user?.roles?.[0] || 'Sistema'}
            </div>
          </div>
        </div>
        <button className="nav-item" onClick={logout}
          style={{color:'rgba(255,90,90,.65)',padding:'6px 10px',fontSize:'.8rem'}}>
          <span>⎋</span><span>Cerrar sesión</span>
        </button>
      </div>
    </aside>
  );
}
