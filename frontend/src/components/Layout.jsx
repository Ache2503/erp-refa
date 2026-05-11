import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Topbar from './Topbar';

export default function Layout() {
  return (
    <div style={{display:'flex'}}>
      <Sidebar/>
      <div className="main-wrap" style={{flex:1}}>
        <Topbar/>
        <main className="page-wrap"><Outlet/></main>
      </div>
    </div>
  );
}
