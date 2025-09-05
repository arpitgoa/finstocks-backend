from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from dotenv import load_dotenv

from models import Stock, StockPrice, Sector, Fundamentals, TechnicalIndicators, ScreenerRequest
from database import db

load_dotenv()

app = FastAPI(
    title="FinStocks API",
    description="Financial stocks data API with screening and analysis",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "OK", "message": "FinStocks API is running"}

# STOCK ENDPOINTS
@app.get("/api/stocks/{symbol}")
async def get_stock(symbol: str):
    """Get stock details with latest price and fundamentals"""
    symbol = symbol.upper()
    
    # Get basic stock info
    stock_query = "SELECT * FROM stocks WHERE symbol = ?"
    stock_data = db.execute_query(stock_query, (symbol,))
    
    if not stock_data:
        raise HTTPException(status_code=404, detail="Stock not found")
    
    stock = stock_data[0]
    
    # Get latest price
    price_query = """
        SELECT * FROM stock_prices 
        WHERE symbol = ? 
        ORDER BY date DESC 
        LIMIT 1
    """
    latest_price = db.execute_query(price_query, (symbol,))
    
    # Get latest fundamentals
    fundamentals_query = """
        SELECT * FROM fundamentals 
        WHERE symbol = ? 
        ORDER BY year DESC, quarter DESC 
        LIMIT 1
    """
    fundamentals = db.execute_query(fundamentals_query, (symbol,))
    
    return {
        **stock,
        "latest_price": latest_price[0] if latest_price else None,
        "fundamentals": fundamentals[0] if fundamentals else None
    }

@app.get("/api/stocks/{symbol}/prices")
async def get_stock_prices(symbol: str, days: int = 30):
    """Get stock price history"""
    symbol = symbol.upper()
    
    query = """
        SELECT * FROM stock_prices 
        WHERE symbol = ? 
        ORDER BY date DESC 
        LIMIT ?
    """
    prices = db.execute_query(query, (symbol, days))
    return prices

@app.get("/api/stocks/{symbol}/technical")
async def get_technical_indicators(symbol: str):
    """Get latest technical indicators"""
    symbol = symbol.upper()
    
    query = """
        SELECT * FROM technical_indicators 
        WHERE symbol = ? 
        ORDER BY date DESC 
        LIMIT 1
    """
    technical = db.execute_query(query, (symbol,))
    return technical[0] if technical else {}

@app.post("/api/stocks")
async def create_stock(stock: Stock):
    """Add new stock"""
    query = """
        INSERT INTO stocks (symbol, name, sector, industry, market_cap) 
        VALUES (?, ?, ?, ?, ?)
    """
    stock_id = db.execute_insert(
        query, 
        (stock.symbol.upper(), stock.name, stock.sector, stock.industry, stock.market_cap)
    )
    return {"id": stock_id, "symbol": stock.symbol.upper()}

# SECTOR ENDPOINTS
@app.get("/api/sectors")
async def get_sectors():
    """Get all sectors performance"""
    query = "SELECT * FROM sectors ORDER BY performance_1d DESC"
    return db.execute_query(query)

@app.get("/api/sectors/top-performers")
async def get_top_sectors(period: str = "1d", limit: int = 5):
    """Get top performing sectors"""
    period_map = {
        "1d": "performance_1d",
        "1w": "performance_1w", 
        "1m": "performance_1m",
        "ytd": "performance_ytd"
    }
    
    order_by = period_map.get(period, "performance_1d")
    query = f"SELECT * FROM sectors ORDER BY {order_by} DESC LIMIT ?"
    return db.execute_query(query, (limit,))

@app.get("/api/sectors/{sector_name}/stocks")
async def get_sector_stocks(sector_name: str):
    """Get stocks in a sector"""
    query = """
        SELECT s.*, sp.close_price, sp.date as price_date
        FROM stocks s
        LEFT JOIN stock_prices sp ON s.symbol = sp.symbol
        WHERE s.sector = ? AND sp.date = (
            SELECT MAX(date) FROM stock_prices WHERE symbol = s.symbol
        )
        ORDER BY s.market_cap DESC
    """
    return db.execute_query(query, (sector_name,))

# SCREENER ENDPOINTS
@app.post("/api/screener")
async def screen_stocks(request: ScreenerRequest):
    """Screen stocks with filters"""
    query = """
        SELECT DISTINCT s.*, sp.close_price, f.pe_ratio, f.roe, f.eps
        FROM stocks s
        LEFT JOIN stock_prices sp ON s.symbol = sp.symbol
        LEFT JOIN fundamentals f ON s.symbol = f.symbol
        WHERE sp.date = (SELECT MAX(date) FROM stock_prices WHERE symbol = s.symbol)
        AND f.year = (SELECT MAX(year) FROM fundamentals WHERE symbol = s.symbol)
    """
    
    params = []
    
    if request.min_market_cap:
        query += " AND s.market_cap >= ?"
        params.append(request.min_market_cap)
    
    if request.max_market_cap:
        query += " AND s.market_cap <= ?"
        params.append(request.max_market_cap)
    
    if request.min_pe_ratio:
        query += " AND f.pe_ratio >= ?"
        params.append(request.min_pe_ratio)
    
    if request.max_pe_ratio:
        query += " AND f.pe_ratio <= ?"
        params.append(request.max_pe_ratio)
    
    if request.min_roe:
        query += " AND f.roe >= ?"
        params.append(request.min_roe)
    
    if request.sectors:
        placeholders = ",".join(["?" for _ in request.sectors])
        query += f" AND s.sector IN ({placeholders})"
        params.extend(request.sectors)
    
    if request.min_price:
        query += " AND sp.close_price >= ?"
        params.append(request.min_price)
    
    if request.max_price:
        query += " AND sp.close_price <= ?"
        params.append(request.max_price)
    
    query += " ORDER BY s.market_cap DESC LIMIT ?"
    params.append(request.limit)
    
    return db.execute_query(query, tuple(params))

@app.get("/api/screener/gainers")
async def get_top_gainers(limit: int = 10):
    """Get top gaining stocks"""
    query = """
        SELECT s.symbol, s.name, s.sector,
               current.close_price as current_price,
               previous.close_price as previous_price,
               ROUND(((current.close_price - previous.close_price) / previous.close_price * 100), 2) as change_percent
        FROM stocks s
        JOIN stock_prices current ON s.symbol = current.symbol
        JOIN stock_prices previous ON s.symbol = previous.symbol
        WHERE current.date = (SELECT MAX(date) FROM stock_prices WHERE symbol = s.symbol)
        AND previous.date = (SELECT MAX(date) FROM stock_prices WHERE symbol = s.symbol AND date < current.date)
        ORDER BY change_percent DESC
        LIMIT ?
    """
    return db.execute_query(query, (limit,))

@app.get("/api/screener/losers")
async def get_top_losers(limit: int = 10):
    """Get top losing stocks"""
    query = """
        SELECT s.symbol, s.name, s.sector,
               current.close_price as current_price,
               previous.close_price as previous_price,
               ROUND(((current.close_price - previous.close_price) / previous.close_price * 100), 2) as change_percent
        FROM stocks s
        JOIN stock_prices current ON s.symbol = current.symbol
        JOIN stock_prices previous ON s.symbol = previous.symbol
        WHERE current.date = (SELECT MAX(date) FROM stock_prices WHERE symbol = s.symbol)
        AND previous.date = (SELECT MAX(date) FROM stock_prices WHERE symbol = s.symbol AND date < current.date)
        ORDER BY change_percent ASC
        LIMIT ?
    """
    return db.execute_query(query, (limit,))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
