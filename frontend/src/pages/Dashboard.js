import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import StatCard from '../components/StatCard';
import NewsCard from '../components/NewsCard';
import LoadingSpinner from '../components/LoadingSpinner';
import { fetchDashboardSummary, fetchSentimentOverview, fetchLatestNews, fetchTrending } from '../services/api';

const PLACEHOLDER_SUMMARY = {
  total_brands: 12,
  total_articles: 248,
  average_sentiment: 0.62,
  top_mover: 'LVMH',
};

const PLACEHOLDER_SENTIMENT = [
  { brand: 'LVMH', avg_sentiment: 0.72 },
  { brand: 'Hermès', avg_sentiment: 0.68 },
  { brand: 'Gucci', avg_sentiment: 0.55 },
  { brand: 'Chanel', avg_sentiment: 0.61 },
  { brand: 'Prada', avg_sentiment: 0.48 },
];

function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [sentimentData, setSentimentData] = useState([]);
  const [latestNews, setLatestNews] = useState([]);
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [summaryRes, sentimentRes, newsRes, trendingRes] = await Promise.allSettled([
          fetchDashboardSummary(),
          fetchSentimentOverview(),
          fetchLatestNews(),
          fetchTrending(),
        ]);

        setSummary(summaryRes.status === 'fulfilled' ? summaryRes.value : PLACEHOLDER_SUMMARY);
        setSentimentData(
          sentimentRes.status === 'fulfilled'
            ? (Array.isArray(sentimentRes.value) ? sentimentRes.value : sentimentRes.value.data || PLACEHOLDER_SENTIMENT)
            : PLACEHOLDER_SENTIMENT
        );
        setLatestNews(
          newsRes.status === 'fulfilled'
            ? (Array.isArray(newsRes.value) ? newsRes.value.slice(0, 5) : (newsRes.value.data || []).slice(0, 5))
            : []
        );
        setTrending(
          trendingRes.status === 'fulfilled'
            ? (Array.isArray(trendingRes.value) ? trendingRes.value : trendingRes.value.data || [])
            : []
        );
      } catch (err) {
        console.error('Dashboard load error:', err);
        setSummary(PLACEHOLDER_SUMMARY);
        setSentimentData(PLACEHOLDER_SENTIMENT);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <LoadingSpinner />;

  const s = summary || PLACEHOLDER_SUMMARY;
  const avgSent = s.avg_sentiment ?? s.average_sentiment;
  const topMover = s.top_movers && s.top_movers.length > 0 ? s.top_movers[0].brand_name : (s.top_mover || '—');

  // Map sentiment overview to chart format
  const chartData = sentimentData.map(item => ({
    brand: item.brand_name || item.brand,
    avg_sentiment: item.avg_sentiment,
  }));

  return (
    <div>
      <h1 className="page-title">
        Dashboard
        <div className="page-subtitle">Overview of luxury brand performance</div>
      </h1>

      <div className="stats-row">
        <StatCard label="Total Brands" value={s.total_brands} icon="👜" />
        <StatCard label="Total Articles" value={s.total_articles} icon="📰" />
        <StatCard
          label="Avg Sentiment"
          value={typeof avgSent === 'number' ? avgSent.toFixed(2) : avgSent}
          icon="📊"
        />
        <StatCard label="Top Mover" value={topMover} icon="🚀" />
      </div>

      <div className="grid-2">
        <div className="chart-container">
          <div className="chart-container__title">Sentiment by Brand</div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="brand" tick={{ fill: '#a0a0b0', fontSize: 12 }} />
              <YAxis tick={{ fill: '#a0a0b0', fontSize: 12 }} domain={[0, 1]} />
              <Tooltip
                contentStyle={{
                  background: '#1a1a2e',
                  border: '1px solid rgba(201,168,76,0.3)',
                  borderRadius: '8px',
                  color: '#f0f0f0',
                }}
              />
              <Bar dataKey="avg_sentiment" fill="#c9a84c" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div>
          <div className="section-title">Trending Brands</div>
          {trending.length > 0 ? (
            <div className="trending-list">
              {trending.map((item, i) => (
                <div key={i} className="trending-item">
                  <span className="trending-item__name">{item.brand_name || item.brand || item.name}</span>
                  <span className="trending-item__score">
                    {item.trending_score !== undefined ? Number(item.trending_score).toFixed(2) : (item.score !== undefined ? Number(item.score).toFixed(2) : '—')}
                  </span>
                </div>
              ))}
            </div>
          ) : (
            <div className="empty-state">
              <div className="empty-state__icon">📈</div>
              <div className="empty-state__text">No trending data available</div>
            </div>
          )}
        </div>
      </div>

      <div className="section-title">Latest News</div>
      {latestNews.length > 0 ? (
        <div className="news-list">
          {latestNews.map((article, i) => (
            <NewsCard key={article.id || i} article={article} />
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state__icon">📰</div>
          <div className="empty-state__text">No recent news articles</div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
