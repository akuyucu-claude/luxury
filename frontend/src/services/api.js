const API_BASE = '/api';

async function request(url, options = {}) {
  try {
    const response = await fetch(url, options);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`API Error [${url}]:`, error);
    throw error;
  }
}

function buildQuery(params) {
  if (!params) return '';
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      query.append(key, value);
    }
  });
  const str = query.toString();
  return str ? `?${str}` : '';
}

export function fetchBrands() {
  return request(`${API_BASE}/brands`);
}

export function fetchBrand(id) {
  return request(`${API_BASE}/brands/${id}`);
}

export function fetchNews(params) {
  return request(`${API_BASE}/news${buildQuery(params)}`);
}

export function fetchLatestNews() {
  return request(`${API_BASE}/news/latest`);
}

export function fetchFinancialData(brandId, params) {
  return request(`${API_BASE}/financial/${brandId}${buildQuery(params)}`);
}

export function fetchLatestFinancial(brandId) {
  return request(`${API_BASE}/financial/${brandId}/latest`);
}

export function fetchSentimentOverview() {
  return request(`${API_BASE}/analytics/sentiment-overview`);
}

export function fetchBrandComparison() {
  return request(`${API_BASE}/analytics/brand-comparison`);
}

export function fetchTrending() {
  return request(`${API_BASE}/analytics/trending`);
}

export function fetchDashboardSummary() {
  return request(`${API_BASE}/analytics/dashboard-summary`);
}

export function triggerNewsFetch() {
  return request(`${API_BASE}/news/fetch`, { method: 'POST' });
}

export function triggerFinancialFetch() {
  return request(`${API_BASE}/financial/fetch`, { method: 'POST' });
}
