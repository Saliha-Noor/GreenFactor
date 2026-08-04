import React from 'react';
import { X, HelpCircle, BookOpen, CheckCircle, Zap, Shield, Code, Cpu } from 'lucide-react';

export function HelpDrawer({ isOpen, onClose, activeTab }) {
  if (!isOpen) return null;

  const tabHelpData = {
    overview: {
      title: "Overview Dashboard Details & FAQs",
      subtitle: "Executive Summary of Empirical Benchmark Evaluation",
      description: "The Overview tab aggregates empirical benchmark results across 120 open-source repositories in 8 programming languages. It provides high-level metrics on energy reduction, statistical significance, and Cohen's d effect size.",
      keyMetrics: [
        { label: "Repos Evaluated", desc: "Total open-source benchmark repositories ingested and tested." },
        { label: "Mean Savings (%)", desc: "Mean percentage reduction in Joules (J) consumed after applying green refactoring." },
        { label: "Significant Rate (%)", desc: "Percentage of benchmark tests achieving p < 0.05 statistical significance." },
        { label: "Cohen's d", desc: "Standardized effect size magnitude (0.2=Small, 0.5=Medium, 0.8+=Large)." }
      ],
      faqs: [
        {
          q: "Are the summary numbers real or hardcoded?",
          a: "All numbers are computed dynamically by the backend API. When empirical benchmark measurement runs complete (stored in Backend/results/), the engine parses raw Joules, runs Paired t-tests, and updates these metrics in real-time."
        },
        {
          q: "How is energy consumption measured?",
          a: "Energy is measured in Joules (J) using Intel RAPL (Running Average Power Limit) MSR hardware counters, with a host TDP (Thermal Design Power) fallback mode for systems without RAPL permissions."
        },
        {
          q: "What does 'p < 0.05' significance mean?",
          a: "It indicates a statistically significant difference between baseline and refactored code execution energy, proving the energy reduction is not due to random hardware variance."
        }
      ]
    },

    refactor: {
      title: "Live Refactor Engine Details & FAQs",
      subtitle: "Real-Time AST Pattern Detection & Mechanical Code Optimization",
      description: "The Live Refactor tab allows you to paste source code in 8 programming languages, perform AST-based pattern analysis, and apply verified mechanical green refactoring patterns.",
      keyMetrics: [
        { label: "AST Scan", desc: "Parses code structure in memory to locate green anti-patterns." },
        { label: "Mechanical Transformation", desc: "Modifies AST nodes directly to preserve semantic equivalence." },
        { label: "Supported Languages", desc: "Python, JavaScript, Java, C#, C, C++, Go, Rust." }
      ],
      faqs: [
        {
          q: "Why does pattern detection run so fast?",
          a: "Pattern detection operates using native Abstract Syntax Tree (AST) parsing in Python memory. AST parsing takes milliseconds because it does not require slow network calls or full recompilation."
        },
        {
          q: "Is auto-refactoring safe?",
          a: "Mechanical transformations (e.g., early termination, cache memoization, loop-invariant hoisting) are designed to preserve original business logic while eliminating wasted CPU cycles."
        },
        {
          q: "How do I apply a refactoring?",
          a: "Click 'Run Pattern Analysis', select a detected pattern hit, and click 'Apply Auto-Refactor' to view the unified diff."
        }
      ]
    },

    benchmark: {
      title: "Benchmark Suite & Catalog Details & FAQs",
      subtitle: "120 Standardized Repositories & Green Pattern Definitions",
      description: "Browse the complete suite of 120 open-source benchmark repositories across 8 language drivers and explore the catalog of 8 green refactoring patterns.",
      keyMetrics: [
        { label: "120 Benchmark Repos", desc: "15 curated repositories per language covering algorithms, web frameworks, and data processing." },
        { label: "8 Green Patterns", desc: "Control flow, memory reuse, loop invariants, batching, and native interop patterns." }
      ],
      faqs: [
        {
          q: "Where is the repository list defined?",
          a: "Repository configurations are stored in Backend/config/repos.yaml and loaded dynamically via GET /api/repos."
        },
        {
          q: "What programming languages are supported?",
          a: "8 target languages: Python, JavaScript, Java, C#, C, C++, Go, Rust."
        },
        {
          q: "How are workloads executed?",
          a: "Each repository has a standardized workload driver script (e.g. TheAlgorithms_Python_driver.py) located in Backend/workloads/."
        }
      ]
    },

    stats: {
      title: "Statistical Inspector Details & FAQs",
      subtitle: "Hypothesis Testing & Empirical Significance Matrix",
      description: "Inspect per-repository energy metrics, baseline vs refactored Joules, Paired t-test / Wilcoxon p-values, and Cohen's d effect sizes.",
      keyMetrics: [
        { label: "Sample Size N=30", desc: "Each workload is executed 30 times for baseline and refactored versions." },
        { label: "Statistical Tests", desc: "Paired t-test (for normal distributions) and Wilcoxon signed-rank test (for non-parametric data)." }
      ],
      faqs: [
        {
          q: "How is Cohen's d calculated?",
          a: "Cohen's d = (Mean Baseline - Mean Refactored) / Pooled Standard Deviation. Values > 0.8 represent large effect sizes."
        },
        {
          q: "Can I filter the results by language?",
          a: "Yes, use the language drop-down filter to inspect specific language runtimes."
        }
      ]
    },

    profile: {
      title: "Researcher Profile & Host Settings Details & FAQs",
      subtitle: "Hardware Measurement Configuration & Data Export",
      description: "Configure host machine TDP (Watts), view session credentials, and export research benchmark artifacts as CSV files.",
      keyMetrics: [
        { label: "Host TDP (Watts)", desc: "Thermal Design Power rating used for hardware fallback energy estimations." },
        { label: "CSV Data Export", desc: "Downloads full statistical benchmark matrix for paper publication." }
      ],
      faqs: [
        {
          q: "Why is Host TDP needed?",
          a: "If Intel RAPL counters are restricted by OS security policy, the engine estimates Joules using CPU utilization time multiplied by Host TDP."
        },
        {
          q: "How do I export benchmark data?",
          a: "Click 'Export CSV' in the Profile tab to trigger an instant download from GET /api/export/csv."
        }
      ]
    }
  };

  const currentData = tabHelpData[activeTab] || tabHelpData.overview;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      zIndex: 1000,
      display: 'flex',
      justifyContent: 'flex-end',
      background: 'rgba(0, 0, 0, 0.6)',
      backdropFilter: 'blur(4px)',
      animation: 'fadeIn 0.2s ease-out'
    }} onClick={onClose}>
      
      {/* Side Drawer Panel */}
      <div style={{
        width: '100%',
        maxWidth: '460px',
        height: '100%',
        background: 'var(--bg-card)',
        borderLeft: '1px solid var(--border-color)',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '-8px 0 32px rgba(0,0,0,0.5)',
        animation: 'slideInRight 0.3s ease-out'
      }} onClick={e => e.stopPropagation()}>

        {/* Drawer Header */}
        <div style={{
          padding: '20px 24px',
          borderBottom: '1px solid var(--border-color)',
          display: 'flex',
          justify: 'space-between',
          alignItems: 'center',
          background: 'var(--bg-subtle)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <HelpCircle size={22} color="var(--emerald-primary)" />
            <div>
              <h3 style={{ fontSize: '1.05rem', fontWeight: 700, margin: 0 }}>Help & Info Panel</h3>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', margin: 0 }}>{currentData.subtitle}</p>
            </div>
          </div>
          <button onClick={onClose} style={{
            background: 'transparent',
            border: 'none',
            color: 'var(--text-dim)',
            cursor: 'pointer',
            padding: '4px',
            borderRadius: '6px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }} className="btn-secondary">
            <X size={20} />
          </button>
        </div>

        {/* Drawer Content Body */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '24px', display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Section: Overview */}
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--emerald-primary)', marginBottom: '6px' }}>
              {currentData.title}
            </h4>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
              {currentData.description}
            </p>
          </div>

          {/* Section: Key Metrics Guide */}
          <div style={{
            background: 'var(--bg-dark)',
            border: '1px solid var(--border-color)',
            borderRadius: '10px',
            padding: '16px'
          }}>
            <h5 style={{ fontSize: '0.85rem', fontWeight: 600, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <BookOpen size={16} color="var(--indigo-primary)" /> Component Highlights
            </h5>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              {currentData.keyMetrics.map((item, idx) => (
                <div key={idx} style={{ fontSize: '0.8rem' }}>
                  <span style={{ fontWeight: 600, color: 'var(--text-main)' }}>• {item.label}:</span>{' '}
                  <span style={{ color: 'var(--text-muted)' }}>{item.desc}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Section: FAQs */}
          <div>
            <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <CheckCircle size={16} color="var(--emerald-primary)" /> Frequently Asked Questions
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {currentData.faqs.map((faq, idx) => (
                <div key={idx} style={{
                  background: 'var(--bg-subtle)',
                  border: '1px solid var(--border-color)',
                  borderRadius: '8px',
                  padding: '12px 14px'
                }}>
                  <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '4px' }}>
                    Q: {faq.q}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.4 }}>
                    {faq.a}
                  </div>
                </div>
              ))}
            </div>
          </div>

        </div>

        {/* Drawer Footer */}
        <div style={{
          padding: '16px 24px',
          borderTop: '1px solid var(--border-color)',
          background: 'var(--bg-subtle)',
          fontSize: '0.75rem',
          color: 'var(--text-dim)',
          textAlign: 'center'
        }}>
          GreenRefactor Automated Code Refactoring Engine v2.0
        </div>

      </div>
    </div>
  );
}
