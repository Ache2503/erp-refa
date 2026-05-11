import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Layout      from './components/Layout';
import LoginPage   from './pages/LoginPage';
import Dashboard   from './pages/Dashboard';
import EmpleadosPage   from './pages/EmpleadosPage';
import ClientesPage    from './pages/ClientesPage';
import ProveedoresPage from './pages/ProveedoresPage';
import ProductosPage   from './pages/ProductosPage';
import CategoriasPage  from './pages/CategoriasPage';
import MarcasPage      from './pages/MarcasPage';
import InventarioPage  from './pages/InventarioPage';
import ComprasPage     from './pages/ComprasPage';
import VentasPage      from './pages/VentasPage';
import PedidosPage     from './pages/PedidosPage';
import EnviosPage      from './pages/EnviosPage';
import TrasladosPage   from './pages/TrasladosPage';
import VehiculosPage   from './pages/VehiculosPage';
import AlmacenesPage   from './pages/AlmacenesPage';
import RolesPage       from './pages/RolesPage';
import VendedorDashboard from './pages/VendedorDashboard';
import ConductorDashboard from './pages/ConductorDashboard';
import AlmacenistaDashboard from './pages/AlmacenistaDashboard';
import ContadorDashboard from './pages/ContadorDashboard';
import GerenteDashboard from './pages/GerenteDashboard';
import AsignacionesPage from './pages/AsignacionesPage';

function PrivateRoute({ children }) {
  const { isAuth, ready } = useAuth();
  if (!ready) return (
    <div style={{minHeight:'100vh',display:'flex',alignItems:'center',justifyContent:'center',background:'#0d0f14'}}>
      <div style={{color:'rgba(255,255,255,.4)',fontSize:'.9rem'}}>Cargando sistema…</div>
    </div>
  );
  return isAuth ? children : <Navigate to="/login" replace />;
}

function getHomePath(user) {
  const role = user?.roles?.[0];
  switch (role) {
    case 'Vendedor': return '/vendedor';
    case 'Transportista': return '/conductor';
    default: return '/';
  }
}

function HomeRouter() {
  const { user } = useAuth();
  const role = user?.roles?.[0];
  switch (role) {
    case 'Vendedor': return <Navigate to="/vendedor" replace />;
    case 'Transportista': return <Navigate to="/conductor" replace />;
    case 'Almacenista': return <AlmacenistaDashboard />;
    case 'Contador': return <ContadorDashboard />;
    case 'Gerente': return <GerenteDashboard />;
    default: return <Dashboard />;
  }
}

function AppRoutes() {
  const { isAuth, user } = useAuth();
  return (
    <Routes>
      <Route path="/login" element={isAuth ? <Navigate to={getHomePath(user)} replace /> : <LoginPage />} />
      <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
        <Route index          element={<HomeRouter />} />
        <Route path="empleados"   element={<EmpleadosPage />} />
        <Route path="clientes"    element={<ClientesPage />} />
        <Route path="proveedores" element={<ProveedoresPage />} />
        <Route path="productos"   element={<ProductosPage />} />
        <Route path="categorias"  element={<CategoriasPage />} />
        <Route path="marcas"      element={<MarcasPage />} />
        <Route path="inventario"  element={<InventarioPage />} />
        <Route path="compras"     element={<ComprasPage />} />
        <Route path="ventas"      element={<VentasPage />} />
        <Route path="pedidos"     element={<PedidosPage />} />
        <Route path="envios"      element={<EnviosPage />} />
        <Route path="traslados"   element={<TrasladosPage />} />
        <Route path="vehiculos"   element={<VehiculosPage />} />
        <Route path="almacenes"   element={<AlmacenesPage />} />
        <Route path="roles"       element={<RolesPage />} />
        <Route path="vendedor"    element={<VendedorDashboard />} />
        <Route path="conductor"   element={<ConductorDashboard />} />
        <Route path="asignaciones" element={<AsignacionesPage />} />
        <Route path="*"           element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}
