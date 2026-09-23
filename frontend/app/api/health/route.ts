import { fetchApi } from '@/lib/api';

export async function GET() {
  try {
    await fetchApi('commodities/?page_size=1');
    return Response.json({ ok: true });
  } catch {
    return Response.json({ ok: false }, { status: 503 });
  }
}
