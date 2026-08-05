import React from 'react';
import { Leaf, BarChart2, Code2, LineChart, Database, User, Sun, Moon } from 'lucide-react';

export function Header({ activeTab, setActiveTab, user, theme, setTheme, onOpenHelp }) {
  const tabs = [
    { id: 'overview', label: 'Overview', icon: BarChart2 },
    { id: 'refactor', label: 'Refactor Engine', icon: Code2 },
    { id: 'benchmark', label: 'Benchmark Suite', icon: Database },
    { id: 'stats', label: 'Statistical Rigor & Diffs', icon: LineChart },
  ];

  const toggleTheme = () => {
    const nextTheme = theme === 'dark' ? 'light' : 'dark';
    setTheme(nextTheme);
    document.documentElement.setAttribute('data-theme', nextTheme);
  };

  return (
    <header style={{ borderBottom: '1px solid var(--border-color)', background: 'var(--bg-card)', position: 'sticky', top: 0, zIndex: 50 }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '12px 24px' }}>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
          {/* Logo */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <div className="panel-framed" style={{
              width: '34px',
              height: '34px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--emerald-subtle)',
              border: '1px solid var(--border-color)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--emerald-primary)'
            }}>
              <Leaf size={18} />
            </div>
            <div>
              <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.1rem', fontWeight: 700, letterSpacing: '-0.01em' }}>GreenRefactor</h1>
            </div>
          </div>

          {/* Right Header Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>

            <button
              onClick={toggleTheme}
              className="btn-secondary"
              title={`Switch to ${theme === 'dark' ? 'Light' : 'Dark'} Mode`}
              style={{ padding: '6px 10px' }}
            >
              {theme === 'dark' ? <Sun size={15} color="var(--amber-primary)" /> : <Moon size={15} color="var(--indigo-primary)" />}
            </button>

            <button
              onClick={() => setActiveTab('profile')}
              className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
              style={{ padding: '6px 10px' }}
            >
              <User size={15} color="var(--emerald-primary)" />
              <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>{user?.name?.split(' ')[0] || 'Profile'}</span>
            </button>

          </div>
        </div>

        {/* Navigation Tabs */}
        <nav style={{ display: 'flex', gap: '8px', alignItems: 'center', flexWrap: 'wrap' }}>
          {tabs.map((t) => {
            const Icon = t.icon;
            const isActive = activeTab === t.id;
            return (
              <button
                key={t.id}
                onClick={() => setActiveTab(t.id)}
                className={`tab-button ${isActive ? 'active' : ''}`}
              >
                <Icon size={15} color={isActive ? 'var(--emerald-primary)' : 'var(--text-dim)'} />
                <span>{t.label}</span>
              </button>
            );
          })}
        </nav>

      </div>
    </header>
  );
}
