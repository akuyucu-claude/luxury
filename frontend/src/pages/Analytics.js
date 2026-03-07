import React, { useState, useEffect } from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
  PieChart, Pie, Cell,
} from 'recharts';
import LoadingSpinner from '../components/LoadingSpinner';
import { fetchBrandComparison, fetchSentimentOverview, fetchTrending } from '../services/api';

const PIE_COLORS = ['#4caf50', '#ef5350', '#78909c'];

function Analytics() {
  const [comparison, setComparison] = useState([]);
  const [sentimentOverview, setSentimentOverview] = useState([]);
  const [trending, setTrending] = useState([]);
  const [loading, setLoading] = useState(true);
  const [sortKey, setSortKey] = useState('brand_name');
  const [sortDir, setSortDir] = useState('asc');

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const [compRes, sentRes, trendRes] = await Promise.allSettled([
          fetchBrandComparison(),
          fetchSentimentOverview(),
          fetchTrending(),
        ]);

        if (compRes.status === 'fulfilled') {
          const d = compRes.value;
          setComparison(Array.isArray(d) ? d : d.data || []);
        }
        if (sentRes.status === 'fulfilled') {
          const d = sentRes.value;
          setSentimentOverview(Array.isArray(d) ? d : d.data || []);
        }
        if (trendRes.status === 'fulfilled') {
          const d = trendRes.value;
          setTrending(Array.isArray(d) ? d : d.data || []);
        }
      } catch (err) {
        console.error('Analytics load error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) return <LoadingSpinner />;

  // Map comparison data for charts
  const comparisonChartData = comparison.map(item => ({
    brand: item.brand_name,
    avg_sentiment: item.avg_sentiment,
    price_change: item.price_change_percent || 0,
  }));

  // Compute sentiment distribution for pie chart from overview data
  const sentimentCounts = sentimentOverview.reduce(
    (acc, item) => {
      acc.positive += item.positive_count || 0;
      acc.negative += item.negative_count || 0;
      acc.neutral += item.neutral_count || 0;
      return acc;
    },
    { positive: 0, negative: 0, neutral: 0 }
  );

  const pieData = [
    { name: 'Positive', value: sentimentCounts.positive || 1 },
    { name: 'Negative', value: sentimentCounts.negative || 1 },
    { name: 'Neutral', value: sentimentCounts.neutral || 1 },
  ];

  // Sort the comparison data for the ranking table
  const sortedComparison = [...comparison].sort((a, b) => {
    let aVal = a[sortKey];
    let bVal = b[sortKey];
    if (typeof aVal === 'string') aVal = aVal.toLowerCase();
    if (typeof bVal === 'string') bVal = bVal.toLowerCase();
    if (aVal == null) return 1;
    if (bVal == null) return -1;
    if (aVal < bVal) return sortDir === 'asc' ? -1 : 1;
    if (aVal > bVal) return sortDir === 'asc' ? 1 : -1;
    return 0;
  });

  function handleSort(key) {
    if (sortKey === key) {
      setSortDir(sortDir === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortDir('asc');
    }
  }

  function sortIndicator(key) {
    if (sortKey !== key) return '';
    return sortDir === 'asc' ? ' \u2191' : ' \u2193';
  }

  return (
    <div>
      <h1 className="page-title">
        Analytics
        <div className="page-subtitle">In-depth brand comparison and sentiment analysis</div>
      </h1>

      <div className="grid-2">
        <div className="chart-container">
          <div className="chart-container__title">Brand Comparison</div>
          {comparisonChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={350}>
              <BarChart data={comparisonChartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="brand" tick={{ fill: '#a0a0b0', fontSize: 12 }} />
                <YAxis tick={{ fill: '#a0a0b0', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    background: '#1a1a2e',
                    border: '1px solid rgba(201,168,76,0.3)',
                    borderRadius: '8px',
                    color: '#f0f0f0',
                  }}
                />
                <Legend wrapperStyle={{ color: '#a0a0b0' }} />
                <Bar dataKey="avg_sentiment" name="Sentiment" fill="#c9a84c" radius={[4, 4, 0, 0]} />
                <Bar dataKey="price_change" name="Price Change %" fill="#4caf50" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              <div className="empty-state__text">No comparison data available</div>
            </div>
          )}
        </div>

        <div className="chart-container">
          <div className="chart-container__title">Sentiment Distribution</div>
          <ResponsiveContainer width="100%" height={350}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={70}
                outerRadius={120}
                paddingAngle={4}
                dataKey="value"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {pieData.map((entry, index) => (
                  <Cell key={entry.name} fill={PIE_COLORS[index]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  background: '#1a1a2e',
                  border: '1px solid rgba(201,168,76,0.3)',
                  borderRadius: '8px',
                  color: '#f0f0f0',
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="chart-container">
        <div className="chart-container__title">Brand Rankings</div>
        {sortedComparison.length > 0 ? (
          <div className="table-wrapper">
            <table className="table">
              <thead>
                <tr>
                  <th onClick={() => handleSort('brand_name')}>Brand{sortIndicator('brand_name')}</th>
                  <th onClick={() => handleSort('avg_sentiment')}>Avg Sentiment{sortIndicator('avg_sentiment')}</th>
                  <th onClick={() => handleSort('price_change_percent')}>Price Change %{sortIndicator('price_change_percent')}</th>
                  <th onClick={() => handleSort('article_count')}>Articles{sortIndicator('article_count')}</th>
                </tr>
              </thead>
              <tbody>
                {sortedComparison.map((row, i) => (
                  <tr key={i}>
                    <td style={{ color: '#f0f0f0', fontWeight: 600 }}>{row.brand_name}</td>
                    <td>
                      <span style={{
                        color: row.avg_sentiment > 0.1 ? '#4caf50' : row.avg_sentiment < -0.1 ? '#ef5350' : '#78909c',
                      }}>
                        {row.avg_sentiment !== undefined ? Number(row.avg_sentiment).toFixed(3) : '\u2014'}
                      </span>
                    </td>
                    <td style={{
                      color: (row.price_change_percent || 0) > 0 ? '#4caf50' : (row.price_change_percent || 0) < 0 ? '#ef5350' : '#a0a0b0',
                    }}>
                      {row.price_change_percent != null ? `${Number(row.price_change_percent).toFixed(2)}%` : '\u2014'}
                    </td>
                    <td>{row.article_count !== undefined ? row.article_count : '\u2014'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="empty-state">
            <div className="empty-state__text">No ranking data available</div>
          </div>
        )}
      </div>

      <div className="chart-container" style={{ marginTop: 24 }}>
        <div className="chart-container__title">Trending Analysis</div>
        {trending.length > 0 ? (
          <div className="trending-list">
            {trending.map((item, i) => (
              <div key={i} className="trending-item">
                <span className="trending-item__name">{item.brand_name}</span>
                <span className="trending-item__score">
                  Score: {Number(item.trending_score).toFixed(2)} | Articles: {item.article_count}
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
  );
}

export default Analytics;
