from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import os
from dotenv import load_dotenv
from functools import lru_cache
import time

from models import Stock, StockPrice, Sector, Fundamentals, TechnicalIndicators, ScreenerRequest
from supabase_db import supabase_db
from etf_routes import get_etf, get_etf_prices, get_all_etfs, get_etfs_by_category, get_leveraged_etfs

load_dotenv()

app = FastAPI(
    title="FinStocks API",
    description="Financial stocks and ETFs data API with screening and analysis",
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
    return {"status": "OK", "message": "FinStocks API is running with Supabase"}

# STOCK ENDPOINTS
@app.get("/api/stocks/{symbol}")
async def get_stock(symbol: str):
    """Get stock details with latest price and fundamentals"""
    try:
        symbol = symbol.upper()
        
        # Get basic stock info
        stock_result = supabase_db.get_stock(symbol)
        if not stock_result.data:
            raise HTTPException(status_code=404, detail="Stock not found")
        
        stock = stock_result.data[0]
        
        # Get latest price
        price_result = supabase_db.get_stock_prices(symbol, 1)
        latest_price = price_result.data[0] if price_result.data else None
        
        # Get latest fundamentals
        fundamentals_result = supabase_db.supabase.table('fundamentals').select('*').eq('symbol', symbol).order('year', desc=True).order('quarter', desc=True).limit(1).execute()
        fundamentals = fundamentals_result.data[0] if fundamentals_result.data else None
        
        return {
            **stock,
            "latest_price": latest_price,
            "fundamentals": fundamentals
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stocks/{symbol}/prices")
async def get_stock_prices(symbol: str, days: int = 30):
    """Get stock price history"""
    try:
        symbol = symbol.upper()
        result = supabase_db.get_stock_prices(symbol, days)
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stocks/{symbol}/technical")
async def get_technical_indicators(symbol: str):
    """Get latest technical indicators"""
    try:
        symbol = symbol.upper()
        result = supabase_db.supabase.table('technical_indicators').select('*').eq('symbol', symbol).order('date', desc=True).limit(1).execute()
        return result.data[0] if result.data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stocks/{symbol}/etfs")
async def get_stock_etfs(symbol: str):
    """Get ETFs that hold this stock"""
    try:
        symbol = symbol.upper()
        result = supabase_db.supabase.table('etf_holdings').select('*, etfs(name, category)').eq('stock_symbol', symbol).order('weight_percentage', desc=True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/stocks")
async def create_stock(stock: Stock):
    """Add new stock"""
    try:
        result = supabase_db.insert_stock({
            "symbol": stock.symbol.upper(),
            "name": stock.name,
            "sector": stock.sector,
            "industry": stock.industry,
            "market_cap": stock.market_cap
        })
        return {"id": result.data[0]["id"], "symbol": stock.symbol.upper()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ETF ENDPOINTS
@app.get("/api/etfs")
async def get_etfs():
    """Get all ETFs"""
    return get_all_etfs()

@app.get("/api/etfs/{symbol}")
async def get_etf_details(symbol: str):
    """Get ETF details with latest price"""
    return get_etf(symbol)

@app.get("/api/etfs/{symbol}/prices")
async def get_etf_price_history(symbol: str, days: int = 30):
    """Get ETF price history"""
    return get_etf_prices(symbol, days)

@app.get("/api/etfs/{symbol}/holdings")
async def get_etf_holdings(symbol: str, limit: int = 50):
    """Get ETF holdings with stock weights"""
    try:
        symbol = symbol.upper()
        result = supabase_db.supabase.table('etf_holdings').select('*, stocks(name, sector)').eq('etf_symbol', symbol).order('weight_percentage', desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/etfs/{symbol}/top-holdings")
async def get_etf_top_holdings(symbol: str, limit: int = 10):
    """Get top holdings of an ETF"""
    try:
        symbol = symbol.upper()
        result = supabase_db.supabase.table('etf_holdings').select('*, stocks(name, sector, market_cap)').eq('etf_symbol', symbol).order('weight_percentage', desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/etfs/category/{category}")
async def get_etfs_in_category(category: str):
    """Get ETFs by category"""
    return get_etfs_by_category(category)

@app.get("/api/etfs/leveraged")
async def get_leveraged_etf_list():
    """Get leveraged ETFs (3x, etc.)"""
    return get_leveraged_etfs()

# SECTOR ENDPOINTS
@lru_cache(maxsize=10)
def get_cached_all_sectors_data(cache_key: str):
    """Cached all sectors data"""
    start_time = time.time()
    
    result = supabase_db.get_sectors()
    
    end_time = time.time()
    query_time = (end_time - start_time) * 1000
    print(f"🏭 Supabase all sectors query took: {query_time:.2f}ms")
    
    return result.data

@app.get("/api/sectors")
async def get_sectors():
    """Get all sectors performance - now cached"""
    try:
        # Cache for 30 seconds
        cache_key = str(int(time.time() // 30))
        return get_cached_all_sectors_data(cache_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@lru_cache(maxsize=50)
def get_cached_sectors_data(period: str, limit: int, cache_key: str):
    """Cached sectors data"""
    start_time = time.time()
    
    period_map = {
        "1d": "performance_1d",
        "1w": "performance_1w", 
        "1m": "performance_1m",
        "ytd": "performance_ytd"
    }
    
    order_by = period_map.get(period, "performance_1d")
    result = supabase_db.supabase.table('sectors').select('*').order(order_by, desc=True).limit(limit).execute()
    
    end_time = time.time()
    query_time = (end_time - start_time) * 1000
    print(f"📊 Supabase sectors query took: {query_time:.2f}ms")
    
    return result.data

@app.get("/api/sectors/top-performers")
async def get_top_sectors(period: str = "1d", limit: int = 5):
    """Get top performing sectors - 30 second cache for real-time data"""
    try:
        # Cache for 30 seconds
        cache_key = str(int(time.time() // 30))
        return get_cached_sectors_data(period, limit, cache_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sectors/{sector_name}/stocks")
async def get_sector_stocks(sector_name: str):
    """Get stocks in a sector"""
    try:
        result = supabase_db.supabase.table('stocks').select('*').eq('sector', sector_name).order('market_cap', desc=True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# SCREENER ENDPOINTS
@lru_cache(maxsize=100)
def get_cached_screener_data(limit: int, sectors: str, min_cap: int, max_cap: int, cache_key: str):
    """Cached screener data - simplified query for speed"""
    start_time = time.time()
    
    # Simple query - just stocks table, no joins
    query = supabase_db.supabase.table('stocks').select('symbol, name, sector, market_cap')
    
    if sectors and sectors != "None":
        sector_list = sectors.split(",")
        query = query.in_('sector', sector_list)
    
    if min_cap and min_cap > 0:
        query = query.gte('market_cap', min_cap)
    
    if max_cap and max_cap > 0:
        query = query.lte('market_cap', max_cap)
    
    result = query.limit(limit).execute()
    
    end_time = time.time()
    query_time = (end_time - start_time) * 1000  # Convert to milliseconds
    print(f"🔍 Supabase screener query took: {query_time:.2f}ms")
    
    return result.data

@app.post("/api/screener")
async def screen_stocks(request: ScreenerRequest):
    """Screen stocks with filters - 30 second cache for real-time data"""
    try:
        # Create cache key that changes every 30 seconds
        cache_key = str(int(time.time() // 30))  # 30 seconds for real-time
        
        # Convert request to cacheable parameters
        sectors_str = ",".join(request.sectors) if request.sectors else "None"
        min_cap = request.min_market_cap or 0
        max_cap = request.max_market_cap or 0
        limit = request.limit or 50
        
        return get_cached_screener_data(limit, sectors_str, min_cap, max_cap, cache_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/screener/gainers")
async def get_top_gainers(limit: int = 10):
    """Get top gaining stocks"""
    try:
        # Get stocks with recent prices
        result = supabase_db.supabase.table('stocks').select('symbol, name, sector').limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/screener/losers")
async def get_top_losers(limit: int = 10):
    """Get top losing stocks"""
    try:
        # Get stocks with recent prices
        result = supabase_db.supabase.table('stocks').select('symbol, name, sector').limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
