from fastapi import HTTPException
from supabase_db import supabase_db

# ETF CRUD operations
def get_etf(symbol: str):
    """Get ETF details"""
    try:
        symbol = symbol.upper()
        
        # Get basic ETF info
        etf_result = supabase_db.supabase.table('etfs').select('*').eq('symbol', symbol).execute()
        if not etf_result.data:
            raise HTTPException(status_code=404, detail="ETF not found")
        
        etf = etf_result.data[0]
        
        # Get latest price
        price_result = supabase_db.supabase.table('etf_prices').select('*').eq('symbol', symbol).order('date', desc=True).limit(1).execute()
        latest_price = price_result.data[0] if price_result.data else None
        
        return {
            **etf,
            "latest_price": latest_price
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_etf_prices(symbol: str, days: int = 30):
    """Get ETF price history"""
    try:
        symbol = symbol.upper()
        result = supabase_db.supabase.table('etf_prices').select('*').eq('symbol', symbol).order('date', desc=True).limit(days).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_all_etfs():
    """Get all ETFs"""
    try:
        result = supabase_db.supabase.table('etfs').select('*').order('aum', desc=True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_etfs_by_category(category: str):
    """Get ETFs by category"""
    try:
        result = supabase_db.supabase.table('etfs').select('*').eq('category', category).order('aum', desc=True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_leveraged_etfs():
    """Get leveraged ETFs (leverage > 1)"""
    try:
        result = supabase_db.supabase.table('etfs').select('*').gt('leverage_ratio', 1.0).order('aum', desc=True).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
