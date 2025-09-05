from supabase_db import supabase_db
from datetime import date, datetime, timedelta
import random

def create_comprehensive_data():
    print("Creating comprehensive 2-year financial data...")
    
    # 11 Major sectors with 5+ stocks each (55 total stocks)
    stocks_by_sector = {
        "Technology": [
            {"symbol": "AAPL", "name": "Apple Inc.", "industry": "Consumer Electronics", "market_cap": 3000000000000},
            {"symbol": "MSFT", "name": "Microsoft Corporation", "industry": "Software", "market_cap": 2800000000000},
            {"symbol": "GOOGL", "name": "Alphabet Inc.", "industry": "Internet Services", "market_cap": 2000000000000},
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "industry": "Semiconductors", "market_cap": 1800000000000},
            {"symbol": "META", "name": "Meta Platforms Inc.", "industry": "Internet Services", "market_cap": 900000000000},
            {"symbol": "NFLX", "name": "Netflix Inc.", "industry": "Entertainment", "market_cap": 200000000000}
        ],
        "Healthcare": [
            {"symbol": "JNJ", "name": "Johnson & Johnson", "industry": "Drug Manufacturers", "market_cap": 420000000000},
            {"symbol": "UNH", "name": "UnitedHealth Group Inc.", "industry": "Healthcare Plans", "market_cap": 520000000000},
            {"symbol": "PFE", "name": "Pfizer Inc.", "industry": "Drug Manufacturers", "market_cap": 180000000000},
            {"symbol": "ABBV", "name": "AbbVie Inc.", "industry": "Drug Manufacturers", "market_cap": 280000000000},
            {"symbol": "TMO", "name": "Thermo Fisher Scientific Inc.", "industry": "Diagnostics & Research", "market_cap": 220000000000}
        ],
        "Financial Services": [
            {"symbol": "BRK.B", "name": "Berkshire Hathaway Inc.", "industry": "Insurance", "market_cap": 750000000000},
            {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "industry": "Banks", "market_cap": 450000000000},
            {"symbol": "V", "name": "Visa Inc.", "industry": "Credit Services", "market_cap": 500000000000},
            {"symbol": "MA", "name": "Mastercard Inc.", "industry": "Credit Services", "market_cap": 400000000000},
            {"symbol": "BAC", "name": "Bank of America Corp.", "industry": "Banks", "market_cap": 280000000000}
        ],
        "Consumer Cyclical": [
            {"symbol": "AMZN", "name": "Amazon.com Inc.", "industry": "Internet Retail", "market_cap": 1500000000000},
            {"symbol": "TSLA", "name": "Tesla Inc.", "industry": "Auto Manufacturers", "market_cap": 800000000000},
            {"symbol": "HD", "name": "Home Depot Inc.", "industry": "Home Improvement", "market_cap": 350000000000},
            {"symbol": "MCD", "name": "McDonald's Corp.", "industry": "Restaurants", "market_cap": 200000000000},
            {"symbol": "NKE", "name": "Nike Inc.", "industry": "Footwear & Accessories", "market_cap": 180000000000}
        ],
        "Consumer Defensive": [
            {"symbol": "PG", "name": "Procter & Gamble Co.", "industry": "Household Products", "market_cap": 380000000000},
            {"symbol": "KO", "name": "Coca-Cola Co.", "industry": "Beverages", "market_cap": 260000000000},
            {"symbol": "PEP", "name": "PepsiCo Inc.", "industry": "Beverages", "market_cap": 240000000000},
            {"symbol": "WMT", "name": "Walmart Inc.", "industry": "Discount Stores", "market_cap": 450000000000},
            {"symbol": "COST", "name": "Costco Wholesale Corp.", "industry": "Discount Stores", "market_cap": 320000000000}
        ],
        "Energy": [
            {"symbol": "XOM", "name": "Exxon Mobil Corp.", "industry": "Oil & Gas", "market_cap": 450000000000},
            {"symbol": "CVX", "name": "Chevron Corp.", "industry": "Oil & Gas", "market_cap": 300000000000},
            {"symbol": "COP", "name": "ConocoPhillips", "industry": "Oil & Gas", "market_cap": 150000000000},
            {"symbol": "SLB", "name": "Schlumberger NV", "industry": "Oil & Gas Equipment", "market_cap": 70000000000},
            {"symbol": "EOG", "name": "EOG Resources Inc.", "industry": "Oil & Gas", "market_cap": 80000000000}
        ],
        "Communication Services": [
            {"symbol": "DIS", "name": "Walt Disney Co.", "industry": "Entertainment", "market_cap": 200000000000},
            {"symbol": "CMCSA", "name": "Comcast Corp.", "industry": "Telecom Services", "market_cap": 180000000000},
            {"symbol": "VZ", "name": "Verizon Communications Inc.", "industry": "Telecom Services", "market_cap": 170000000000},
            {"symbol": "T", "name": "AT&T Inc.", "industry": "Telecom Services", "market_cap": 120000000000},
            {"symbol": "TMUS", "name": "T-Mobile US Inc.", "industry": "Telecom Services", "market_cap": 200000000000}
        ],
        "Industrials": [
            {"symbol": "BA", "name": "Boeing Co.", "industry": "Aerospace & Defense", "market_cap": 130000000000},
            {"symbol": "CAT", "name": "Caterpillar Inc.", "industry": "Farm & Heavy Construction", "market_cap": 150000000000},
            {"symbol": "GE", "name": "General Electric Co.", "industry": "Specialty Industrial Machinery", "market_cap": 180000000000},
            {"symbol": "UPS", "name": "United Parcel Service Inc.", "industry": "Integrated Freight & Logistics", "market_cap": 140000000000},
            {"symbol": "HON", "name": "Honeywell International Inc.", "industry": "Specialty Industrial Machinery", "market_cap": 160000000000}
        ],
        "Materials": [
            {"symbol": "LIN", "name": "Linde PLC", "industry": "Specialty Chemicals", "market_cap": 200000000000},
            {"symbol": "APD", "name": "Air Products & Chemicals Inc.", "industry": "Specialty Chemicals", "market_cap": 60000000000},
            {"symbol": "SHW", "name": "Sherwin-Williams Co.", "industry": "Specialty Chemicals", "market_cap": 80000000000},
            {"symbol": "FCX", "name": "Freeport-McMoRan Inc.", "industry": "Copper", "market_cap": 60000000000},
            {"symbol": "NEM", "name": "Newmont Corp.", "industry": "Gold", "market_cap": 40000000000}
        ],
        "Real Estate": [
            {"symbol": "AMT", "name": "American Tower Corp.", "industry": "REIT - Specialty", "market_cap": 100000000000},
            {"symbol": "PLD", "name": "Prologis Inc.", "industry": "REIT - Industrial", "market_cap": 120000000000},
            {"symbol": "CCI", "name": "Crown Castle Inc.", "industry": "REIT - Specialty", "market_cap": 60000000000},
            {"symbol": "EQIX", "name": "Equinix Inc.", "industry": "REIT - Specialty", "market_cap": 80000000000},
            {"symbol": "SPG", "name": "Simon Property Group Inc.", "industry": "REIT - Retail", "market_cap": 50000000000}
        ],
        "Utilities": [
            {"symbol": "NEE", "name": "NextEra Energy Inc.", "industry": "Utilities - Regulated Electric", "market_cap": 160000000000},
            {"symbol": "DUK", "name": "Duke Energy Corp.", "industry": "Utilities - Regulated Electric", "market_cap": 80000000000},
            {"symbol": "SO", "name": "Southern Co.", "industry": "Utilities - Regulated Electric", "market_cap": 75000000000},
            {"symbol": "D", "name": "Dominion Energy Inc.", "industry": "Utilities - Regulated Electric", "market_cap": 70000000000},
            {"symbol": "AEP", "name": "American Electric Power Co. Inc.", "industry": "Utilities - Regulated Electric", "market_cap": 50000000000}
        ]
    }
    
    # Flatten stocks with sector info
    all_stocks = []
    for sector, stocks in stocks_by_sector.items():
        for stock in stocks:
            stock["sector"] = sector
            all_stocks.append(stock)
    
    # Enhanced sector performance data
    sectors_data = [
        {"name": "Technology", "performance_1d": 1.5, "performance_1w": 3.2, "performance_1m": 8.7, "performance_ytd": 25.4},
        {"name": "Healthcare", "performance_1d": 0.8, "performance_1w": 1.9, "performance_1m": 4.3, "performance_ytd": 12.1},
        {"name": "Financial Services", "performance_1d": -0.3, "performance_1w": 2.1, "performance_1m": 6.8, "performance_ytd": 18.9},
        {"name": "Consumer Cyclical", "performance_1d": 2.1, "performance_1w": 4.5, "performance_1m": 12.3, "performance_ytd": 28.7},
        {"name": "Consumer Defensive", "performance_1d": 0.2, "performance_1w": 0.8, "performance_1m": 2.1, "performance_ytd": 8.5},
        {"name": "Energy", "performance_1d": -1.2, "performance_1w": -2.8, "performance_1m": 3.4, "performance_ytd": 15.6},
        {"name": "Communication Services", "performance_1d": 0.9, "performance_1w": 2.3, "performance_1m": 5.7, "performance_ytd": 14.2},
        {"name": "Industrials", "performance_1d": 1.1, "performance_1w": 2.8, "performance_1m": 7.2, "performance_ytd": 16.8},
        {"name": "Materials", "performance_1d": -0.5, "performance_1w": 1.2, "performance_1m": 4.8, "performance_ytd": 11.3},
        {"name": "Real Estate", "performance_1d": 0.3, "performance_1w": 1.5, "performance_1m": 3.2, "performance_ytd": 9.7},
        {"name": "Utilities", "performance_1d": -0.1, "performance_1w": 0.5, "performance_1m": 1.8, "performance_ytd": 6.2}
    ]
    
    # Generate 2 years of stock prices (730 days)
    def generate_2_year_prices():
        prices = []
        base_prices = {}
        
        # Set realistic base prices for each stock
        for stock in all_stocks:
            symbol = stock["symbol"]
            if symbol in ["AAPL", "MSFT", "GOOGL"]:
                base_prices[symbol] = random.uniform(150, 200)
            elif symbol in ["AMZN", "NVDA", "TSLA"]:
                base_prices[symbol] = random.uniform(200, 500)
            elif symbol in ["BRK.B", "UNH"]:
                base_prices[symbol] = random.uniform(300, 600)
            else:
                base_prices[symbol] = random.uniform(30, 150)
        
        # Generate 2 years of data
        for symbol, base_price in base_prices.items():
            current_price = base_price
            
            for i in range(730):  # 2 years
                date_obj = date.today() - timedelta(days=729-i)
                
                # Add some trend and seasonality
                trend = 0.0002 if i > 365 else 0.0001  # Slight upward trend
                seasonal = 0.001 * random.uniform(-1, 1)  # Random seasonal effect
                daily_change = random.uniform(-0.03, 0.03)  # ±3% daily change
                
                total_change = trend + seasonal + daily_change
                current_price *= (1 + total_change)
                
                # Ensure price doesn't go negative
                current_price = max(current_price, 1.0)
                
                open_price = current_price * random.uniform(0.99, 1.01)
                high_price = max(open_price, current_price) * random.uniform(1.0, 1.02)
                low_price = min(open_price, current_price) * random.uniform(0.98, 1.0)
                volume = random.randint(5000000, 150000000)
                
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
    
    # Generate fundamentals for all stocks (8 quarters of data)
    def generate_fundamentals():
        fundamentals = []
        quarters = ["Q1", "Q2", "Q3", "Q4"]
        years = [2022, 2023]
        
        for stock in all_stocks:
            symbol = stock["symbol"]
            
            for year in years:
                for quarter in quarters:
                    # Vary fundamentals by sector
                    sector = stock["sector"]
                    
                    if sector == "Technology":
                        pe_base, roe_base = 25, 25
                    elif sector == "Healthcare":
                        pe_base, roe_base = 18, 15
                    elif sector == "Financial Services":
                        pe_base, roe_base = 12, 12
                    elif sector == "Energy":
                        pe_base, roe_base = 15, 8
                    else:
                        pe_base, roe_base = 20, 18
                    
                    fundamentals.append({
                        "symbol": symbol,
                        "pe_ratio": round(pe_base + random.uniform(-5, 10), 2),
                        "pb_ratio": round(random.uniform(1.5, 8.0), 2),
                        "debt_to_equity": round(random.uniform(0.1, 2.5), 2),
                        "roe": round(roe_base + random.uniform(-5, 15), 2),
                        "revenue": random.randint(10000000000, 500000000000),
                        "net_income": random.randint(1000000000, 100000000000),
                        "eps": round(random.uniform(1.0, 15.0), 2),
                        "dividend_yield": round(random.uniform(0.0, 4.0), 2),
                        "quarter": quarter,
                        "year": year
                    })
        
        return fundamentals
    
    # Generate technical indicators for last 90 days
    def generate_technical_indicators():
        indicators = []
        
        for stock in all_stocks[:20]:  # First 20 stocks to keep it manageable
            symbol = stock["symbol"]
            
            for i in range(90):  # Last 90 days
                date_obj = date.today() - timedelta(days=89-i)
                
                base_price = random.uniform(50, 300)
                
                indicators.append({
                    "symbol": symbol,
                    "date": date_obj.isoformat(),
                    "sma_20": round(base_price * random.uniform(0.95, 1.05), 2),
                    "sma_50": round(base_price * random.uniform(0.90, 1.10), 2),
                    "sma_200": round(base_price * random.uniform(0.85, 1.15), 2),
                    "rsi": round(random.uniform(25.0, 75.0), 2),
                    "macd": round(random.uniform(-3.0, 3.0), 4),
                    "bollinger_upper": round(base_price * 1.1, 2),
                    "bollinger_lower": round(base_price * 0.9, 2)
                })
        
        return indicators
    
    print("📊 Generating comprehensive data...")
    print(f"   • {len(all_stocks)} stocks across {len(sectors_data)} sectors")
    print("   • 2 years of daily price data")
    print("   • 8 quarters of fundamentals")
    print("   • 90 days of technical indicators")
    
    return {
        "stocks": all_stocks,
        "sectors": sectors_data,
        "stock_prices": generate_2_year_prices(),
        "fundamentals": generate_fundamentals(),
        "technical_indicators": generate_technical_indicators()
    }

def insert_comprehensive_data():
    print("🚀 Creating and inserting comprehensive 2-year financial data...")
    
    try:
        # Clear existing data first
        print("\n🧹 Clearing existing data...")
        try:
            supabase_db.supabase.table('technical_indicators').delete().neq('id', 0).execute()
            supabase_db.supabase.table('fundamentals').delete().neq('id', 0).execute()
            supabase_db.supabase.table('stock_prices').delete().neq('id', 0).execute()
            supabase_db.supabase.table('stocks').delete().neq('id', 0).execute()
            supabase_db.supabase.table('sectors').delete().neq('id', 0).execute()
            print("✅ Existing data cleared")
        except Exception as e:
            print(f"⚠️  Error clearing data (might be empty): {e}")
        
        # Generate new data
        data = create_comprehensive_data()
        
        # Insert sectors
        print(f"\n🏢 Inserting {len(data['sectors'])} sectors...")
        for sector in data["sectors"]:
            try:
                result = supabase_db.insert_sector(sector)
                print(f"✅ {sector['name']}")
            except Exception as e:
                print(f"❌ Error inserting {sector['name']}: {e}")
        
        # Insert stocks
        print(f"\n📊 Inserting {len(data['stocks'])} stocks...")
        for stock in data["stocks"]:
            try:
                result = supabase_db.insert_stock(stock)
                print(f"✅ {stock['symbol']} - {stock['name']} ({stock['sector']})")
            except Exception as e:
                print(f"❌ Error inserting {stock['symbol']}: {e}")
        
        # Insert stock prices in batches
        print(f"\n💹 Inserting {len(data['stock_prices'])} stock prices (2 years)...")
        batch_size = 100
        success_count = 0
        
        for i in range(0, len(data['stock_prices']), batch_size):
            batch = data['stock_prices'][i:i+batch_size]
            try:
                result = supabase_db.supabase.table('stock_prices').insert(batch).execute()
                success_count += len(batch)
                if success_count % 1000 == 0:
                    print(f"✅ Inserted {success_count} prices...")
            except Exception as e:
                print(f"❌ Error inserting price batch: {e}")
        
        print(f"✅ Inserted {success_count} stock prices")
        
        # Insert fundamentals in batches
        print(f"\n📈 Inserting {len(data['fundamentals'])} fundamentals...")
        batch_size = 50
        success_count = 0
        
        for i in range(0, len(data['fundamentals']), batch_size):
            batch = data['fundamentals'][i:i+batch_size]
            try:
                result = supabase_db.supabase.table('fundamentals').insert(batch).execute()
                success_count += len(batch)
            except Exception as e:
                print(f"❌ Error inserting fundamentals batch: {e}")
        
        print(f"✅ Inserted {success_count} fundamental records")
        
        # Insert technical indicators in batches
        print(f"\n📊 Inserting {len(data['technical_indicators'])} technical indicators...")
        batch_size = 50
        success_count = 0
        
        for i in range(0, len(data['technical_indicators']), batch_size):
            batch = data['technical_indicators'][i:i+batch_size]
            try:
                result = supabase_db.supabase.table('technical_indicators').insert(batch).execute()
                success_count += len(batch)
            except Exception as e:
                print(f"❌ Error inserting technical batch: {e}")
        
        print(f"✅ Inserted {success_count} technical indicators")
        
        print("\n🎉 COMPREHENSIVE DATA INSERTION COMPLETE!")
        print("\n📋 Final Summary:")
        print(f"   • {len(data['stocks'])} stocks across {len(data['sectors'])} sectors")
        print(f"   • {len(data['stock_prices'])} stock prices (2 years daily data)")
        print(f"   • {len(data['fundamentals'])} fundamental records (8 quarters)")
        print(f"   • {len(data['technical_indicators'])} technical indicators (90 days)")
        
        print("\n🔗 Test your APIs:")
        print("   • http://localhost:8000/docs")
        print("   • http://localhost:8000/api/stocks/AAPL")
        print("   • http://localhost:8000/api/sectors")
        print("   • http://localhost:8000/api/screener/gainers")
        
    except Exception as e:
        print(f"❌ Error during comprehensive data insertion: {e}")

if __name__ == "__main__":
    insert_comprehensive_data()
