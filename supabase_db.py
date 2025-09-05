import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseDB:
    def __init__(self):
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env file")
        
        self.supabase: Client = create_client(url, key)
    
    def create_tables(self):
        """Create tables in Supabase (run this once)"""
        # Note: You'll need to run these SQL commands in Supabase SQL Editor
        sql_commands = """
        -- Create stocks table
        CREATE TABLE IF NOT EXISTS stocks (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            sector VARCHAR(100),
            industry VARCHAR(100),
            market_cap DECIMAL(15,2),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Create stock_prices table
        CREATE TABLE IF NOT EXISTS stock_prices (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open_price DECIMAL(10,4),
            high_price DECIMAL(10,4),
            low_price DECIMAL(10,4),
            close_price DECIMAL(10,4),
            volume BIGINT,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (symbol) REFERENCES stocks(symbol),
            UNIQUE(symbol, date)
        );

        -- Create sectors table
        CREATE TABLE IF NOT EXISTS sectors (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) UNIQUE NOT NULL,
            performance_1d DECIMAL(5,2),
            performance_1w DECIMAL(5,2),
            performance_1m DECIMAL(5,2),
            performance_ytd DECIMAL(5,2),
            updated_at TIMESTAMP DEFAULT NOW()
        );

        -- Create fundamentals table
        CREATE TABLE IF NOT EXISTS fundamentals (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            pe_ratio DECIMAL(8,2),
            pb_ratio DECIMAL(8,2),
            debt_to_equity DECIMAL(8,2),
            roe DECIMAL(5,2),
            revenue DECIMAL(15,2),
            net_income DECIMAL(15,2),
            eps DECIMAL(8,2),
            dividend_yield DECIMAL(5,2),
            quarter VARCHAR(10),
            year INTEGER,
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (symbol) REFERENCES stocks(symbol),
            UNIQUE(symbol, quarter, year)
        );

        -- Create technical_indicators table
        CREATE TABLE IF NOT EXISTS technical_indicators (
            id SERIAL PRIMARY KEY,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            sma_20 DECIMAL(10,4),
            sma_50 DECIMAL(10,4),
            sma_200 DECIMAL(10,4),
            rsi DECIMAL(5,2),
            macd DECIMAL(8,4),
            bollinger_upper DECIMAL(10,4),
            bollinger_lower DECIMAL(10,4),
            created_at TIMESTAMP DEFAULT NOW(),
            FOREIGN KEY (symbol) REFERENCES stocks(symbol),
            UNIQUE(symbol, date)
        );

        -- Create indexes
        CREATE INDEX IF NOT EXISTS idx_stock_prices_symbol_date ON stock_prices(symbol, date);
        CREATE INDEX IF NOT EXISTS idx_fundamentals_symbol ON fundamentals(symbol);
        CREATE INDEX IF NOT EXISTS idx_technical_symbol_date ON technical_indicators(symbol, date);
        """
        
        print("Copy and paste this SQL into Supabase SQL Editor:")
        print("=" * 50)
        print(sql_commands)
        print("=" * 50)
    
    # CRUD operations
    def insert_stock(self, stock_data):
        return self.supabase.table('stocks').insert(stock_data).execute()
    
    def get_stock(self, symbol):
        return self.supabase.table('stocks').select('*').eq('symbol', symbol.upper()).execute()
    
    def get_all_stocks(self):
        return self.supabase.table('stocks').select('*').execute()
    
    def insert_stock_price(self, price_data):
        return self.supabase.table('stock_prices').insert(price_data).execute()
    
    def get_stock_prices(self, symbol, limit=30):
        return self.supabase.table('stock_prices').select('*').eq('symbol', symbol.upper()).order('date', desc=True).limit(limit).execute()
    
    def insert_sector(self, sector_data):
        return self.supabase.table('sectors').insert(sector_data).execute()
    
    def get_sectors(self):
        return self.supabase.table('sectors').select('*').order('performance_1d', desc=True).execute()

# Global instance
supabase_db = SupabaseDB()
