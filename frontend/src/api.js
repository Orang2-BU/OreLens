export const API_BASE_URL = import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000/api/v1/';

export async function apiGet(path, { signal, baseUrl = API_BASE_URL } = {}) {
  const url = new URL(path.replace(/^\/+/, ''), baseUrl.replace(/\/?$/, '/'));
  const response = await fetch(url, {
    headers: { Accept: 'application/json' },
    signal: signal ? AbortSignal.any([signal, AbortSignal.timeout(10000)]) : AbortSignal.timeout(10000),
  });
  if (!response.ok) throw new Error(`Permintaan gagal (HTTP ${response.status}).`);
  return response.json();
}
