from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import Brand, NewsArticle, SentimentSummary


def analyze_sentiment(text: str) -> tuple[float, str]:
    """Analyze sentiment of text using TextBlob. Returns (score, label)."""
    try:
        from textblob import TextBlob

        blob = TextBlob(text)
        score = blob.sentiment.polarity
    except Exception:
        score = 0.0

    score = round(score, 4)

    if score > 0.1:
        label = "positive"
    elif score < -0.1:
        label = "negative"
    else:
        label = "neutral"

    return score, label


async def compute_sentiment_summaries(db: AsyncSession) -> int:
    """Compute daily sentiment summaries for all brands."""
    result = await db.execute(select(Brand))
    brands = result.scalars().all()

    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    count = 0

    for brand in brands:
        # Get articles from the last 24 hours
        yesterday = today - timedelta(days=1)
        articles_result = await db.execute(
            select(NewsArticle)
            .where(NewsArticle.brand_id == brand.id)
            .where(NewsArticle.published_at >= yesterday)
            .where(NewsArticle.published_at < today + timedelta(days=1))
        )
        articles = articles_result.scalars().all()

        if not articles:
            continue

        scores = [a.sentiment_score for a in articles if a.sentiment_score is not None]
        avg_sentiment = sum(scores) / len(scores) if scores else 0.0

        positive_count = sum(1 for a in articles if a.sentiment_label == "positive")
        negative_count = sum(1 for a in articles if a.sentiment_label == "negative")
        neutral_count = sum(1 for a in articles if a.sentiment_label == "neutral")

        # Check if summary already exists for today
        existing_result = await db.execute(
            select(SentimentSummary)
            .where(SentimentSummary.brand_id == brand.id)
            .where(SentimentSummary.date >= today)
            .where(SentimentSummary.date < today + timedelta(days=1))
        )
        existing = existing_result.scalar_one_or_none()

        if existing:
            existing.avg_sentiment = round(avg_sentiment, 4)
            existing.article_count = len(articles)
            existing.positive_count = positive_count
            existing.negative_count = negative_count
            existing.neutral_count = neutral_count
        else:
            summary = SentimentSummary(
                brand_id=brand.id,
                date=today,
                avg_sentiment=round(avg_sentiment, 4),
                article_count=len(articles),
                positive_count=positive_count,
                negative_count=negative_count,
                neutral_count=neutral_count,
            )
            db.add(summary)

        count += 1

    await db.commit()
    return count
