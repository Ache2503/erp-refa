import { createContext, useContext, useState, useEffect } from 'react';
const Ctx = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser]   = useState(null);
  const [token, setToken] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const t = sessionStorage.getItem('erp_tk');
    const u = sessionStorage.getItem('erp_usr');
    if (t && u) { setToken(t); setUser(JSON.parse(u)); }
    setReady(true);
  }, []);

  const login = (tk, usr) => {
    setToken(tk); setUser(usr);
    sessionStorage.setItem('erp_tk', tk);
    sessionStorage.setItem('erp_usr', JSON.stringify(usr));
  };
  const logout = () => {
    setToken(null); setUser(null);
    sessionStorage.removeItem('erp_tk');
    sessionStorage.removeItem('erp_usr');
  };

  return (
    <Ctx.Provider value={{ user, token, login, logout, ready, isAuth: !!token }}>
      {children}
    </Ctx.Provider>
  );
}
export const useAuth = () => useContext(Ctx);
