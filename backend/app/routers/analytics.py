from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc

from app.database import get_db
from app.models import Brand, NewsArticle, FinancialData, SentimentSummary
from app.schemas import (
    SentimentOverview,
    BrandComparison,
    TrendingBrand,
    DashboardSummary,
)

router = APIRouter(tags=["analytics"])


@router.get("/analytics/sentiment-overview", response_model=list[SentimentOverview])
async def sentiment_overview(db: AsyncSession = Depends(get_db)):
    brands_result = await db.execute(select(Brand).order_by(Brand.name))
    brands = brands_result.scalars().all()

    overviews = []
    for brand in brands:
        articles_result = await db.execute(
            select(NewsArticle).where(NewsArticle.brand_id == brand.id)
        )
        articles = articles_result.scalars().all()

        if articles:
            avg_sent = sum(a.sentiment_score for a in articles) / len(articles)
            positive = sum(1 for a in articles if a.sentiment_label == "positive")
            negative = sum(1 for a in articles if a.sentiment_label == "negative")
            neutral = sum(1 for a in articles if a.sentiment_label == "neutral")
        else:
            avg_sent = 0.0
            positive = negative = neutral = 0

        overviews.append(
            SentimentOverview(
                brand_id=brand.id,
                brand_name=brand.name,
                avg_sentiment=round(avg_sent, 4),
                article_count=len(articles),
                positive_count=positive,
                negative_count=negative,
                neutral_count=neutral,
            )
        )

    return overviews


@router.get("/analytics/brand-comparison", response_model=list[BrandComparison])
async def brand_comparison(db: AsyncSession = Depends(get_db)):
    brands_result = await db.execute(select(Brand).order_by(Brand.name))
    brands = brands_result.scalars().all()

    comparisons = []
    for brand in brands:
        # Sentiment
        articles_result = await db.execute(
            select(NewsArticle).where(NewsArticle.brand_id == brand.id)
        )
        articles = articles_result.scalars().all()
        avg_sent = (
            sum(a.sentiment_score for a in articles) / len(articles) if articles else 0.0
        )

        # Financial
        fin_result = await db.execute(
            select(FinancialData)
            .where(FinancialData.brand_id == brand.id)
            .order_by(desc(FinancialData.date))
            .limit(1)
        )
        latest_fin = fin_result.scalar_one_or_none()

        comparisons.append(
            BrandComparison(
                brand_id=brand.id,
                brand_name=brand.name,
                ticker=brand.ticker,
                avg_sentiment=round(avg_sent, 4),
                article_count=len(articles),
                latest_close_price=latest_fin.close_price if latest_fin else None,
                price_change_percent=latest_fin.change_percent if latest_fin else None,
            )
        )

    return comparisons


@router.get("/analytics/trending", response_model=list[TrendingBrand])
async def trending_brands(db: AsyncSession = Depends(get_db)):
    brands_result = await db.execute(select(Brand))
    brands = brands_result.scalars().all()

    trending = []
    for brand in brands:
        articles_result = await db.execute(
            select(NewsArticle).where(NewsArticle.brand_id == brand.id)
        )
        articles = articles_result.scalars().all()
        article_count = len(articles)

        if article_count > 0:
            avg_sent = sum(a.sentiment_score for a in articles) / article_count
            # Simple trending score: combination of volume and sentiment magnitude
            trending_score = article_count * (1 + abs(avg_sent))
            sentiment_change = avg_sent  # simplified
        else:
            trending_score = 0.0
            sentiment_change = 0.0

        trending.append(
            TrendingBrand(
                brand_id=brand.id,
                brand_name=brand.name,
                article_count=article_count,
                sentiment_change=round(sentiment_change, 4),
                trending_score=round(trending_score, 4),
            )
        )

    trending.sort(key=lambda x: x.trending_score, reverse=True)
    return trending


@router.get("/analytics/dashboard-summary", response_model=DashboardSummary)
async def dashboard_summary(db: AsyncSession = Depends(get_db)):
    # Total brands
    brands_count_result = await db.execute(select(func.count(Brand.id)))
    total_brands = brands_count_result.scalar() or 0

    # Total articles
    articles_count_result = await db.execute(select(func.count(NewsArticle.id)))
    total_articles = articles_count_result.scalar() or 0

    # Average sentiment
    avg_sent_result = await db.execute(select(func.avg(NewsArticle.sentiment_score)))
    avg_sentiment = avg_sent_result.scalar() or 0.0

    # Top movers (brands with highest absolute price change)
    brands_result = await db.execute(select(Brand))
    brands = brands_result.scalars().all()

    movers = []
    for brand in brands:
        articles_result = await db.execute(
            select(NewsArticle).where(NewsArticle.brand_id == brand.id)
        )
        articles = articles_result.scalars().all()
        brand_avg_sent = (
            sum(a.sentiment_score for a in articles) / len(articles) if articles else 0.0
        )

        fin_result = await db.execute(
            select(FinancialData)
            .where(FinancialData.brand_id == brand.id)
            .order_by(desc(FinancialData.date))
            .limit(1)
        )
        latest_fin = fin_result.scalar_one_or_none()

        movers.append(
            BrandComparison(
                brand_id=brand.id,
                brand_name=brand.name,
                ticker=brand.ticker,
                avg_sentiment=round(brand_avg_sent, 4),
                article_count=len(articles),
                latest_close_price=latest_fin.close_price if latest_fin else None,
                price_change_percent=latest_fin.change_percent if latest_fin else None,
            )
        )

    # Sort by absolute change percent, nulls last
    movers.sort(
        key=lambda x: abs(x.price_change_percent) if x.price_change_percent else 0,
        reverse=True,
    )

    return DashboardSummary(
        total_brands=total_brands,
        total_articles=total_articles,
        avg_sentiment=round(float(avg_sentiment), 4),
        top_movers=movers[:5],
    )
