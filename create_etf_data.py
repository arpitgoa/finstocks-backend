from supabase_db import supabase_db
from datetime import date, datetime, timedelta
import random

def create_etf_schema():
    """Create ETF table in Supabase"""
    sql_schema = """
    -- Create ETFs table
    CREATE TABLE IF NOT EXISTS etfs (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10) UNIQUE NOT NULL,
        name VARCHAR(255) NOT NULL,
        category VARCHAR(100) NOT NULL,
        expense_ratio DECIMAL(4,3),
        aum DECIMAL(15,2),
        inception_date DATE,
        benchmark VARCHAR(255),
        leverage_ratio DECIMAL(3,1) DEFAULT 1.0,
        created_at TIMESTAMP DEFAULT NOW(),
        updated_at TIMESTAMP DEFAULT NOW()
    );

    -- Create ETF prices table
    CREATE TABLE IF NOT EXISTS etf_prices (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10) NOT NULL,
        date DATE NOT NULL,
        open_price DECIMAL(10,4),
        high_price DECIMAL(10,4),
        low_price DECIMAL(10,4),
        close_price DECIMAL(10,4),
        volume BIGINT,
        created_at TIMESTAMP DEFAULT NOW(),
        FOREIGN KEY (symbol) REFERENCES etfs(symbol),
        UNIQUE(symbol, date)
    );

    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_etf_prices_symbol_date ON etf_prices(symbol, date);
    CREATE INDEX IF NOT EXISTS idx_etfs_category ON etfs(category);
    """
    
    print("Copy and paste this SQL into Supabase SQL Editor:")
    print("=" * 60)
    print(sql_schema)
    print("=" * 60)
    return sql_schema

def create_comprehensive_etf_data():
    print("Creating comprehensive ETF data...")
    
    # Comprehensive ETF data by category
    etfs_by_category = {
        "Broad Market": [
            {"symbol": "SPY", "name": "SPDR S&P 500 ETF Trust", "expense_ratio": 0.095, "aum": 400000000000, "benchmark": "S&P 500", "leverage": 1.0},
            {"symbol": "VTI", "name": "Vanguard Total Stock Market ETF", "expense_ratio": 0.03, "aum": 300000000000, "benchmark": "CRSP US Total Market", "leverage": 1.0},
            {"symbol": "IVV", "name": "iShares Core S&P 500 ETF", "expense_ratio": 0.03, "aum": 350000000000, "benchmark": "S&P 500", "leverage": 1.0},
            {"symbol": "VOO", "name": "Vanguard S&P 500 ETF", "expense_ratio": 0.03, "aum": 320000000000, "benchmark": "S&P 500", "leverage": 1.0}
        ],
        "Technology": [
            {"symbol": "QQQ", "name": "Invesco QQQ Trust", "expense_ratio": 0.20, "aum": 200000000000, "benchmark": "NASDAQ-100", "leverage": 1.0},
            {"symbol": "XLK", "name": "Technology Select Sector SPDR Fund", "expense_ratio": 0.12, "aum": 50000000000, "benchmark": "Technology Select Sector", "leverage": 1.0},
            {"symbol": "VGT", "name": "Vanguard Information Technology ETF", "expense_ratio": 0.10, "aum": 60000000000, "benchmark": "MSCI US IT Index", "leverage": 1.0},
            {"symbol": "FTEC", "name": "Fidelity MSCI Information Technology ETF", "expense_ratio": 0.084, "aum": 15000000000, "benchmark": "MSCI USA IT Index", "leverage": 1.0}
        ],
        "Leveraged": [
            {"symbol": "TQQQ", "name": "ProShares UltraPro QQQ", "expense_ratio": 0.95, "aum": 15000000000, "benchmark": "NASDAQ-100", "leverage": 3.0},
            {"symbol": "UPRO", "name": "ProShares UltraPro S&P500", "expense_ratio": 0.92, "aum": 3000000000, "benchmark": "S&P 500", "leverage": 3.0},
            {"symbol": "SOXL", "name": "Direxion Daily Semiconductor Bull 3X Shares", "expense_ratio": 0.99, "aum": 8000000000, "benchmark": "ICE Semiconductor Index", "leverage": 3.0},
            {"symbol": "TECL", "name": "Direxion Daily Technology Bull 3X Shares", "expense_ratio": 0.95, "aum": 2000000000, "benchmark": "Technology Select Sector", "leverage": 3.0},
            {"symbol": "SPXL", "name": "Direxion Daily S&P 500 Bull 3X Shares", "expense_ratio": 0.99, "aum": 4000000000, "benchmark": "S&P 500", "leverage": 3.0}
        ],
        "Small Cap": [
            {"symbol": "IWM", "name": "iShares Russell 2000 ETF", "expense_ratio": 0.19, "aum": 60000000000, "benchmark": "Russell 2000", "leverage": 1.0},
            {"symbol": "VB", "name": "Vanguard Small-Cap ETF", "expense_ratio": 0.05, "aum": 40000000000, "benchmark": "CRSP US Small Cap", "leverage": 1.0},
            {"symbol": "VTWO", "name": "Vanguard Russell 2000 ETF", "expense_ratio": 0.10, "aum": 15000000000, "benchmark": "Russell 2000", "leverage": 1.0},
            {"symbol": "IJR", "name": "iShares Core S&P Small-Cap ETF", "expense_ratio": 0.06, "aum": 70000000000, "benchmark": "S&P SmallCap 600", "leverage": 1.0}
        ],
        "Mid Cap": [
            {"symbol": "MDY", "name": "SPDR S&P MidCap 400 ETF Trust", "expense_ratio": 0.23, "aum": 20000000000, "benchmark": "S&P MidCap 400", "leverage": 1.0},
            {"symbol": "VO", "name": "Vanguard Mid-Cap ETF", "expense_ratio": 0.04, "aum": 35000000000, "benchmark": "CRSP US Mid Cap", "leverage": 1.0},
            {"symbol": "IJH", "name": "iShares Core S&P Mid-Cap ETF", "expense_ratio": 0.05, "aum": 80000000000, "benchmark": "S&P MidCap 400", "leverage": 1.0},
            {"symbol": "VMOT", "name": "Vanguard Russell Mid-Cap ETF", "expense_ratio": 0.20, "aum": 5000000000, "benchmark": "Russell Mid Cap", "leverage": 1.0}
        ],
        "Large Cap": [
            {"symbol": "VV", "name": "Vanguard Large-Cap ETF", "expense_ratio": 0.04, "aum": 25000000000, "benchmark": "CRSP US Large Cap", "leverage": 1.0},
            {"symbol": "IVW", "name": "iShares Russell 1000 Growth ETF", "expense_ratio": 0.19, "aum": 40000000000, "benchmark": "Russell 1000 Growth", "leverage": 1.0},
            {"symbol": "IVE", "name": "iShares Russell 1000 Value ETF", "expense_ratio": 0.19, "aum": 20000000000, "benchmark": "Russell 1000 Value", "leverage": 1.0},
            {"symbol": "VUG", "name": "Vanguard Growth ETF", "expense_ratio": 0.04, "aum": 100000000000, "benchmark": "CRSP US Large Cap Growth", "leverage": 1.0}
        ],
        "Sector ETFs": [
            {"symbol": "XLF", "name": "Financial Select Sector SPDR Fund", "expense_ratio": 0.12, "aum": 40000000000, "benchmark": "Financial Select Sector", "leverage": 1.0},
            {"symbol": "XLE", "name": "Energy Select Sector SPDR Fund", "expense_ratio": 0.12, "aum": 25000000000, "benchmark": "Energy Select Sector", "leverage": 1.0},
            {"symbol": "XLV", "name": "Health Care Select Sector SPDR Fund", "expense_ratio": 0.12, "aum": 35000000000, "benchmark": "Health Care Select Sector", "leverage": 1.0},
            {"symbol": "XLI", "name": "Industrial Select Sector SPDR Fund", "expense_ratio": 0.12, "aum": 20000000000, "benchmark": "Industrial Select Sector", "leverage": 1.0},
            {"symbol": "XLP", "name": "Consumer Staples Select Sector SPDR Fund", "expense_ratio": 0.12, "aum": 15000000000, "benchmark": "Consumer Staples Select Sector", "leverage": 1.0}
        ],
        "International": [
            {"symbol": "VEA", "name": "Vanguard FTSE Developed Markets ETF", "expense_ratio": 0.05, "aum": 100000000000, "benchmark": "FTSE Developed All Cap ex US", "leverage": 1.0},
            {"symbol": "VWO", "name": "Vanguard FTSE Emerging Markets ETF", "expense_ratio": 0.10, "aum": 80000000000, "benchmark": "FTSE Emerging Markets All Cap", "leverage": 1.0},
            {"symbol": "IEFA", "name": "iShares Core MSCI EAFE IMI Index ETF", "expense_ratio": 0.07, "aum": 90000000000, "benchmark": "MSCI EAFE IMI", "leverage": 1.0},
            {"symbol": "EEM", "name": "iShares MSCI Emerging Markets ETF", "expense_ratio": 0.68, "aum": 25000000000, "benchmark": "MSCI Emerging Markets", "leverage": 1.0}
        ],
        "Bond ETFs": [
            {"symbol": "BND", "name": "Vanguard Total Bond Market ETF", "expense_ratio": 0.03, "aum": 300000000000, "benchmark": "Bloomberg US Aggregate Float Adjusted", "leverage": 1.0},
            {"symbol": "AGG", "name": "iShares Core US Aggregate Bond ETF", "expense_ratio": 0.03, "aum": 90000000000, "benchmark": "Bloomberg US Aggregate Bond", "leverage": 1.0},
            {"symbol": "TLT", "name": "iShares 20+ Year Treasury Bond ETF", "expense_ratio": 0.15, "aum": 20000000000, "benchmark": "ICE US Treasury 20+ Year", "leverage": 1.0},
            {"symbol": "HYG", "name": "iShares iBoxx $ High Yield Corporate Bond ETF", "expense_ratio": 0.49, "aum": 15000000000, "benchmark": "Markit iBoxx USD Liquid High Yield", "leverage": 1.0}
        ]
    }
    
    # Flatten ETFs with category info
    all_etfs = []
    for category, etfs in etfs_by_category.items():
        for etf in etfs:
            etf["category"] = category
            etf["inception_date"] = "2010-01-01"  # Simplified for demo
            all_etfs.append(etf)
    
    # Generate 2 years of ETF prices
    def generate_etf_prices():
        prices = []
        base_prices = {}
        
        # Set realistic base prices for ETFs
        for etf in all_etfs:
            symbol = etf["symbol"]
            if symbol in ["SPY", "QQQ", "IVV", "VOO"]:
                base_prices[symbol] = random.uniform(400, 500)
            elif symbol in ["TQQQ", "UPRO", "SOXL"]:  # Leveraged ETFs
                base_prices[symbol] = random.uniform(50, 150)
            elif symbol in ["TLT", "BND", "AGG"]:  # Bond ETFs
                base_prices[symbol] = random.uniform(80, 120)
            else:
                base_prices[symbol] = random.uniform(100, 300)
        
        # Generate 2 years of data
        for symbol, base_price in base_prices.items():
            current_price = base_price
            
            # Get leverage multiplier for volatility
            etf_info = next((e for e in all_etfs if e["symbol"] == symbol), {})
            leverage = etf_info.get("leverage", 1.0)
            
            for i in range(730):  # 2 years
                date_obj = date.today() - timedelta(days=729-i)
                
                # Adjust volatility based on leverage and category
                if etf_info.get("category") == "Leveraged":
                    daily_change = random.uniform(-0.08, 0.08) * leverage  # Higher volatility for leveraged
                elif etf_info.get("category") == "Bond ETFs":
                    daily_change = random.uniform(-0.01, 0.01)  # Lower volatility for bonds
                else:
                    daily_change = random.uniform(-0.03, 0.03)  # Normal ETF volatility
                
                current_price *= (1 + daily_change)
                current_price = max(current_price, 1.0)  # Prevent negative prices
                
                open_price = current_price * random.uniform(0.995, 1.005)
                high_price = max(open_price, current_price) * random.uniform(1.0, 1.015)
                low_price = min(open_price, current_price) * random.uniform(0.985, 1.0)
                
                # Volume varies by ETF popularity
                if symbol in ["SPY", "QQQ", "IWM"]:
                    volume = random.randint(50000000, 200000000)  # High volume
                elif etf_info.get("category") == "Leveraged":
                    volume = random.randint(20000000, 100000000)  # Medium-high volume
                else:
                    volume = random.randint(1000000, 50000000)  # Normal volume
                
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
    
    print(f"📊 Generating ETF data...")
    print(f"   • {len(all_etfs)} ETFs across {len(etfs_by_category)} categories")
    print("   • 2 years of daily price data")
    
    return {
        "etfs": all_etfs,
        "etf_prices": generate_etf_prices()
    }

def insert_etf_data():
    print("🚀 Creating and inserting comprehensive ETF data...")
    
    try:
        # First show schema
        print("\n📋 ETF Table Schema:")
        create_etf_schema()
        
        print("\n⚠️  Please create the ETF tables in Supabase first, then press Enter to continue...")
        input()
        
        # Generate ETF data
        data = create_comprehensive_etf_data()
        
        # Insert ETFs
        print(f"\n📊 Inserting {len(data['etfs'])} ETFs...")
        for etf in data["etfs"]:
            try:
                result = supabase_db.supabase.table('etfs').insert({
                    "symbol": etf["symbol"],
                    "name": etf["name"],
                    "category": etf["category"],
                    "expense_ratio": etf["expense_ratio"],
                    "aum": etf["aum"],
                    "inception_date": etf["inception_date"],
                    "benchmark": etf["benchmark"],
                    "leverage_ratio": etf["leverage"]
                }).execute()
                print(f"✅ {etf['symbol']} - {etf['name']} ({etf['category']})")
            except Exception as e:
                if "duplicate key" in str(e).lower():
                    print(f"⚠️  {etf['symbol']} already exists")
                else:
                    print(f"❌ Error inserting {etf['symbol']}: {e}")
        
        # Insert ETF prices in batches
        print(f"\n💹 Inserting {len(data['etf_prices'])} ETF prices (2 years)...")
        batch_size = 100
        success_count = 0
        
        for i in range(0, len(data['etf_prices']), batch_size):
            batch = data['etf_prices'][i:i+batch_size]
            try:
                result = supabase_db.supabase.table('etf_prices').insert(batch).execute()
                success_count += len(batch)
                if success_count % 1000 == 0:
                    print(f"✅ Inserted {success_count} ETF prices...")
            except Exception as e:
                print(f"❌ Error inserting ETF price batch: {e}")
        
        print(f"✅ Inserted {success_count} ETF prices")
        
        print("\n🎉 ETF DATA INSERTION COMPLETE!")
        print("\n📋 ETF Summary:")
        print(f"   • {len(data['etfs'])} ETFs across 9 categories")
        print(f"   • {len(data['etf_prices'])} ETF prices (2 years daily data)")
        print("\n📊 Categories:")
        categories = {}
        for etf in data['etfs']:
            cat = etf['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        for cat, count in categories.items():
            print(f"   • {cat}: {count} ETFs")
        
        print("\n🔗 Test ETF APIs (you'll need to add these endpoints):")
        print("   • /api/etfs")
        print("   • /api/etfs/SPY")
        print("   • /api/etfs/SPY/prices?days=365")
        
    except Exception as e:
        print(f"❌ Error during ETF data insertion: {e}")

if __name__ == "__main__":
    insert_etf_data()
