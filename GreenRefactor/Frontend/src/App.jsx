import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { LoginScreen } from './components/LoginScreen';
import { OverviewTab } from './components/OverviewTab';
import { RefactorTab } from './components/RefactorTab';
import { BenchmarkCatalogTab } from './components/BenchmarkCatalogTab';
import { StatsInspectorTab } from './components/StatsInspectorTab';
import { UserProfileTab } from './components/UserProfileTab';
import { HelpDrawer } from './components/HelpDrawer';
import { API_BASE_URL } from './apiConfig';

export default function App() {
  const [user, setUser] = useState(() => {
    try {
      const saved = localStorage.getItem('greenrefactor_user');
      return saved ? JSON.parse(saved) : null;
    } catch {
      return null;
    }
  });
  const [token, setToken] = useState(() => localStorage.getItem('greenrefactor_token') || null);
  const [theme, setTheme] = useState('dark');
  const [activeTab, setActiveTab] = useState('overview');
  const [summaryData, setSummaryData] = useState(null);
  const [isBackendConnected, setIsBackendConnected] = useState(true);
  const [isHelpOpen, setIsHelpOpen] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  // Load live benchmark summary data from backend API
  const fetchSummaryData = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/api/summary`);
      if (res.ok) {
        const data = await res.json();
        setSummaryData(data);
        setIsBackendConnected(true);
      } else {
        setIsBackendConnected(false);
      }
    } catch (err) {
      console.warn('Backend server disconnected:', err);
      setIsBackendConnected(false);
    }
  };

  useEffect(() => {
    fetchSummaryData();
    if (activeTab !== 'overview' && activeTab !== 'stats') return;
    const interval = setInterval(fetchSummaryData, 5000);
    return () => clearInterval(interval);
  }, [activeTab]);

  // Session token (if any) is stored alongside the user profile so it
  // survives a page reload and can be sent as `Authorization: Bearer <token>`
  // on requests that now require it (e.g. /api/user/settings).
  const handleLogin = (userData, sessionToken) => {
    setUser(userData);
    setToken(sessionToken || null);
    try {
      localStorage.setItem('greenrefactor_user', JSON.stringify(userData));
      if (sessionToken) {
        localStorage.setItem('greenrefactor_token', sessionToken);
      } else {
        localStorage.removeItem('greenrefactor_token');
      }
    } catch {
      // localStorage unavailable (e.g. private browsing) -- session just won't survive a reload
    }
  };

  const handleLogout = () => {
    setUser(null);
    setToken(null);
    try {
      localStorage.removeItem('greenrefactor_user');
      localStorage.removeItem('greenrefactor_token');
    } catch {
      // ignore
    }
  };

  // Show login screen if not logged in
  if (!user) {
    return <LoginScreen onLogin={handleLogin} />;
  }

  // Helper to re-fetch benchmark data from backend on request
  const handleLoadSample = () => {
    fetchSummaryData();
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg-dark)' }}>
      
      {/* Header Bar */}
      <Header
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        theme={theme}
        setTheme={setTheme}
        onOpenHelp={() => setIsHelpOpen(true)}
      />

      {/* Help & FAQs Side Drawer Panel */}
      <HelpDrawer
        isOpen={isHelpOpen}
        onClose={() => setIsHelpOpen(false)}
        activeTab={activeTab}
      />

      {!isBackendConnected && (
        <div style={{
          background: 'var(--rose-subtle)',
          borderBottom: '1px solid var(--rose-primary)',
          color: 'var(--rose-primary)',
          padding: '10px 24px',
          textAlign: 'center',
          fontSize: '0.85rem',
          fontWeight: 500,
          display: 'flex',
          justify: 'center',
          alignItems: 'center',
          gap: '8px'
        }}>
          <span>⚠️ <strong>FastAPI Backend Disconnected</strong> — To enable live backend features, run in a separate terminal: <code>cd greenrefactor/Backend && python -m uvicorn api:app --reload --port 8000</code></span>
        </div>
      )}

      {/* Main Viewport */}
      <main style={{ flex: 1, maxWidth: '1200px', width: '100%', margin: '0 auto', padding: '24px' }}>
        {activeTab === 'overview' && (
          <OverviewTab
            summaryData={summaryData}
            onLoadSample={handleLoadSample}
          />
        )}
        
        {activeTab === 'refactor' && <RefactorTab />}

        {activeTab === 'benchmark' && <BenchmarkCatalogTab />}
        
        {activeTab === 'stats' && (
          <StatsInspectorTab
            summaryData={summaryData}
            onLoadSample={handleLoadSample}
          />
        )}
        
        {activeTab === 'profile' && (
          <UserProfileTab user={user} token={token} onLogout={handleLogout} />
        )}
      </main>

      {/* Minimal Executive Footer */}
      <footer style={{ borderTop: '1px solid var(--border-color)', padding: '16px 24px', fontSize: '0.8rem', color: 'var(--text-dim)', background: 'var(--bg-card)' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          <div>
            <strong>GreenRefactor Engine</strong> — Energy-Efficient Software Refactoring
          </div>
          <div>
            Python • JavaScript • C • C++ • Java • Go • Rust • C#
          </div>
        </div>
      </footer>

    </div>
  );
}
