import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts';
import LoadingSpinner from '../components/LoadingSpinner';
import NewsCard from '../components/NewsCard';
import { fetchBrand, fetchFinancialData, fetchLatestFinancial, fetchNews } from '../services/api';

function BrandDetail() {
  const { id } = useParams();
  const [brand, setBrand] = useState(null);
  const [financialData, setFinancialData] = useState([]);
  const [latestFinancial, setLatestFinancial] = useState(null);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [brandRes, finRes, latestFinRes, newsRes] = await Promise.allSettled([
          fetchBrand(id),
          fetchFinancialData(id),
          fetchLatestFinancial(id),
          fetchNews({ brand_id: id, limit: 10 }),
        ]);

        if (brandRes.status === 'fulfilled') setBrand(brandRes.value);
        if (finRes.status === 'fulfilled') {
          const d = finRes.value;
          setFinancialData(Array.isArray(d) ? d : d.data || []);
        }
        if (latestFinRes.status === 'fulfilled') setLatestFinancial(latestFinRes.value);
        if (newsRes.status === 'fulfilled') {
          const n = newsRes.value;
          setNews(Array.isArray(n) ? n : n.data || []);
        }
      } catch (err) {
        console.error('Brand detail load error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, [id]);

  if (loading) return <LoadingSpinner />;

  if (!brand) {
    return (
      <div className="empty-state">
        <div className="empty-state__icon">404</div>
        <div className="empty-state__text">Brand not found</div>
      </div>
    );
  }

  const chartData = financialData.map((d) => ({
    date: d.date ? new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }) : '',
    close_price: d.close_price,
    sentiment: d.sentiment_score,
  }));

  const sentimentData = news
    .filter((n) => n.sentiment_score !== undefined && n.published_at)
    .map((n) => ({
      date: new Date(n.published_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
      sentiment: n.sentiment_score,
    }));

  const lf = latestFinancial || {};

  return (
    <div>
      <div className="brand-header">
        <h1 className="brand-header__name">{brand.name}</h1>
        <div className="brand-header__meta">
          {brand.sector && <span className="brand-header__tag">{brand.sector}</span>}
          {brand.country && <span className="brand-header__tag">{brand.country}</span>}
        </div>
        {brand.description && (
          <p className="brand-header__description">{brand.description}</p>
        )}
      </div>

      <div className="metrics-row">
        <div className="metric-card">
          <div className="metric-card__label">Price</div>
          <div className="metric-card__value">
            {lf.close_price !== undefined ? `$${Number(lf.close_price).toLocaleString()}` : '—'}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-card__label">Change %</div>
          <div className="metric-card__value" style={{ color: lf.change_percent > 0 ? '#4caf50' : lf.change_percent < 0 ? '#ef5350' : '#c9a84c' }}>
            {lf.change_percent !== undefined ? `${lf.change_percent > 0 ? '+' : ''}${Number(lf.change_percent).toFixed(2)}%` : '—'}
          </div>
        </div>
        <div className="metric-card">
          <div className="metric-card__label">Volume</div>
          <div className="metric-card__value">
            {lf.volume !== undefined ? Number(lf.volume).toLocaleString() : '—'}
          </div>
        </div>
      </div>

      <div className="grid-2">
        <div className="chart-container">
          <div className="chart-container__title">Price History</div>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="date" tick={{ fill: '#a0a0b0', fontSize: 12 }} />
                <YAxis tick={{ fill: '#a0a0b0', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: '#1a1a2e',
                    border: '1px solid rgba(201,168,76,0.3)',
                    borderRadius: '8px',
                    color: '#f0f0f0',
                  }}
                />
                <Line type="monotone" dataKey="close_price" stroke="#c9a84c" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              <div className="empty-state__text">No financial data available</div>
            </div>
          )}
        </div>

        <div className="chart-container">
          <div className="chart-container__title">Sentiment Trend</div>
          {sentimentData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={sentimentData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="date" tick={{ fill: '#a0a0b0', fontSize: 12 }} />
                <YAxis tick={{ fill: '#a0a0b0', fontSize: 12 }} domain={[0, 1]} />
                <Tooltip
                  contentStyle={{
                    background: '#1a1a2e',
                    border: '1px solid rgba(201,168,76,0.3)',
                    borderRadius: '8px',
                    color: '#f0f0f0',
                  }}
                />
                <Line type="monotone" dataKey="sentiment" stroke="#4caf50" strokeWidth={2} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              <div className="empty-state__text">No sentiment data available</div>
            </div>
          )}
        </div>
      </div>

      <div className="section-title">Recent News</div>
      {news.length > 0 ? (
        <div className="news-list">
          {news.map((article, i) => (
            <NewsCard key={article.id || i} article={article} />
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state__icon">📰</div>
          <div className="empty-state__text">No news articles for this brand</div>
        </div>
      )}
    </div>
  );
}

export default BrandDetail;
