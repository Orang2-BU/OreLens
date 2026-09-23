# OreLens frontend

FE-01 foundation: React + Vite, OreLens purple design tokens, responsive workspace, accessible navigation, route fallback, reusable loading/error/empty panel, and a manual API connection check. Product pages are explicitly marked as not implemented yet (FE-02 onward).

## Run

Use Node 20.19+ or a supported newer LTS version.

```sh
cd frontend
npm ci
npm run dev
```

Open http://127.0.0.1:5173. Optional: copy `.env.example` to `.env.local` and change `VITE_API_BASE_URL`. Restart Vite after changing environment variables. Provider secrets belong only in the backend; Vite environment variables are public.

The default API is `http://localhost:8000/api/v1/`. Start Django separately to use “Periksa koneksi”. A successful check means the commodities endpoint responds, not that its data is verified. Backend failures never silently switch to mock data.

## Verify

```sh
npm test
npm run build
```

Routes: `/commodities`, `/companies`, `/evidence`, `/scenarios`. `/` redirects to commodities; unknown routes show a recovery link. For hosting, configure fallback to `index.html` for frontend routes (keep the API routed separately).

`src/api.js` preserves Django pagination (`count`, `next`, `previous`, `results`), supports cancellation, and uses a 10-second timeout. `StatePanel` accepts `kind="loading"`, `"error"`, or `"empty"`, plus a title, content, and optional `onRetry` callback.
