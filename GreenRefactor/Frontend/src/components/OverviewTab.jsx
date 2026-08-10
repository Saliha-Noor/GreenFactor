import React from 'react';
import { Leaf, Zap, Award, CheckCircle2, FileJson } from 'lucide-react';

export function OverviewTab({ summaryData, onLoadSample }) {
  if (!summaryData) {
    return (
      <div className="animate-fade-in" style={{ maxWidth: '800px', margin: '40px auto' }}>
        <div className="glass-card panel-framed" style={{ padding: '48px 32px', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
          <div style={{
            width: '56px',
            height: '56px',
            borderRadius: 'var(--radius-lg)',
            background: 'var(--bg-subtle)',
            border: '1px solid var(--border-color)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: 'var(--text-dim)'
          }}>
            <FileJson size={28} />
          </div>

          <div>
            <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 600, marginBottom: '6px' }}>No Benchmark Results Loaded</h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', maxWidth: '500px', margin: '0 auto', lineHeight: 1.5 }}>
              Click below to load benchmark data from the backend pipeline.
            </p>
          </div>

          <div style={{ display: 'flex', gap: '12px', marginTop: '8px' }}>
            <button className="btn-primary" onClick={onLoadSample}>
              <Zap size={16} /> Load Benchmark Data
            </button>
          </div>
        </div>
      </div>
    );
  }

  const overall = summaryData?.overall_stats || {};
  const rq1 = summaryData?.rq1_language_summary || {};
  const languages = Object.keys(rq1);
  const maxSavings = Math.max(...languages.map(l => rq1[l].mean_savings_percent || 0), 20);
  const isSynthetic = summaryData?.data_source === 'synthetic_placeholder' || summaryData?.no_data;

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '1100px', margin: '0 auto' }}>
      
      {isSynthetic && (
        <div style={{
          background: 'var(--amber-subtle)',
          border: '1px solid var(--amber-primary)',
          color: 'var(--amber-primary)',
          padding: '12px 20px',
          borderRadius: '8px',
          fontSize: '0.88rem',
          fontWeight: 600,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '8px'
        }}>
          <span>⚠️ <strong>No benchmark run yet — showing sample data</strong></span>
        </div>
      )}

      {/* 4 Metric Cards */}
      <div className="panel-framed" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>

        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-dim)', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>REPOS EVALUATED</span>
            <Leaf size={16} color="var(--emerald-primary)" />
          </div>
          <span className="stat-value" style={{ fontSize: '1.6rem', fontWeight: 600, color: 'var(--text-main)', textShadow: 'none' }}>
            {summaryData?.experiment_info?.repos_evaluated || 0}
            {summaryData?.experiment_info?.total_repos_configured && summaryData.experiment_info.total_repos_configured !== summaryData.experiment_info.repos_evaluated ? <span style={{fontSize: '1rem', color: 'var(--text-dim)'}}> / {summaryData.experiment_info.total_repos_configured}</span> : ''}
          </span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginTop: '2px' }}>Tested Repositories</span>
        </div>

        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-dim)', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>MEAN SAVINGS</span>
            <Zap size={16} color="var(--emerald-primary)" />
          </div>
          <span className="stat-value" style={{ fontSize: '1.6rem', fontWeight: 600 }}>
            -{overall.mean_energy_savings_pct || 0}%
          </span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginTop: '2px' }}>Energy Reduction</span>
        </div>

        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-dim)', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>SIGNIFICANT RATE</span>
            <CheckCircle2 size={16} color="var(--indigo-primary)" />
          </div>
          <span className="stat-value" style={{ fontSize: '1.6rem', fontWeight: 600, color: 'var(--indigo-primary)', textShadow: 'none' }}>{overall.significant_refactor_rate_pct || 0}%</span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginTop: '2px' }}>p &lt; 0.05 Significance</span>
        </div>

        <div className="glass-card" style={{ padding: '20px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <span style={{ fontSize: '0.72rem', fontWeight: 600, color: 'var(--text-dim)', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>AVG COHEN'S D</span>
            <Award size={16} color="var(--amber-primary)" />
          </div>
          <span className="stat-value" style={{ fontSize: '1.6rem', fontWeight: 600, color: 'var(--amber-primary)', textShadow: 'none' }}>{overall.avg_effect_size_cohens_d || 0}</span>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', display: 'block', marginTop: '2px' }}>Effect Size</span>
        </div>

      </div>

      {/* Language Breakdown Chart */}
      <div className="glass-card" style={{ padding: '24px' }}>
        <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '0.95rem', fontWeight: 600, marginBottom: '16px' }}>Mean Energy Reduction by Language</h3>
        
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {languages.map((lang) => {
            const data = rq1[lang];
            const pct = data.mean_savings_percent || 0;
            const barWidth = `${(pct / maxSavings) * 100}%`;

            return (
              <div key={lang} style={{ display: 'grid', gridTemplateColumns: '90px 1fr 60px', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '0.85rem', textTransform: 'capitalize', fontWeight: 500 }}>{lang}</span>
                <div style={{ height: '20px', background: 'var(--bg-subtle)', borderRadius: '4px', overflow: 'hidden', padding: '0 2px', display: 'flex', alignItems: 'center' }}>
                  <div style={{
                    height: '14px',
                    width: barWidth,
                    background: 'var(--emerald-primary)',
                    borderRadius: '3px',
                    transition: 'width 0.3s ease'
                  }} />
                </div>
                <span className="stat-value" style={{ fontSize: '0.85rem', fontWeight: 600, textAlign: 'right' }}>
                  -{pct.toFixed(1)}%
                </span>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
