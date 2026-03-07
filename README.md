# Luxury Brand Monitor

A full-stack application to collect, monitor, and analyze news, financial data, and sentiment for the world's top luxury brands.

---

## Table of Contents

1. [Features](#features)
2. [Architecture Overview](#architecture-overview)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the Application](#running-the-application)
7. [API Documentation](#api-documentation)
8. [Frontend Components](#frontend-components)
9. [Data Flow](#data-flow)
10. [Project Structure](#project-structure)

---

## Features

- **News Aggregation** - Collects and displays the latest news for 10 luxury brands from live APIs or realistic mock data
- **Financial Monitoring** - Tracks stock prices, market cap, volume, and daily price changes for publicly traded luxury companies
- **Sentiment Analysis** - Analyzes news article sentiment using NLP (TextBlob) and classifies as positive, negative, or neutral
- **Brand Comparison** - Side-by-side comparison of brands across financial performance and sentiment metrics
- **Trending Analysis** - Identifies trending brands based on news volume and sentiment magnitude
- **Interactive Dashboard** - Real-time charts, stat cards, and data visualizations with a luxury dark/gold theme
- **Scheduled Data Collection** - Background scheduler automatically fetches news and financial data at configurable intervals

### Tracked Brands

| Brand | Ticker | Sector | Country |
|-------|--------|--------|---------|
| LVMH | MC.PA | Conglomerate | France |
| Kering | KER.PA | Conglomerate | France |
| Hermes | RMS.PA | Fashion | France |
| Chanel | Private | Fashion | France |
| Prada | 1913.HK | Fashion | Italy |
| Burberry | BRBY.L | Fashion | UK |
| Richemont | CFR.SW | Jewelry/Watches | Switzerland |
| Tiffany & Co. | Private (LVMH) | Jewelry | USA |
| Rolex | Private | Watches | Switzerland |
| Ferrari | RACE | Automotive | Italy |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Frontend (React)                      │
│  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌────────────┐  │
│  │Dashboard │ │BrandList │ │NewsFeed │ │ Analytics  │  │
│  └────┬─────┘ └────┬─────┘ └────┬────┘ └─────┬──────┘  │
│       └─────────────┴────────────┴─────────────┘        │
│                         │ HTTP/JSON                      │
├─────────────────────────┼───────────────────────────────┤
│                    Backend (FastAPI)                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐  │
│  │ Brands   │ │  News    │ │Financial │ │ Analytics │  │
│  │ Router   │ │  Router  │ │ Router   │ │  Router   │  │
│  └────┬─────┘ └────┬─────┘ └────┬────┘ └─────┬─────┘  │
│       └─────────────┴────────────┴─────────────┘        │
│                         │                                │
│  ┌──────────────────────┼───────────────────────┐       │
│  │              Services Layer                   │       │
│  │  ┌─────────┐ ┌──────────┐ ┌───────────────┐ │       │
│  │  │  News   │ │Financial │ │  Sentiment    │ │       │
│  │  │ Service │ │ Service  │ │  Service      │ │       │
│  │  └─────────┘ └──────────┘ └───────────────┘ │       │
│  └──────────────────────────────────────────────┘       │
│                         │                                │
│  ┌──────────────────────┼───────────────────────┐       │
│  │           SQLite Database                     │       │
│  │  brands | news_articles | financial_data |    │       │
│  │  sentiment_summaries                          │       │
│  └──────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

---

## Tech Stack

### Backend
- **Python 3.10+**
- **FastAPI** - High-performance async web framework
- **SQLAlchemy 2.0** - Async ORM with SQLite via aiosqlite
- **APScheduler** - Background job scheduling for data collection
- **TextBlob** - NLP-based sentiment analysis
- **yfinance** - Yahoo Finance API for stock data
- **httpx** - Async HTTP client for API calls
- **Pydantic** - Data validation and serialization

### Frontend
- **React 18** - UI component library
- **React Router 6** - Client-side routing
- **Recharts** - Charting library (bar charts, line charts, pie charts)
- **CSS** - Custom dark/gold luxury theme

---

## Installation

### Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- npm 8 or higher

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# Install Python dependencies
pip install -r requirements.txt

# Download TextBlob corpora (needed for sentiment analysis)
python -m textblob.download_corpora
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

---

## Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory (optional):

```env
# NewsAPI key for live news data (optional - falls back to mock data)
NEWS_API_KEY=your_newsapi_key_here

# Database URL (optional - defaults to SQLite)
DATABASE_URL=sqlite+aiosqlite:///luxury_brands.db
```

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NEWS_API_KEY` | No | None | API key from [newsapi.org](https://newsapi.org). If not set, the app generates realistic mock news data |
| `DATABASE_URL` | No | `sqlite+aiosqlite:///luxury_brands.db` | SQLAlchemy async database URL |

### Getting a NewsAPI Key

1. Go to [newsapi.org](https://newsapi.org)
2. Sign up for a free account
3. Copy your API key
4. Add it to your `.env` file

> Without a NewsAPI key, the app works fully with realistic mock data including brand-specific headlines and sentiment analysis.

---

## Running the Application

### Start the Backend

```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

The backend will:
1. Create the SQLite database and tables
2. Seed 10 default luxury brands
3. Start the background scheduler for data collection
4. Serve the API at `http://localhost:8000`

### Start the Frontend

```bash
cd frontend
npm start
```

The frontend runs at `http://localhost:3000` and proxies API requests to the backend on port 8000.

### Verify It's Working

- Backend API docs: `http://localhost:8000/docs` (Swagger UI)
- Backend health check: `http://localhost:8000/health`
- Frontend app: `http://localhost:3000`

### Trigger Initial Data Load

After starting both servers, fetch initial data:

```bash
# Fetch news articles
curl -X POST http://localhost:8000/api/news/fetch

# Fetch financial data
curl -X POST http://localhost:8000/api/financial/fetch
```

Or use the "Fetch Latest News" button on the News Feed page.

---

## API Documentation

### Brands

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/brands` | List all tracked brands |
| `GET` | `/api/brands/{id}` | Get a specific brand by ID |
| `POST` | `/api/brands` | Add a new brand |

### News

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/news` | List news articles (supports `brand_id`, `limit`, `offset` query params) |
| `GET` | `/api/news/latest` | Get the 20 most recent articles across all brands |
| `POST` | `/api/news/fetch` | Trigger news data collection for all brands |

### Financial

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/financial/{brand_id}` | Get financial history for a brand (supports date range params) |
| `GET` | `/api/financial/{brand_id}/latest` | Get the latest financial snapshot for a brand |
| `POST` | `/api/financial/fetch` | Trigger financial data collection for all brands |

### Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/analytics/sentiment-overview` | Sentiment summary per brand (avg score, positive/negative/neutral counts) |
| `GET` | `/api/analytics/brand-comparison` | Compare brands by sentiment and financial metrics |
| `GET` | `/api/analytics/trending` | Trending brands ranked by news volume and sentiment magnitude |
| `GET` | `/api/analytics/dashboard-summary` | High-level stats: total brands, articles, avg sentiment, top movers |

### Example API Responses

**GET /api/analytics/dashboard-summary**
```json
{
  "total_brands": 10,
  "total_articles": 42,
  "avg_sentiment": 0.1523,
  "top_movers": [
    {
      "brand_id": 1,
      "brand_name": "LVMH",
      "ticker": "MC.PA",
      "avg_sentiment": 0.2145,
      "article_count": 5,
      "latest_close_price": 862.34,
      "price_change_percent": 1.82
    }
  ]
}
```

**GET /api/analytics/trending**
```json
[
  {
    "brand_id": 3,
    "brand_name": "Hermes",
    "article_count": 6,
    "sentiment_change": 0.3201,
    "trending_score": 7.92
  }
]
```

---

## Frontend Components

### Pages

| Component | Route | Description |
|-----------|-------|-------------|
| **Dashboard** | `/` | Main overview with stat cards (total brands, articles, avg sentiment, top mover), sentiment bar chart, trending brands list, and latest news feed |
| **BrandList** | `/brands` | Grid of brand cards with name, sector, country, and sentiment indicator. Includes search/filter. Click a card to view brand detail |
| **BrandDetail** | `/brands/:id` | Detailed brand page with financial line chart (stock price over time), latest metrics, recent news, and sentiment trend chart |
| **NewsFeed** | `/news` | Full news feed with sentiment-colored badges. Filter by brand via dropdown. "Fetch Latest News" button to trigger data collection |
| **Analytics** | `/analytics` | Brand comparison bar chart, sentiment distribution pie chart, sortable brand ranking table, and trending analysis section |

### Shared Components

| Component | Props | Description |
|-----------|-------|-------------|
| **StatCard** | `label`, `value`, `icon` | Reusable metric card with a gold border, showing a stat label, value, and emoji icon |
| **SentimentBadge** | `label`, `score` | Colored badge indicating sentiment: green (positive), red (negative), gray (neutral) |
| **NewsCard** | `article` | News article card displaying title, description, source, published date, and sentiment badge |
| **LoadingSpinner** | none | Elegant gold-colored loading spinner shown during data fetches |

### Component Hierarchy

```
App
├── Sidebar (navigation)
│   ├── NavLink -> Dashboard
│   ├── NavLink -> Brands
│   ├── NavLink -> News
│   └── NavLink -> Analytics
│
├── Dashboard
│   ├── StatCard x4 (summary metrics)
│   ├── BarChart (sentiment by brand)
│   ├── Trending list
│   └── NewsCard x5 (latest news)
│
├── BrandList
│   ├── Search/filter bar
│   └── Brand cards (clickable grid)
│
├── BrandDetail
│   ├── Brand header info
│   ├── LineChart (stock price)
│   ├── Financial metrics
│   ├── LineChart (sentiment trend)
│   └── NewsCard list
│
├── NewsFeed
│   ├── Brand filter dropdown
│   ├── Fetch button
│   └── NewsCard list
│
└── Analytics
    ├── BarChart (brand comparison)
    ├── PieChart (sentiment distribution)
    ├── Ranking table (sortable)
    └── Trending analysis
```

---

## Data Flow

### 1. Data Collection Pipeline

```
Scheduler (APScheduler)
    │
    ├── Every 2 hours ── News Service
    │                       ├── Try NewsAPI (if API key set)
    │                       │   └── Fetch articles for each brand
    │                       └── Fallback: Generate mock news
    │                           └── Brand-specific realistic headlines
    │                                   │
    │                                   ▼
    │                           Sentiment Service
    │                               ├── TextBlob polarity analysis
    │                               ├── Score: -1.0 to +1.0
    │                               └── Label: positive (>0.1) / negative (<-0.1) / neutral
    │
    ├── Every 1 hour ── Financial Service
    │                       ├── Try yfinance (real stock data)
    │                       └── Fallback: Random walk mock prices
    │                           └── 30-day history with realistic volatility
    │
    └── Every 3 hours ── Sentiment Summary
                            └── Aggregate daily sentiment per brand
```

### 2. Request/Response Flow

```
User Browser
    │
    ▼
React Frontend (port 3000)
    │ fetch('/api/...')
    │ (proxied via package.json proxy setting)
    ▼
FastAPI Backend (port 8000)
    │
    ├── Router layer (validates request, extracts params)
    ├── Service layer (business logic, external API calls)
    ├── Model layer (SQLAlchemy ORM)
    └── Database (SQLite)
    │
    ▼
JSON Response -> React State -> UI Render
```

### 3. Sentiment Analysis Flow

```
News Article Title + Description
    │
    ▼
TextBlob(text).sentiment.polarity
    │
    ├── polarity > 0.1  → "positive" (green badge)
    ├── polarity < -0.1 → "negative" (red badge)
    └── else            → "neutral"  (gray badge)
    │
    ▼
Stored in DB: sentiment_score (float), sentiment_label (string)
    │
    ▼
Aggregated into SentimentSummary per brand per day
```

---

## Project Structure

```
luxury/
├── README.md
├── backend/
│   ├── requirements.txt          # Python dependencies
│   └── app/
│       ├── __init__.py
│       ├── main.py               # FastAPI app entry point, CORS, lifespan
│       ├── database.py           # SQLAlchemy async engine, session, init_db with seed data
│       ├── models.py             # ORM models: Brand, NewsArticle, FinancialData, SentimentSummary
│       ├── schemas.py            # Pydantic schemas for request/response validation
│       ├── routers/
│       │   ├── __init__.py
│       │   ├── brands.py         # CRUD endpoints for brands
│       │   ├── news.py           # News listing and fetch trigger endpoints
│       │   ├── financial.py      # Financial data retrieval and fetch trigger
│       │   └── analytics.py      # Aggregated analytics: sentiment, comparison, trending
│       └── services/
│           ├── __init__.py
│           ├── news_service.py       # News fetching (NewsAPI + mock fallback)
│           ├── financial_service.py  # Financial data (yfinance + mock fallback)
│           ├── sentiment_service.py  # TextBlob sentiment analysis
│           └── scheduler.py          # APScheduler for periodic data collection
│
└── frontend/
    ├── package.json              # React dependencies and scripts
    ├── public/
    │   └── index.html            # HTML entry point
    └── src/
        ├── index.js              # React entry point with BrowserRouter
        ├── App.js                # Main layout: sidebar, routing, responsive design
        ├── App.css               # Global styles: dark/gold luxury theme
        ├── services/
        │   └── api.js            # API client functions for all backend endpoints
        ├── pages/
        │   ├── Dashboard.js      # Overview: stats, charts, news, trending
        │   ├── BrandList.js      # Searchable brand grid
        │   ├── BrandDetail.js    # Brand deep-dive: financials, news, sentiment
        │   ├── NewsFeed.js       # Full news feed with filters
        │   └── Analytics.js      # Charts, rankings, and comparisons
        └── components/
            ├── StatCard.js       # Reusable metric display card
            ├── SentimentBadge.js # Color-coded sentiment indicator
            ├── NewsCard.js       # News article card
            └── LoadingSpinner.js # Gold loading spinner
```

---

## Development Notes

- The app works fully offline with mock data - no API keys required
- Mock news includes brand-specific realistic headlines from sources like Reuters, Bloomberg, FT
- Mock financial data uses random walk simulation with realistic base prices
- The SQLite database is created automatically on first run
- The scheduler runs data collection in the background automatically
- All API endpoints support async operations for high performance
