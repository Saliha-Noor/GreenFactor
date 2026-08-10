import React, { useState, useEffect } from 'react';
import { Search, Filter, CheckCircle, ExternalLink, Code2, Database, Shield } from 'lucide-react';
import { realBenchmarkRepos } from '../data/reposData';
import { mockPatternCatalog } from '../data/mockData';
import { API_BASE_URL } from '../apiConfig';

export function BenchmarkCatalogTab() {
  const [subTab, setSubTab] = useState('repos'); // 'repos' | 'patterns'
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedLang, setSelectedLang] = useState('all');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [repos, setRepos] = useState(realBenchmarkRepos || []);
  const [patterns, setPatterns] = useState(mockPatternCatalog || []);

  useEffect(() => {
    // Load repositories catalog from FastAPI backend
    fetch(`${API_BASE_URL}/api/repos`)
      .then(res => res.ok ? res.json() : null)
      .then(data => { if (data) setRepos(data); })
      .catch(err => console.warn('Using initial repos state:', err));

    // Load patterns catalog from FastAPI backend
    fetch(`${API_BASE_URL}/api/patterns`)
      .then(res => res.ok ? res.json() : null)
      .then(data => { if (data) setPatterns(data); })
      .catch(err => console.warn('Using initial patterns state:', err));
  }, []);

  const languages = ['all', 'python', 'javascript', 'java', 'csharp', 'c', 'cpp', 'go', 'rust'];
  const categories = ['all', 'Control Flow', 'Memory & Computation', 'Loop Invariants', 'I/O & Networking', 'Language Interop', 'Dependencies', 'Data Structures'];

  const allRepos = repos || [];

  const filteredRepos = allRepos.filter(r => {
    const matchesSearch = (r.name || '').toLowerCase().includes(searchTerm.toLowerCase()) || (r.entrypoint || '').toLowerCase().includes(searchTerm.toLowerCase());
    const matchesLang = selectedLang === 'all' || r.language === selectedLang;
    return matchesSearch && matchesLang;
  });

  const filteredPatterns = (patterns || []).filter(p => {
    return selectedCategory === 'all' || p.category === selectedCategory;
  });

  return (
    <div className="animate-fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '1240px', margin: '0 auto' }}>
      
      {/* Top Consolidated Sub-Navigation Controls */}
      <div className="glass-card" style={{ padding: '16px 24px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        
        {/* Toggle Switch */}
        <div style={{ display: 'flex', gap: '6px', background: 'var(--bg-subtle)', padding: '4px', borderRadius: '8px' }}>
          <button
            onClick={() => setSubTab('repos')}
            className={`tab-button ${subTab === 'repos' ? 'active' : ''}`}
            style={{ padding: '8px 16px', fontSize: '0.85rem' }}
          >
            <Database size={16} color={subTab === 'repos' ? 'var(--emerald-primary)' : 'var(--text-dim)'} />
            <span>120 Repositories Suite</span>
          </button>

          <button
            onClick={() => setSubTab('patterns')}
            className={`tab-button ${subTab === 'patterns' ? 'active' : ''}`}
            style={{ padding: '8px 16px', fontSize: '0.85rem' }}
          >
            <Code2 size={16} color={subTab === 'patterns' ? 'var(--emerald-primary)' : 'var(--text-dim)'} />
            <span>8 Green Energy Patterns</span>
          </button>
        </div>

        {/* Filters for Active View */}
        {subTab === 'repos' ? (
          <div style={{ display: 'flex', gap: '14px', flexWrap: 'wrap', alignItems: 'center' }}>
            <div style={{ position: 'relative', minWidth: '240px' }}>
              <Search size={15} color="var(--text-dim)" style={{ position: 'absolute', left: '12px', top: '50%', transform: 'translateY(-50%)', pointerEvents: 'none' }} />
              <input 
                type="text" 
                placeholder="Search repository or path..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{ width: '100%', paddingLeft: '36px', height: '38px', fontSize: '0.85rem' }}
              />
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Filter size={15} color="var(--text-muted)" />
              <select
                value={selectedLang}
                onChange={(e) => setSelectedLang(e.target.value)}
                style={{ height: '38px', padding: '0 14px', fontSize: '0.85rem', textTransform: 'capitalize' }}
              >
                {languages.map(l => (
                  <option key={l} value={l}>
                    {l === 'all' ? 'All Languages (8)' : l === 'cpp' ? 'C++' : l === 'csharp' ? 'C#' : l}
                  </option>
                ))}
              </select>
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', gap: '8px', overflowX: 'auto' }}>
            {categories.slice(0, 5).map(cat => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`btn-secondary ${selectedCategory === cat ? 'btn-primary' : ''}`}
                style={{ fontSize: '0.8rem', padding: '6px 12px' }}
              >
                {cat === 'all' ? 'All Categories' : cat}
              </button>
            ))}
          </div>
        )}

      </div>

      {/* Main View Area */}
      {subTab === 'repos' ? (
        <div className="glass-card" style={{ overflow: 'hidden' }}>
          <div style={{ overflowX: 'auto' }}>
            <table className="custom-table">
              <thead>
                <tr>
                  <th style={{ paddingLeft: '24px' }}>REPOSITORY NAME</th>
                  <th>LANGUAGE</th>
                  <th>ENTRYPOINT PATH</th>
                  <th>PATTERNS EVALUATED</th>
                  <th>STATUS</th>
                  <th style={{ paddingRight: '24px' }}>GITHUB LINK</th>
                </tr>
              </thead>
              <tbody>
                {filteredRepos.slice(0, 40).map((r, idx) => (
                  <tr key={idx}>
                    <td style={{ fontWeight: 600, paddingLeft: '24px', color: 'var(--text-main)' }}>{r.name}</td>
                    <td>
                      <span className="badge badge-indigo" style={{ textTransform: 'capitalize' }}>
                        {r.language}
                      </span>
                    </td>
                    <td style={{ fontFamily: 'var(--font-code)', fontSize: '0.8rem', color: 'var(--text-muted)', maxWidth: '320px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {r.entrypoint}
                    </td>
                    <td style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                      {r.patterns_checked} AST Patterns
                    </td>
                    <td>
                      {r.excluded ? (
                        <span className="badge badge-amber" title={r.exclusion_reason || 'Formally excluded from measurement'}>
                          <Shield size={13} /> Excluded
                        </span>
                      ) : (
                        <span className="badge badge-emerald">
                          <CheckCircle size={13} /> {r.status}
                        </span>
                      )}
                    </td>
                    <td style={{ paddingRight: '24px' }}>
                      <a
                        href={r.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ color: 'var(--emerald-primary)', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: '5px', fontSize: '0.825rem', fontWeight: 500 }}
                      >
                        GitHub <ExternalLink size={13} />
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {filteredRepos.length > 40 && (
            <div style={{ padding: '14px 24px', textAlign: 'center', background: 'var(--bg-subtle)', fontSize: '0.8rem', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)' }}>
              Showing 40 of {filteredRepos.length} registered benchmark repositories. Filter by language to inspect all 15 repositories per language.
            </div>
          )}
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(480px, 1fr))', gap: '24px' }}>
          {filteredPatterns.map(pattern => (
            <div key={pattern.id} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', gap: '20px' }}>
              
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                  <div>
                    <span className="badge badge-indigo" style={{ marginBottom: '6px' }}>{pattern.category}</span>
                    <h4 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.15rem', fontWeight: 700 }}>{pattern.name}</h4>
                  </div>
                  <span className="badge badge-emerald" style={{ fontSize: '0.75rem' }}>{pattern.complexity}</span>
                </div>

                <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)', lineHeight: 1.6, marginBottom: '18px' }}>
                  {pattern.description}
                </p>

                {/* Code Snippets Side-by-Side with Proper Heights and Scrolling */}
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '14px' }}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--rose-primary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      Baseline Code
                    </span>
                    <pre className="code-block" style={{ minHeight: '110px', maxHeight: '200px', margin: 0 }}>
                      <code>{pattern.before_code}</code>
                    </pre>
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--emerald-primary)', display: 'flex', alignItems: 'center', gap: '4px' }}>
                      Green Refactored Code
                    </span>
                    <pre className="code-block" style={{ minHeight: '110px', maxHeight: '200px', margin: 0 }}>
                      <code>{pattern.after_code}</code>
                    </pre>
                  </div>
                </div>
              </div>

              <div style={{ paddingTop: '14px', borderTop: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.85rem' }}>
                <span>Avg Energy Reduction: <strong style={{ color: 'var(--emerald-primary)', fontFamily: 'var(--font-code)' }}>{pattern.avg_energy_saving}</strong></span>
                <span className="badge badge-emerald">Risk Level: {pattern.risk_level}</span>
              </div>

            </div>
          ))}
        </div>
      )}

    </div>
  );
}
