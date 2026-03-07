from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    ticker = Column(String(20), nullable=True)
    sector = Column(String(50), nullable=False)
    parent_company = Column(String(100), nullable=True)
    country = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    logo_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    news_articles = relationship("NewsArticle", back_populates="brand", cascade="all, delete-orphan")
    financial_data = relationship("FinancialData", back_populates="brand", cascade="all, delete-orphan")
    sentiment_summaries = relationship("SentimentSummary", back_populates="brand", cascade="all, delete-orphan")


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    source = Column(String(200), nullable=True)
    url = Column(String(1000), nullable=True)
    image_url = Column(String(1000), nullable=True)
    published_at = Column(DateTime, nullable=True)
    sentiment_score = Column(Float, default=0.0)
    sentiment_label = Column(String(20), default="neutral")
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="news_articles")


class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    open_price = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    high = Column(Float, nullable=True)
    low = Column(Float, nullable=True)
    volume = Column(Float, nullable=True)
    market_cap = Column(Float, nullable=True)
    change_percent = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="financial_data")


class SentimentSummary(Base):
    __tablename__ = "sentiment_summaries"

    id = Column(Integer, primary_key=True, index=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=False, index=True)
    date = Column(DateTime, nullable=False)
    avg_sentiment = Column(Float, default=0.0)
    article_count = Column(Integer, default=0)
    positive_count = Column(Integer, default=0)
    negative_count = Column(Integer, default=0)
    neutral_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    brand = relationship("Brand", back_populates="sentiment_summaries")
