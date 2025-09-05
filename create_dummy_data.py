from supabase_db import supabase_db
from datetime import date, datetime, timedelta
import random

def create_dummy_data():
    print("Creating comprehensive dummy financial data...")
    
    # 20 Popular stocks with realistic data
    stocks_data = [
        {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "industry": "Consumer Electronics", "market_cap": 3000000000000},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "sector": "Technology", "industry": "Software", "market_cap": 2800000000000},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "industry": "Internet Services", "market_cap": 2000000000000},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "industry": "Internet Retail", "market_cap": 1500000000000},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "sector": "Technology", "industry": "Semiconductors", "market_cap": 1800000000000},
        {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer Cyclical", "industry": "Auto Manufacturers", "market_cap": 800000000000},
        {"symbol": "META", "name": "Meta Platforms Inc.", "sector": "Technology", "industry": "Internet Services", "market_cap": 900000000000},
        {"symbol": "BRK.B", "name": "Berkshire Hathaway Inc.", "sector": "Financial Services", "industry": "Insurance", "market_cap": 750000000000},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "sector": "Financial Services", "industry": "Banks", "market_cap": 450000000000},
        {"symbol": "JNJ", "name": "Johnson & Johnson", "sector": "Healthcare", "industry": "Drug Manufacturers", "market_cap": 420000000000},
        {"symbol": "V", "name": "Visa Inc.", "sector": "Financial Services", "industry": "Credit Services", "market_cap": 500000000000},
        {"symbol": "PG", "name": "Procter & Gamble Co.", "sector": "Consumer Defensive", "industry": "Household Products", "market_cap": 380000000000},
        {"symbol": "UNH", "name": "UnitedHealth Group Inc.", "sector": "Healthcare", "industry": "Healthcare Plans", "market_cap": 520000000000},
        {"symbol": "HD", "name": "Home Depot Inc.", "sector": "Consumer Cyclical", "industry": "Home Improvement", "market_cap": 350000000000},
        {"symbol": "MA", "name": "Mastercard Inc.", "sector": "Financial Services", "industry": "Credit Services", "market_cap": 400000000000},
        {"symbol": "PFE", "name": "Pfizer Inc.", "sector": "Healthcare", "industry": "Drug Manufacturers", "market_cap": 180000000000},
        {"symbol": "BAC", "name": "Bank of America Corp.", "sector": "Financial Services", "industry": "Banks", "market_cap": 280000000000},
        {"symbol": "KO", "name": "Coca-Cola Co.", "sector": "Consumer Defensive", "industry": "Beverages", "market_cap": 260000000000},
        {"symbol": "DIS", "name": "Walt Disney Co.", "sector": "Communication Services", "industry": "Entertainment", "market_cap": 200000000000},
        {"symbol": "XOM", "name": "Exxon Mobil Corp.", "sector": "Energy", "industry": "Oil & Gas", "market_cap": 450000000000}
    ]
    
    # Sector performance data
    sectors_data = [
        {"name": "Technology", "performance_1d": 1.5, "performance_1w": 3.2, "performance_1m": 8.7, "performance_ytd": 25.4},
        {"name": "Healthcare", "performance_1d": 0.8, "performance_1w": 1.9, "performance_1m": 4.3, "performance_ytd": 12.1},
        {"name": "Financial Services", "performance_1d": -0.3, "performance_1w": 2.1, "performance_1m": 6.8, "performance_ytd": 18.9},
        {"name": "Consumer Cyclical", "performance_1d": 2.1, "performance_1w": 4.5, "performance_1m": 12.3, "performance_ytd": 28.7},
        {"name": "Consumer Defensive", "performance_1d": 0.2, "performance_1w": 0.8, "performance_1m": 2.1, "performance_ytd": 8.5},
        {"name": "Energy", "performance_1d": -1.2, "performance_1w": -2.8, "performance_1m": 3.4, "performance_ytd": 15.6},
        {"name": "Communication Services", "performance_1d": 0.9, "performance_1w": 2.3, "performance_1m": 5.7, "performance_ytd": 14.2}
    ]
    
    # Generate stock prices for last 30 days
    def generate_stock_prices():
        prices = []
        base_prices = {
            "AAPL": 185.0, "MSFT": 380.0, "GOOGL": 140.0, "AMZN": 145.0, "NVDA": 480.0,
            "TSLA": 240.0, "META": 320.0, "BRK.B": 350.0, "JPM": 150.0, "JNJ": 160.0,
            "V": 250.0, "PG": 155.0, "UNH": 520.0, "HD": 320.0, "MA": 420.0,
            "PFE": 35.0, "BAC": 32.0, "KO": 60.0, "DIS": 95.0, "XOM": 110.0
        }
        
        for symbol, base_price in base_prices.items():
            current_price = base_price
            for i in range(30):
                date_obj = date.today() - timedelta(days=29-i)
                
                # Random price movement
                change = random.uniform(-0.05, 0.05)  # ±5% daily change
                current_price *= (1 + change)
                
                open_price = current_price * random.uniform(0.98, 1.02)
                high_price = max(open_price, current_price) * random.uniform(1.0, 1.03)
                low_price = min(open_price, current_price) * random.uniform(0.97, 1.0)
                volume = random.randint(10000000, 100000000)
                
                prices.append({
                    "symbol": symbol,
                    "date": date_obj.isoformat(),
                    "open_price": round(open_price, 2),
                    "high_price": round(high_price, 2),
                    "low_price": round(low_price, 2),
                    "close_price": round(current_price, 2),
                    "volume": volume
                })
        
        return prices
    
    # Generate fundamentals data
    def generate_fundamentals():
        fundamentals = []
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "JPM", "JNJ", "V"]
        
        for symbol in symbols:
            fundamentals.append({
                "symbol": symbol,
                "pe_ratio": round(random.uniform(15.0, 35.0), 2),
                "pb_ratio": round(random.uniform(2.0, 15.0), 2),
                "debt_to_equity": round(random.uniform(0.1, 2.0), 2),
                "roe": round(random.uniform(10.0, 40.0), 2),
                "revenue": random.randint(50000000000, 400000000000),
                "net_income": random.randint(10000000000, 100000000000),
                "eps": round(random.uniform(2.0, 12.0), 2),
                "dividend_yield": round(random.uniform(0.0, 3.0), 2),
                "quarter": "Q4",
                "year": 2023
            })
        
        return fundamentals
    
    # Generate technical indicators
    def generate_technical_indicators():
        indicators = []
        symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
        
        for symbol in symbols:
            for i in range(10):  # Last 10 days
                date_obj = date.today() - timedelta(days=9-i)
                
                indicators.append({
                    "symbol": symbol,
                    "date": date_obj.isoformat(),
                    "sma_20": round(random.uniform(150.0, 200.0), 2),
                    "sma_50": round(random.uniform(140.0, 190.0), 2),
                    "sma_200": round(random.uniform(130.0, 180.0), 2),
                    "rsi": round(random.uniform(30.0, 70.0), 2),
                    "macd": round(random.uniform(-2.0, 2.0), 4),
                    "bollinger_upper": round(random.uniform(180.0, 210.0), 2),
                    "bollinger_lower": round(random.uniform(140.0, 170.0), 2)
                })
        
        return indicators
    
    # Generate all data
    stock_prices = generate_stock_prices()
    fundamentals = generate_fundamentals()
    technical_indicators = generate_technical_indicators()
    
    return {
        "stocks": stocks_data,
        "sectors": sectors_data,
        "stock_prices": stock_prices,
        "fundamentals": fundamentals,
        "technical_indicators": technical_indicators
    }

def insert_all_dummy_data():
    print("🚀 Creating and inserting comprehensive dummy data...")
    
    try:
        # Generate data
        data = create_dummy_data()
        
        # Insert stocks
        print("\n📊 Inserting stocks...")
        for stock in data["stocks"]:
            try:
                result = supabase_db.insert_stock(stock)
                print(f"✅ {stock['symbol']} - {stock['name']}")
            except Exception as e:
                if "duplicate key" in str(e).lower():
                    print(f"⚠️  {stock['symbol']} already exists")
                else:
                    print(f"❌ Error inserting {stock['symbol']}: {e}")
        
        # Insert sectors
        print("\n🏢 Inserting sectors...")
        for sector in data["sectors"]:
            try:
                result = supabase_db.insert_sector(sector)
                print(f"✅ {sector['name']}")
            except Exception as e:
                if "duplicate key" in str(e).lower():
                    print(f"⚠️  {sector['name']} already exists")
                else:
                    print(f"❌ Error inserting {sector['name']}: {e}")
        
        # Insert stock prices
        print(f"\n💹 Inserting {len(data['stock_prices'])} stock prices...")
        success_count = 0
        for price in data["stock_prices"]:
            try:
                result = supabase_db.insert_stock_price(price)
                success_count += 1
                if success_count % 50 == 0:
                    print(f"✅ Inserted {success_count} prices...")
            except Exception as e:
                if "duplicate key" not in str(e).lower():
                    print(f"❌ Error inserting price for {price['symbol']}: {e}")
        
        print(f"✅ Inserted {success_count} stock prices")
        
        # Insert fundamentals
        print(f"\n📈 Inserting {len(data['fundamentals'])} fundamentals...")
        for fundamental in data["fundamentals"]:
            try:
                result = supabase_db.supabase.table('fundamentals').insert(fundamental).execute()
                print(f"✅ {fundamental['symbol']} fundamentals")
            except Exception as e:
                if "duplicate key" not in str(e).lower():
                    print(f"❌ Error inserting fundamentals for {fundamental['symbol']}: {e}")
        
        # Insert technical indicators
        print(f"\n📊 Inserting {len(data['technical_indicators'])} technical indicators...")
        success_count = 0
        for indicator in data["technical_indicators"]:
            try:
                result = supabase_db.supabase.table('technical_indicators').insert(indicator).execute()
                success_count += 1
            except Exception as e:
                if "duplicate key" not in str(e).lower():
                    print(f"❌ Error inserting indicator for {indicator['symbol']}: {e}")
        
        print(f"✅ Inserted {success_count} technical indicators")
        
        print("\n🎉 DUMMY DATA INSERTION COMPLETE!")
        print("\n📋 Summary:")
        print(f"   • {len(data['stocks'])} stocks")
        print(f"   • {len(data['sectors'])} sectors") 
        print(f"   • {len(data['stock_prices'])} stock prices (30 days)")
        print(f"   • {len(data['fundamentals'])} fundamental records")
        print(f"   • {len(data['technical_indicators'])} technical indicators")
        
        print("\n🔗 Test your APIs:")
        print("   • http://localhost:8000/docs")
        print("   • http://localhost:8000/api/stocks/AAPL")
        print("   • http://localhost:8000/api/sectors")
        print("   • http://localhost:8000/api/screener/gainers")
        
    except Exception as e:
        print(f"❌ Error during data insertion: {e}")

if __name__ == "__main__":
    insert_all_dummy_data()
