from supabase_db import supabase_db
import random

def create_etf_holdings_schema():
    """Create ETF holdings table schema"""
    sql_schema = """
    -- Create ETF holdings table
    CREATE TABLE IF NOT EXISTS etf_holdings (
        id SERIAL PRIMARY KEY,
        etf_symbol VARCHAR(10) NOT NULL,
        stock_symbol VARCHAR(10) NOT NULL,
        weight_percentage DECIMAL(5,3) NOT NULL,
        shares_held BIGINT,
        market_value DECIMAL(15,2),
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (etf_symbol) REFERENCES etfs(symbol),
        FOREIGN KEY (stock_symbol) REFERENCES stocks(symbol),
        UNIQUE(etf_symbol, stock_symbol)
    );

    -- Create index for performance
    CREATE INDEX IF NOT EXISTS idx_etf_holdings_etf_symbol ON etf_holdings(etf_symbol);
    CREATE INDEX IF NOT EXISTS idx_etf_holdings_stock_symbol ON etf_holdings(stock_symbol);
    """
    
    print("Copy and paste this SQL into Supabase SQL Editor:")
    print("=" * 60)
    print(sql_schema)
    print("=" * 60)
    return sql_schema

def create_etf_holdings_data():
    """Create realistic ETF holdings based on actual ETF compositions"""
    
    # Get all available stocks from database
    try:
        stocks_result = supabase_db.supabase.table('stocks').select('symbol, sector, market_cap').execute()
        available_stocks = stocks_result.data
        print(f"Found {len(available_stocks)} stocks to use in ETF compositions")
    except Exception as e:
        print(f"Error fetching stocks: {e}")
        return []
    
    # Create realistic ETF compositions
    etf_compositions = {
        # Broad Market ETFs - Top holdings by market cap
        "SPY": {
            "top_holdings": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK.B", "V", "JPM"],
            "sector_weights": {"Technology": 30, "Financial Services": 13, "Healthcare": 12, "Consumer Cyclical": 10}
        },
        "QQQ": {
            "top_holdings": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "NFLX"],
            "sector_weights": {"Technology": 60, "Consumer Cyclical": 20, "Communication Services": 15}
        },
        "VTI": {
            "top_holdings": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK.B", "V", "JPM"],
            "sector_weights": {"Technology": 28, "Financial Services": 14, "Healthcare": 13, "Consumer Cyclical": 11}
        },
        
        # Technology ETFs
        "XLK": {
            "top_holdings": ["AAPL", "MSFT", "NVDA", "GOOGL", "META"],
            "sector_weights": {"Technology": 100}
        },
        "VGT": {
            "top_holdings": ["AAPL", "MSFT", "NVDA", "GOOGL", "META"],
            "sector_weights": {"Technology": 100}
        },
        
        # Leveraged ETFs (same as underlying but 3x leverage)
        "TQQQ": {
            "top_holdings": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA"],
            "sector_weights": {"Technology": 60, "Consumer Cyclical": 25, "Communication Services": 15}
        },
        "UPRO": {
            "top_holdings": ["AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK.B"],
            "sector_weights": {"Technology": 30, "Financial Services": 13, "Healthcare": 12}
        },
        "SOXL": {
            "top_holdings": ["NVDA", "AAPL", "MSFT"],
            "sector_weights": {"Technology": 100}
        },
        
        # Small Cap ETFs
        "IWM": {
            "top_holdings": [],  # Will use smaller market cap stocks
            "sector_weights": {"Technology": 20, "Healthcare": 18, "Financial Services": 15, "Industrials": 15}
        },
        
        # Sector ETFs
        "XLF": {
            "top_holdings": ["JPM", "BRK.B", "V", "MA", "BAC"],
            "sector_weights": {"Financial Services": 100}
        },
        "XLE": {
            "top_holdings": ["XOM", "CVX", "COP", "EOG", "SLB"],
            "sector_weights": {"Energy": 100}
        },
        "XLV": {
            "top_holdings": ["JNJ", "UNH", "PFE", "ABBV", "TMO"],
            "sector_weights": {"Healthcare": 100}
        },
        "XLI": {
            "top_holdings": ["BA", "CAT", "GE", "UPS", "HON"],
            "sector_weights": {"Industrials": 100}
        },
        
        # Consumer ETFs
        "XLP": {
            "top_holdings": ["PG", "KO", "PEP", "WMT", "COST"],
            "sector_weights": {"Consumer Defensive": 100}
        }
    }
    
    all_holdings = []
    
    for etf_symbol, composition in etf_compositions.items():
        print(f"\nCreating holdings for {etf_symbol}...")
        
        holdings = []
        total_weight = 0
        
        # Add top holdings with higher weights
        top_holdings = composition["top_holdings"]
        if top_holdings:
            # Top 3 holdings get 8-15% each
            for i, stock_symbol in enumerate(top_holdings[:3]):
                if any(s["symbol"] == stock_symbol for s in available_stocks):
                    weight = random.uniform(8.0, 15.0)
                    holdings.append({
                        "etf_symbol": etf_symbol,
                        "stock_symbol": stock_symbol,
                        "weight_percentage": round(weight, 3),
                        "shares_held": random.randint(10000000, 50000000),
                        "market_value": random.randint(5000000000, 20000000000)
                    })
                    total_weight += weight
            
            # Next 7 holdings get 2-8% each
            for i, stock_symbol in enumerate(top_holdings[3:10]):
                if any(s["symbol"] == stock_symbol for s in available_stocks):
                    weight = random.uniform(2.0, 8.0)
                    holdings.append({
                        "etf_symbol": etf_symbol,
                        "stock_symbol": stock_symbol,
                        "weight_percentage": round(weight, 3),
                        "shares_held": random.randint(5000000, 25000000),
                        "market_value": random.randint(1000000000, 10000000000)
                    })
                    total_weight += weight
        
        # Fill remaining weight with sector-appropriate stocks
        sector_weights = composition["sector_weights"]
        remaining_weight = 100 - total_weight
        
        # Get stocks by sector for this ETF
        for sector, sector_target_weight in sector_weights.items():
            sector_stocks = [s for s in available_stocks if s["sector"] == sector]
            
            # Skip stocks already in top holdings
            existing_symbols = [h["stock_symbol"] for h in holdings]
            sector_stocks = [s for s in sector_stocks if s["symbol"] not in existing_symbols]
            
            if sector_stocks and remaining_weight > 0:
                # Add 5-15 stocks from this sector
                num_stocks = min(random.randint(5, 15), len(sector_stocks), int(remaining_weight / 0.1))
                selected_stocks = random.sample(sector_stocks, num_stocks)
                
                sector_weight_available = min(remaining_weight, sector_target_weight * remaining_weight / 100)
                
                for stock in selected_stocks:
                    if sector_weight_available > 0.1:
                        # Smaller holdings get 0.1-2% each
                        weight = min(random.uniform(0.1, 2.0), sector_weight_available)
                        holdings.append({
                            "etf_symbol": etf_symbol,
                            "stock_symbol": stock["symbol"],
                            "weight_percentage": round(weight, 3),
                            "shares_held": random.randint(100000, 5000000),
                            "market_value": random.randint(50000000, 2000000000)
                        })
                        sector_weight_available -= weight
                        remaining_weight -= weight
        
        # Normalize weights to ensure they sum to ~100%
        current_total = sum(h["weight_percentage"] for h in holdings)
        if current_total > 0:
            normalization_factor = 100.0 / current_total
            for holding in holdings:
                holding["weight_percentage"] = round(holding["weight_percentage"] * normalization_factor, 3)
        
        all_holdings.extend(holdings)
        print(f"  Created {len(holdings)} holdings (total weight: {sum(h['weight_percentage'] for h in holdings):.1f}%)")
    
    return all_holdings

def insert_etf_holdings():
    print("🚀 Creating ETF holdings with stock weightings...")
    
    try:
        # Show schema first
        print("\n📋 ETF Holdings Table Schema:")
        create_etf_holdings_schema()
        
        print("\n⚠️  Please create the ETF holdings table in Supabase first, then press Enter to continue...")
        input()
        
        # Generate holdings data
        holdings_data = create_etf_holdings_data()
        
        if not holdings_data:
            print("❌ No holdings data generated")
            return
        
        # Insert holdings in batches
        print(f"\n📊 Inserting {len(holdings_data)} ETF holdings...")
        batch_size = 50
        success_count = 0
        
        for i in range(0, len(holdings_data), batch_size):
            batch = holdings_data[i:i+batch_size]
            try:
                result = supabase_db.supabase.table('etf_holdings').insert(batch).execute()
                success_count += len(batch)
                if success_count % 100 == 0:
                    print(f"✅ Inserted {success_count} holdings...")
            except Exception as e:
                print(f"❌ Error inserting holdings batch: {e}")
        
        print(f"✅ Inserted {success_count} ETF holdings")
        
        # Show summary by ETF
        print("\n📋 Holdings Summary by ETF:")
        etf_summary = {}
        for holding in holdings_data:
            etf = holding["etf_symbol"]
            if etf not in etf_summary:
                etf_summary[etf] = {"count": 0, "total_weight": 0}
            etf_summary[etf]["count"] += 1
            etf_summary[etf]["total_weight"] += holding["weight_percentage"]
        
        for etf, summary in etf_summary.items():
            print(f"   • {etf}: {summary['count']} holdings, {summary['total_weight']:.1f}% total weight")
        
        print("\n🎉 ETF HOLDINGS INSERTION COMPLETE!")
        print("\n🔗 New API endpoints available:")
        print("   • GET /api/etfs/SPY/holdings - Get ETF holdings")
        print("   • GET /api/stocks/AAPL/etfs - Get ETFs that hold this stock")
        
    except Exception as e:
        print(f"❌ Error during ETF holdings insertion: {e}")

# Add ETF holdings endpoints
def add_etf_holdings_endpoints():
    """Add new endpoints to main.py for ETF holdings"""
    
    endpoints_code = '''
# ETF HOLDINGS ENDPOINTS
@app.get("/api/etfs/{symbol}/holdings")
async def get_etf_holdings(symbol: str, limit: int = 50):
    """Get ETF holdings with stock weights"""
    try:
        symbol = symbol.upper()
        result = supabase_db.supabase.table('etf_holdings').select('*, stocks(name, sector)').eq('etf_symbol', symbol).order('weight_percentage', desc=True).limit(limit).execute()
        return result.data
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

@app.get("/api/etfs/{symbol}/top-holdings")
async def get_etf_top_holdings(symbol: str, limit: int = 10):
    """Get top holdings of an ETF"""
    try:
        symbol = symbol.upper()
        result = supabase_db.supabase.table('etf_holdings').select('*, stocks(name, sector, market_cap)').eq('etf_symbol', symbol).order('weight_percentage', desc=True).limit(limit).execute()
        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
'''
    
    print("\n📝 Add these endpoints to your main.py:")
    print("=" * 60)
    print(endpoints_code)
    print("=" * 60)

if __name__ == "__main__":
    insert_etf_holdings()
    add_etf_holdings_endpoints()
