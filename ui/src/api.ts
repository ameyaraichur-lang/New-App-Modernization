const KEY = 'appmod_token';

export const getToken = () => localStorage.getItem(KEY) ?? '';
export const setToken = (t: string) => (t ? localStorage.setItem(KEY, t) : localStorage.removeItem(KEY));

export class ApiError extends Error {
  constructor(public status: number, message: string) { super(message); }
}

export async function api<T = unknown>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  const tok = getToken();
  if (tok) headers.set('Authorization', `Bearer ${tok}`);
  if (init.body && !headers.has('Content-Type')) headers.set('Content-Type', 'application/json');
  const r = await fetch(path, { ...init, headers });
  if (!r.ok) {
    const body = await r.json().catch(() => ({ detail: r.statusText }));
    throw new ApiError(r.status, typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail));
  }
  const ct = r.headers.get('content-type') ?? '';
  return (ct.includes('json') ? r.json() : r.text()) as Promise<T>;
}

/** URL usable by EventSource / <a download> (which cannot send headers). */
export const withToken = (path: string) =>
  `${path}${path.includes('?') ? '&' : '?'}token=${encodeURIComponent(getToken())}`;

export interface Me { user: string; roles: string[] }
export const can = (me: Me | null, role: string) =>
  !!me && (me.roles.includes('admin') || me.roles.includes(role) || role === 'viewer');
