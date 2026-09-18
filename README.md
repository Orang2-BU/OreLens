# OreLens

## Frontend (FE-01)

Fondasi workspace React tersedia di `frontend/`. Jalankan `npm ci` lalu `npm run dev` dari folder tersebut. Lihat [panduan frontend](frontend/README.md) untuk konfigurasi API dan pengujian. Halaman fitur masih menunggu FE-02 dan seterusnya.

OreLens - Commodity and Company Intelligence Platform untuk Sectors Hackathon.

## Structure

```
OreLens/
├── backend/              # Django REST API backend
│   ├── apps/             # Django apps (commodities, companies, evidence, scenarios, integrations)
│   ├── orelens/          # Django settings & URLs
│   ├── manage.py
│   └── requirements.txt
└── docs/                 # Product requirements & data dictionary
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

