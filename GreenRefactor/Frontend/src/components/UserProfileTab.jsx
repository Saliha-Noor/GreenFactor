import React, { useState } from 'react';
import { User, Shield, Download, Cpu, LogOut, CheckCircle2 } from 'lucide-react';
import { API_BASE_URL } from '../apiConfig';

export function UserProfileTab({ user, token, onLogout }) {
  const [tdpWatts, setTdpWatts] = useState('15');
  const [savedMessage, setSavedMessage] = useState(false);
  const [saveError, setSaveError] = useState('');

  const handleSaveSettings = async (e) => {
    e.preventDefault();
    setSaveError('');
    if (!token) {
      setSaveError('Signed in as an offline guest -- connect to the backend and sign in to save settings.');
      return;
    }
    try {
      const res = await fetch(`${API_BASE_URL}/api/user/settings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          tdp_watts: tdpWatts
        })
      });
      if (!res.ok) {
        throw new Error(res.status === 401 ? 'Session expired -- please sign in again.' : 'Failed to save settings.');
      }
      setSavedMessage(true);
      setTimeout(() => setSavedMessage(false), 2000);
    } catch (err) {
      console.warn('Failed saving settings to backend:', err);
      setSaveError(err.message || 'Failed saving settings to backend.');
    }
  };

  const handleExportCSV = () => {
    window.location.href = `${API_BASE_URL}/api/export/csv`;
  };

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '900px', margin: '0 auto' }}>
      
      {/* Profile Overview Card */}
      <div className="glass-card panel-framed" style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: 'var(--radius-lg)',
            background: 'var(--bg-subtle)',
            border: '1px solid var(--border-color)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--emerald-primary)'
          }}>
            <User size={28} />
          </div>
          <div>
            <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 600, marginBottom: '4px' }}>{user?.name || 'Dr. Alex Vance'}</h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>{user?.email || 'researcher@greenrefactor.org'}</p>
            <div style={{ display: 'flex', gap: '8px', marginTop: '6px' }}>
              <span className="badge badge-emerald">{user?.role || 'Lead Researcher'}</span>
              <span className="badge badge-indigo">{user?.organization || 'Green Compute Initiative'}</span>
            </div>
          </div>
        </div>

        <button onClick={onLogout} className="btn-secondary" style={{ padding: '8px 14px' }}>
          <LogOut size={16} /> Sign Out
        </button>
      </div>

      {/* Researcher Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
        <div className="glass-card" style={{ padding: '18px' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 600, display: 'block', marginBottom: '6px', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>
            BENCHMARKS ANALYZED
          </span>
          <span className="stat-value" style={{ fontSize: '1.5rem', fontWeight: 600, color: 'var(--text-main)', textShadow: 'none' }}>120 Repos</span>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'block', marginTop: '4px' }}>Across 8 Languages</span>
        </div>

        <div className="glass-card" style={{ padding: '18px' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 600, display: 'block', marginBottom: '6px', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>
            TOTAL ENERGY SAVED
          </span>
          <span className="stat-value" style={{ fontSize: '1.5rem', fontWeight: 600 }}>1,482.4 J</span>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'block', marginTop: '4px' }}>-18.4% Mean Reduction</span>
        </div>

        <div className="glass-card" style={{ padding: '18px' }}>
          <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 600, display: 'block', marginBottom: '6px', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>
            STATISTICAL SIGNIFICANCE
          </span>
          <span className="stat-value" style={{ fontSize: '1.5rem', fontWeight: 600, color: 'var(--indigo-primary)', textShadow: 'none' }}>88.2%</span>
          <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', display: 'block', marginTop: '4px' }}>Paired t-test / Wilcoxon (p &lt; 0.05)</span>
        </div>
      </div>

      {/* Settings Form */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1rem', fontWeight: 600, marginBottom: '16px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Shield size={18} color="var(--emerald-primary)" /> Researcher Environment Settings
        </h3>

        <form onSubmit={handleSaveSettings} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-dim)', marginBottom: '6px', fontWeight: 500 }}>
              GROQ API KEY CONFIGURATION (SEMANTIC CODE REVIEW ENGINE)
            </label>
            <div className="code-block" style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Set <code style={{ color: 'var(--emerald-primary)', fontWeight: 600 }}>GROQ_API_KEY</code> environment variable on the host backend machine to enable semantic review agent pattern suggestions.
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.78rem', color: 'var(--text-dim)', marginBottom: '6px', fontWeight: 500 }}>
              ASSUMED HOST CPU TDP (WATTS — FOR TDP ESTIMATION MODE)
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                value={tdpWatts}
                onChange={(e) => setTdpWatts(e.target.value)}
                style={{ width: '100%', paddingLeft: '38px' }}
              />
              <Cpu size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '12px', top: '12px' }} />
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginTop: '8px' }}>
            <button type="submit" className="btn-primary">
              Save Settings
            </button>
            {savedMessage && (
              <span style={{ fontSize: '0.8rem', color: 'var(--emerald-primary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                <CheckCircle2 size={16} /> Saved!
              </span>
            )}
            {saveError && (
              <span style={{ fontSize: '0.8rem', color: 'var(--rose-primary)' }}>
                {saveError}
              </span>
            )}
          </div>
        </form>
      </div>

      {/* Export Section */}
      <div className="glass-card" style={{ padding: '24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: '4px' }}>Export Research Artifacts</h4>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Download full benchmark suite dataset for empirical validation paper.</p>
        </div>
        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="btn-secondary" onClick={handleExportCSV}>
            <Download size={16} /> Export CSV
          </button>
        </div>
      </div>

    </div>
  );
}
