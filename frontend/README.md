# OreLens frontend

Next.js App Router frontend. FE-01 provides the purple responsive app shell; FE-02 adds a server-rendered Commodity Overview with current prices, daily/YTD movement, historical sparklines, provenance labels, and explicit loading/error/empty states.

## Run

Use Node 20.9+ or a supported newer LTS version.

```sh
cd frontend
npm ci
npm run dev
```

Open http://127.0.0.1:3000. Optional: copy `.env.example` to `.env.local` and change `API_BASE_URL`. Restart Next.js after changing environment variables. This value is read on the server and must point to the Django `/api/v1/` base URL.

The default API is `http://127.0.0.1:8000/api/v1/`. Start Django separately before opening Commodity Overview. A successful connection check means the commodities endpoint responds, not that its data is verified. Backend failures never silently switch to mock data.

## Verify

```sh
npm test
npm run build
```

Routes: `/commodities`, `/companies`, `/evidence`, `/scenarios`. `/` redirects to commodities; unknown routes use the App Router not-found page.

`lib/api.ts` preserves Django pagination and fetches data in Server Components. Commodity history failures stay visible per card while a commodities endpoint failure is handled by `app/commodities/error.tsx`.
