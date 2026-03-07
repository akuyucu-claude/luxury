import React, { useState, useEffect } from 'react';
import LoadingSpinner from '../components/LoadingSpinner';
import NewsCard from '../components/NewsCard';
import { fetchNews, fetchBrands, triggerNewsFetch } from '../services/api';

function NewsFeed() {
  const [articles, setArticles] = useState([]);
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(true);
  const [fetching, setFetching] = useState(false);
  const [brandFilter, setBrandFilter] = useState('');

  useEffect(() => {
    loadBrands();
    loadNews();
  }, []);

  useEffect(() => {
    loadNews();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [brandFilter]);

  async function loadBrands() {
    try {
      const data = await fetchBrands();
      setBrands(Array.isArray(data) ? data : data.data || []);
    } catch (err) {
      console.error('Failed to load brands:', err);
    }
  }

  async function loadNews() {
    setLoading(true);
    try {
      const params = {};
      if (brandFilter) params.brand_id = brandFilter;
      params.limit = 50;
      const data = await fetchNews(params);
      setArticles(Array.isArray(data) ? data : data.data || []);
    } catch (err) {
      console.error('Failed to load news:', err);
      setArticles([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleFetchLatest() {
    setFetching(true);
    try {
      await triggerNewsFetch();
      await loadNews();
    } catch (err) {
      console.error('Failed to trigger news fetch:', err);
    } finally {
      setFetching(false);
    }
  }

  return (
    <div>
      <h1 className="page-title">
        News Feed
        <div className="page-subtitle">Latest luxury brand news and sentiment analysis</div>
      </h1>

      <div className="filter-bar">
        <select
          className="filter-bar__select"
          value={brandFilter}
          onChange={(e) => setBrandFilter(e.target.value)}
        >
          <option value="">All Brands</option>
          {brands.map((b) => (
            <option key={b.id} value={b.id}>{b.name}</option>
          ))}
        </select>
        <button
          className="btn btn--gold"
          onClick={handleFetchLatest}
          disabled={fetching}
        >
          {fetching ? 'Fetching...' : 'Fetch Latest News'}
        </button>
      </div>

      {loading ? (
        <LoadingSpinner />
      ) : articles.length > 0 ? (
        <div className="news-list">
          {articles.map((article, i) => (
            <NewsCard key={article.id || i} article={article} />
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state__icon">📰</div>
          <div className="empty-state__text">No news articles found</div>
        </div>
      )}
    </div>
  );
}

export default NewsFeed;
