import { test } from 'node:test';
import assert from 'node:assert/strict';
import { apiGet } from './api.js';

test('API preserves pagination, builds the base path, and rejects errors', async () => {
  const original = globalThis.fetch;
  try {
    globalThis.fetch = async (url, options) => {
      assert.equal(url.href, 'http://localhost:8000/api/v1/commodities/?page=2');
      assert.ok(options.signal);
      return Response.json({ count: 1, next: null, previous: null, results: [{ id: 4 }] });
    };
    const page = await apiGet('/commodities/?page=2', { baseUrl: 'http://localhost:8000/api/v1' });
    assert.equal(page.results[0].id, 4);
    globalThis.fetch = async () => new Response('', { status: 503 });
    await assert.rejects(apiGet('commodities/'), /503/);
  } finally {
    globalThis.fetch = original;
  }
});
