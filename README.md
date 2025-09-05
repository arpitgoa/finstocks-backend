# FinStocks FastAPI Backend

Financial data API backend with SQLite database and automatic documentation.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start development server:
```bash
uvicorn main:app --reload --port 8000
```

## API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Stocks
- `GET /api/stocks/{symbol}` - Get stock details
- `GET /api/stocks/{symbol}/prices?days=30` - Get price history
- `GET /api/stocks/{symbol}/technical` - Get technical indicators
- `POST /api/stocks` - Add new stock

### Sectors
- `GET /api/sectors` - Get all sectors performance
- `GET /api/sectors/top-performers?period=1d&limit=5` - Top performers
- `GET /api/sectors/{sector_name}/stocks` - Stocks in sector

### Screener
- `POST /api/screener` - Filter stocks with criteria
- `GET /api/screener/gainers?limit=10` - Top gainers
- `GET /api/screener/losers?limit=10` - Top losers

## Database

SQLite database with automatic schema creation:
- Pydantic models for type safety
- Automatic API validation
- Built-in documentation
