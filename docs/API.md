# API Reference

## Base URL

```
http://localhost:8000/api
```

Interactive documentation is available at `http://localhost:8000/docs` (Swagger UI).

---

## Brands

### List All Brands

```
GET /api/brands
```

**Response** `200 OK`
```json
[
  {
    "id": 1,
    "name": "LVMH",
    "ticker": "MC.PA",
    "sector": "Conglomerate",
    "parent_company": null,
    "country": "France",
    "description": "LVMH Moet Hennessy Louis Vuitton...",
    "logo_url": null,
    "created_at": "2026-03-07T10:00:00"
  }
]
```

### Get Brand by ID

```
GET /api/brands/{id}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `id` | int | Brand ID |

### Create Brand

```
POST /api/brands
```

**Request Body**
```json
{
  "name": "Dior",
  "ticker": null,
  "sector": "Fashion",
  "parent_company": "LVMH",
  "country": "France",
  "description": "Christian Dior SE"
}
```

---

## News

### List News Articles

```
GET /api/news
```

| Query Param | Type | Default | Description |
|-------------|------|---------|-------------|
| `brand_id` | int | null | Filter by brand |
| `limit` | int | 50 | Max articles to return |
| `offset` | int | 0 | Pagination offset |

### Get Latest News

```
GET /api/news/latest
```

Returns the 20 most recent articles across all brands.

### Trigger News Fetch

```
POST /api/news/fetch
```

Triggers immediate news collection for all brands. Returns the count of articles fetched.

**Response** `200 OK`
```json
{
  "message": "Fetched 42 articles"
}
```

---

## Financial Data

### Get Financial History

```
GET /api/financial/{brand_id}
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `brand_id` | int | Brand ID |

| Query Param | Type | Description |
|-------------|------|-------------|
| `start_date` | datetime | Filter from date |
| `end_date` | datetime | Filter to date |

### Get Latest Financial Snapshot

```
GET /api/financial/{brand_id}/latest
```

Returns the most recent financial data point for a brand.

**Response** `200 OK`
```json
{
  "id": 1,
  "brand_id": 1,
  "date": "2026-03-07T10:00:00",
  "open_price": 848.50,
  "close_price": 862.34,
  "high": 865.10,
  "low": 845.20,
  "volume": 2340000,
  "market_cap": 435000000000,
  "change_percent": 1.63,
  "created_at": "2026-03-07T10:00:00"
}
```

### Trigger Financial Fetch

```
POST /api/financial/fetch
```

---

## Analytics

### Sentiment Overview

```
GET /api/analytics/sentiment-overview
```

Returns aggregated sentiment metrics for each brand.

**Response** `200 OK`
```json
[
  {
    "brand_id": 1,
    "brand_name": "LVMH",
    "avg_sentiment": 0.2145,
    "article_count": 5,
    "positive_count": 3,
    "negative_count": 1,
    "neutral_count": 1
  }
]
```

### Brand Comparison

```
GET /api/analytics/brand-comparison
```

Returns each brand with combined sentiment and financial metrics.

**Response** `200 OK`
```json
[
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
```

### Trending Brands

```
GET /api/analytics/trending
```

Returns brands ranked by trending score (news volume * sentiment magnitude).

### Dashboard Summary

```
GET /api/analytics/dashboard-summary
```

Returns high-level stats for the dashboard.

**Response** `200 OK`
```json
{
  "total_brands": 10,
  "total_articles": 42,
  "avg_sentiment": 0.1523,
  "top_movers": [...]
}
```
