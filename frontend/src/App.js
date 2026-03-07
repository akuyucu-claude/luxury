import React, { useState } from 'react';
import { Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import BrandList from './pages/BrandList';
import BrandDetail from './pages/BrandDetail';
import NewsFeed from './pages/NewsFeed';
import Analytics from './pages/Analytics';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const navItems = [
    { path: '/', label: 'Dashboard', icon: '📊' },
    { path: '/brands', label: 'Brands', icon: '👜' },
    { path: '/news', label: 'News', icon: '📰' },
    { path: '/analytics', label: 'Analytics', icon: '📈' },
  ];

  return (
    <div className="app">
      <aside className={`sidebar ${sidebarOpen ? 'sidebar--open' : ''}`}>
        <div className="sidebar__header">
          <span className="sidebar__icon">💎</span>
          <h1 className="sidebar__title">Luxury Brand Monitor</h1>
        </div>
        <nav className="sidebar__nav">
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `sidebar__link ${isActive ? 'sidebar__link--active' : ''}`
              }
              onClick={() => setSidebarOpen(false)}
            >
              <span className="sidebar__link-icon">{item.icon}</span>
              <span className="sidebar__link-label">{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="sidebar__footer">
          <span className="sidebar__footer-text">&copy; 2026 LBM</span>
        </div>
      </aside>

      <div className="main">
        <header className="topbar">
          <button
            className="topbar__menu-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle menu"
          >
            ☰
          </button>
          <div className="topbar__title">
            <span className="topbar__diamond">💎</span> Luxury Brand Monitor
          </div>
        </header>
        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/brands" element={<BrandList />} />
            <Route path="/brands/:id" element={<BrandDetail />} />
            <Route path="/news" element={<NewsFeed />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>

      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}
    </div>
  );
}

export default App;
