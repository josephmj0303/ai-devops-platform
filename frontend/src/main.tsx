import React from 'react';
import ReactDOM from 'react-dom/client';
import { Bell, ChevronRight, Github, LayoutDashboard, Lock, Menu, Search, Settings, ShieldCheck, User, X } from 'lucide-react';
import './styles.css';

type Page = 'login' | 'dashboard' | 'settings';

const navigationItems = [
  { id: 'dashboard' as const, label: 'Dashboard', icon: LayoutDashboard },
  { id: 'settings' as const, label: 'Settings', icon: Settings },
];

const kpis = [
  { label: 'Deployments', value: '128', trend: '+12%', tone: 'green' },
  { label: 'Open incidents', value: '4', trend: '-3 today', tone: 'amber' },
  { label: 'Pipeline health', value: '98.4%', trend: '+1.8%', tone: 'blue' },
  { label: 'Mean recovery', value: '14m', trend: '-6m', tone: 'purple' },
];

const activities = [
  ['Kubernetes rollout completed', 'prod-cluster', '2 min ago', 'success'],
  ['Terraform plan awaiting review', 'networking', '18 min ago', 'warning'],
  ['CI cache warmed', 'frontend', '42 min ago', 'success'],
  ['Security scan queued', 'payments-api', '1 hr ago', 'neutral'],
];

function App() {
  const [page, setPage] = React.useState<Page>('login');
  const [menuOpen, setMenuOpen] = React.useState(false);

  if (page === 'login') {
    return <LoginPage onLogin={() => setPage('dashboard')} />;
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${menuOpen ? 'open' : ''}`}>
        <div className="brand"><span className="brand-mark">AD</span><div><strong>AI DevOps</strong><small>Platform Console</small></div></div>
        <nav aria-label="Main navigation">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            return <button key={item.id} className={page === item.id ? 'active' : ''} onClick={() => { setPage(item.id); setMenuOpen(false); }}><Icon size={18} />{item.label}</button>;
          })}
        </nav>
        <div className="sidebar-card"><ShieldCheck size={18} /><span>No AI integrations enabled yet.</span></div>
      </aside>
      <div className="content-frame">
        <header className="topbar">
          <button className="icon-button mobile-only" onClick={() => setMenuOpen(true)} aria-label="Open navigation"><Menu /></button>
          <div className="search"><Search size={18} /><input placeholder="Search services, deploys, settings..." /></div>
          <button className="icon-button" aria-label="Notifications"><Bell /></button>
          <div className="avatar"><User size={18} /> Platform Admin</div>
        </header>
        <main>{page === 'dashboard' ? <Dashboard /> : <SettingsPage />}</main>
      </div>
      {menuOpen && <button className="backdrop" onClick={() => setMenuOpen(false)} aria-label="Close navigation"><X /></button>}
    </div>
  );
}

function LoginPage({ onLogin }: { onLogin: () => void }) {
  return <main className="login-page"><section className="hero"><span className="eyebrow">Enterprise DevOps Console</span><h1>Operate your delivery platform from one secure frontend.</h1><p>Monitor deployments, review incidents, and manage workspace settings. AI capabilities can be added later without changing the user journey.</p><div className="trust"><span>JWT-ready</span><span>RBAC-ready</span><span>Audit-friendly</span></div></section><section className="login-card"><div className="card-header"><Lock /><div><h2>Welcome back</h2><p>Sign in to continue to the dashboard.</p></div></div><label>Email<input type="email" placeholder="admin@example.com" /></label><label>Password<input type="password" placeholder="••••••••" /></label><div className="form-row"><label className="checkbox"><input type="checkbox" /> Remember device</label><a href="#">Forgot password?</a></div><button className="primary" onClick={onLogin}>Sign in <ChevronRight size={18} /></button><button className="secondary"><Github size={18} /> Continue with GitHub</button><p className="security-note">Demo-only frontend: no AI integration or live authentication is wired yet.</p></section></main>;
}

function Dashboard() {
  return <div className="page"><div className="page-header"><div><span className="eyebrow">Dashboard</span><h1>Delivery operations overview</h1><p>Responsive control center for deployments, incidents, and platform health.</p></div><button className="primary">Create deployment</button></div><section className="kpi-grid">{kpis.map((kpi) => <article className="card kpi" key={kpi.label}><span>{kpi.label}</span><strong>{kpi.value}</strong><small className={kpi.tone}>{kpi.trend}</small></article>)}</section><section className="dashboard-grid"><article className="card wide"><h2>Recent activity</h2>{activities.map(([title, target, time, status]) => <div className="activity" key={title}><span className={`dot ${status}`} /><div><strong>{title}</strong><small>{target}</small></div><time>{time}</time></div>)}</article><article className="card"><h2>Platform health</h2>{['API gateway', 'Workers', 'PostgreSQL', 'Redis'].map((item) => <div className="health" key={item}><span>{item}</span><strong>Healthy</strong></div>)}</article><article className="card"><h2>Quick actions</h2><button className="action">Review pull requests</button><button className="action">Open runbooks</button><button className="action">Invite teammate</button></article></section></div>;
}

function SettingsPage() {
  return <div className="page"><div className="page-header"><div><span className="eyebrow">Settings</span><h1>Workspace settings</h1><p>Manage profile, security, integrations, and interface preferences.</p></div></div><section className="settings-grid"><article className="card"><h2>Profile</h2><label>Display name<input defaultValue="Platform Admin" /></label><label>Role<input defaultValue="DevOps Lead" /></label></article><article className="card"><h2>Security</h2><div className="toggle"><span>Multi-factor authentication</span><input type="checkbox" defaultChecked /></div><div className="toggle"><span>Session audit logging</span><input type="checkbox" defaultChecked /></div></article><article className="card"><h2>Preferences</h2><label>Theme<select defaultValue="dark"><option value="dark">Dark</option><option value="light">Light</option></select></label><label>Density<select defaultValue="comfortable"><option>comfortable</option><option>compact</option></select></label></article><article className="card"><h2>Integrations</h2><p className="muted">GitHub, Kubernetes, Terraform, observability, and AI providers are placeholders only.</p><button className="secondary">Configure later</button></article></section></div>;
}

ReactDOM.createRoot(document.getElementById('root')!).render(<App />);
