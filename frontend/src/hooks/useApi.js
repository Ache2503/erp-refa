const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function api() {
  const tk = sessionStorage.getItem('erp_tk');
  const h  = { 'Content-Type':'application/json', ...(tk ? {Authorization:`Bearer ${tk}`} : {}) };

  const req = async (method, path, body) => {
    const res = await fetch(`${BASE}${path}`, {
      method, headers: h,
      ...(body ? { body: JSON.stringify(body) } : {}),
    });
    if (res.status === 204) return null;
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || `Error ${res.status}`);
    return data;
  };

  return {
    get:  (path)       => req('GET',    path),
    post: (path, body) => req('POST',   path, body),
    put:   (path, body) => req('PUT',    path, body),
    patch: (path, body) => req('PATCH',  path, body),
    del:   (path)       => req('DELETE', path),
  };
}
