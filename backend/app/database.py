import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///luxury_brands.db")

engine = create_async_engine(DATABASE_URL, echo=False)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    from app.models import Brand, NewsArticle, FinancialData, SentimentSummary  # noqa: F401
    from sqlalchemy import select

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    default_brands = [
        {
            "name": "LVMH",
            "ticker": "MC.PA",
            "sector": "Conglomerate",
            "parent_company": None,
            "country": "France",
            "description": "LVMH Moet Hennessy Louis Vuitton, the world's largest luxury goods conglomerate.",
        },
        {
            "name": "Kering",
            "ticker": "KER.PA",
            "sector": "Conglomerate",
            "parent_company": None,
            "country": "France",
            "description": "Kering SA, a global luxury group managing renowned fashion, leather goods, and jewelry brands.",
        },
        {
            "name": "Hermes",
            "ticker": "RMS.PA",
            "sector": "Fashion",
            "parent_company": None,
            "country": "France",
            "description": "Hermes International, a French luxury goods manufacturer known for leather, lifestyle accessories, and perfumery.",
        },
        {
            "name": "Chanel",
            "ticker": None,
            "sector": "Fashion",
            "parent_company": None,
            "country": "France",
            "description": "Chanel S.A., a privately held French luxury fashion house founded by Coco Chanel.",
        },
        {
            "name": "Prada",
            "ticker": "1913.HK",
            "sector": "Fashion",
            "parent_company": None,
            "country": "Italy",
            "description": "Prada S.p.A., an Italian luxury fashion house specializing in leather handbags and accessories.",
        },
        {
            "name": "Burberry",
            "ticker": "BRBY.L",
            "sector": "Fashion",
            "parent_company": None,
            "country": "UK",
            "description": "Burberry Group plc, a British luxury fashion house known for its iconic trench coats and check pattern.",
        },
        {
            "name": "Richemont",
            "ticker": "CFR.SW",
            "sector": "Jewelry/Watches",
            "parent_company": None,
            "country": "Switzerland",
            "description": "Compagnie Financiere Richemont SA, a Swiss luxury goods conglomerate owning Cartier and Van Cleef & Arpels.",
        },
        {
            "name": "Tiffany & Co.",
            "ticker": None,
            "sector": "Jewelry",
            "parent_company": "LVMH",
            "country": "USA",
            "description": "Tiffany & Co., an American luxury jewelry and specialty retailer, now owned by LVMH.",
        },
        {
            "name": "Rolex",
            "ticker": None,
            "sector": "Watches",
            "parent_company": None,
            "country": "Switzerland",
            "description": "Rolex SA, a Swiss luxury watchmaker known for its prestigious timepieces.",
        },
        {
            "name": "Ferrari",
            "ticker": "RACE",
            "sector": "Automotive",
            "parent_company": None,
            "country": "Italy",
            "description": "Ferrari N.V., an Italian luxury sports car manufacturer.",
        },
    ]

    async with async_session_maker() as session:
        result = await session.execute(select(Brand))
        existing_brands = result.scalars().all()

        if not existing_brands:
            for brand_data in default_brands:
                brand = Brand(**brand_data)
                session.add(brand)
            await session.commit()
