from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ── Brand Schemas ──

class BrandCreate(BaseModel):
    name: str
    ticker: Optional[str] = None
    sector: str
    parent_company: Optional[str] = None
    country: str
    description: Optional[str] = None
    logo_url: Optional[str] = None


class BrandRead(BaseModel):
    id: int
    name: str
    ticker: Optional[str] = None
    sector: str
    parent_company: Optional[str] = None
    country: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── NewsArticle Schemas ──

class NewsArticleCreate(BaseModel):
    brand_id: int
    title: str
    description: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    published_at: Optional[datetime] = None
    sentiment_score: float = 0.0
    sentiment_label: str = "neutral"


class NewsArticleRead(BaseModel):
    id: int
    brand_id: int
    title: str
    description: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    image_url: Optional[str] = None
    published_at: Optional[datetime] = None
    sentiment_score: float
    sentiment_label: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ── FinancialData Schemas ──

class FinancialDataCreate(BaseModel):
    brand_id: int
    date: datetime
    open_price: Optional[float] = None
    close_price: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None
    market_cap: Optional[float] = None
    change_percent: Optional[float] = None


class FinancialDataRead(BaseModel):
    id: int
    brand_id: int
    date: datetime
    open_price: Optional[float] = None
    close_price: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    volume: Optional[float] = None
    market_cap: Optional[float] = None
    change_percent: Optional[float] = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── SentimentSummary Schemas ──

class SentimentSummaryCreate(BaseModel):
    brand_id: int
    date: datetime
    avg_sentiment: float = 0.0
    article_count: int = 0
    positive_count: int = 0
    negative_count: int = 0
    neutral_count: int = 0


class SentimentSummaryRead(BaseModel):
    id: int
    brand_id: int
    date: datetime
    avg_sentiment: float
    article_count: int
    positive_count: int
    negative_count: int
    neutral_count: int
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Analytics Schemas ──

class SentimentOverview(BaseModel):
    brand_id: int
    brand_name: str
    avg_sentiment: float
    article_count: int
    positive_count: int
    negative_count: int
    neutral_count: int


class BrandComparison(BaseModel):
    brand_id: int
    brand_name: str
    ticker: Optional[str] = None
    avg_sentiment: float
    article_count: int
    latest_close_price: Optional[float] = None
    price_change_percent: Optional[float] = None


class TrendingBrand(BaseModel):
    brand_id: int
    brand_name: str
    article_count: int
    sentiment_change: float
    trending_score: float


class DashboardSummary(BaseModel):
    total_brands: int
    total_articles: int
    avg_sentiment: float
    top_movers: list[BrandComparison]
