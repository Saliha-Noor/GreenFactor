import React, { useState } from 'react';
import { Activity, BarChart2, CheckCircle, HelpCircle, FileText } from 'lucide-react';

export function StatsInspectorTab({ summaryData }) {
  const rows = summaryData?.rows || [];
  const [selectedIndex, setSelectedIndex] = useState(rows.length > 0 ? 0 : -1);

  if (!summaryData || rows.length === 0) {
    return (
      <div className="animate-fade-in" style={{ maxWidth: '800px', margin: '40px auto' }}>
        <div className="glass-card" style={{ padding: '48px 32px', textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
          <Activity size={36} color="var(--text-dim)" />
          <div>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 600, marginBottom: '6px' }}>No Statistical Rows Available</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Upload or run a pipeline benchmark to inspect detailed per-pattern statistical analysis (Shapiro-Wilk normality, paired t-test / Wilcoxon, Cohen's d effect size).
            </p>
          </div>
        </div>
      </div>
    );
  }

  const selectedRow = selectedIndex >= 0 && selectedIndex < rows.length ? rows[selectedIndex] : null;
  const isSynthetic = summaryData?.data_source === 'synthetic_placeholder' || summaryData?.no_data;

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      
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

      <div className="glass-card" style={{ padding: '20px 24px' }}>
        <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 700, display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--text-main)' }}>
          <Activity size={22} color="var(--emerald-primary)" />
          Statistical Rigor Inspector
        </h2>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '4px' }}>
          Detailed paired hypothesis testing & effect sizes for real benchmark measurements.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '20px' }}>
        
        {/* Left Column: List of evaluated cases */}
        <div className="glass-card" style={{ padding: '20px', display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '600px', overflowY: 'auto' }}>
          <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-dim)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span>Evaluated Benchmark Cases</span>
            <span className="badge badge-emerald">{rows.length} Total</span>
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {rows.map((row, idx) => {
              const isSelected = idx === selectedIndex;
              const pct = row.percent_change;
              const isSaved = pct < 0;

              return (
                <button
                  key={idx}
                  onClick={() => setSelectedIndex(idx)}
                  className={`btn-secondary ${isSelected ? 'btn-primary' : ''}`}
                  style={{
                    width: '100%',
                    textAlign: 'left',
                    padding: '12px',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'stretch',
                    gap: '4px',
                    border: isSelected ? '1px solid var(--emerald-primary)' : '1px solid var(--border-color)',
                    background: isSelected ? 'var(--emerald-subtle)' : 'var(--bg-card)'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 600, fontSize: '0.85rem', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {row.repo}
                    </span>
                    <span style={{ fontSize: '0.8rem', fontFamily: 'var(--font-code)', fontWeight: 600, color: isSaved ? 'var(--emerald-primary)' : 'var(--text-muted)' }}>
                      {pct ? `${pct.toFixed(1)}%` : '0.0%'}
                    </span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    <span style={{ textTransform: 'capitalize' }}>{row.language}</span>
                    <span className="badge badge-indigo" style={{ fontSize: '0.7rem' }}>{row.pattern}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right Column: Detailed Inspector Card */}
        {selectedRow ? (
          <div className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {/* Header info */}
            <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.75rem' }}>
                  <span className="badge badge-emerald" style={{ textTransform: 'uppercase' }}>
                    {selectedRow.language}
                  </span>
                  <span style={{ color: 'var(--text-dim)' }}>•</span>
                  <span style={{ fontFamily: 'var(--font-code)', color: 'var(--text-muted)' }}>{selectedRow.runtime_category}</span>
                </div>
                <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 700, marginTop: '6px' }}>
                  {selectedRow.repo} — <span className="badge badge-indigo">{selectedRow.pattern}</span>
                </h3>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontFamily: 'var(--font-code)', letterSpacing: '0.04em' }}>ENERGY CHANGE</div>
                <div className="stat-value" style={{ fontSize: '1.5rem', fontWeight: 600, color: selectedRow.percent_change < 0 ? 'var(--emerald-primary)' : 'var(--text-main)', textShadow: selectedRow.percent_change < 0 ? undefined : 'none' }}>
                  {selectedRow.percent_change?.toFixed(2)}%
                </div>
              </div>
            </div>

            {/* Core Stats Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
              <div className="glass-card" style={{ padding: '12px' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Sample Runs (n)</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-code)', marginTop: '4px' }}>{selectedRow.n}</div>
              </div>
              <div className="glass-card" style={{ padding: '12px' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Test Method</div>
                <div style={{ fontSize: '0.85rem', fontWeight: 600, marginTop: '4px' }}>{selectedRow.test_used || 'Paired Test'}</div>
              </div>
              <div className="glass-card" style={{ padding: '12px' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>p-value</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-code)', marginTop: '4px' }}>
                  {selectedRow.p_value != null ? selectedRow.p_value.toFixed(4) : 'N/A'}
                </div>
              </div>
              <div className="glass-card" style={{ padding: '12px' }}>
                <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)' }}>Cohen's d</div>
                <div style={{ fontSize: '1.1rem', fontWeight: 700, fontFamily: 'var(--font-code)', color: 'var(--emerald-primary)', marginTop: '4px' }}>
                  {selectedRow.cohens_d != null ? selectedRow.cohens_d.toFixed(2) : 'N/A'}
                </div>
              </div>
            </div>

            {/* Mean Baseline vs Refactored */}
            <div className="glass-card" style={{ padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <h4 style={{ fontFamily: 'var(--font-heading)', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-dim)', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <BarChart2 size={16} color="var(--emerald-primary)" /> Mean Energy Consumption (Joules)
              </h4>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Baseline Mean</span>
                  <p style={{ fontSize: '1.2rem', fontWeight: 700, fontFamily: 'var(--font-code)', margin: 0 }}>
                    {selectedRow.mean_baseline_j != null ? `${selectedRow.mean_baseline_j.toFixed(4)} J` : 'N/A'}
                  </p>
                </div>
                <div>
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Refactored Mean</span>
                  <p style={{ fontSize: '1.2rem', fontWeight: 700, fontFamily: 'var(--font-code)', color: 'var(--emerald-primary)', margin: 0 }}>
                    {selectedRow.mean_refactored_j != null ? `${selectedRow.mean_refactored_j.toFixed(4)} J` : 'N/A'}
                  </p>
                </div>
              </div>
            </div>

            {/* Statistical Significance Callout */}
            <div style={{
              padding: '16px',
              borderRadius: '8px',
              border: selectedRow.significant ? '1px solid var(--emerald-subtle)' : '1px solid var(--border-color)',
              background: selectedRow.significant ? 'var(--emerald-subtle)' : 'var(--bg-subtle)',
              display: 'flex',
              alignItems: 'flex-start',
              gap: '12px'
            }}>
              <CheckCircle size={20} color="var(--emerald-primary)" style={{ marginTop: '2px', flexShrink: 0 }} />
              <div>
                <h4 style={{ fontFamily: 'var(--font-heading)', fontSize: '0.9rem', fontWeight: 600 }}>
                  {selectedRow.significant ? 'Statistically Significant (p < 0.05)' : 'Not Statistically Significant (p ≥ 0.05)'}
                </h4>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px', margin: 0, lineHeight: 1.4 }}>
                  {selectedRow.significant
                    ? `The measured energy reduction for pattern '${selectedRow.pattern}' on ${selectedRow.repo} is statistically significant under ${selectedRow.test_used || 'paired test'} with an effect size of ${selectedRow.cohens_d?.toFixed(2)}.`
                    : `The difference in energy consumption between baseline and refactored versions did not reach statistical significance.`}
                </p>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
