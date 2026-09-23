# OreLens

OreLens - Commodity and Company Intelligence Platform untuk Sectors Hackathon.

OreLens membantu pengguna menelusuri driver komoditas, exposure dan resilience perusahaan, serta evidence dan scenario. Scope awal: Coal, Gold, Nickel, Copper. Sectors adalah sumber data inti yang direncanakan; metric dan sumber lain tercatat di [Data Dictionary](docs/data/DATA_DICTIONARY.md).

Implementasi saat ini: Django/DRF + SQLite di backend dan Next.js App Router + TypeScript di frontend. Arah arsitektur selanjutnya mencakup PostgreSQL dan DuckDB/Parquet untuk historical analytics. Lihat [Technical Architecture](docs/data/TECHNICAL_ARCHITECTURE.md).

## Structure

```
OreLens/
├── backend/             # Django REST API
├── frontend/            # Next.js shell, commodity views, Company Comparison (FE-01–FE-04)
└── docs/                # Product, data, intelligence, research
```

## Quick Start (Backend)

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_sample_data
python manage.py runserver
```

Akses ReDoc API Documentation di: `http://localhost:8000/redoc/`
OpenAPI Schema: `http://localhost:8000/api/schema/`

## Quick Start (Frontend)

```bash
cd frontend
npm ci
npm run dev
```

Buka `http://127.0.0.1:3000/`. Backend dijalankan terpisah; `API_BASE_URL` dapat diatur sesuai [panduan frontend](frontend/README.md). Commodity Overview, Driver Map, dan Company Comparison sudah tersedia; Company Detail, evidence, dan scenario masih placeholder.

## Dokumentasi tim

Mulai dari [indeks docs](docs/README.md): PRD dan MVP scope untuk product, Data Dictionary dan API Architecture untuk backend, engine docs untuk quant, serta UI Flow untuk frontend. Data Availability Audit dan aturan submission masih membutuhkan verifikasi nyata.

