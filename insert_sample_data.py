from supabase_db import supabase_db
from datetime import date

def insert_sample_data():
    print("Inserting sample data...")
    
    # Sample stocks
    stocks = [
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "market_cap": 3000000000000},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "industry": "Internet Services", "market_cap": 2000000000000},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "industry": "Software", "market_cap": 2800000000000},
        {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers", "market_cap": 800000000000},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors", "market_cap": 1800000000000}
    ]
    
    # Sample sectors
    sectors = [
        {"name": "Technology", "performance_1d": 1.5, "performance_1w": 3.2, "performance_1m": 8.7, "performance_ytd": 25.4},
        {"name": "Healthcare", "performance_1d": 0.8, "performance_1w": 1.9, "performance_1m": 4.3, "performance_ytd": 12.1},
        {"name": "Financial Services", "performance_1d": -0.3, "performance_1w": 2.1, "performance_1m": 6.8, "performance_ytd": 18.9},
        {"name": "Consumer Cyclical", "performance_1d": 2.1, "performance_1w": 4.5, "performance_1m": 12.3, "performance_ytd": 28.7},
        {"name": "Energy", "performance_1d": -1.2, "performance_1w": -2.8, "performance_1m": 3.4, "performance_ytd": 15.6}
    ]
    
    # Sample stock prices
    stock_prices = [
        {"symbol": "AAPL", "date": "2024-01-15", "open_price": 185.50, "high_price": 188.20, "low_price": 184.30, "close_price": 187.45, "volume": 45000000},
        {"symbol": "AAPL", "date": "2024-01-16", "open_price": 187.45, "high_price": 189.80, "low_price": 186.90, "close_price": 189.25, "volume": 42000000},
        {"symbol": "GOOGL", "date": "2024-01-15", "open_price": 142.30, "high_price": 144.50, "low_price": 141.80, "close_price": 143.90, "volume": 28000000},
        {"symbol": "GOOGL", "date": "2024-01-16", "open_price": 143.90, "high_price": 145.20, "low_price": 143.10, "close_price": 144.75, "volume": 25000000},
        {"symbol": "MSFT", "date": "2024-01-15", "open_price": 384.20, "high_price": 387.50, "low_price": 383.10, "close_price": 386.95, "volume": 22000000}
    ]
    
    # Sample fundamentals
    fundamentals = [
        {"symbol": "AAPL", "pe_ratio": 28.5, "pb_ratio": 45.2, "debt_to_equity": 1.73, "roe": 160.58, "revenue": 394328000000, "net_income": 99803000000, "eps": 6.16, "dividend_yield": 0.44, "quarter": "Q4", "year": 2023},
        {"symbol": "GOOGL", "pe_ratio": 25.8, "pb_ratio": 5.9, "debt_to_equity": 0.11, "roe": 30.22, "revenue": 307394000000, "net_income": 73795000000, "eps": 5.80, "dividend_yield": 0.0, "quarter": "Q4", "year": 2023},
        {"symbol": "MSFT", "pe_ratio": 32.1, "pb_ratio": 12.8, "debt_to_equity": 0.47, "roe": 38.52, "revenue": 211915000000, "net_income": 72361000000, "eps": 9.65, "dividend_yield": 0.72, "quarter": "Q4", "year": 2023}
    ]
    
    try:
        # Insert stocks
        for stock in stocks:
            result = supabase_db.insert_stock(stock)
            print(f"✅ Inserted stock: {stock['symbol']}")
        
        # Insert sectors
        for sector in sectors:
            result = supabase_db.insert_sector(sector)
            print(f"✅ Inserted sector: {sector['name']}")
        
        # Insert stock prices
        for price in stock_prices:
            result = supabase_db.insert_stock_price(price)
            print(f"✅ Inserted price for: {price['symbol']} on {price['date']}")
        
        # Insert fundamentals (using raw supabase client)
        for fundamental in fundamentals:
            result = supabase_db.supabase.table('fundamentals').insert(fundamental).execute()
            print(f"✅ Inserted fundamentals for: {fundamental['symbol']}")
        
        print("\n🎉 Sample data inserted successfully!")
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")

if __name__ == "__main__":
    insert_sample_data()
