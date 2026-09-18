# OreLens

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

