import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import LoadingSpinner from '../components/LoadingSpinner';
import { fetchBrands } from '../services/api';

function BrandList() {
  const [brands, setBrands] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [sectorFilter, setSectorFilter] = useState('');

  useEffect(() => {
    async function loadBrands() {
      try {
        const data = await fetchBrands();
        setBrands(Array.isArray(data) ? data : data.data || []);
      } catch (err) {
        console.error('Failed to load brands:', err);
        setBrands([]);
      } finally {
        setLoading(false);
      }
    }
    loadBrands();
  }, []);

  if (loading) return <LoadingSpinner />;

  const sectors = [...new Set(brands.map((b) => b.sector).filter(Boolean))];

  const filtered = brands.filter((b) => {
    const matchesSearch =
      !search ||
      (b.name || '').toLowerCase().includes(search.toLowerCase()) ||
      (b.sector || '').toLowerCase().includes(search.toLowerCase()) ||
      (b.country || '').toLowerCase().includes(search.toLowerCase());
    const matchesSector = !sectorFilter || b.sector === sectorFilter;
    return matchesSearch && matchesSector;
  });

  function getSentimentClass(label) {
    if (!label) return 'neutral';
    const l = label.toLowerCase();
    if (l === 'positive') return 'positive';
    if (l === 'negative') return 'negative';
    return 'neutral';
  }

  return (
    <div>
      <h1 className="page-title">
        Brands
        <div className="page-subtitle">Explore luxury brands and their performance</div>
      </h1>

      <div className="filter-bar">
        <input
          className="filter-bar__input"
          type="text"
          placeholder="Search brands..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="filter-bar__select"
          value={sectorFilter}
          onChange={(e) => setSectorFilter(e.target.value)}
        >
          <option value="">All Sectors</option>
          {sectors.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {filtered.length > 0 ? (
        <div className="brand-grid">
          {filtered.map((brand) => (
            <Link
              key={brand.id}
              to={`/brands/${brand.id}`}
              className="brand-card"
            >
              <div className="brand-card__name">{brand.name}</div>
              <div className="brand-card__meta">{brand.sector || 'Luxury'}</div>
              <div className="brand-card__meta">{brand.country || '—'}</div>
              <div className="brand-card__sentiment">
                <span className={`sentiment-dot sentiment-dot--${getSentimentClass(brand.sentiment_label)}`} />
                <span>{brand.sentiment_label || 'N/A'}</span>
              </div>
            </Link>
          ))}
        </div>
      ) : (
        <div className="empty-state">
          <div className="empty-state__icon">👜</div>
          <div className="empty-state__text">No brands found</div>
        </div>
      )}
    </div>
  );
}

export default BrandList;
