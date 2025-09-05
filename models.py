from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal

class Stock(BaseModel):
    id: Optional[int] = None
    symbol: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class StockPrice(BaseModel):
    id: Optional[int] = None
    symbol: str
    date: date
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[int] = None
    created_at: Optional[datetime] = None

class Sector(BaseModel):
    id: Optional[int] = None
    name: str
    performance_1d: Optional[float] = None
    performance_1w: Optional[float] = None
    performance_1m: Optional[float] = None
    performance_ytd: Optional[float] = None
    updated_at: Optional[datetime] = None

class Fundamentals(BaseModel):
    id: Optional[int] = None
    symbol: str
    pe_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    debt_to_equity: Optional[float] = None
    roe: Optional[float] = None
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    eps: Optional[float] = None
    dividend_yield: Optional[float] = None
    quarter: Optional[str] = None
    year: Optional[int] = None
    created_at: Optional[datetime] = None

class TechnicalIndicators(BaseModel):
    id: Optional[int] = None
    symbol: str
    date: date
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    rsi: Optional[float] = None
    macd: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None
    created_at: Optional[datetime] = None

class ScreenerRequest(BaseModel):
    min_market_cap: Optional[float] = None
    max_market_cap: Optional[float] = None
    min_pe_ratio: Optional[float] = None
    max_pe_ratio: Optional[float] = None
    min_roe: Optional[float] = None
    sectors: Optional[List[str]] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    limit: Optional[int] = 50
