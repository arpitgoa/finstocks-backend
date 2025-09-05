import sqlite3
import os
from typing import List, Dict, Any, Optional

class Database:
    def __init__(self, db_path: str = "finstocks.db"):
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        """Initialize database with schema"""
        schema = """
        -- Companies/Stocks table
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol VARCHAR(10) UNIQUE NOT NULL,
            name VARCHAR(255) NOT NULL,
            sector VARCHAR(100),
            industry VARCHAR(100),
            market_cap DECIMAL(15,2),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Stock prices (historical and current)
        CREATE TABLE IF NOT EXISTS stock_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            open_price DECIMAL(10,4),
            high_price DECIMAL(10,4),
            low_price DECIMAL(10,4),
            close_price DECIMAL(10,4),
            volume BIGINT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (symbol) REFERENCES stocks(symbol),
            UNIQUE(symbol, date)
        );

        -- Sectors performance
        CREATE TABLE IF NOT EXISTS sectors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(100) UNIQUE NOT NULL,
            performance_1d DECIMAL(5,2),
            performance_1w DECIMAL(5,2),
            performance_1m DECIMAL(5,2),
            performance_ytd DECIMAL(5,2),
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        -- Fundamental data
        CREATE TABLE IF NOT EXISTS fundamentals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (symbol) REFERENCES stocks(symbol),
            UNIQUE(symbol, quarter, year)
        );

        -- Technical indicators
        CREATE TABLE IF NOT EXISTS technical_indicators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol VARCHAR(10) NOT NULL,
            date DATE NOT NULL,
            sma_20 DECIMAL(10,4),
            sma_50 DECIMAL(10,4),
            sma_200 DECIMAL(10,4),
            rsi DECIMAL(5,2),
            macd DECIMAL(8,4),
            bollinger_upper DECIMAL(10,4),
            bollinger_lower DECIMAL(10,4),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (symbol) REFERENCES stocks(symbol),
            UNIQUE(symbol, date)
        );

        -- Indexes for performance
        CREATE INDEX IF NOT EXISTS idx_stock_prices_symbol_date ON stock_prices(symbol, date);
        CREATE INDEX IF NOT EXISTS idx_fundamentals_symbol ON fundamentals(symbol);
        CREATE INDEX IF NOT EXISTS idx_technical_symbol_date ON technical_indicators(symbol, date);
        """
        
        with self.get_connection() as conn:
            conn.executescript(schema)
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Execute SELECT query and return results as list of dicts"""
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_insert(self, query: str, params: tuple = ()) -> int:
        """Execute INSERT query and return last row id"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.lastrowid
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Execute UPDATE/DELETE query and return affected rows"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount

# Global database instance
db = Database()
