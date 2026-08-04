import React, { useState } from 'react';
import { Leaf, Lock, Mail, User, Building, ArrowRight, CheckCircle2, Cpu, Zap, Activity } from 'lucide-react';
import { API_BASE_URL } from '../apiConfig';

export function LoginScreen({ onLogin }) {
  const [mode, setMode] = useState('signin');
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [institution, setInstitution] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [resetSent, setResetSent] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrorMsg('');

    if (mode === 'forgot') {
      try {
        const res = await fetch(`${API_BASE_URL}/api/auth/reset-password`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email || 'dev@greenrefactor.org' }),
        });
        if (res.ok) {
          setResetSent(true);
        } else {
          setErrorMsg('Failed to process reset request.');
        }
      } catch (err) {
        setErrorMsg('Could not reach the backend server to send a reset link.');
      } finally {
        setLoading(false);
      }
      return;
    }

    const endpoint = mode === 'signup' ? `${API_BASE_URL}/api/auth/signup` : `${API_BASE_URL}/api/auth/login`;
    const bodyPayload = mode === 'signup'
      ? { name: name || 'New Developer', email: email || 'dev@greenrefactor.org', password, institution: institution || 'Green Compute Initiative' }
      : { email: email || 'dev@greenrefactor.org', password };

    let res;
    try {
      res = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bodyPayload),
      });
    } catch (err) {
      // Network error reaching backend API
      console.warn('Backend unreachable:', err);
      setErrorMsg('Could not reach the backend server. Start it, or use "Quick Demo Access" below.');
      setLoading(false);
      return;
    }

    // Handle authentication response status
    if (!res.ok) {
      let detail = 'Authentication failed.';
      try {
        const errBody = await res.json();
        if (errBody?.detail) detail = typeof errBody.detail === 'string' ? errBody.detail : detail;
      } catch {
        // ignore parse failure, keep default message
      }
      setErrorMsg(detail);
      setLoading(false);
      return;
    }

    const data = await res.json();
    if (data.user) {
      onLogin(data.user, data.token);
    } else {
      setErrorMsg('Invalid response from backend server.');
    }
    setLoading(false);
  };

  const handleQuickDemo = async () => {
    setLoading(true);
    setErrorMsg('');
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: 'dev@greenrefactor.org', password: 'greenrefactor-dev' }),
      });
      if (res.ok) {
        const data = await res.json();
        onLogin(data.user, data.token);
        setLoading(false);
        return;
      }
    } catch (err) {
      console.warn('Backend unreachable for demo login:', err);
    }
    // Fallback to guest mode session if offline
    onLogin({
      name: 'Dr. Alex Vance (Offline Guest)',
      email: 'researcher@greenrefactor.org',
      role: 'Lead Researcher',
      organization: 'Green Compute Initiative'
    }, null);
    setLoading(false);
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px 24px',
      background: 'radial-gradient(circle at 15% 10%, var(--emerald-subtle) 0%, transparent 42%), radial-gradient(circle at 85% 90%, var(--indigo-subtle) 0%, transparent 38%), var(--bg-dark)'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '1040px',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))',
        gap: '32px',
        alignItems: 'center'
      }}>

        {/* Left Side: Refactoring Engine Highlights */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px', paddingRight: '12px' }}>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{
              width: '42px',
              height: '42px',
              borderRadius: 'var(--radius-md)',
              background: 'var(--emerald-subtle)',
              border: '1px solid var(--border-color)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--emerald-primary)'
            }}>
              <Leaf size={22} />
            </div>
            <div>
              <span className="badge badge-emerald">AUTOMATED REFACTORING PLATFORM</span>
              <h1 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.4rem', fontWeight: 700, letterSpacing: '-0.02em', marginTop: '4px' }}>
                GreenRefactor Engine
              </h1>
            </div>
          </div>

          <div>
            <h2 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.9rem', fontWeight: 700, lineHeight: 1.15, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
              Measure what your code actually costs to run.
            </h2>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', marginTop: '14px', lineHeight: 1.6 }}>
              An automated refactoring platform that scans software codebases, identifies high-consumption code smells, and applies non-disruptive AST energy refactoring patterns — backed by hardware-measured Joules, not estimates.
            </p>
          </div>

          {/* Key Stat Badges */}
          <div className="panel-framed" style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
            <div className="glass-card" style={{ padding: '14px', textAlign: 'center' }}>
              <Zap size={18} color="var(--emerald-primary)" style={{ margin: '0 auto 6px' }} />
              <div className="stat-value" style={{ fontSize: '1.25rem', fontWeight: 600 }}>120</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '2px' }}>Repositories</div>
            </div>

            <div className="glass-card" style={{ padding: '14px', textAlign: 'center' }}>
              <Cpu size={18} color="var(--indigo-primary)" style={{ margin: '0 auto 6px' }} />
              <div className="stat-value" style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--indigo-primary)', textShadow: 'none' }}>8</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '2px' }}>Languages</div>
            </div>

            <div className="glass-card" style={{ padding: '14px', textAlign: 'center' }}>
              <Activity size={18} color="var(--amber-primary)" style={{ margin: '0 auto 6px' }} />
              <div className="stat-value" style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--amber-primary)', textShadow: 'none' }}>p &lt; 0.05</div>
              <div style={{ fontSize: '0.7rem', color: 'var(--text-dim)', marginTop: '2px' }}>Paired Testing</div>
            </div>
          </div>

          {/* Feature List */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '11px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              <CheckCircle2 size={16} color="var(--emerald-primary)" style={{ flexShrink: 0 }} />
              <span>Multi-agent ingestion, AST pattern scanning &amp; mechanical refactoring</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              <CheckCircle2 size={16} color="var(--emerald-primary)" style={{ flexShrink: 0 }} />
              <span>Hardware RAPL &amp; CPU energy consumption measurement</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              <CheckCircle2 size={16} color="var(--emerald-primary)" style={{ flexShrink: 0 }} />
              <span>Shapiro-Wilk, paired t-test &amp; Cohen's <em>d</em> statistical validation</span>
            </div>
          </div>

        </div>

        {/* Right Side: Form Card */}
        <div className="glass-card panel-framed animate-fade-in" style={{ padding: '8px 36px 36px' }}>
          <div className="scan-bar" style={{ margin: '0 -36px 24px', width: 'calc(100% + 72px)', borderRadius: 0 }} />

          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <h3 style={{ fontFamily: 'var(--font-heading)', fontSize: '1.2rem', fontWeight: 700 }}>
              {mode === 'signin' && 'Sign In to Workspace'}
              {mode === 'signup' && 'Create Researcher Account'}
              {mode === 'forgot' && 'Reset Password'}
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '4px' }}>
              Access the live benchmark &amp; refactoring engine
            </p>
          </div>

          {/* Tab Navigation */}
          {mode !== 'forgot' && (
            <div style={{ display: 'flex', gap: '6px', background: 'var(--bg-subtle)', padding: '4px', borderRadius: 'var(--radius-md)', marginBottom: '20px' }}>
              <button
                type="button"
                onClick={() => setMode('signin')}
                style={{
                  flex: 1,
                  padding: '8px',
                  borderRadius: 'var(--radius-sm)',
                  border: 'none',
                  background: mode === 'signin' ? 'var(--bg-card)' : 'transparent',
                  color: mode === 'signin' ? 'var(--text-main)' : 'var(--text-dim)',
                  fontWeight: 600,
                  fontSize: '0.8rem',
                  cursor: 'pointer'
                }}
              >
                Sign In
              </button>
              <button
                type="button"
                onClick={() => setMode('signup')}
                style={{
                  flex: 1,
                  padding: '8px',
                  borderRadius: 'var(--radius-sm)',
                  border: 'none',
                  background: mode === 'signup' ? 'var(--bg-card)' : 'transparent',
                  color: mode === 'signup' ? 'var(--text-main)' : 'var(--text-dim)',
                  fontWeight: 600,
                  fontSize: '0.8rem',
                  cursor: 'pointer'
                }}
              >
                Sign Up
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>

            {mode === 'signup' && (
              <div>
                <label style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-dim)', marginBottom: '6px', fontWeight: 600, letterSpacing: '0.06em', fontFamily: 'var(--font-code)' }}>
                  FULL NAME
                </label>
                <div style={{ position: 'relative', display: 'flex', alignItems: 'center', width: '100%' }}>
                  <User size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '14px', pointerEvents: 'none', zIndex: 2 }} />
                  <input
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="e.g. Dr. Alex Vance"
                    required
                    style={{ width: '100%', paddingLeft: '40px', paddingRight: '14px', height: '42px' }}
                  />
                </div>
              </div>
            )}

            {mode === 'signup' && (
              <div>
                <label style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-dim)', marginBottom: '6px', fontWeight: 600, letterSpacing: '0.06em', fontFamily: 'var(--font-code)' }}>
                  INSTITUTION / ORGANIZATION
                </label>
                <div style={{ position: 'relative', display: 'flex', alignItems: 'center', width: '100%' }}>
                  <Building size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '14px', pointerEvents: 'none', zIndex: 2 }} />
                  <input
                    type="text"
                    value={institution}
                    onChange={(e) => setInstitution(e.target.value)}
                    placeholder="e.g. Green Compute Initiative"
                    required
                    style={{ width: '100%', paddingLeft: '40px', paddingRight: '14px', height: '42px' }}
                  />
                </div>
              </div>
            )}

            <div>
              <label style={{ display: 'block', fontSize: '0.72rem', color: 'var(--text-dim)', marginBottom: '6px', fontWeight: 600, letterSpacing: '0.06em', fontFamily: 'var(--font-code)' }}>
                EMAIL ADDRESS
              </label>
              <div style={{ position: 'relative', display: 'flex', alignItems: 'center', width: '100%' }}>
                <Mail size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '14px', pointerEvents: 'none', zIndex: 2 }} />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="researcher@institution.org"
                  required
                  style={{ width: '100%', paddingLeft: '40px', paddingRight: '14px', height: '42px' }}
                />
              </div>
            </div>

            {mode !== 'forgot' && (
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <label style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontWeight: 600, letterSpacing: '0.06em', fontFamily: 'var(--font-code)' }}>PASSWORD</label>
                  {mode === 'signin' && (
                    <button
                      type="button"
                      onClick={() => { setMode('forgot'); setErrorMsg(''); }}
                      style={{ background: 'none', border: 'none', color: 'var(--emerald-primary)', fontSize: '0.75rem', cursor: 'pointer', fontWeight: 500 }}
                    >
                      Forgot Password?
                    </button>
                  )}
                </div>
                <div style={{ position: 'relative', display: 'flex', alignItems: 'center', width: '100%' }}>
                  <Lock size={16} color="var(--text-dim)" style={{ position: 'absolute', left: '14px', pointerEvents: 'none', zIndex: 2 }} />
                  <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="••••••••••••"
                    required
                    style={{ width: '100%', paddingLeft: '40px', paddingRight: '14px', height: '42px' }}
                  />
                </div>
              </div>
            )}

            {mode === 'forgot' && resetSent && (
              <div className="badge badge-emerald" style={{ justifyContent: 'center', padding: '10px', fontFamily: 'var(--font-body)' }}>
                Password reset link sent to <strong style={{ marginLeft: '4px' }}>{email || 'your email'}</strong>!
              </div>
            )}

            {errorMsg && (
              <div className="badge badge-rose" style={{ justifyContent: 'center', padding: '10px', fontFamily: 'var(--font-body)', width: '100%' }}>
                {errorMsg}
              </div>
            )}

            <button type="submit" className="btn-primary" disabled={loading} style={{ width: '100%', padding: '11px', marginTop: '4px' }}>
              {mode === 'signin' && 'Sign In to Dashboard'}
              {mode === 'signup' && 'Create Account'}
              {mode === 'forgot' && (resetSent ? 'Resend Reset Link' : 'Send Reset Link')}
              <ArrowRight size={15} />
            </button>
          </form>

          {mode === 'forgot' && (
            <button
              type="button"
              onClick={() => { setMode('signin'); setResetSent(false); }}
              style={{ width: '100%', marginTop: '12px', background: 'none', border: 'none', color: 'var(--text-muted)', fontSize: '0.8rem', cursor: 'pointer' }}
            >
              ← Back to Sign In
            </button>
          )}

          <div style={{ margin: '18px 0', display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ flex: 1, height: '1px', background: 'var(--border-color)' }} />
            <span style={{ fontSize: '0.72rem', color: 'var(--text-dim)', fontFamily: 'var(--font-code)' }}>OR</span>
            <div style={{ flex: 1, height: '1px', background: 'var(--border-color)' }} />
          </div>

          <button
            type="button"
            className="btn-secondary"
            onClick={handleQuickDemo}
            disabled={loading}
            style={{ width: '100%', padding: '10px' }}
          >
            <CheckCircle2 size={15} color="var(--emerald-primary)" />
            Quick Demo Access (Guest Mode)
          </button>

        </div>

      </div>
    </div>
  );
}
