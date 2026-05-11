import { useState } from 'react';
import { useAuth } from '../context/AuthContext';

export default function LoginPage() {
  const { login } = useAuth();
  const [form, setForm]   = useState({ username:'', password:'' });
  const [err,  setErr]    = useState('');
  const [busy, setBusy]   = useState(false);

  const submit = async e => {
    e.preventDefault(); setBusy(true); setErr('');
    try {
      const res = await fetch('http://localhost:8000/auth/login', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify(form),
      });
      if (!res.ok) { const d=await res.json(); throw new Error(d.detail||'Error'); }
      const d = await res.json();
      login(d.access_token, d.user);
    } catch(e) { setErr(e.message); }
    finally { setBusy(false); }
  };

  const set = k => e => setForm(p=>({...p,[k]:e.target.value}));

  return (
    <div className="login-wrap">
      {/* Panel izquierdo */}
      <div className="login-left">
        <div className="login-glow"/>
        <div className="login-glow2"/>
        <div style={{position:'relative',zIndex:1}}>
          <div style={{display:'flex',alignItems:'center',gap:10,marginBottom:10}}>
            <div style={{
              width:38,height:38,borderRadius:10,
              background:'linear-gradient(135deg,#6366f1,#818cf8)',
              display:'flex',alignItems:'center',justifyContent:'center',
              fontSize:'1.1rem',
            }}>⬡</div>
            <span className="sidebar-logo-text" style={{fontSize:'1.2rem'}}>ERP Logístico</span>
          </div>
          <p style={{color:'rgba(255,255,255,.35)',fontSize:'.88rem',marginBottom:52}}>
            Sistema de gestión empresarial
          </p>

          {[
            ['📦','Control de inventario por almacén'],
            ['🚚','Gestión de envíos y logística'],
            ['📊','Dashboard con métricas en tiempo real'],
            ['🔐','Autenticación segura con JWT'],
            ['🔄','Traslados internos y devoluciones'],
          ].map(([ic,lb],i)=>(
            <div key={i} style={{
              display:'flex',alignItems:'center',gap:12,marginBottom:16,
              animation:`slideInLeft .4s ease ${i*.07}s both`,
            }}>
              <div style={{
                width:34,height:34,borderRadius:8,flexShrink:0,
                background:'rgba(99,102,241,.15)',
                border:'1px solid rgba(99,102,241,.25)',
                display:'flex',alignItems:'center',justifyContent:'center',
                fontSize:'.9rem',
              }}>{ic}</div>
              <span style={{color:'rgba(255,255,255,.6)',fontSize:'.87rem'}}>{lb}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Formulario */}
      <div className="login-right">
        <div style={{width:'100%',maxWidth:380,animation:'fadeUp .4s ease'}}>
          <h1 style={{
            fontFamily:'Syne,sans-serif',fontWeight:800,
            fontSize:'2rem',letterSpacing:'-0.03em',marginBottom:6,
          }}>Bienvenido</h1>
          <p style={{color:'var(--text-secondary)',fontSize:'.9rem',marginBottom:32}}>
            Ingresa tus credenciales para acceder al sistema
          </p>

          <form onSubmit={submit}>
            <div style={{marginBottom:14}}>
              <label className="lbl">USUARIO</label>
              <input className="inp" placeholder="admin" value={form.username}
                onChange={set('username')} required />
            </div>
            <div style={{marginBottom:22}}>
              <label className="lbl">CONTRASEÑA</label>
              <input className="inp" type="password" placeholder="••••••••"
                value={form.password} onChange={set('password')} required />
            </div>

            {err && (
              <div style={{
                background:'var(--danger-bg)',border:'1px solid #fecaca',
                borderRadius:8,padding:'10px 14px',color:'var(--danger-text)',
                fontSize:'.85rem',marginBottom:16,
              }}>⚠ {err}</div>
            )}

            <button className="btn btn-primary" type="submit" disabled={busy}
              style={{width:'100%',justifyContent:'center',padding:'11px 0',fontSize:'.95rem'}}>
              {busy ? 'Ingresando…' : 'Ingresar al sistema →'}
            </button>
          </form>

          <p style={{textAlign:'center',marginTop:28,fontSize:'.76rem',color:'var(--text-tertiary)'}}>
            ERP Logístico v2.0 · Solo personal autorizado
          </p>
        </div>
      </div>
    </div>
  );
}
