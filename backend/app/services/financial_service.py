import random
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Brand, FinancialData


# Base prices for mock data (approximate real prices)
MOCK_BASE_PRICES = {
    "MC.PA": 850.0,     # LVMH
    "KER.PA": 380.0,    # Kering
    "RMS.PA": 2100.0,   # Hermes
    "1913.HK": 62.0,    # Prada
    "BRBY.L": 14.0,     # Burberry
    "CFR.SW": 135.0,    # Richemont
    "RACE": 420.0,      # Ferrari
}

MOCK_MARKET_CAPS = {
    "MC.PA": 430e9,     # LVMH
    "KER.PA": 48e9,     # Kering
    "RMS.PA": 220e9,    # Hermes
    "1913.HK": 16e9,    # Prada
    "BRBY.L": 5.5e9,    # Burberry
    "CFR.SW": 76e9,     # Richemont
    "RACE": 78e9,       # Ferrari
}


async def fetch_financial_for_all_brands(db: AsyncSession) -> int:
    """Fetch financial data for all brands with tickers."""
    result = await db.execute(select(Brand).where(Brand.ticker.isnot(None)))
    brands = result.scalars().all()

    count = 0
    for brand in brands:
        try:
            fetched = await _fetch_real_financial(brand, db)
            if fetched:
                count += 1
                continue
        except Exception:
            pass

        # Fall back to mock data
        await _generate_mock_financial(brand, db)
        count += 1

    return count


async def _fetch_real_financial(brand: Brand, db: AsyncSession) -> bool:
    """Try to fetch real financial data using yfinance."""
    try:
        import yfinance as yf

        ticker = yf.Ticker(brand.ticker)
        hist = ticker.history(period="1d")

        if hist.empty:
            return False

        latest = hist.iloc[-1]
        open_price = float(latest.get("Open", 0))
        close_price = float(latest.get("Close", 0))
        high = float(latest.get("High", 0))
        low = float(latest.get("Low", 0))
        volume = float(latest.get("Volume", 0))

        change_percent = ((close_price - open_price) / open_price * 100) if open_price else 0

        info = ticker.info
        market_cap = float(info.get("marketCap", 0)) if info.get("marketCap") else None

        financial_data = FinancialData(
            brand_id=brand.id,
            date=datetime.utcnow(),
            open_price=open_price,
            close_price=close_price,
            high=high,
            low=low,
            volume=volume,
            market_cap=market_cap,
            change_percent=round(change_percent, 4),
        )
        db.add(financial_data)
        await db.commit()
        return True

    except Exception:
        return False


async def _generate_mock_financial(brand: Brand, db: AsyncSession) -> None:
    """Generate realistic mock financial data using random walk."""
    if not brand.ticker:
        return

    base_price = MOCK_BASE_PRICES.get(brand.ticker, 100.0)
    market_cap = MOCK_MARKET_CAPS.get(brand.ticker, 10e9)

    # Generate data for the last 30 days
    now = datetime.utcnow()

    # Check if we already have recent data
    existing_result = await db.execute(
        select(FinancialData)
        .where(FinancialData.brand_id == brand.id)
        .where(FinancialData.date >= now - timedelta(hours=2))
    )
    if existing_result.scalars().first():
        return  # Skip if recent data exists

    price = base_price
    for day_offset in range(30, -1, -1):
        date = now - timedelta(days=day_offset)

        # Skip weekends
        if date.weekday() >= 5:
            continue

        # Random walk: daily change between -3% and +3%
        daily_change = random.uniform(-0.03, 0.03)
        open_price = price
        close_price = round(price * (1 + daily_change), 2)
        high = round(max(open_price, close_price) * (1 + random.uniform(0, 0.015)), 2)
        low = round(min(open_price, close_price) * (1 - random.uniform(0, 0.015)), 2)
        volume = random.randint(500000, 5000000)
        change_percent = round(daily_change * 100, 4)

        # Update market cap proportionally
        current_market_cap = round(market_cap * (close_price / base_price), 2)

        financial_data = FinancialData(
            brand_id=brand.id,
            date=date,
            open_price=round(open_price, 2),
            close_price=close_price,
            high=high,
            low=low,
            volume=volume,
            market_cap=current_market_cap,
            change_percent=change_percent,
        )
        db.add(financial_data)

        price = close_price

    await db.commit()
