import os
import random
from datetime import datetime, timedelta

import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Brand, NewsArticle
from app.services.sentiment_service import analyze_sentiment


NEWS_API_KEY = os.getenv("NEWS_API_KEY")

MOCK_HEADLINES = {
    "LVMH": [
        "LVMH Reports Record Q4 Revenue Growth Driven by Strong Asian Demand",
        "LVMH Acquires New Italian Luxury Leather Goods Maker",
        "Louis Vuitton Unveils Exclusive Collaboration with Japanese Artist",
        "LVMH Shares Rise as Luxury Spending Rebounds Post-Pandemic",
        "LVMH Faces Headwinds as China Luxury Market Shows Signs of Slowdown",
        "Bernard Arnault Announces Major Sustainability Initiative at LVMH",
    ],
    "Kering": [
        "Kering Reports Mixed Results as Gucci Sales Decline",
        "Kering Invests in Emerging Luxury Brands to Diversify Portfolio",
        "Gucci Launches Sustainable Fashion Collection Under Kering's New Strategy",
        "Kering Stock Drops After Disappointing Revenue Forecast",
        "Kering Appoints New CEO for Bottega Veneta Division",
        "Kering Expands Digital Presence with New E-Commerce Platform",
    ],
    "Hermes": [
        "Hermes Opens New Flagship Store in Tokyo's Ginza District",
        "Hermes Reports Double-Digit Growth Across All Regions",
        "Hermes Birkin Bag Prices Surge Amid Record Demand",
        "Hermes Launches Exclusive Watch Collection at Watches & Wonders",
        "Hermes Revenue Beats Expectations with Strong Leather Goods Sales",
        "Hermes Announces Expansion of Artisan Training Program in France",
    ],
    "Chanel": [
        "Chanel Raises Prices Again on Classic Handbags Amid Luxury Inflation",
        "Chanel Opens Largest Boutique in Asia in Seoul's Gangnam District",
        "Chanel Debuts Haute Couture Collection to Critical Acclaim",
        "Chanel Reports Record Revenue Despite Keeping Private Status",
        "Chanel Invests in Sustainable Cashmere Supply Chain",
        "Chanel Partners with Metropolitan Museum for Major Exhibition",
    ],
    "Prada": [
        "Prada Group Revenue Surges on Strong Miu Miu Performance",
        "Prada Unveils Innovative Re-Nylon Collection Made from Ocean Plastic",
        "Prada Opens New Research and Development Center in Milan",
        "Prada Stock Hits All-Time High on Hong Kong Exchange",
        "Prada Collaborates with adidas on Limited-Edition Sneaker Line",
        "Prada Reports Strong Growth in Americas Market",
    ],
    "Burberry": [
        "Burberry Struggles with Brand Repositioning Under New Creative Director",
        "Burberry Sales Fall as Luxury Market Softens in Europe",
        "Burberry Launches Digital Innovation Lab in London",
        "Burberry CEO Outlines Turnaround Strategy Focused on British Heritage",
        "Burberry Cuts Profit Forecast Amid Challenging Market Conditions",
        "Burberry Partners with Minecraft for Virtual Fashion Experience",
    ],
    "Richemont": [
        "Richemont Reports Strong Jewelry Sales Led by Cartier Division",
        "Richemont's Van Cleef & Arpels Sees Record Demand in Middle East",
        "Richemont Acquires Stake in Emerging Swiss Watchmaker",
        "Richemont Shares Rise on Better-Than-Expected Annual Results",
        "Cartier Love Bracelet Becomes Best-Selling Luxury Jewelry Item",
        "Richemont Invests in Blockchain Technology for Watch Authentication",
    ],
    "Tiffany & Co.": [
        "Tiffany & Co. Thrives Under LVMH Ownership with Record Sales",
        "Tiffany Launches New High Jewelry Collection Inspired by Nature",
        "Tiffany Blue Box Cafe Expands to New Global Locations",
        "Tiffany & Co. Partners with Beyonce for Iconic Ad Campaign",
        "Tiffany Reports Strong Engagement Ring Sales in Q3",
        "Tiffany Opens Renovated Fifth Avenue Flagship 'The Landmark'",
    ],
    "Rolex": [
        "Rolex Waitlists Grow Longer as Demand Outpaces Supply",
        "Rolex Announces New Submariner Model at Watches & Wonders",
        "Rolex Certified Pre-Owned Program Expands to More Retailers",
        "Rolex Raises Retail Prices Across All Collections",
        "Rolex Invests in New Manufacturing Facility in Switzerland",
        "Rolex Daytona Sets New Record at Christie's Auction",
    ],
    "Ferrari": [
        "Ferrari Reports Record Profits with Strong Supercar Demand",
        "Ferrari Unveils First Fully Electric Vehicle, the Ferrari EV1",
        "Ferrari Stock Reaches All-Time High on NYSE",
        "Ferrari Expands Lifestyle Brand with New Fashion Collection",
        "Ferrari Announces Limited-Edition Hypercar with 1000 HP",
        "Ferrari Revenue Grows as Personalization Program Drives Higher ASPs",
    ],
}

MOCK_SOURCES = [
    "Reuters", "Bloomberg", "Financial Times", "Wall Street Journal",
    "Business of Fashion", "Luxury Daily", "WWD", "Vogue Business",
    "CNBC", "The Guardian",
]

MOCK_DESCRIPTIONS = {
    "positive": [
        "The luxury brand reported impressive results that exceeded analyst expectations.",
        "Strong demand across key markets drove significant revenue growth.",
        "The company's strategic investments are paying off with record performance.",
        "Market analysts view the latest developments as a positive signal for growth.",
    ],
    "negative": [
        "The company faces challenges amid shifting consumer preferences.",
        "Analysts express concern over declining performance in key segments.",
        "Economic headwinds continue to pressure luxury market valuations.",
        "The brand struggles to maintain momentum in a competitive landscape.",
    ],
    "neutral": [
        "The company announced strategic changes to its business operations.",
        "Industry observers are watching developments closely for future impact.",
        "The latest move represents a shift in the company's long-term strategy.",
        "Market participants remain cautious about the implications of recent changes.",
    ],
}


async def fetch_news_for_all_brands(db: AsyncSession) -> int:
    """Fetch news for all brands. Uses real API if available, otherwise mock data."""
    result = await db.execute(select(Brand))
    brands = result.scalars().all()

    total_count = 0
    for brand in brands:
        if NEWS_API_KEY:
            count = await _fetch_real_news(brand, db)
        else:
            count = await _generate_mock_news(brand, db)
        total_count += count

    return total_count


async def _fetch_real_news(brand: Brand, db: AsyncSession) -> int:
    """Fetch real news from NewsAPI."""
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": brand.name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 10,
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()

        articles = data.get("articles", [])
        count = 0
        for article in articles:
            title = article.get("title", "")
            if not title:
                continue

            sentiment_score, sentiment_label = analyze_sentiment(title)

            news_article = NewsArticle(
                brand_id=brand.id,
                title=title,
                description=article.get("description"),
                source=article.get("source", {}).get("name"),
                url=article.get("url"),
                image_url=article.get("urlToImage"),
                published_at=datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
                if article.get("publishedAt")
                else datetime.utcnow(),
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label,
            )
            db.add(news_article)
            count += 1

        await db.commit()
        return count

    except Exception:
        return await _generate_mock_news(brand, db)


async def _generate_mock_news(brand: Brand, db: AsyncSession) -> int:
    """Generate realistic mock news data for a brand."""
    headlines = MOCK_HEADLINES.get(brand.name, [])
    if not headlines:
        # Generic headlines for unknown brands
        headlines = [
            f"{brand.name} Reports Strong Quarterly Results",
            f"{brand.name} Announces New Product Line Launch",
            f"{brand.name} Expands Global Retail Presence",
            f"{brand.name} Faces Market Challenges in Key Region",
            f"{brand.name} Invests in Digital Transformation",
            f"{brand.name} CEO Discusses Future Growth Strategy",
        ]

    # Select 3-6 random headlines
    num_articles = random.randint(3, 6)
    selected_headlines = random.sample(headlines, min(num_articles, len(headlines)))

    count = 0
    for headline in selected_headlines:
        sentiment_score, sentiment_label = analyze_sentiment(headline)

        # Pick a matching description based on sentiment
        descriptions = MOCK_DESCRIPTIONS.get(sentiment_label, MOCK_DESCRIPTIONS["neutral"])
        description = random.choice(descriptions)

        # Random date within the past 30 days
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        published_at = datetime.utcnow() - timedelta(days=days_ago, hours=hours_ago)

        source = random.choice(MOCK_SOURCES)

        news_article = NewsArticle(
            brand_id=brand.id,
            title=headline,
            description=description,
            source=source,
            url=f"https://example.com/news/{brand.name.lower().replace(' ', '-')}/{count}",
            image_url=None,
            published_at=published_at,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
        )
        db.add(news_article)
        count += 1

    await db.commit()
    return count
