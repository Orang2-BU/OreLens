# OreLens — Technical Architecture

## Architecture decision

OreLens menggunakan Django dan Django REST Framework sebagai backend utama. Pilihan ini sesuai dengan kebutuhan aplikasi data yang memiliki banyak domain object, persistence, internal audit, dan admin panel.

Keputusan ini mengutamakan:

- Django ORM untuk entitas aplikasi.
- Django Admin untuk audit data internal.
- Django REST Framework untuk API frontend.
- Pemisahan logic bisnis dan quant dari views serta serializers.

FastAPI tidak digunakan sebagai backend utama karena kebutuhan OreLens lebih dekat ke dashboard aplikasi dengan banyak entitas dan workflow data yang tersimpan.

## System layout

```text
Next.js + TypeScript
          │
          ▼
Django + Django REST Framework
          │
          ├── Commodity Engine
          ├── Company Engine
          ├── Exposure Engine
          ├── Resilience Engine
          └── Scenario Engine
          │
          ├── PostgreSQL
          │
          └── DuckDB + Parquet
```

## Storage responsibilities

### PostgreSQL

Gunakan PostgreSQL untuk:

- Application state.
- Companies.
- Commodities.
- Current normalized metrics.
- Analysis results.
- Scenario runs.

### DuckDB dan Parquet

Gunakan DuckDB dan Parquet untuk:

- Historical data.
- Research datasets.
- Regression workloads.
- Backtesting.
- Feature engineering.

Historical data tidak perlu dipaksa masuk seluruhnya ke PostgreSQL.

## Django structure

Struktur target aplikasi:

```text
backend/
├── config/
├── commodities/
├── companies/
├── data_sources/
├── intelligence/
├── scenarios/
├── analytics/
└── manage.py
```

Struktur tersebut adalah arah arsitektur. Implementasi saat ini masih memakai aplikasi Django di `backend/apps/` dan dapat dipindahkan secara bertahap jika kebutuhan domain bertambah.

## Intelligence layer

Logic intelligence ditempatkan terpisah dari HTTP layer:

```text
intelligence/
├── commodity.py
├── exposure.py
├── resilience.py
├── fundamentals.py
└── evidence.py
```

Logic ini tidak ditempatkan langsung di `views.py` atau serializer.

## Analytics layer

Logic quant dipisahkan ke modul analytics:

```text
analytics/
├── regression.py
├── normalization.py
├── concentration.py
├── sensitivity.py
└── backtest.py
```

Bobot scoring dan decision logic final tetap menunggu data historis, audit availability, dan backtest.

## External data sources

Client provider dikelompokkan di data source layer:

```text
data_sources/
├── sectors.py
├── fred.py
├── world_bank.py
├── comtrade.py
└── eia.py
```

Di repository saat ini, client tersebut tersedia di `backend/apps/integrations/clients/`.

## Admin and internal audit

Django Admin digunakan untuk memeriksa:

- Commodity observations.
- Company data.
- API fetch status.
- Missing metrics.
- Scenario results.
- Data freshness.

Admin menjadi panel internal untuk audit data tanpa membangun UI debug terpisah.

## Final stack direction

| Area | Technology |
|---|---|
| Frontend | Next.js + TypeScript |
| Backend | Django + Django REST Framework |
| Application database | PostgreSQL |
| Historical analytics storage | DuckDB + Parquet |
| Data processing | Polars |
| Scientific computing | NumPy + SciPy |
| Statistical modeling | statsmodels + scikit-learn |
| Testing | pytest + pytest-django |
| Local infrastructure | Docker |
| CI/CD | GitHub Actions |
| Frontend hosting | Vercel |
| Backend hosting | Railway atau Render |
| Managed PostgreSQL | Neon PostgreSQL |

## Migration notes

Implementasi saat ini sudah memiliki Django, DRF, SQLite, Django Admin, API clients, dan endpoint MVP. PostgreSQL, DuckDB, Parquet, Polars, analytics modules, Docker, dan CI/CD belum menjadi bagian dari implementasi saat ini.
