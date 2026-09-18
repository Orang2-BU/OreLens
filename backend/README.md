# OreLens Backend API

Django REST API backend untuk OreLens - Commodity and Company Intelligence Platform.

## Arsitektur

```
backend/
├── apps/
│   ├── commodities/      # Commodity data, price series, drivers
│   ├── companies/        # Company profiles, exposures, resilience
│   ├── evidence/         # Raw data logs, normalized metrics, audit
│   ├── scenarios/        # Scenario analysis & sensitivity tests
│   └── integrations/     # API clients (Sectors, World Bank, FRED, UN Comtrade, EIA)
├── orelens/             # Django project settings
└── manage.py
```

## Tech Stack

- **Django 6.1.1** - Web framework
- **Django REST Framework 3.18.1** - REST API
- **drf-spectacular 0.30.0** - OpenAPI 3.0 schema & ReDoc
- **SQLite** - Database (MVP; production migrate ke PostgreSQL)
- **requests** - HTTP client untuk external APIs

## Setup

### 1. Install Dependencies

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac
# Edit .env dan isi API keys untuk Sectors, FRED, UN Comtrade, EIA
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Seed Sample Data

```bash
python manage.py seed_sample_data
```

Ini akan populate database dengan:
- 4 commodities: Coal, Gold, Nickel, Copper
- 5 Indonesian mining companies: ADRO, PTBA, MDKA, INCO, ANTM
- Commodity drivers dengan correlation scores
- 30 hari price history per commodity
- Exposure & resilience profiles
- Sample scenario analysis
- Data audit items

### 5. Run Development Server

```bash
python manage.py runserver
```

Server berjalan di `http://localhost:8000`

## API Documentation

### Interactive Docs

- **ReDoc**: http://localhost:8000/redoc/
- **Swagger UI**: http://localhost:8000/api/docs/swagger/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Main Endpoints

#### Commodities
- `GET /api/v1/commodities/` - List semua commodities
- `GET /api/v1/commodities/{id}/` - Detail commodity
- `GET /api/v1/commodity-prices/` - Historical price series
- `GET /api/v1/commodity-drivers/` - Driver analysis & correlations

#### Companies
- `GET /api/v1/companies/` - List companies
- `GET /api/v1/companies/{id}/` - Company profile
- `GET /api/v1/company-exposures/` - Commodity exposure breakdown
- `GET /api/v1/company-resilience/` - Resilience scores & financials

#### Evidence & Data
- `GET /api/v1/raw-data-logs/` - Raw API call logs (provenance)
- `GET /api/v1/normalized-metrics/` - Normalized metric observations
- `GET /api/v1/data-audit/` - Data availability audit results

#### Scenarios
- `GET /api/v1/scenarios/` - Scenario analysis list
- `GET /api/v1/scenarios/{id}/` - Scenario detail dengan inputs & results
- `GET /api/v1/scenario-inputs/` - Input adjustments per scenario
- `GET /api/v1/scenario-results/` - Computed scenario outcomes

### Filtering & Search

Semua list endpoints support:
- **Filtering**: `?category=ENERGY&is_active=true`
- **Search**: `?search=coal`
- **Ordering**: `?ordering=-current_price`
- **Pagination**: `?page=2` (default 50 items per page)

Contoh:
```bash
# Commodities dengan price change tertinggi YTD
GET /api/v1/commodities/?ordering=-price_change_pct_ytd

# Companies di mining sector
GET /api/v1/companies/?sector=Basic%20Materials

# Drivers untuk COAL dengan positive impact
GET /api/v1/commodity-drivers/?commodity=1&impact_direction=POSITIVE
```

## Admin Panel

Django admin tersedia di http://localhost:8000/admin/

Create superuser:
```bash
python manage.py createsuperuser
```

## Data Integration Clients

API clients tersedia di `apps/integrations/clients/`:

```python
from apps.integrations.clients import (
    SectorsClient,
    WorldBankClient, 
    FredClient,
    UNComtradeClient,
    EiaClient
)

# Example usage
sectors = SectorsClient(api_key='your_key')
company_data = sectors.get_company_profile('ADRO.JK')

fred = FredClient(api_key='your_fred_key')
coal_prices = fred.get_series('PCOALAUUSDM')
```

Semua API calls di-log otomatis ke `RawDataLog` model untuk audit trail sesuai data dictionary rules.

## Testing

```bash
python manage.py test
```

## MVP Scope Status

✅ Backend setup complete  
✅ REST API dengan OpenAPI 3.0 documentation  
✅ Models untuk Commodities, Companies, Drivers, Evidence, Scenarios  
✅ API clients untuk 5 data sources (Sectors, World Bank, FRED, UN Comtrade, EIA)  
✅ Sample data seeded (Coal, Gold, Nickel, Copper + 5 companies)  
✅ Admin panel  

⏳ Pending (sesuai MVP_SCOPE.md):
- Actual API availability audit execution
- Historical data collection & normalization pipeline
- Correlation screening & regression analysis
- Final scoring weights (blocked until backtest complete)

## Development Notes

### CORS

CORS enabled untuk all origins di development. Production: set `CORS_ALLOWED_ORIGINS` di settings.

### Database

SQLite untuk MVP. Production checklist:
- Migrate ke PostgreSQL
- Configure proper `SECRET_KEY` via environment
- Set `DEBUG=False`
- Configure `ALLOWED_HOSTS`
- Set up proper logging & monitoring

### Scoring Methodology Status

⚠️ **IMPORTANT**: Resilience scores dan exposure scores di sample data adalah **preliminary/placeholder**. 

Sesuai PRD & MVP Scope:
> "The MVP must not present the unfinished scoring model as final."

Final weights require:
1. Complete data availability audit
2. Correlation screening dengan actual historical data
3. Regression analysis
4. Rolling analysis
5. Regime comparison
6. Historical weighting validation
7. Backtest

`CompanyResilience.scoring_status` default: `"Pending Validation"` untuk transparency.
