import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.database import async_session_maker
from app.services.news_service import fetch_news_for_all_brands
from app.services.financial_service import fetch_financial_for_all_brands
from app.services.sentiment_service import compute_sentiment_summaries

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()
_initial_fetch_done = False


async def _fetch_news_job():
    """Scheduled job: fetch news for all brands."""
    try:
        async with async_session_maker() as session:
            count = await fetch_news_for_all_brands(session)
            logger.info(f"Scheduled news fetch complete: {count} articles")
    except Exception as e:
        logger.error(f"Error in scheduled news fetch: {e}")


async def _fetch_financial_job():
    """Scheduled job: fetch financial data for all brands."""
    try:
        async with async_session_maker() as session:
            count = await fetch_financial_for_all_brands(session)
            logger.info(f"Scheduled financial fetch complete: {count} brands")
    except Exception as e:
        logger.error(f"Error in scheduled financial fetch: {e}")


async def _compute_sentiment_job():
    """Scheduled job: compute sentiment summaries."""
    try:
        async with async_session_maker() as session:
            count = await compute_sentiment_summaries(session)
            logger.info(f"Scheduled sentiment computation complete: {count} brands")
    except Exception as e:
        logger.error(f"Error in scheduled sentiment computation: {e}")


async def _run_initial_fetch():
    """Run initial data fetch on startup."""
    global _initial_fetch_done
    if _initial_fetch_done:
        return

    logger.info("Running initial data fetch...")
    try:
        async with async_session_maker() as session:
            news_count = await fetch_news_for_all_brands(session)
            logger.info(f"Initial news fetch: {news_count} articles")

        async with async_session_maker() as session:
            fin_count = await fetch_financial_for_all_brands(session)
            logger.info(f"Initial financial fetch: {fin_count} brands")

        async with async_session_maker() as session:
            sent_count = await compute_sentiment_summaries(session)
            logger.info(f"Initial sentiment computation: {sent_count} brands")

        _initial_fetch_done = True
        logger.info("Initial data fetch complete.")
    except Exception as e:
        logger.error(f"Error in initial data fetch: {e}")


def start_scheduler():
    """Start the APScheduler with all recurring jobs."""
    # Fetch news every 2 hours
    scheduler.add_job(
        _fetch_news_job,
        trigger=IntervalTrigger(hours=2),
        id="fetch_news",
        name="Fetch news articles",
        replace_existing=True,
    )

    # Fetch financial data every 1 hour
    scheduler.add_job(
        _fetch_financial_job,
        trigger=IntervalTrigger(hours=1),
        id="fetch_financial",
        name="Fetch financial data",
        replace_existing=True,
    )

    # Compute sentiment summaries every 3 hours
    scheduler.add_job(
        _compute_sentiment_job,
        trigger=IntervalTrigger(hours=3),
        id="compute_sentiment",
        name="Compute sentiment summaries",
        replace_existing=True,
    )

    scheduler.start()
    logger.info("Scheduler started with recurring jobs.")

    # Schedule initial fetch to run shortly after startup
    asyncio.ensure_future(_run_initial_fetch())
