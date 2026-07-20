"""Generate the complete ChurnGuard AI frontend with Landing, Login and Dashboard."""

PART1 = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>ChurnGuard AI - Customer Churn Prediction Platform</title>
<meta name="description" content="AI-powered customer churn prediction platform. Predict, analyze and retain customers with machine learning."/>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://unpkg.com/react@18/umd/react.development.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Inter",sans-serif;overflow-x:hidden}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-thumb{background:#334155;border-radius:4px}

/* ── Landing ── */
.land-bg{background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 40%,#0c1445 70%,#0f172a 100%);min-height:100vh}
.orb{position:absolute;border-radius:50%;filter:blur(80px);opacity:.35;pointer-events:none;animation:orb-float 8s ease-in-out infinite alternate}
.orb1{width:500px;height:500px;background:radial-gradient(circle,#6366f1,#4338ca);top:-100px;right:-100px}
.orb2{width:400px;height:400px;background:radial-gradient(circle,#06b6d4,#0e7490);bottom:100px;left:-80px;animation-delay:-4s}
.orb3{width:300px;height:300px;background:radial-gradient(circle,#8b5cf6,#6d28d9);top:40%;left:40%;animation-delay:-2s}
@keyframes orb-float{from{transform:translateY(0) scale(1)}to{transform:translateY(-40px) scale(1.08)}}
.glass{background:rgba(255,255,255,0.06);backdrop-filter:blur(16px);border:1px solid rgba(255,255,255,0.12);border-radius:16px}
.glass-card{background:rgba(255,255,255,0.05);backdrop-filter:blur(12px);border:1px solid rgba(255,255,255,0.10);border-radius:16px;transition:all .25s}
.glass-card:hover{background:rgba(255,255,255,0.09);border-color:rgba(99,102,241,0.4);transform:translateY(-4px);box-shadow:0 20px 40px rgba(0,0,0,0.3)}
.hero-grad{background:linear-gradient(90deg,#ffffff,#a5b4fc,#38bdf8,#a5b4fc,#ffffff);background-size:300% auto;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:grad-anim 5s linear infinite}
@keyframes grad-anim{to{background-position:300% center}}
.glow-btn{background:linear-gradient(135deg,#6366f1,#4f46e5);box-shadow:0 0 20px rgba(99,102,241,.45),0 4px 15px rgba(0,0,0,.3);transition:all .2s}
.glow-btn:hover{transform:translateY(-2px);box-shadow:0 0 32px rgba(99,102,241,.65),0 8px 24px rgba(0,0,0,.4)}
.outline-btn{border:1.5px solid rgba(255,255,255,0.25);color:#e2e8f0;transition:all .2s}
.outline-btn:hover{border-color:rgba(99,102,241,.6);background:rgba(99,102,241,.15);transform:translateY(-2px)}
.stat-num{font-size:2.5rem;font-weight:800;background:linear-gradient(135deg,#fff,#a5b4fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
.fu{animation:fadeUp .5s ease both}
@keyframes sp{to{transform:rotate(360deg)}}
.spin{animation:sp .9s linear infinite}
.fu1{animation:fadeUp .5s .05s ease both}
.fu2{animation:fadeUp .5s .1s ease both}
.fu3{animation:fadeUp .5s .15s ease both}
.fu4{animation:fadeUp .5s .2s ease both}
.fu5{animation:fadeUp .5s .25s ease both}
.fu6{animation:fadeUp .5s .3s ease both}

/* ── Login ── */
.login-bg{background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 50%,#0c1445 100%);min-height:100vh;display:flex;align-items:center;justify-content:center}
.login-card{background:rgba(255,255,255,0.97);border-radius:24px;padding:48px;width:100%;max-width:420px;box-shadow:0 30px 80px rgba(0,0,0,0.5)}
.lfi{width:100%;padding:11px 14px;border:1.5px solid #e2e8f0;border-radius:10px;font-size:14px;color:#1e293b;outline:none;transition:all .18s;font-family:inherit;background:#f8fafc}
.lfi:focus{border-color:#6366f1;background:#fff;box-shadow:0 0 0 3px rgba(99,102,241,0.12)}
.lfl{font-size:12px;font-weight:600;color:#475569;margin-bottom:6px;display:block;text-transform:uppercase;letter-spacing:.5px}
.lerr{background:#fef2f2;border:1px solid #fecaca;border-radius:10px;padding:10px 14px;font-size:13px;color:#dc2626;display:flex;align-items:center;gap:8px}

/* ── Dashboard ── */
body.dash-mode{background:#f1f5f9;color:#1e293b}
.sl{display:flex;align-items:center;gap:10px;padding:10px 16px;border-radius:10px;font-size:14px;font-weight:500;color:#64748b;cursor:pointer;transition:all .18s;white-space:nowrap;background:none;border:none;width:100%;text-align:left}
.sl:hover{background:#eff6ff;color:#2563eb}
.sl.active{background:#eff6ff;color:#2563eb;font-weight:600}
.badge{display:inline-flex;align-items:center;padding:2px 10px;border-radius:999px;font-size:11px;font-weight:600;letter-spacing:.2px}
.fi{width:100%;padding:9px 12px;border:1.5px solid #e2e8f0;border-radius:9px;font-size:14px;color:#1e293b;background:#fff;outline:none;transition:border-color .18s}
.fi:focus{border-color:#3b82f6;box-shadow:0 0 0 3px rgba(59,130,246,0.12)}
.fl{font-size:11px;font-weight:600;color:#64748b;margin-bottom:5px;display:block;text-transform:uppercase;letter-spacing:.5px}
.pb{height:6px;background:#e2e8f0;border-radius:999px;overflow:hidden}
.pf{height:100%;border-radius:999px;transition:width 1s cubic-bezier(.4,0,.2,1)}
.card{background:#fff;border-radius:16px;box-shadow:0 1px 3px rgba(0,0,0,0.07),0 4px 16px rgba(0,0,0,0.05)}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const {useState, useEffect, useRef, useCallback} = React;

/* ── API ─── */
const BASE = "";
const apiGet  = p => fetch(BASE+p).then(r=>r.json());
const apiPost = (p,b) => fetch(BASE+p,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(b)}).then(r=>r.json());

/* ── SVG Icons ─── */
const P = {
  dashboard:"M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6",
  analytics:"M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z",
  customers:"M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z",
  predict:"M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z",
  history:"M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z",
  bell:"M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9",
  search:"M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z",
  cr:"M9 5l7 7-7 7", cd:"M19 9l-7 7-7-7",
  up:"M5 10l7-7m0 0l7 7m-7-7v18", down:"M19 14l-7 7m0 0l-7-7m7 7V3",
  users:"M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z",
  money:"M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
  shield:"M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z",
  warning:"M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z",
  check:"M5 13l4 4L19 7", x:"M6 18L18 6M6 6l12 12",
  logout:"M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1",
  eye:"M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z",
  eyeoff:"M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21",
  trend:"M13 7h8m0 0v8m0-8l-8 8-4-4-6 6",
  spark:"M13 10V3L4 14h7v7l9-11h-7z",
  chart2:"M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z",
  globe:"M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z",
  lock:"M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z",
  mail:"M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z",
  arrow:"M14 5l7 7m0 0l-7 7m7-7H3",
};
const Ic = ({n,cls="w-5 h-5"}) => (
  <svg className={cls} fill="none" stroke="currentColor" strokeWidth="1.8" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" d={P[n]}/>
  </svg>
);

/* ── Badge ── */
const BS={High:"bg-red-50 text-red-600",Medium:"bg-amber-50 text-amber-600",Low:"bg-emerald-50 text-emerald-600",Bronze:"bg-orange-50 text-orange-600",Silver:"bg-slate-100 text-slate-600",Gold:"bg-yellow-50 text-yellow-700"};
const Badge=({text})=><span className={`badge ${BS[text]||"bg-blue-50 text-blue-600"}`}>{text}</span>;

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   LANDING PAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
const FEATURES = [
  {icon:"spark",  title:"AI Predictions",   desc:"Random Forest + XGBoost ensemble delivers 91.4% accuracy on churn predictions in real time.",       color:"from-indigo-500 to-purple-600"},
  {icon:"chart2", title:"Live Analytics",   desc:"Interactive charts, risk distribution donut, feature importance bars — all updating automatically.",color:"from-cyan-500 to-blue-600"},
  {icon:"users",  title:"Customer Intel",   desc:"Searchable customer table with risk filters, tenure tracking and monthly charge analytics.",         color:"from-emerald-500 to-teal-600"},
  {icon:"globe",  title:"REST API",         desc:"Full Flask REST API with CORS. Connect to any BI tool, CRM or custom application via JSON endpoints.",color:"from-orange-500 to-red-500"},
  {icon:"shield", title:"Risk Segmentation",desc:"Automatic High / Medium / Low risk classification with color-coded badges and progress indicators.",  color:"from-violet-500 to-indigo-600"},
  {icon:"history","title":"Full Audit Trail",desc:"Every prediction logged with timestamp, confidence score, customer tier and churn probability bar.",    color:"from-pink-500 to-rose-600"},
];
const STATS = [
  {num:"91.4%",  label:"Model Accuracy"},
  {num:"12,847", label:"Customers Analyzed"},
  {num:"<50ms",  label:"Prediction Speed"},
  {num:"6",      label:"ML Features"},
];

const LandingPage = ({onLogin}) => {
  const [scrolled, setScrolled] = useState(false);
  useEffect(()=>{
    const h=()=>setScrolled(window.scrollY>20);
    window.addEventListener("scroll",h);
    return()=>window.removeEventListener("scroll",h);
  },[]);

  return (
    <div className="land-bg relative overflow-hidden">
      {/* Background orbs */}
      <div className="orb orb1"/>
      <div className="orb orb2"/>
      <div className="orb orb3"/>

      {/* ── Navbar ── */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled?"glass":"bg-transparent"}`}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-700 flex items-center justify-center">
              <Ic n="shield" cls="w-5 h-5 text-white"/>
            </div>
            <span className="font-bold text-white text-lg tracking-tight">ChurnGuard <span className="text-indigo-400">AI</span></span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            {["Features","Analytics","API","Pricing"].map(l=>(
              <a key={l} href="#" className="text-slate-300 hover:text-white text-sm font-medium transition-colors">{l}</a>
            ))}
          </div>
          <div className="flex items-center gap-3">
            <button onClick={onLogin} className="outline-btn px-5 py-2 rounded-xl text-sm font-semibold">Sign In</button>
            <button onClick={onLogin} className="glow-btn text-white px-5 py-2 rounded-xl text-sm font-semibold">Get Started</button>
          </div>
        </div>
      </nav>

      {/* ── Hero ── */}
      <section className="relative min-h-screen flex items-center justify-center px-6 pt-24 pb-16">
        <div className="max-w-5xl mx-auto text-center">
          <div className="fu inline-flex items-center gap-2 glass px-4 py-2 rounded-full text-xs font-semibold text-indigo-300 mb-8">
            <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-pulse"></span>
            Powered by Random Forest + XGBoost Ensemble
          </div>
          <h1 className="fu1 text-5xl md:text-7xl font-black text-white leading-tight mb-6">
            Predict Customer<br/>
            <span className="hero-grad">Churn with AI</span>
          </h1>
          <p className="fu2 text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
            Stop losing customers before it happens. ChurnGuard AI analyzes behavioral patterns and predicts who's at risk — so you can act before they leave.
          </p>
          <div className="fu3 flex flex-col sm:flex-row items-center justify-center gap-4">
            <button onClick={onLogin}
              className="glow-btn text-white px-8 py-4 rounded-2xl text-base font-bold flex items-center gap-3 w-full sm:w-auto justify-center">
              Launch Dashboard <Ic n="arrow" cls="w-5 h-5"/>
            </button>
            <button className="outline-btn px-8 py-4 rounded-2xl text-base font-semibold w-full sm:w-auto">
              View Demo
            </button>
          </div>
          {/* Mini preview card */}
          <div className="fu4 mt-16 glass rounded-2xl p-1 max-w-3xl mx-auto">
            <div className="bg-slate-900/60 rounded-xl p-4">
              <div className="flex items-center gap-2 mb-4">
                <div className="w-3 h-3 rounded-full bg-red-500"></div>
                <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                <div className="w-3 h-3 rounded-full bg-green-500"></div>
                <span className="ml-2 text-xs text-slate-500 font-mono">http://127.0.0.1:8080/</span>
              </div>
              <div className="grid grid-cols-4 gap-3 mb-4">
                {[["12,847","Customers","bg-blue-600"],["24.5%","Churn Rate","bg-red-500"],["9,699","Retained","bg-emerald-500"],["$68.40","Avg Revenue","bg-amber-500"]].map(([v,l,c])=>(
                  <div key={l} className="glass-card p-3 text-left">
                    <div className={`w-6 h-6 rounded-lg ${c} mb-2 flex items-center justify-center`}>
                      <div className="w-2 h-2 bg-white rounded-sm opacity-80"/>
                    </div>
                    <p className="text-xs text-slate-400 mb-0.5">{l}</p>
                    <p className="text-sm font-bold text-white">{v}</p>
                  </div>
                ))}
              </div>
              <div className="h-2 bg-slate-700 rounded-full overflow-hidden">
                <div className="h-full bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-full" style={{width:"65%"}}/>
              </div>
              <p className="text-right text-xs text-slate-500 mt-1">Churn Risk: 65%</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── Stats ── */}
      <section className="relative py-16 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="glass rounded-3xl p-8">
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
              {STATS.map((s,i)=>(
                <div key={i}>
                  <div className="stat-num mb-2">{s.num}</div>
                  <p className="text-slate-400 text-sm font-medium">{s.label}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Features ── */}
      <section className="relative py-20 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-14">
            <p className="text-indigo-400 text-sm font-semibold uppercase tracking-widest mb-3">Everything you need</p>
            <h2 className="text-4xl font-black text-white mb-4">Built for Customer Success Teams</h2>
            <p className="text-slate-400 max-w-xl mx-auto">A complete platform to identify at-risk customers, understand churn drivers and take action before it's too late.</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {FEATURES.map((f,i)=>(
              <div key={i} className="glass-card p-6">
                <div className={`w-12 h-12 rounded-2xl bg-gradient-to-br ${f.color} flex items-center justify-center mb-4`}>
                  <Ic n={f.icon} cls="w-6 h-6 text-white"/>
                </div>
                <h3 className="text-white font-bold text-lg mb-2">{f.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="relative py-20 px-6">
        <div className="max-w-3xl mx-auto text-center">
          <div className="glass rounded-3xl p-12">
            <h2 className="text-4xl font-black text-white mb-4">Ready to stop churn?</h2>
            <p className="text-slate-400 mb-8">Sign in and run your first AI prediction in under 60 seconds.</p>
            <button onClick={onLogin}
              className="glow-btn text-white px-10 py-4 rounded-2xl text-base font-bold inline-flex items-center gap-3">
              Start Predicting Now <Ic n="arrow" cls="w-5 h-5"/>
            </button>
          </div>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="relative border-t border-white/10 py-8 px-6 text-center">
        <div className="flex items-center justify-center gap-2 mb-3">
          <div className="w-6 h-6 rounded-lg bg-gradient-to-br from-indigo-500 to-indigo-700 flex items-center justify-center">
            <Ic n="shield" cls="w-3.5 h-3.5 text-white"/>
          </div>
          <span className="text-white font-bold text-sm">ChurnGuard AI</span>
        </div>
        <p className="text-slate-500 text-xs">Built with Random Forest + XGBoost · Flask · React · Tailwind CSS</p>
      </footer>
    </div>
  );
};

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   LOGIN PAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
const DEMO_USERS = [
  {email:"admin@churnguard.ai", password:"admin123",  name:"Admin",   role:"Administrator"},
  {email:"analyst@churnguard.ai",password:"analyst123",name:"Analyst", role:"Data Analyst"},
  {email:"demo@churnguard.ai",  password:"demo123",   name:"Demo",    role:"Read Only"},
];

const LoginPage = ({onLogin, onBack}) => {
  const [email,    setEmail]    = useState("");
  const [password, setPassword] = useState("");
  const [showPw,   setShowPw]   = useState(false);
  const [remember, setRemember] = useState(false);
  const [loading,  setLoading]  = useState(false);
  const [err,      setErr]      = useState("");

  const submit = async (e) => {
    e.preventDefault();
    setErr(""); setLoading(true);
    await new Promise(r=>setTimeout(r,900)); // simulate auth delay
    const user = DEMO_USERS.find(u=>u.email===email.trim().toLowerCase() && u.password===password);
    if (user) {
      if(remember) localStorage.setItem("cg_user", JSON.stringify(user));
      onLogin(user);
    } else {
      setErr("Invalid email or password. Try a demo account below.");
    }
    setLoading(false);
  };

  const fillDemo = (u) => { setEmail(u.email); setPassword(u.password); setErr(""); };

  return (
    <div className="login-bg relative overflow-hidden">
      <div className="orb orb1" style={{opacity:.25}}/>
      <div className="orb orb2" style={{opacity:.2}}/>
      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-4 py-12">

        {/* Back button */}
        <button onClick={onBack} className="absolute top-6 left-6 flex items-center gap-2 text-slate-400 hover:text-white transition-colors text-sm font-medium">
          <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7"/>
          </svg>
          Back to Home
        </button>

        <div className="login-card fu">
          {/* Logo */}
          <div className="flex items-center justify-center gap-2.5 mb-8">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-700 flex items-center justify-center shadow-lg">
              <Ic n="shield" cls="w-5 h-5 text-white"/>
            </div>
            <div>
              <p className="font-black text-slate-800 text-lg leading-none">ChurnGuard</p>
              <p className="text-indigo-600 font-bold text-sm leading-none">AI Platform</p>
            </div>
          </div>

          <h2 className="text-2xl font-black text-slate-800 mb-1 text-center">Welcome back</h2>
          <p className="text-slate-500 text-sm text-center mb-7">Sign in to your dashboard</p>

          {err && (
            <div className="lerr mb-4">
              <Ic n="warning" cls="w-4 h-4 flex-shrink-0"/>
              {err}
            </div>
          )}

          <form onSubmit={submit} className="space-y-4">
            <div>
              <label className="lfl">Email Address</label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                  <Ic n="mail" cls="w-4 h-4"/>
                </span>
                <input type="email" className="lfi pl-10" placeholder="admin@churnguard.ai"
                  value={email} onChange={e=>{setEmail(e.target.value);setErr("")}} required/>
              </div>
            </div>
            <div>
              <label className="lfl">Password</label>
              <div className="relative">
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                  <Ic n="lock" cls="w-4 h-4"/>
                </span>
                <input type={showPw?"text":"password"} className="lfi pl-10 pr-10"
                  placeholder="Enter your password"
                  value={password} onChange={e=>{setPassword(e.target.value);setErr("")}} required/>
                <button type="button" onClick={()=>setShowPw(!showPw)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600">
                  <Ic n={showPw?"eyeoff":"eye"} cls="w-4 h-4"/>
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 rounded accent-indigo-600"
                  checked={remember} onChange={e=>setRemember(e.target.checked)}/>
                <span className="text-sm text-slate-600">Remember me</span>
              </label>
              <a href="#" className="text-sm text-indigo-600 font-semibold hover:text-indigo-700">Forgot password?</a>
            </div>

            <button type="submit" disabled={loading}
              className="w-full py-3 rounded-xl text-white font-bold text-sm flex items-center justify-center gap-2 transition-all"
              style={{background:"linear-gradient(135deg,#6366f1,#4f46e5)",boxShadow:"0 4px 20px rgba(99,102,241,0.4)"}}>
              {loading
                ? <><span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full spin"/>Signing in...</>
                : <><Ic n="shield" cls="w-4 h-4"/>Sign In to Dashboard</>}
            </button>
          </form>

          {/* Demo accounts */}
          <div className="mt-6 pt-6 border-t border-slate-100">
            <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide text-center mb-3">Demo Accounts — Click to fill</p>
            <div className="space-y-2">
              {DEMO_USERS.map((u,i)=>(
                <button key={i} onClick={()=>fillDemo(u)}
                  className="w-full flex items-center justify-between px-3 py-2.5 rounded-xl bg-slate-50 hover:bg-indigo-50 border border-slate-100 hover:border-indigo-200 transition-all text-left">
                  <div className="flex items-center gap-3">
                    <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-400 to-indigo-600 flex items-center justify-center text-white text-xs font-bold">
                      {u.name[0]}
                    </div>
                    <div>
                      <p className="text-xs font-semibold text-slate-700">{u.email}</p>
                      <p className="text-xs text-slate-400">{u.role}</p>
                    </div>
                  </div>
                  <span className="text-xs font-mono text-slate-400 bg-slate-100 px-2 py-0.5 rounded">{u.password}</span>
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
"""

PART2 = """
/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   DASHBOARD COMPONENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
const KPI=({label,val,sub,up,icon,bg,delay=0})=>(
  <div className="card fu p-5 flex flex-col gap-3 hover:shadow-lg transition-shadow" style={{animationDelay:`${delay}ms`}}>
    <div className="flex items-center justify-between">
      <span className="text-xs font-semibold text-slate-400 uppercase tracking-wide">{label}</span>
      <span className={`w-9 h-9 rounded-xl flex items-center justify-center ${bg}`}><Ic n={icon} cls="w-5 h-5 text-white"/></span>
    </div>
    <div className="flex items-end gap-2">
      <span className="text-2xl font-bold text-slate-800 leading-none">{val}</span>
      {sub&&<span className={`flex items-center gap-0.5 text-xs font-semibold mb-0.5 ${up?"text-emerald-500":"text-red-500"}`}><Ic n={up?"up":"down"} cls="w-3 h-3"/>{sub}</span>}
    </div>
  </div>
);

const useChart=(id,mkCfg,deps)=>{
  const ref=useRef(null);
  useEffect(()=>{
    const el=document.getElementById(id);
    if(!el)return;
    if(ref.current)ref.current.destroy();
    ref.current=new Chart(el,mkCfg());
    return()=>{try{ref.current.destroy();}catch(e){}};
  },deps);
};
const LineChart=({id,labels,data,color="#3b82f6"})=>{
  useChart(id,()=>({type:"line",data:{labels,datasets:[{data,borderColor:color,backgroundColor:color+"15",fill:true,tension:0.45,borderWidth:2.5,pointRadius:4,pointHoverRadius:6,pointBackgroundColor:color}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false},tooltip:{backgroundColor:"#1e293b",cornerRadius:8,padding:10}},scales:{x:{grid:{display:false},ticks:{font:{size:10},color:"#94a3b8"}},y:{grid:{color:"rgba(0,0,0,0.04)"},ticks:{font:{size:10},color:"#94a3b8"},beginAtZero:true}}}}),[id,JSON.stringify(data),color]);
  return <div style={{height:180}}><canvas id={id}/></div>;
};
const DonutChart=({id="dc",high=30,med=45,low=25})=>{
  useChart(id,()=>({type:"doughnut",data:{labels:["High Risk","Medium Risk","Low Risk"],datasets:[{data:[high,med,low],backgroundColor:["#ef4444","#f59e0b","#10b981"],borderWidth:0,hoverOffset:6}]},options:{responsive:true,maintainAspectRatio:false,cutout:"70%",plugins:{legend:{position:"bottom",labels:{font:{size:11},color:"#64748b",padding:12,boxWidth:10,usePointStyle:true,pointStyle:"circle"}},tooltip:{backgroundColor:"#1e293b",cornerRadius:8,padding:10}}}}),[id,high,med,low]);
  return <div style={{height:200}}><canvas id={id}/></div>;
};
const HBarChart=({id="bc",featureImp})=>{
  const defL=["Age","Tenure","Purch.Freq","Spent","Avg Order","Days Since","Membership","Support"];
  const defV=[12,18,15,22,10,14,5,14];
  const labels=featureImp?Object.keys(featureImp):defL;
  const vals=featureImp?Object.values(featureImp):defV;
  useChart(id,()=>({type:"bar",data:{labels,datasets:[{label:"Importance %",data:vals,backgroundColor:labels.map((_,i)=>`hsla(${210+i*15},70%,${55+i*3}%,0.85)`),borderRadius:6,borderSkipped:false}]},options:{responsive:true,maintainAspectRatio:false,indexAxis:"y",plugins:{legend:{display:false},tooltip:{backgroundColor:"#1e293b",cornerRadius:8,padding:10}},scales:{x:{grid:{color:"rgba(0,0,0,0.04)"},ticks:{font:{size:10},color:"#94a3b8"}},y:{grid:{display:false},ticks:{font:{size:10},color:"#64748b"}}}}}),[id,JSON.stringify(featureImp)]);
  return <div style={{height:220}}><canvas id={id}/></div>;
};
const Gauge=({prob})=>{
  const pct=Math.round(prob*100);
  const color=prob>=0.75?"#ef4444":prob>=0.45?"#f59e0b":"#10b981";
  return(<div><div className="flex justify-between text-xs text-slate-400 mb-1.5"><span>0%</span><span>Churn Probability</span><span>100%</span></div><div className="pb"><div className="pf" style={{width:`${pct}%`,background:color}}/></div><div className="text-center mt-2"><span className="text-2xl font-bold" style={{color}}>{pct}%</span></div></div>);
};
const Empty=({icon,title,sub})=>(
  <div className="flex flex-col items-center py-12 text-slate-300">
    <Ic n={icon} cls="w-12 h-12 mb-3"/>
    <p className="font-medium text-slate-400">{title}</p>
    {sub&&<p className="text-sm text-slate-300 mt-1">{sub}</p>}
  </div>
);

/* ── Sidebar ── */
const NAV=[{id:"dashboard",label:"Dashboard",icon:"dashboard"},{id:"predict",label:"Predict Churn",icon:"predict"},{id:"analytics",label:"Analytics",icon:"analytics"},{id:"customers",label:"Customers",icon:"customers"},{id:"history",label:"History",icon:"history"}];
const Sidebar=({page,setPage,col,setCol})=>(
  <aside className={`fixed top-0 left-0 h-full bg-white border-r border-slate-200 z-50 flex flex-col transition-all duration-300 ${col?"w-16":"w-56"}`} style={{boxShadow:"2px 0 16px rgba(0,0,0,0.05)"}}>
    <div className="flex items-center gap-2.5 px-4 py-5 border-b border-slate-100">
      <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-700 flex items-center justify-center flex-shrink-0"><Ic n="shield" cls="w-4 h-4 text-white"/></div>
      {!col&&<span className="font-bold text-slate-800 text-sm">ChurnGuard <span className="text-indigo-600">AI</span></span>}
      <button onClick={()=>setCol(!col)} className="ml-auto text-slate-400 hover:text-indigo-600 transition-colors"><Ic n={col?"cr":"x"} cls="w-4 h-4"/></button>
    </div>
    <nav className="flex-1 py-4 px-2 flex flex-col gap-1 overflow-y-auto">
      {NAV.map(n=>(
        <button key={n.id} onClick={()=>setPage(n.id)} className={`sl ${page===n.id?"active":""} ${col?"justify-center px-0":""}`} title={col?n.label:""}>
          <Ic n={n.icon} cls={`w-[18px] h-[18px] flex-shrink-0 ${page===n.id?"text-indigo-600":"text-slate-400"}`}/>
          {!col&&<span>{n.label}</span>}
        </button>
      ))}
    </nav>
    {!col&&<div className="p-4 border-t border-slate-100"><div className="bg-indigo-50 rounded-xl p-3"><div className="flex items-center gap-2 mb-1"><span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span><span className="text-xs font-semibold text-slate-700">Model Online</span></div><p className="text-xs text-slate-400">RF + XGBoost Ensemble</p></div></div>}
  </aside>
);

/* ── Navbar ── */
const PT={dashboard:"Dashboard",predict:"Predict Churn",analytics:"Analytics",customers:"Customers",history:"Prediction History"};
const Navbar=({page,online,user,onLogout})=>(
  <header className="bg-white border-b border-slate-200 px-6 py-3.5 flex items-center justify-between sticky top-0 z-40" style={{boxShadow:"0 1px 6px rgba(0,0,0,0.05)"}}>
    <div>
      <h1 className="text-base font-bold text-slate-800">{PT[page]}</h1>
      <p className="text-xs text-slate-400">AI-powered churn analysis · RF + XGBoost</p>
    </div>
    <div className="flex items-center gap-3">
      <div className="hidden md:flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2">
        <Ic n="search" cls="w-4 h-4 text-slate-400"/>
        <input className="bg-transparent text-sm outline-none text-slate-700 w-36 placeholder-slate-400" placeholder="Search anything..."/>
      </div>
      <div className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold ${online?"bg-emerald-50 text-emerald-600":"bg-red-50 text-red-500"}`}>
        <span className={`w-1.5 h-1.5 rounded-full ${online?"bg-emerald-500 animate-pulse":"bg-red-500"}`}></span>
        {online?"API Live":"API Offline"}
      </div>
      <button className="w-9 h-9 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 hover:text-indigo-600 hover:border-indigo-200 transition-all relative">
        <Ic n="bell" cls="w-4 h-4"/>
        <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-red-500 rounded-full"></span>
      </button>
      <div className="flex items-center gap-2">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-indigo-700 flex items-center justify-center text-white text-sm font-bold">{(user?.name||"A")[0]}</div>
        <div className="hidden md:block">
          <p className="text-xs font-semibold text-slate-700 leading-none">{user?.name||"Admin"}</p>
          <p className="text-xs text-slate-400">{user?.role||"Administrator"}</p>
        </div>
        <button onClick={onLogout} title="Logout" className="w-8 h-8 rounded-xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-400 hover:text-red-500 hover:border-red-200 transition-all ml-1">
          <Ic n="logout" cls="w-4 h-4"/>
        </button>
      </div>
    </div>
  </header>
);

/* ── Dashboard Page ── */
const DashPage=({stats,hist,fiData,setPage})=>{
  const recent=[...(hist||[])].reverse().slice(0,5);
  const high=(hist||[]).filter(h=>h.risk==="High").length;
  const med=(hist||[]).filter(h=>h.risk==="Medium").length;
  const low=(hist||[]).filter(h=>h.risk==="Low").length;
  return(
    <div className="space-y-6 fu">
      <div className="flex items-center justify-between">
        <div><h2 className="text-xl font-bold text-slate-800">Welcome back!</h2><p className="text-sm text-slate-400">Here is what is happening with your customers today.</p></div>
        <button onClick={()=>setPage("predict")} className="flex items-center gap-2 text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors" style={{background:"linear-gradient(135deg,#6366f1,#4f46e5)",boxShadow:"0 4px 20px rgba(99,102,241,0.3)"}}>
          <Ic n="predict" cls="w-4 h-4"/>New Prediction
        </button>
      </div>
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <KPI label="Total Customers" val={(stats?.total_customers||12847).toLocaleString()} sub="+2.1%" up icon="users"   bg="bg-blue-600"    delay={0}/>
        <KPI label="Churn Rate"      val={`${stats?.churn_rate||24.5}%`}                    sub="-1.2%"    icon="warning" bg="bg-red-500"     delay={60}/>
        <KPI label="Retained"        val={(stats?.retained||9699).toLocaleString()}           sub="+3.4%" up icon="shield"  bg="bg-emerald-500" delay={120}/>
        <KPI label="Avg Revenue"     val={`$${stats?.avg_revenue||68.40}`}                   sub="+7.8%" up icon="money"   bg="bg-amber-500"   delay={180}/>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="lg:col-span-2 card p-5">
          <div className="flex items-center justify-between mb-4">
            <div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Churn Trend</p><p className="text-lg font-bold text-slate-800">Monthly Risk Overview</p></div>
            <span className="badge bg-blue-50 text-blue-600">Last 7 months</span>
          </div>
          <LineChart id="lc1" labels={["Jan","Feb","Mar","Apr","May","Jun","Jul"]} data={[22,28,24,31,26,29,24]}/>
        </div>
        <div className="card p-5">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Risk Distribution</p>
          <p className="text-lg font-bold text-slate-800 mb-3">Churn Segments</p>
          <DonutChart id="dc1" high={high||30} med={med||45} low={low||25}/>
        </div>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div className="card p-5">
          <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Model Insights</p>
          <p className="text-lg font-bold text-slate-800 mb-3">Feature Importance</p>
          <HBarChart id="bc1" featureImp={fiData?.feature_importance||null}/>
        </div>
        <div className="lg:col-span-2 card p-5">
          <div className="flex items-center justify-between mb-4">
            <div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Latest Activity</p><p className="text-lg font-bold text-slate-800">Recent Predictions</p></div>
            <button onClick={()=>setPage("history")} className="text-xs font-semibold text-indigo-600 flex items-center gap-1 hover:text-indigo-700">See all <Ic n="cr" cls="w-3 h-3"/></button>
          </div>
          {recent.length===0?<Empty icon="history" title="No predictions yet" sub="Click New Prediction to get started"/>:(
            <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="border-b border-slate-100">{["Customer ID","Contract","Tenure","Risk","Date"].map(h=><th key={h} className="text-left text-xs font-semibold text-slate-400 pb-2 pr-4 whitespace-nowrap">{h}</th>)}</tr></thead>
            <tbody>{recent.map((r,i)=><tr key={i} className="border-b border-slate-50 hover:bg-indigo-50/30 transition-colors"><td className="py-2.5 pr-4 font-medium text-slate-700">{r.id}</td><td className="py-2.5 pr-4"><Badge text={(r.contract||"Silver").split(" ")[0]}/></td><td className="py-2.5 pr-4 text-slate-400">{r.tenure} mo</td><td className="py-2.5 pr-4"><Badge text={r.risk}/></td><td className="py-2.5 text-slate-400 text-xs">{r.date}</td></tr>)}</tbody></table></div>
          )}
        </div>
      </div>
    </div>
  );
};

/* ── Predict Page ── */
const PredPage=({onDone})=>{
  const [form,setForm]=useState({customer_id:"",name:"",age:35,tenure:12,purchase_freq:8,total_spent:450,avg_order:56,days_since:90,membership:"Silver",support_calls:2});
  const [result,setResult]=useState(null);
  const [loading,setLoading]=useState(false);
  const [err,setErr]=useState("");
  const set=(k,v)=>setForm(p=>({...p,[k]:v}));
  const submit=async()=>{setLoading(true);setErr("");setResult(null);try{const r=await apiPost("/predict",form);if(r.error)throw new Error(r.error);setResult(r);onDone&&onDone();}catch(e){setErr(e.message||"Prediction failed.");}finally{setLoading(false);}};
  const RC={High:"text-red-600 bg-red-50",Medium:"text-amber-600 bg-amber-50",Low:"text-emerald-600 bg-emerald-50"};
  const F=({label,k,type="text",...rest})=>(<div><label className="fl">{label}</label><input type={type} className="fi" value={form[k]} onChange={e=>set(k,type==="number"?+e.target.value:e.target.value)} {...rest}/></div>);
  return(
    <div className="fu max-w-5xl mx-auto">
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        <div className="lg:col-span-3 card p-6">
          <h2 className="text-lg font-bold text-slate-800 mb-1">Customer Profile</h2>
          <p className="text-sm text-slate-400 mb-5">Fill in the details to get an AI churn prediction.</p>
          <div className="grid grid-cols-2 gap-4">
            <F label="Customer ID" k="customer_id" placeholder="C-1001"/>
            <F label="Name" k="name" placeholder="John Doe"/>
            <F label="Age" k="age" type="number" min={18} max={100}/>
            <F label="Tenure (Months)" k="tenure" type="number" min={0}/>
            <F label="Purchase Frequency/yr" k="purchase_freq" type="number" min={0}/>
            <F label="Total Spent ($)" k="total_spent" type="number" min={0} step="10"/>
            <F label="Avg Order Value ($)" k="avg_order" type="number" min={0} step="5"/>
            <F label="Days Since Purchase" k="days_since" type="number" min={0} max={365}/>
            <div><label className="fl">Membership Tier</label><select className="fi" value={form.membership} onChange={e=>set("membership",e.target.value)}><option>Bronze</option><option>Silver</option><option>Gold</option></select></div>
            <F label="Support Calls" k="support_calls" type="number" min={0} max={30}/>
          </div>
          {err&&<div className="mt-4 flex items-start gap-2 bg-red-50 border border-red-200 rounded-xl p-3 text-sm text-red-600"><Ic n="warning" cls="w-4 h-4 mt-0.5 flex-shrink-0"/>{err}</div>}
          <button onClick={submit} disabled={loading} className="mt-5 w-full flex items-center justify-center gap-2 text-white font-semibold py-3 rounded-xl transition-colors" style={{background:"linear-gradient(135deg,#6366f1,#4f46e5)",boxShadow:"0 4px 20px rgba(99,102,241,0.3)"}}>
            {loading?<><span className="w-4 h-4 border-2 border-white/40 border-t-white rounded-full spin"/>Predicting...</>:<><Ic n="predict" cls="w-4 h-4"/>Predict Churn</>}
          </button>
        </div>
        <div className="lg:col-span-2 space-y-4">
          {result?(
            <><div className={`card p-5 border-l-4 ${result.churn_label?"border-red-500":"border-emerald-500"}`}>
              <p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-2">Prediction Result</p>
              <div className="flex items-center gap-3 mb-4"><span className="text-3xl">{result.churn_label?"🔴":"🟢"}</span><div><p className="font-bold text-slate-800 text-lg leading-tight">{result.will_churn}</p><p className="text-xs text-slate-400">Customer #{result.customer_id||"—"}</p></div></div>
              <Gauge prob={result.churn_prob}/>
              <div className="grid grid-cols-2 gap-3 mt-4">
                <div className="bg-slate-50 rounded-xl p-3 text-center"><p className="text-xs text-slate-400 mb-1">Risk Level</p><span className={`badge ${RC[result.risk_level]||"bg-blue-50 text-blue-600"}`}>{result.risk_level}</span></div>
                <div className="bg-slate-50 rounded-xl p-3 text-center"><p className="text-xs text-slate-400 mb-1">Confidence</p><p className="font-bold text-slate-800 text-lg">{result.confidence}%</p></div>
              </div>
            </div>
            <div className="card p-5"><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3">AI Insights</p><ul className="space-y-2">{(result.insights||[]).map((ins,i)=><li key={i} className="flex items-start gap-2 text-sm text-slate-700"><Ic n="cr" cls="w-3.5 h-3.5 mt-0.5 text-indigo-400 flex-shrink-0"/>{ins}</li>)}</ul></div></>
          ):(
            <div className="card p-8 flex flex-col items-center justify-center text-center" style={{minHeight:260}}>
              <div className="w-14 h-14 rounded-2xl bg-indigo-50 flex items-center justify-center mb-4"><Ic n="predict" cls="w-7 h-7 text-indigo-500"/></div>
              <p className="font-semibold text-slate-700 mb-1">No result yet</p>
              <p className="text-sm text-slate-400">Fill the form and click Predict Churn.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

/* ── Analytics Page ── */
const AnalyticsPage=({stats,hist,fiData})=>{
  const h=(hist||[]).filter(x=>x.risk==="High").length;
  const m=(hist||[]).filter(x=>x.risk==="Medium").length;
  const l=(hist||[]).filter(x=>x.risk==="Low").length;
  return(<div className="space-y-6 fu">
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <KPI label="Total Predictions" val={(hist||[]).length} sub="+12%" up icon="trend"   bg="bg-blue-600"    delay={0}/>
      <KPI label="High Risk"         val={h}                 sub="risky"  icon="warning" bg="bg-red-500"     delay={60}/>
      <KPI label="Medium Risk"       val={m}                 sub="watch" up icon="shield"  bg="bg-amber-500"   delay={120}/>
      <KPI label="Low Risk"          val={l}                 sub="safe"  up icon="check"   bg="bg-emerald-500" delay={180}/>
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div className="card p-5"><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Risk Segments</p><p className="text-lg font-bold text-slate-800 mb-3">Distribution</p><DonutChart id="dc2" high={h||30} med={m||45} low={l||25}/></div>
      <div className="card p-5"><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Model Intelligence</p><p className="text-lg font-bold text-slate-800 mb-3">Feature Importance</p><HBarChart id="bc2" featureImp={fiData?.feature_importance||null}/></div>
    </div>
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <div className="card p-5"><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Churn Trend</p><p className="text-lg font-bold text-slate-800 mb-3">Monthly Rate (%)</p><LineChart id="lc2" labels={["Jan","Feb","Mar","Apr","May","Jun","Jul"]} data={[22,28,24,31,26,29,24]} color="#6366f1"/></div>
      <div className="card p-5"><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-1">Revenue Trend</p><p className="text-lg font-bold text-slate-800 mb-3">Avg Monthly ($)</p><LineChart id="lc3" labels={["Jan","Feb","Mar","Apr","May","Jun","Jul"]} data={[64,71,68,74,69,72,68]} color="#10b981"/></div>
    </div>
  </div>);
};

/* ── Customers Page ── */
const CustomersPage=({hist})=>{
  const [q,setQ]=useState("");
  const [flt,setFlt]=useState("All");
  const rows=(hist||[]).filter(r=>{const ms=!q||r.id?.toLowerCase().includes(q.toLowerCase())||r.name?.toLowerCase().includes(q.toLowerCase());const mf=flt==="All"||r.risk===flt;return ms&&mf;});
  return(<div className="fu"><div className="card p-5">
    <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-5">
      <div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Customer Intelligence</p><p className="text-lg font-bold text-slate-800">All Customers</p></div>
      <div className="flex flex-wrap items-center gap-2">
        <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-3 py-2"><Ic n="search" cls="w-4 h-4 text-slate-400"/><input className="bg-transparent text-sm outline-none text-slate-700 w-28 placeholder-slate-400" placeholder="Search..." value={q} onChange={e=>setQ(e.target.value)}/></div>
        {["All","High","Medium","Low"].map(f=><button key={f} onClick={()=>setFlt(f)} className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-colors ${flt===f?"bg-indigo-600 text-white":"bg-slate-50 text-slate-500 hover:bg-indigo-50 hover:text-indigo-600"}`}>{f}</button>)}
      </div>
    </div>
    {rows.length===0?<Empty icon="users" title="No customers found" sub="Make predictions to populate this list"/>:(
      <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="border-b-2 border-slate-100">{["Customer","Name","Contract","Tenure","Monthly Charge","Risk","Date"].map(h=><th key={h} className="text-left text-xs font-semibold text-slate-400 pb-3 pr-4 whitespace-nowrap">{h}</th>)}</tr></thead>
      <tbody>{rows.map((r,i)=><tr key={i} className="border-b border-slate-50 hover:bg-indigo-50/30 transition-colors">
        <td className="py-3 pr-4"><div className="flex items-center gap-2"><div className="w-7 h-7 rounded-lg bg-gradient-to-br from-indigo-400 to-indigo-600 flex items-center justify-center text-white text-xs font-bold">{(r.id||"C")[0]}</div><span className="font-medium text-slate-700">{r.id}</span></div></td>
        <td className="py-3 pr-4 text-slate-600">{r.name||"—"}</td>
        <td className="py-3 pr-4"><Badge text={(r.contract||"Silver").split(" ")[0]}/></td>
        <td className="py-3 pr-4 text-slate-400">{r.tenure} mo</td>
        <td className="py-3 pr-4 text-slate-700">${r.mc||"—"}</td>
        <td className="py-3 pr-4"><Badge text={r.risk}/></td>
        <td className="py-3 text-slate-400 text-xs whitespace-nowrap">{r.date}</td>
      </tr>)}</tbody></table></div>
    )}
  </div></div>);
};

/* ── History Page ── */
const HistoryPage=({hist})=>{
  const rows=[...(hist||[])].reverse();
  return(<div className="fu"><div className="card p-5">
    <div className="flex items-center justify-between mb-5"><div><p className="text-xs font-semibold text-slate-400 uppercase tracking-wide">Session Log</p><p className="text-lg font-bold text-slate-800">Prediction History</p></div><span className="badge bg-indigo-50 text-indigo-600">{rows.length} records</span></div>
    {rows.length===0?<Empty icon="history" title="No history yet" sub="Predictions appear here in real time"/>:(
      <div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="border-b-2 border-slate-100">{["#","Customer ID","Contract","Tenure","Charge","Churn Prob","Risk","Date"].map(h=><th key={h} className="text-left text-xs font-semibold text-slate-400 pb-3 pr-4 whitespace-nowrap">{h}</th>)}</tr></thead>
      <tbody>{rows.map((r,i)=>{const pct=(r.cp*100).toFixed(1);const bc=r.risk==="High"?"#ef4444":r.risk==="Medium"?"#f59e0b":"#10b981";return(<tr key={i} className="border-b border-slate-50 hover:bg-indigo-50/30 transition-colors">
        <td className="py-3 pr-4 text-slate-400 text-xs tabular-nums">{rows.length-i}</td>
        <td className="py-3 pr-4 font-medium text-slate-700">{r.id}</td>
        <td className="py-3 pr-4"><Badge text={(r.contract||"Silver").split(" ")[0]}/></td>
        <td className="py-3 pr-4 text-slate-400">{r.tenure} mo</td>
        <td className="py-3 pr-4 text-slate-700">${r.mc||"—"}</td>
        <td className="py-3 pr-4" style={{minWidth:130}}><div className="flex items-center gap-2"><div className="pb flex-1"><div className="pf" style={{width:`${pct}%`,background:bc}}/></div><span className="text-xs font-semibold text-slate-600 tabular-nums">{pct}%</span></div></td>
        <td className="py-3 pr-4"><Badge text={r.risk}/></td>
        <td className="py-3 text-slate-400 text-xs whitespace-nowrap">{r.date}</td>
      </tr>);})}</tbody></table></div>
    )}
  </div></div>);
};

/* ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ROOT APP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ */
const App=()=>{
  const [screen,  setScreen]  = useState("landing"); // landing | login | app
  const [user,    setUser]    = useState(null);
  const [page,    setPage]    = useState("dashboard");
  const [col,     setCol]     = useState(false);
  const [online,  setOnline]  = useState(false);
  const [stats,   setStats]   = useState(null);
  const [hist,    setHist]    = useState([]);
  const [fiData,  setFiData]  = useState(null);

  // Check for remembered session
  useEffect(()=>{
    const saved=localStorage.getItem("cg_user");
    if(saved){try{setUser(JSON.parse(saved));setScreen("app");}catch(e){}}
  },[]);

  // Update body class
  useEffect(()=>{
    document.body.className = screen==="app" ? "dash-mode" : "";
  },[screen]);

  const refresh=useCallback(async()=>{
    try{
      const [s,h,f]=await Promise.all([apiGet("/stats"),apiGet("/history"),apiGet("/feature-importance")]);
      setStats(s);setHist(h.predictions||[]);setFiData(f);setOnline(true);
    }catch{setOnline(false);}
  },[]);

  useEffect(()=>{
    if(screen==="app"){refresh();const t=setInterval(refresh,15000);return()=>clearInterval(t);}
  },[screen]);

  const handleLogin=(u)=>{setUser(u);setScreen("app");};
  const handleLogout=()=>{localStorage.removeItem("cg_user");setUser(null);setPage("dashboard");setScreen("landing");};

  if(screen==="landing") return <LandingPage onLogin={()=>setScreen("login")}/>;
  if(screen==="login")   return <LoginPage   onLogin={handleLogin} onBack={()=>setScreen("landing")}/>;

  const ml=col?"ml-16":"ml-56";
  const pages={
    dashboard:<DashPage stats={stats} hist={hist} fiData={fiData} setPage={setPage}/>,
    predict:<PredPage onDone={()=>setTimeout(refresh,600)}/>,
    analytics:<AnalyticsPage stats={stats} hist={hist} fiData={fiData}/>,
    customers:<CustomersPage hist={hist}/>,
    history:<HistoryPage hist={hist}/>,
  };

  return(
    <div className="min-h-screen bg-slate-100">
      <Sidebar page={page} setPage={setPage} col={col} setCol={setCol}/>
      <div className={`${ml} transition-all duration-300 min-h-screen flex flex-col`}>
        <Navbar page={page} online={online} user={user} onLogout={handleLogout}/>
        {!online&&(
          <div className="mx-6 mt-4 flex items-start gap-3 bg-amber-50 border border-amber-200 rounded-xl p-3 text-sm text-amber-700">
            <Ic n="warning" cls="w-4 h-4 mt-0.5 flex-shrink-0"/>
            <div><strong>Flask API is offline.</strong> Run: <code className="bg-amber-100 px-1.5 py-0.5 rounded font-mono text-xs">python api.py</code></div>
          </div>
        )}
        <main className="flex-1 p-6">{pages[page]}</main>
        <footer className="px-6 py-3 border-t border-slate-200 bg-white">
          <p className="text-xs text-slate-400 text-center">ChurnGuard AI &mdash; RF + XGBoost &mdash; v1.0.0</p>
        </footer>
      </div>
    </div>
  );
};

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
</script>
</body>
</html>"""

html = PART1 + PART2

with open("frontend/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Written {len(html):,} bytes to frontend/index.html")
print("Screens: Landing Page -> Login Page -> Dashboard")
print("Demo accounts:")
print("  admin@churnguard.ai   / admin123")
print("  analyst@churnguard.ai / analyst123")
print("  demo@churnguard.ai    / demo123")
