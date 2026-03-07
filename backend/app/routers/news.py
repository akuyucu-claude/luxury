from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional

from app.database import get_db
from app.models import NewsArticle
from app.schemas import NewsArticleRead
from app.services.news_service import fetch_news_for_all_brands

router = APIRouter(tags=["news"])


@router.get("/news", response_model=list[NewsArticleRead])
async def list_news(
    brand_id: Optional[int] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    query = select(NewsArticle).order_by(desc(NewsArticle.published_at))

    if brand_id is not None:
        query = query.where(NewsArticle.brand_id == brand_id)

    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    articles = result.scalars().all()
    return articles


@router.get("/news/latest", response_model=list[NewsArticleRead])
async def latest_news(db: AsyncSession = Depends(get_db)):
    query = (
        select(NewsArticle)
        .order_by(desc(NewsArticle.published_at))
        .limit(20)
    )
    result = await db.execute(query)
    articles = result.scalars().all()
    return articles


@router.post("/news/fetch")
async def trigger_news_fetch(db: AsyncSession = Depends(get_db)):
    count = await fetch_news_for_all_brands(db)
    return {"message": f"Fetched {count} news articles"}
