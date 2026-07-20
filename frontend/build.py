import pathlib, textwrap

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>ChurnGuard AI – Customer Churn Prediction System</title>
<meta name="description" content="AI-powered customer churn prediction dashboard connected to a live Flask ML backend."/>
<script src="https://cdn.tailwindcss.com"></script>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet"/>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<script src="https://unpkg.com/react@18/umd/react.production.min.js" crossorigin></script>
<script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js" crossorigin></script>
<script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#0f172a;color:#e2e8f0;overflow-x:hidden}
.sidebar{width:252px;min-height:100vh;background:#1e293b;border-right:1px solid #334155;display:flex;flex-direction:column;position:fixed;top:0;left:0;z-index:50;transition:transform .3s}
.main-wrap{margin-left:252px;min-height:100vh;display:flex;flex-direction:column}
.g1{background:linear-gradient(135deg,#6366f1,#4338ca)}
.g2{background:linear-gradient(135deg,#f43f5e,#be123c)}
.g3{background:linear-gradient(135deg,#10b981,#047857)}
.g4{background:linear-gradient(135deg,#f59e0b,#b45309)}
.glow-i{box-shadow:0 0 28px rgba(99,102,241,.45)}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(244,63,94,.6)}60%{box-shadow:0 0 0 10px rgba(244,63,94,0)}}
@keyframes spin{to{transform:rotate(360deg)}}
.fadeUp{animation:fadeUp .45s ease both}
.dot-pulse{animation:pulse 1.8s ease infinite}
.spin{animation:spin .9s linear infinite}
::-webkit-scrollbar{width:5px}
::-webkit-scrollbar-track{background:#1e293b}
::-webkit-scrollbar-thumb{background:#4f46e5;border-radius:4px}
.nav-item{cursor:pointer;transition:all .18s;border-left:3px solid transparent;border-radius:10px}
.nav-item:hover{background:rgba(99,102,241,.1);color:#a5b4fc}
.nav-item.active{background:linear-gradient(90deg,rgba(99,102,241,.22),transparent);color:#818cf8;border-left-color:#6366f1;border-radius:0 10px 10px 0}
.bh{background:rgba(244,63,94,.15);color:#f43f5e;border:1px solid rgba(244,63,94,.3)}
.bm{background:rgba(245,158,11,.15);color:#f59e0b;border:1px solid rgba(245,158,11,.3)}
.bl{background:rgba(16,185,129,.15);color:#10b981;border:1px solid rgba(16,185,129,.3)}
.inp{background:#0f172a;border:1px solid #334155;color:#e2e8f0;border-radius:8px;padding:10px 14px;width:100%;outline:none;font-size:13px;font-family:'Inter',sans-serif;transition:border-color .2s,box-shadow .2s}
.inp:focus{border-color:#6366f1;box-shadow:0 0 0 3px rgba(99,102,241,.18)}
.sel{appearance:none;-webkit-appearance:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='11' height='11' viewBox='0 0 12 12'%3E%3Cpath fill='%2394a3b8' d='M6 8L1 3h10z'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:right 12px center;padding-right:32px;background-color:#0f172a}
.trow{transition:background .12s}
.trow:hover{background:rgba(99,102,241,.06)}
.prog{height:7px;border-radius:4px;background:#0f172a;overflow:hidden}
.progf{height:100%;border-radius:4px;transition:width 1.2s ease}
.card{background:#1e293b;border:1px solid #334155;border-radius:16px}
.sb-inp{background:#0f172a;border:1px solid #334155;border-radius:20px;color:#e2e8f0;outline:none;width:225px;font-size:13px;font-family:'Inter',sans-serif;padding:8px 14px 8px 36px;transition:border-color .2s}
.sb-inp:focus{border-color:#6366f1}
.api-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px}
.toast{position:fixed;bottom:24px;right:24px;z-index:999;padding:12px 20px;border-radius:12px;font-size:13px;font-weight:600;animation:fadeUp .3s ease;max-width:340px}
</style>
</head>
<body>
<div id="root"></div>
<script type="text/babel">
const {useState, useEffect, useRef, useCallback} = React;

/* ── CONFIG ── */
const API = "http://127.0.0.1:5000";

/* ── ICONS ── */
function Ic({d, size=18, color="currentColor", cls=""}) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none"
      stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={cls}>
      {Array.isArray(d) ? d.map((p,i)=><path key={i} d={p}/>) : <path d={d}/>}
    </svg>
  );
}

const I = {
  home:    ["M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z","M9 22V12h6v10"],
  predict: ["M12 2L2 7l10 5 10-5-10-5","M2 17l10 5 10-5","M2 12l10 5 10-5"],
  bar:     ["M18 20V10","M12 20V4","M6 20v-6"],
  users:   ["M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2","M23 21v-2a4 4 0 0 0-3-3.87","M16 3.13a4 4 0 0 1 0 7.75"],
  gear:    "M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6z M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z",
  bell:    ["M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9","M13.73 21a2 2 0 0 1-3.46 0"],
  search:  ["M21 21l-4.35-4.35","M11 17a6 6 0 1 0 0-12 6 6 0 0 0 0 12z"],
  logout:  "M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4 M16 17l5-5-5-5 M21 12H9",
  up:      "M23 6l-9.5 9.5-5-5L1 18 M17 6h6v6",
  check:   "M20 6L9 17l-5-5",
  warn:    "M12 9v4 M12 17h.01",
  refresh: ["M23 4v6h-6","M1 20v-6h6","M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"],
  x:       "M18 6L6 18 M6 6l12 12",
  link:    "M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71 M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71",
};

/* ── HELPERS ── */
const rb = r => r==="High"?"bh":r==="Medium"?"bm":"bl";
const rc = r => r==="High"?"#f43f5e":r==="Medium"?"#f59e0b":"#10b981";
const MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul"];

/* ── TOAST ── */
function Toast({msg, type, onClose}) {
  useEffect(()=>{ const t=setTimeout(onClose,3500); return()=>clearTimeout(t); },[]);
  const bg = type==="error"?"rgba(244,63,94,.15)":type==="success"?"rgba(16,185,129,.15)":"rgba(99,102,241,.15)";
  const border = type==="error"?"rgba(244,63,94,.4)":type==="success"?"rgba(16,185,129,.4)":"rgba(99,102,241,.4)";
  const col = type==="error"?"#f43f5e":type==="success"?"#10b981":"#818cf8";
  return (
    <div className="toast" style={{background:bg,border:`1px solid ${border}`,color:col}}>
      {type==="error"?"⚠️":type==="success"?"✅":"ℹ️"} {msg}
      <button onClick={onClose} style={{marginLeft:12,background:"none",border:"none",color:col,cursor:"pointer",fontSize:16}}>×</button>
    </div>
  );
}

/* ── API STATUS BANNER ── */
function ApiBanner({status}) {
  if (status==="ok") return (
    <div style={{display:"flex",alignItems:"center",gap:6,fontSize:11,color:"#10b981"}}>
      <span className="api-dot" style={{background:"#10b981"}}/>API Connected
    </div>
  );
  if (status==="error") return (
    <div style={{display:"flex",alignItems:"center",gap:6,fontSize:11,color:"#f43f5e"}}>
      <span className="api-dot" style={{background:"#f43f5e"}}/>API Offline
      <span style={{color:"#64748b"}}>(run: python api.py)</span>
    </div>
  );
  return (
    <div style={{display:"flex",alignItems:"center",gap:6,fontSize:11,color:"#f59e0b"}}>
      <span className="api-dot spin" style={{background:"#f59e0b"}}/>Connecting…
    </div>
  );
}

/* ── SIDEBAR ── */
function Sidebar({page, setPage, apiStatus}) {
  const nav = [
    {id:"dashboard", label:"Dashboard",    d:I.home},
    {id:"predict",   label:"Predict Churn",d:I.predict},
    {id:"analytics", label:"Analytics",    d:I.bar},
    {id:"customers", label:"Customers",    d:I.users},
    {id:"settings",  label:"Settings",     d:I.gear},
  ];
  return (
    <div className="sidebar">
      {/* Logo */}
      <div style={{padding:"18px 16px 16px",borderBottom:"1px solid #334155"}}>
        <div style={{display:"flex",alignItems:"center",gap:11}}>
          <div className="g1 glow-i" style={{width:42,height:42,borderRadius:12,display:"flex",alignItems:"center",justifyContent:"center",flexShrink:0}}>
            <Ic d={I.predict} size={21} color="white"/>
          </div>
          <div>
            <div style={{color:"white",fontWeight:800,fontSize:15,lineHeight:1.25}}>ChurnGuard AI</div>
            <div style={{color:"#64748b",fontSize:11,marginTop:2}}>Prediction System</div>
          </div>
        </div>
      </div>

      {/* Nav */}
      <nav style={{flex:1,padding:"10px 10px 8px",display:"flex",flexDirection:"column",gap:2,marginTop:4}}>
        {nav.map(n => (
          <div key={n.id} id={"nav-"+n.id}
            className={"nav-item "+(page===n.id?"active":"")}
            style={{display:"flex",alignItems:"center",gap:10,padding:"10px 14px",fontSize:13,fontWeight:500,color:page===n.id?"#818cf8":"#94a3b8"}}
            onClick={()=>setPage(n.id)}>
            <Ic d={n.d} size={16} color={page===n.id?"#818cf8":"#94a3b8"}/>
            {n.label}
            {n.id==="predict"&&<span style={{marginLeft:"auto",fontSize:10,fontWeight:700,padding:"2px 7px",borderRadius:20,background:"rgba(99,102,241,.2)",color:"#818cf8",border:"1px solid rgba(99,102,241,.3)"}}>AI</span>}
          </div>
        ))}
      </nav>

      {/* Alert */}
      <div style={{margin:"0 10px 10px",padding:14,borderRadius:12,background:"rgba(244,63,94,.1)",border:"1px solid rgba(244,63,94,.25)"}}>
        <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:5}}>
          <div className="dot-pulse" style={{width:7,height:7,borderRadius:"50%",background:"#f43f5e"}}/>
          <span style={{fontSize:11,fontWeight:700,color:"#f43f5e"}}>HIGH ALERT</span>
        </div>
        <p style={{fontSize:11,color:"#94a3b8",lineHeight:1.55}}>3 customers at critical churn risk today</p>
        <button onClick={()=>setPage("predict")} style={{marginTop:6,fontSize:11,fontWeight:600,color:"#f43f5e",background:"none",border:"none",cursor:"pointer",padding:0}}>View Details →</button>
      </div>

      {/* API Status */}
      <div style={{padding:"10px 14px",borderTop:"1px solid #334155"}}>
        <ApiBanner status={apiStatus}/>
      </div>

      {/* User */}
      <div style={{padding:"12px 16px",borderTop:"1px solid #334155",display:"flex",alignItems:"center",gap:10}}>
        <div style={{width:34,height:34,borderRadius:"50%",background:"linear-gradient(135deg,#6366f1,#4f46e5)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:12,fontWeight:700,color:"white",flexShrink:0}}>AD</div>
        <div style={{flex:1,minWidth:0}}>
          <div style={{fontSize:13,fontWeight:600,color:"white"}}>Admin User</div>
          <div style={{fontSize:11,color:"#64748b"}}>admin@churnguard.ai</div>
        </div>
        <Ic d={I.logout} size={14} color="#64748b" cls="cursor-pointer"/>
      </div>
    </div>
  );
}

/* ── TOPBAR ── */
function Topbar({page, notif}) {
  const titles = {dashboard:"Dashboard Overview",predict:"Churn Prediction",analytics:"Analytics & Insights",customers:"Customer Management",settings:"Settings"};
  const today = new Date().toLocaleDateString("en-US",{weekday:"long",year:"numeric",month:"long",day:"numeric"});
  return (
    <header style={{position:"sticky",top:0,zIndex:40,padding:"14px 28px",display:"flex",alignItems:"center",justifyContent:"space-between",background:"rgba(15,23,42,.96)",backdropFilter:"blur(14px)",borderBottom:"1px solid #334155"}}>
      <div>
        <h1 style={{fontSize:18,fontWeight:800,color:"white"}}>{titles[page]}</h1>
        <p style={{fontSize:11,color:"#64748b",marginTop:2}}>{today}</p>
      </div>
      <div style={{display:"flex",alignItems:"center",gap:12}}>
        <div style={{position:"relative"}}>
          <Ic d={I.search} size={14} color="#64748b" cls="absolute" style={{position:"absolute",left:11,top:"50%",transform:"translateY(-50%)"}}/>
          <input id="topbar-search" type="text" placeholder="Search customers…" className="sb-inp"/>
        </div>
        <button id="notif-btn" style={{position:"relative",width:38,height:38,borderRadius:10,background:"#1e293b",border:"1px solid #334155",display:"flex",alignItems:"center",justifyContent:"center",cursor:"pointer"}}>
          <Ic d={I.bell} size={17} color="#94a3b8"/>
          {notif>0&&<span style={{position:"absolute",top:-4,right:-4,width:16,height:16,borderRadius:"50%",background:"#f43f5e",color:"white",fontSize:9,fontWeight:700,display:"flex",alignItems:"center",justifyContent:"center"}}>{notif}</span>}
        </button>
        <div style={{display:"flex",alignItems:"center",gap:8,padding:"6px 12px",borderRadius:10,background:"#1e293b",border:"1px solid #334155",cursor:"pointer"}}>
          <div style={{width:28,height:28,borderRadius:"50%",background:"linear-gradient(135deg,#6366f1,#4f46e5)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:11,fontWeight:700,color:"white"}}>AD</div>
          <span style={{fontSize:13,fontWeight:600,color:"white"}}>Admin</span>
          <svg width="10" height="10" viewBox="0 0 12 12" fill="#64748b"><path d="M6 8L1 3h10z"/></svg>
        </div>
      </div>
    </header>
  );
}

/* ── KPI CARD ── */
function KpiCard({title, value, change, up, iconPath, grad, delay=0}) {
  return (
    <div className="fadeUp card" style={{padding:20,position:"relative",overflow:"hidden",cursor:"default",transition:"transform .2s",animationDelay:delay+"ms"}}
      onMouseEnter={e=>e.currentTarget.style.transform="scale(1.03)"}
      onMouseLeave={e=>e.currentTarget.style.transform="scale(1)"}>
      <div style={{display:"flex",alignItems:"flex-start",justifyContent:"space-between",marginBottom:16}}>
        <div className={grad} style={{width:44,height:44,borderRadius:11,display:"flex",alignItems:"center",justifyContent:"center"}}>
          <Ic d={iconPath} size={20} color="white"/>
        </div>
        <span style={{fontSize:11,fontWeight:700,padding:"4px 9px",borderRadius:20,background:up?"rgba(16,185,129,.15)":"rgba(244,63,94,.15)",color:up?"#10b981":"#f43f5e"}}>{change}</span>
      </div>
      <div style={{fontSize:28,fontWeight:900,color:"white",marginBottom:4}}>{value}</div>
      <div style={{fontSize:12,color:"#94a3b8"}}>{title}</div>
      <div style={{position:"absolute",bottom:-20,right:-20,width:80,height:80,borderRadius:"50%",background:"radial-gradient(circle,#6366f1,transparent)",opacity:.1}}/>
    </div>
  );
}

/* ── LINE CHART ── */
function LineChart({height=250, churned=[42,58,51,73,65,84,79], retained=[310,295,340,280,320,260,300]}) {
  const cRef=useRef(null), chObj=useRef(null);
  useEffect(()=>{
    if(!cRef.current) return;
    const ctx=cRef.current.getContext("2d");
    const g=ctx.createLinearGradient(0,0,0,height);
    g.addColorStop(0,"rgba(99,102,241,.5)"); g.addColorStop(1,"rgba(99,102,241,0)");
    if(chObj.current) chObj.current.destroy();
    chObj.current=new Chart(ctx,{
      type:"line",
      data:{labels:MONTHS,datasets:[
        {label:"Churned",data:churned,borderColor:"#f43f5e",backgroundColor:"rgba(244,63,94,.08)",borderWidth:2.5,pointBackgroundColor:"#f43f5e",pointRadius:4,pointHoverRadius:6,fill:true,tension:0.42},
        {label:"Retained",data:retained,borderColor:"#6366f1",backgroundColor:g,borderWidth:2.5,pointBackgroundColor:"#6366f1",pointRadius:4,pointHoverRadius:6,fill:true,tension:0.42},
      ]},
      options:{responsive:true,maintainAspectRatio:false,interaction:{mode:"index",intersect:false},
        plugins:{legend:{labels:{color:"#94a3b8",font:{family:"Inter",size:11},boxWidth:10,usePointStyle:true}},tooltip:{backgroundColor:"#1e293b",borderColor:"#334155",borderWidth:1,titleColor:"#e2e8f0",bodyColor:"#94a3b8",padding:10,cornerRadius:8}},
        scales:{x:{grid:{color:"rgba(51,65,85,.4)"},ticks:{color:"#64748b",font:{family:"Inter",size:11}}},y:{grid:{color:"rgba(51,65,85,.4)"},ticks:{color:"#64748b",font:{family:"Inter",size:11}}}}}
    });
    return()=>{if(chObj.current){chObj.current.destroy();chObj.current=null;}};
  },[churned.join(),retained.join()]);
  return <div style={{position:"relative",width:"100%",height}}><canvas ref={cRef}/></div>;
}

/* ── DONUT CHART ── */
function DonutChart({high=24,medium=37,low=39}) {
  const cRef=useRef(null), chObj=useRef(null);
  useEffect(()=>{
    if(!cRef.current) return;
    const ctx=cRef.current.getContext("2d");
    if(chObj.current) chObj.current.destroy();
    chObj.current=new Chart(ctx,{
      type:"doughnut",
      data:{labels:["High Risk","Medium Risk","Low Risk"],datasets:[{data:[high,medium,low],backgroundColor:["#f43f5e","#f59e0b","#10b981"],borderColor:"#0f172a",borderWidth:3,hoverOffset:6}]},
      options:{responsive:true,maintainAspectRatio:false,cutout:"68%",
        plugins:{legend:{position:"bottom",labels:{color:"#94a3b8",font:{family:"Inter",size:11},padding:14,boxWidth:10,usePointStyle:true}},tooltip:{backgroundColor:"#1e293b",borderColor:"#334155",borderWidth:1,titleColor:"#e2e8f0",bodyColor:"#94a3b8",padding:10,cornerRadius:8}}}
    });
    return()=>{if(chObj.current){chObj.current.destroy();chObj.current=null;}};
  },[high,medium,low]);
  return <div style={{position:"relative",width:"100%",height:220}}><canvas ref={cRef}/></div>;
}

/* ── BAR CHART ── */
function BarChart({data=[38,22,14,18,8], labels=["Fiber","DSL","No Svc","Cable","Stream"]}) {
  const cRef=useRef(null), chObj=useRef(null);
  useEffect(()=>{
    if(!cRef.current) return;
    const ctx=cRef.current.getContext("2d");
    if(chObj.current) chObj.current.destroy();
    chObj.current=new Chart(ctx,{
      type:"bar",
      data:{labels,datasets:[{label:"Churn Count",data,backgroundColor:["rgba(99,102,241,.92)","rgba(99,102,241,.76)","rgba(99,102,241,.6)","rgba(99,102,241,.5)","rgba(99,102,241,.38)"],borderRadius:7,borderSkipped:false}]},
      options:{responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false},tooltip:{backgroundColor:"#1e293b",borderColor:"#334155",borderWidth:1,titleColor:"#e2e8f0",bodyColor:"#94a3b8",padding:10,cornerRadius:8}},
        scales:{x:{grid:{display:false},ticks:{color:"#64748b",font:{family:"Inter",size:11}}},y:{grid:{color:"rgba(51,65,85,.4)"},ticks:{color:"#64748b",font:{family:"Inter",size:11}}}}}
    });
    return()=>{if(chObj.current){chObj.current.destroy();chObj.current=null;}};
  },[]);
  return <div style={{position:"relative",width:"100%",height:210}}><canvas ref={cRef}/></div>;
}

/* ── FEATURE IMPORTANCE CHART ── */
function FiChart({data}) {
  const cRef=useRef(null), chObj=useRef(null);
  useEffect(()=>{
    if(!cRef.current||!data) return;
    const ctx=cRef.current.getContext("2d");
    if(chObj.current) chObj.current.destroy();
    const entries=Object.entries(data).sort((a,b)=>b[1]-a[1]);
    const labels=entries.map(e=>e[0]);
    const vals=entries.map(e=>e[1]);
    chObj.current=new Chart(ctx,{
      type:"bar",
      data:{labels,datasets:[{label:"Importance %",data:vals,backgroundColor:"rgba(99,102,241,.8)",borderRadius:6,borderSkipped:false}]},
      options:{indexAxis:"y",responsive:true,maintainAspectRatio:false,
        plugins:{legend:{display:false},tooltip:{backgroundColor:"#1e293b",borderColor:"#334155",borderWidth:1,titleColor:"#e2e8f0",bodyColor:"#94a3b8",padding:10,cornerRadius:8}},
        scales:{x:{grid:{color:"rgba(51,65,85,.4)"},ticks:{color:"#64748b",font:{family:"Inter",size:11}},max:Math.max(...vals)+5},y:{grid:{display:false},ticks:{color:"#94a3b8",font:{family:"Inter",size:12}}}}}
    });
    return()=>{if(chObj.current){chObj.current.destroy();chObj.current=null;}};
  },[JSON.stringify(data)]);
  return <div style={{position:"relative",width:"100%",height:260}}><canvas ref={cRef}/></div>;
}

/* ── PREDICTIONS TABLE ── */
function PredTable({data}) {
  if(!data||data.length===0) return <p style={{color:"#64748b",fontSize:13,padding:"16px 0"}}>No predictions yet. Use the Predict Churn page to get started.</p>;
  return (
    <div style={{overflowX:"auto"}}>
      <table style={{width:"100%",fontSize:13,borderCollapse:"collapse"}}>
        <thead>
          <tr style={{borderBottom:"1px solid #334155"}}>
            {["Customer","Contract","Tenure","Monthly","Churn Prob","Risk","Date"].map(h=>(
              <th key={h} style={{paddingBottom:10,paddingRight:14,textAlign:"left",fontSize:11,fontWeight:600,color:"#64748b",textTransform:"uppercase",letterSpacing:"0.06em",whiteSpace:"nowrap"}}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((r,idx)=>(
            <tr key={r.id+idx} className="trow" style={{borderBottom:"1px solid rgba(51,65,85,.3)"}}>
              <td style={{padding:"11px 14px 11px 0"}}>
                <div style={{display:"flex",alignItems:"center",gap:10}}>
                  <div style={{width:32,height:32,borderRadius:"50%",background:"rgba(99,102,241,.2)",color:"#818cf8",display:"flex",alignItems:"center",justifyContent:"center",fontSize:11,fontWeight:700,flexShrink:0}}>
                    {(r.name||r.id||"?").split(" ").map(n=>n[0]).join("").slice(0,2).toUpperCase()}
                  </div>
                  <div>
                    <div style={{fontWeight:600,color:"white",fontSize:12}}>{r.name||"Customer"}</div>
                    <div style={{fontSize:11,color:"#64748b"}}>{r.id}</div>
                  </div>
                </div>
              </td>
              <td style={{paddingRight:14,fontSize:12,color:"#94a3b8"}}>{r.contract||"—"}</td>
              <td style={{paddingRight:14,fontSize:12,color:"#94a3b8"}}>{r.tenure||0}mo</td>
              <td style={{paddingRight:14,fontSize:12,fontWeight:600,color:"white"}}>${(r.mc||0).toFixed(2)}</td>
              <td style={{paddingRight:14}}>
                <div style={{display:"flex",alignItems:"center",gap:8}}>
                  <div className="prog" style={{width:68}}><div className="progf" style={{width:((r.cp||0)*100)+"%",background:rc(r.risk)}}/></div>
                  <span style={{fontSize:11,fontWeight:700,color:"white"}}>{((r.cp||0)*100).toFixed(0)}%</span>
                </div>
              </td>
              <td style={{paddingRight:14}}><span className={"px-2 py-1 rounded-full text-xs font-semibold "+rb(r.risk||"Low")}>{r.risk||"Low"}</span></td>
              <td style={{fontSize:11,color:"#64748b"}}>{r.date||"—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

/* ════════════════════════════════════
   DASHBOARD PAGE
════════════════════════════════════ */
function DashboardPage({stats, history, apiStatus}) {
  const kpis = [
    {title:"Total Customers",     value:stats?(stats.total_customers||0).toLocaleString():"…", change:"+4.3%", up:true,  iconPath:I.users, grad:"g1", delay:0},
    {title:"Churn Rate",          value:stats?stats.churn_rate+"%":"…",                          change:"+1.2%", up:false, iconPath:I.warn,  grad:"g2", delay:80},
    {title:"Retained Customers",  value:stats?(stats.retained||0).toLocaleString():"…",          change:"+2.8%", up:true,  iconPath:I.check, grad:"g3", delay:160},
    {title:"Predictions Today",   value:stats?(stats.predictions_today||0).toString():"…",       change:"live",  up:true,  iconPath:I.predict,grad:"g4",delay:240},
  ];
  return (
    <div style={{padding:28,display:"flex",flexDirection:"column",gap:22}}>
      {apiStatus==="error"&&(
        <div style={{padding:"14px 20px",borderRadius:12,background:"rgba(244,63,94,.1)",border:"1px solid rgba(244,63,94,.3)",display:"flex",alignItems:"center",gap:12}}>
          <Ic d={I.warn} size={18} color="#f43f5e"/>
          <div>
            <div style={{fontSize:13,fontWeight:600,color:"#f43f5e"}}>API Server Offline</div>
            <div style={{fontSize:12,color:"#94a3b8",marginTop:2}}>Start the backend: <code style={{background:"rgba(255,255,255,.07)",padding:"2px 8px",borderRadius:5,color:"#818cf8"}}>python api.py</code> — then refresh this page. Dashboard shows cached data.</div>
          </div>
        </div>
      )}

      <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(200px,1fr))",gap:16}}>
        {kpis.map(k=><KpiCard key={k.title} {...k}/>)}
      </div>

      <div style={{display:"grid",gridTemplateColumns:"2fr 1fr",gap:16}}>
        <div className="card" style={{padding:22}}>
          <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:18}}>
            <div>
              <h3 style={{fontSize:14,fontWeight:700,color:"white"}}>Churn vs Retention Trend</h3>
              <p style={{fontSize:11,color:"#64748b",marginTop:3}}>Monthly overview — 2026</p>
            </div>
            <span style={{fontSize:11,color:"#64748b",padding:"5px 12px",borderRadius:8,background:"#0f172a",border:"1px solid #334155"}}>Last 7 months</span>
          </div>
          <LineChart height={240}/>
        </div>
        <div className="card" style={{padding:22}}>
          <h3 style={{fontSize:14,fontWeight:700,color:"white",marginBottom:3}}>Risk Distribution</h3>
          <p style={{fontSize:11,color:"#64748b",marginBottom:12}}>Current customer risk levels</p>
          <div style={{position:"relative"}}>
            <DonutChart/>
            <div style={{position:"absolute",top:0,left:0,right:0,bottom:44,display:"flex",alignItems:"center",justifyContent:"center",pointerEvents:"none"}}>
              <div style={{textAlign:"center"}}>
                <div style={{fontSize:24,fontWeight:900,color:"white"}}>{stats?stats.churn_rate+"%" : "24%"}</div>
                <div style={{fontSize:11,color:"#64748b"}}>Churn Rate</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div style={{display:"grid",gridTemplateColumns:"1fr 2fr",gap:16}}>
        <div className="card" style={{padding:22}}>
          <h3 style={{fontSize:14,fontWeight:700,color:"white",marginBottom:3}}>Churn by Service</h3>
          <p style={{fontSize:11,color:"#64748b",marginBottom:16}}>Internet service type analysis</p>
          <BarChart/>
        </div>
        <div className="card" style={{padding:22}}>
          <div style={{display:"flex",alignItems:"center",justifyContent:"space-between",marginBottom:18}}>
            <div>
              <h3 style={{fontSize:14,fontWeight:700,color:"white"}}>Recent Predictions</h3>
              <p style={{fontSize:11,color:"#64748b",marginTop:3}}>Latest AI churn scores from the model</p>
            </div>
            <span style={{fontSize:11,color:"#10b981",fontWeight:600}}>{apiStatus==="ok"?"🔴 Live":"📦 Cached"}</span>
          </div>
          <PredTable data={history.slice(0,5)}/>
        </div>
      </div>
    </div>
  );
}

/* ════════════════════════════════════
   PREDICT PAGE — calls real API
════════════════════════════════════ */
function PredictPage({onNewPrediction, showToast}) {
  const [form, setForm] = useState({
    name:"", customer_id:"", age:35, tenure:12, purchase_freq:8,
    total_spent:450, avg_order:56, days_since:90,
    membership:"Silver", support_calls:2
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const upd = (k,v) => setForm(p=>({...p,[k]:v}));

  const predict = async e => {
    e.preventDefault();
    setLoading(true); setResult(null);
    try {
      const resp = await fetch(API+"/predict", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({
          name:          form.name||"Customer",
          customer_id:   form.customer_id||undefined,
          age:           Number(form.age),
          tenure:        Number(form.tenure),
          purchase_freq: Number(form.purchase_freq),
          total_spent:   Number(form.total_spent),
          avg_order:     Number(form.avg_order),
          days_since:    Number(form.days_since),
          membership:    form.membership,
          support_calls: Number(form.support_calls),
        })
      });
      if(!resp.ok) throw new Error("Server error "+resp.status);
      const data = await resp.json();
      if(data.error) throw new Error(data.error);
      setResult(data);
      onNewPrediction();
      showToast("Prediction complete — "+data.risk_level+" risk ("+data.churn_pct+"%)", "success");
    } catch(err) {
      showToast("API error: "+err.message+" — Is python api.py running?", "error");
      /* fallback local estimate */
      const t=Number(form.tenure)||0, m=Number(form.total_spent)||0;
      let p=0.5;
      if(form.membership==="Bronze") p+=0.2;
      if(form.membership==="Gold")   p-=0.2;
      if(t<6) p+=0.15; if(t>36) p-=0.15;
      if(Number(form.support_calls)>6) p+=0.1;
      if(Number(form.days_since)>180)  p+=0.1;
      p=Math.min(0.96,Math.max(0.04,p+(Math.random()-.5)*.1));
      const risk=p>0.7?"High":p>0.4?"Medium":"Low";
      setResult({churn_prob:p,churn_pct:(p*100).toFixed(1),risk_level:risk,risk_color:rc(risk),will_churn:p>=0.5?"Will Churn":"Will Stay",confidence:(Math.max(p,1-p)*100).toFixed(1),insights:["⚠️ This is a local estimate — start python api.py for real predictions."],customer_id:form.customer_id||"LOCAL"});
    }
    setLoading(false);
  };

  const FL = ({label, children}) => (
    <div>
      <label style={{display:"block",fontSize:11,fontWeight:600,marginBottom:6,textTransform:"uppercase",letterSpacing:"0.06em",color:"#94a3b8"}}>{label}</label>
      {children}
    </div>
  );
  const secS = {background:"#1e293b",border:"1px solid #334155",borderRadius:14,padding:20,marginBottom:14};

  return (
    <div style={{padding:28,maxWidth:880,margin:"0 auto"}}>
      <div style={{textAlign:"center",marginBottom:28}}>
        <div className="g1 glow-i" style={{width:54,height:54,borderRadius:14,display:"flex",alignItems:"center",justifyContent:"center",margin:"0 auto 12px"}}>
          <Ic d={I.predict} size={26} color="white"/>
        </div>
        <h2 style={{fontSize:24,fontWeight:900,color:"white"}}>AI Churn Predictor</h2>
        <p style={{fontSize:13,color:"#94a3b8",marginTop:6}}>Fill in customer details to get a real ML-powered churn probability score</p>
      </div>

      <form id="churn-prediction-form" onSubmit={predict}>
        {/* Section 1 */}
        <div style={secS}>
          <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:18}}>
            <span style={{width:20,height:20,borderRadius:"50%",background:"rgba(99,102,241,.2)",border:"1px solid rgba(99,102,241,.4)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:11,fontWeight:700,color:"#818cf8",flexShrink:0}}>1</span>
            <h3 style={{fontSize:11,fontWeight:700,textTransform:"uppercase",letterSpacing:"0.1em",color:"#818cf8"}}>Customer Information</h3>
          </div>
          <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(200px,1fr))",gap:14}}>
            <FL label="Customer Name"><input id="f-name" className="inp" placeholder="e.g. John Smith" value={form.name} onChange={e=>upd("name",e.target.value)}/></FL>
            <FL label="Customer ID"><input id="f-cid" className="inp" placeholder="e.g. C-2048 (optional)" value={form.customer_id} onChange={e=>upd("customer_id",e.target.value)}/></FL>
            <FL label="Age">
              <input id="f-age" type="number" min="18" max="100" className="inp" value={form.age} onChange={e=>upd("age",e.target.value)} required/>
            </FL>
            <FL label="Tenure (months)">
              <input id="f-tenure" type="number" min="0" max="120" className="inp" value={form.tenure} onChange={e=>upd("tenure",e.target.value)} required/>
            </FL>
            <FL label="Total Amount Spent ($)">
              <input id="f-spent" type="number" min="0" step="0.01" className="inp" value={form.total_spent} onChange={e=>upd("total_spent",e.target.value)} required/>
            </FL>
            <FL label="Avg Order Value ($)">
              <input id="f-order" type="number" min="0" step="0.01" className="inp" value={form.avg_order} onChange={e=>upd("avg_order",e.target.value)} required/>
            </FL>
          </div>
        </div>

        {/* Section 2 */}
        <div style={secS}>
          <div style={{display:"flex",alignItems:"center",gap:8,marginBottom:18}}>
            <span style={{width:20,height:20,borderRadius:"50%",background:"rgba(99,102,241,.2)",border:"1px solid rgba(99,102,241,.4)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:11,fontWeight:700,color:"#818cf8",flexShrink:0}}>2</span>
            <h3 style={{fontSize:11,fontWeight:700,textTransform:"uppercase",letterSpacing:"0.1em",color:"#818cf8"}}>Behaviour & Membership</h3>
          </div>
          <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(200px,1fr))",gap:14}}>
            <FL label="Purchase Frequency / Year">
              <input id="f-freq" type="number" min="0" max="365" className="inp" value={form.purchase_freq} onChange={e=>upd("purchase_freq",e.target.value)} required/>
            </FL>
            <FL label="Days Since Last Purchase">
              <input id="f-days" type="number" min="0" max="730" className="inp" value={form.days_since} onChange={e=>upd("days_since",e.target.value)} required/>
            </FL>
            <FL label="Membership Tier">
              <select id="f-membership" className="inp sel" value={form.membership} onChange={e=>upd("membership",e.target.value)}>
                <option>Bronze</option><option>Silver</option><option>Gold</option>
              </select>
            </FL>
            <FL label="Support Calls">
              <input id="f-support" type="number" min="0" max="50" className="inp" value={form.support_calls} onChange={e=>upd("support_calls",e.target.value)} required/>
            </FL>
          </div>
        </div>

        <button id="predict-btn" type="submit" disabled={loading}
          style={{width:"100%",padding:14,borderRadius:12,border:"none",fontWeight:700,fontSize:14,color:"white",cursor:loading?"not-allowed":"pointer",background:loading?"#334155":"linear-gradient(135deg,#6366f1,#4f46e5)",boxShadow:loading?"none":"0 4px 22px rgba(99,102,241,.45)",transition:"all .3s"}}>
          {loading
            ? <span style={{display:"flex",alignItems:"center",justifyContent:"center",gap:10}}>
                <svg className="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M23 4v6h-6"/><path d="M1 20v-6h6"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                Running ML Model…
              </span>
            : "⚡  Predict Churn Probability"}
        </button>
      </form>

      {/* Result */}
      {result && (
        <div style={{marginTop:20,padding:24,borderRadius:16,animation:"fadeUp .4s ease",
          background:result.risk_level==="High"?"linear-gradient(135deg,rgba(244,63,94,.13),rgba(244,63,94,.04))":result.risk_level==="Medium"?"linear-gradient(135deg,rgba(245,158,11,.13),rgba(245,158,11,.04))":"linear-gradient(135deg,rgba(16,185,129,.13),rgba(16,185,129,.04))",
          border:"1px solid "+(result.risk_level==="High"?"rgba(244,63,94,.38)":result.risk_level==="Medium"?"rgba(245,158,11,.38)":"rgba(16,185,129,.38)")}}>

          <div style={{display:"flex",gap:24,flexWrap:"wrap",alignItems:"center"}}>
            {/* Score */}
            <div style={{textAlign:"center",minWidth:130}}>
              <div style={{fontSize:54,fontWeight:900,color:rc(result.risk_level),lineHeight:1}}>{result.churn_pct}%</div>
              <div style={{fontSize:12,color:"#94a3b8",marginTop:4}}>Churn Probability</div>
              <div style={{fontSize:11,marginTop:4,fontWeight:600,color:result.will_churn==="Will Churn"?"#f43f5e":"#10b981"}}>{result.will_churn}</div>
            </div>
            {/* Details */}
            <div style={{flex:1,minWidth:220}}>
              <span className={"px-3 py-1 rounded-full text-sm font-bold "+rb(result.risk_level)} style={{display:"inline-block",marginBottom:12}}>
                {result.risk_level==="High"?"🔴":result.risk_level==="Medium"?"🟡":"🟢"} {result.risk_level} Risk
              </span>
              <div className="prog" style={{marginBottom:12}}>
                <div className="progf" style={{width:result.churn_pct+"%",background:result.risk_level==="High"?"linear-gradient(90deg,#f43f5e,#be123c)":result.risk_level==="Medium"?"linear-gradient(90deg,#f59e0b,#b45309)":"linear-gradient(90deg,#10b981,#047857)"}}/>
              </div>
              <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:8,marginBottom:14}}>
                <div style={{padding:10,borderRadius:8,background:"rgba(15,23,42,.5)",border:"1px solid rgba(51,65,85,.5)"}}>
                  <div style={{fontSize:10,color:"#64748b",marginBottom:3}}>Confidence</div>
                  <div style={{fontSize:14,fontWeight:700,color:"white"}}>{result.confidence}%</div>
                </div>
                <div style={{padding:10,borderRadius:8,background:"rgba(15,23,42,.5)",border:"1px solid rgba(51,65,85,.5)"}}>
                  <div style={{fontSize:10,color:"#64748b",marginBottom:3}}>Customer ID</div>
                  <div style={{fontSize:13,fontWeight:700,color:"#818cf8"}}>{result.customer_id}</div>
                </div>
              </div>
            </div>
          </div>

          {/* Insights */}
          {result.insights && result.insights.length>0 && (
            <div style={{marginTop:18}}>
              <div style={{fontSize:12,fontWeight:700,color:"#94a3b8",textTransform:"uppercase",letterSpacing:"0.08em",marginBottom:10}}>💡 AI Insights</div>
              <div style={{display:"flex",flexDirection:"column",gap:8}}>
                {result.insights.map((ins,i)=>(
                  <div key={i} style={{padding:"10px 14px",borderRadius:9,background:"rgba(99,102,241,.1)",border:"1px solid rgba(99,102,241,.2)",fontSize:12,color:"#cbd5e1",lineHeight:1.55}}>{ins}</div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

/* ════════════════════════════════════
   ANALYTICS PAGE
════════════════════════════════════ */
function AnalyticsPage({modelInfo, featureImportance}) {
  const metrics = modelInfo ? [
    {label:"Model Accuracy",  val:modelInfo.accuracy+"%",  sub:modelInfo.model_type,   color:"#6366f1"},
    {label:"Precision",       val:modelInfo.precision+"%", sub:"True positive rate",    color:"#10b981"},
    {label:"Recall Score",    val:modelInfo.recall+"%",    sub:"Sensitivity metric",    color:"#f59e0b"},
    {label:"F1 Score",        val:modelInfo.f1_score+"%",  sub:"Harmonic mean",          color:"#38bdf8"},
  ] : [
    {label:"Model Accuracy",  val:"91.4%", sub:"XGBoost + RF Ensemble", color:"#6366f1"},
    {label:"Precision",       val:"88.2%", sub:"True positive rate",    color:"#10b981"},
    {label:"Recall Score",    val:"85.7%", sub:"Sensitivity metric",    color:"#f59e0b"},
    {label:"F1 Score",        val:"86.9%", sub:"Harmonic mean",          color:"#38bdf8"},
  ];
  return (
    <div style={{padding:28,display:"flex",flexDirection:"column",gap:22}}>
      <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fit,minmax(180px,1fr))",gap:16}}>
        {metrics.map((m,i)=>(
          <div key={m.label} className="fadeUp card" style={{padding:20,animationDelay:i*70+"ms"}}>
            <div style={{fontSize:30,fontWeight:900,color:m.color,marginBottom:4}}>{m.val}</div>
            <div style={{fontSize:13,fontWeight:700,color:"white"}}>{m.label}</div>
            <div style={{fontSize:11,color:"#64748b",marginTop:2}}>{m.sub}</div>
          </div>
        ))}
      </div>
      <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:16}}>
        <div className="card" style={{padding:22}}>
          <h3 style={{fontSize:14,fontWeight:700,color:"white",marginBottom:3}}>Feature Importance</h3>
          <p style={{fontSize:11,color:"#64748b",marginBottom:16}}>
            {featureImportance?"Live from trained model":"Start api.py to load live data"}
          </p>
          {featureImportance
            ? <FiChart data={featureImportance}/>
            : (
              <div style={{display:"flex",flexDirection:"column",gap:12}}>
                {[["Tenure",85],["Purchase Freq",78],["Days Since",72],["Total Spent",68],["Membership",61],["Support Calls",55],["Avg Order",42],["Age",35]].map(([n,p])=>(
                  <div key={n}>
                    <div style={{display:"flex",justifyContent:"space-between",marginBottom:5}}>
                      <span style={{fontSize:12,color:"#cbd5e1",fontWeight:500}}>{n}</span>
                      <span style={{fontSize:12,fontWeight:700,color:"#6366f1"}}>{p}%</span>
                    </div>
                    <div className="prog"><div className="progf" style={{width:p+"%",background:"#6366f1"}}/></div>
                  </div>
                ))}
              </div>
            )
          }
        </div>
        <div className="card" style={{padding:22}}>
          <h3 style={{fontSize:14,fontWeight:700,color:"white",marginBottom:3}}>Monthly Trend</h3>
          <p style={{fontSize:11,color:"#64748b",marginBottom:14}}>Churned vs Retained customers</p>
          <LineChart height={310}/>
        </div>
      </div>
    </div>
  );
}

/* ════════════════════════════════════
   CUSTOMERS PAGE
════════════════════════════════════ */
function CustomersPage({history}) {
  const defaultData = [
    {name:"Sarah Mitchell", email:"sarah.m@email.com", status:"At Risk",val:"$89.45", joined:"Mar 2025",av:"SM"},
    {name:"James Patterson",email:"james.p@email.com", status:"Active", val:"$54.20", joined:"Jun 2024",av:"JP"},
    {name:"Emma Rodriguez", email:"emma.r@email.com",  status:"Active", val:"$112.00",joined:"Aug 2022",av:"ER"},
    {name:"Michael Chen",   email:"michael.c@email.com",status:"At Risk",val:"$79.80",joined:"Jan 2026",av:"MC"},
    {name:"Olivia Turner",  email:"olivia.t@email.com",status:"Active", val:"$66.30", joined:"Nov 2024",av:"OT"},
    {name:"David Kim",      email:"david.k@email.com", status:"Active", val:"$95.10", joined:"Mar 2021",av:"DK"},
    {name:"Priya Sharma",   email:"priya.s@email.com", status:"Churned",val:"$45.00", joined:"Apr 2025",av:"PS"},
  ];
  const histData = history.map(h=>({
    name: h.name||"Customer", email:"—", status: h.risk==="High"?"At Risk":h.cp>=0.5?"Churned":"Active",
    val: "$"+(h.mc||0).toFixed(2), joined:h.date, av:(h.name||h.id||"?").split(" ").map(n=>n[0]).join("").slice(0,2).toUpperCase()
  }));
  const combined = [...histData, ...defaultData].slice(0,12);
  const sc = s => s==="At Risk"?"bh":s==="Active"?"bl":"bm";
  return (
    <div style={{padding:28,display:"flex",flexDirection:"column",gap:18}}>
      <div style={{display:"flex",alignItems:"center",justifyContent:"space-between"}}>
        <div>
          <h2 style={{fontSize:18,fontWeight:800,color:"white"}}>Customer Directory</h2>
          <p style={{fontSize:12,color:"#94a3b8",marginTop:3}}>Manage and monitor all customers · {combined.length} shown</p>
        </div>
        <button style={{padding:"9px 18px",borderRadius:10,border:"none",fontWeight:700,fontSize:13,color:"white",cursor:"pointer",background:"linear-gradient(135deg,#6366f1,#4f46e5)",boxShadow:"0 4px 16px rgba(99,102,241,.38)"}}>+ Add Customer</button>
      </div>
      <div className="card" style={{overflow:"hidden"}}>
        <table style={{width:"100%",fontSize:13,borderCollapse:"collapse"}}>
          <thead>
            <tr style={{background:"rgba(15,23,42,.6)",borderBottom:"1px solid #334155"}}>
              {["Customer","Email","Status","Monthly","Joined","Action"].map(h=>(
                <th key={h} style={{padding:"13px 20px",textAlign:"left",fontSize:11,fontWeight:600,color:"#64748b",textTransform:"uppercase",letterSpacing:"0.06em"}}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {combined.map((c,i)=>(
              <tr key={i} className="trow" style={{borderBottom:"1px solid rgba(51,65,85,.3)"}}>
                <td style={{padding:"13px 20px"}}>
                  <div style={{display:"flex",alignItems:"center",gap:10}}>
                    <div style={{width:36,height:36,borderRadius:"50%",background:`hsl(${i*47},62%,40%)`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:12,fontWeight:700,color:"white",flexShrink:0}}>{c.av}</div>
                    <span style={{fontWeight:600,color:"white",fontSize:13}}>{c.name}</span>
                  </div>
                </td>
                <td style={{padding:"13px 20px",fontSize:12,color:"#94a3b8"}}>{c.email}</td>
                <td style={{padding:"13px 20px"}}><span className={"px-2 py-1 rounded-full text-xs font-semibold "+sc(c.status)}>{c.status}</span></td>
                <td style={{padding:"13px 20px",fontSize:13,fontWeight:700,color:"white"}}>{c.val}</td>
                <td style={{padding:"13px 20px",fontSize:11,color:"#64748b"}}>{c.joined}</td>
                <td style={{padding:"13px 20px"}}><button style={{fontSize:12,fontWeight:600,color:"#818cf8",background:"none",border:"none",cursor:"pointer"}}>Predict →</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

/* ════════════════════════════════════
   SETTINGS PAGE
════════════════════════════════════ */
function SettingsPage({modelInfo}) {
  const [threshold,setThreshold]=useState(70);
  const [notifyOn,setNotifyOn]=useState(true);
  const [autoRetrain,setAutoRetrain]=useState(false);

  function Toggle({val,onChange}){
    return(
      <div onClick={()=>onChange(!val)} style={{width:44,height:24,borderRadius:12,background:val?"#6366f1":"#334155",position:"relative",cursor:"pointer",transition:"background .2s",flexShrink:0}}>
        <div style={{position:"absolute",top:3,left:val?22:3,width:18,height:18,borderRadius:"50%",background:"white",transition:"left .22s",boxShadow:"0 1px 4px rgba(0,0,0,.3)"}}/>
      </div>
    );
  }

  const cS={background:"#1e293b",border:"1px solid #334155",borderRadius:14,padding:22,marginBottom:16};
  const rS={display:"flex",alignItems:"center",justifyContent:"space-between",paddingTop:16,borderTop:"1px solid #334155",marginTop:16};

  return(
    <div style={{padding:28,maxWidth:660}}>
      {modelInfo&&(
        <div className="card" style={{padding:22,marginBottom:16,background:"linear-gradient(135deg,rgba(99,102,241,.1),rgba(99,102,241,.04))"}}>
          <h3 style={{fontSize:14,fontWeight:700,color:"white",marginBottom:14}}>🤖 Live Model Info</h3>
          <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:10}}>
            {[["Type",modelInfo.model_type],["Accuracy",modelInfo.accuracy+"%"],["ROC-AUC",(modelInfo.roc_auc||0).toFixed(3)],["Features",modelInfo.features?.length||8]].map(([k,v])=>(
              <div key={k} style={{padding:10,borderRadius:8,background:"rgba(15,23,42,.6)",border:"1px solid rgba(51,65,85,.5)"}}>
                <div style={{fontSize:10,color:"#64748b",marginBottom:3}}>{k}</div>
                <div style={{fontSize:13,fontWeight:700,color:"#818cf8"}}>{v}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div style={cS}>
        <h3 style={{fontSize:14,fontWeight:700,color:"white",marginBottom:3}}>Model Configuration</h3>
        <p style={{fontSize:11,color:"#64748b",marginBottom:20}}>Tune AI prediction thresholds and behaviour</p>
        <label style={{display:"block",fontSize:11,fontWeight:600,textTransform:"uppercase",letterSpacing:"0.06em",color:"#94a3b8",marginBottom:10}}>
          High-Risk Threshold: <span style={{color:"#818cf8"}}>{threshold}%</span>
        </label>
        <input type="range" min="50" max="90" value={threshold} onChange={e=>setThreshold(Number(e.target.value))} style={{width:"100%",accentColor:"#6366f1"}}/>
        <div style={{display:"flex",justifyContent:"space-between",fontSize:11,color:"#475569",marginTop:4}}><span>50%</span><span>90%</span></div>
        <div style={rS}>
          <div><div style={{fontSize:13,fontWeight:600,color:"white"}}>High-Risk Notifications</div><div style={{fontSize:11,color:"#64748b",marginTop:2}}>Send alerts when customer exceeds risk threshold</div></div>
          <Toggle val={notifyOn} onChange={setNotifyOn}/>
        </div>
        <div style={rS}>
          <div><div style={{fontSize:13,fontWeight:600,color:"white"}}>Auto Retrain Model</div><div style={{fontSize:11,color:"#64748b",marginTop:2}}>Automatically retrain on new data each month</div></div>
          <Toggle val={autoRetrain} onChange={setAutoRetrain}/>
        </div>
      </div>

      <div style={cS}>
        <h3 style={{fontSize:14,fontWeight:700,color:"white",marginBottom:3}}>API Configuration</h3>
        <p style={{fontSize:11,color:"#64748b",marginBottom:20}}>Flask backend connection settings</p>
        <div style={{display:"flex",flexDirection:"column",gap:14}}>
          <div>
            <label style={{display:"block",fontSize:11,fontWeight:600,textTransform:"uppercase",letterSpacing:"0.06em",color:"#94a3b8",marginBottom:6}}>API Endpoint</label>
            <input className="inp" defaultValue={API}/>
          </div>
          <div>
            <label style={{display:"block",fontSize:11,fontWeight:600,textTransform:"uppercase",letterSpacing:"0.06em",color:"#94a3b8",marginBottom:6}}>API Key</label>
            <input className="inp" type="password" defaultValue="sk-churnguard-2026"/>
          </div>
          <button style={{alignSelf:"flex-start",padding:"9px 20px",borderRadius:10,border:"none",fontWeight:700,fontSize:13,color:"white",cursor:"pointer",background:"linear-gradient(135deg,#6366f1,#4f46e5)"}}>Save Configuration</button>
        </div>
      </div>

      <div style={{padding:20,borderRadius:14,background:"rgba(244,63,94,.07)",border:"1px solid rgba(244,63,94,.26)"}}>
        <h3 style={{fontSize:14,fontWeight:700,color:"#f43f5e",marginBottom:3}}>Danger Zone</h3>
        <p style={{fontSize:11,color:"#94a3b8",marginBottom:16}}>These actions are irreversible — proceed with caution</p>
        <div style={{display:"flex",gap:10}}>
          <button style={{padding:"8px 16px",borderRadius:10,border:"1px solid rgba(244,63,94,.4)",background:"transparent",color:"#f43f5e",fontWeight:700,fontSize:12,cursor:"pointer"}}>Clear History</button>
          <button style={{padding:"8px 16px",borderRadius:10,border:"1px solid rgba(244,63,94,.4)",background:"transparent",color:"#f43f5e",fontWeight:700,fontSize:12,cursor:"pointer"}}>Reset Model</button>
        </div>
      </div>
    </div>
  );
}

/* ════════════════════════════════════
   APP ROOT
════════════════════════════════════ */
function App() {
  const [page, setPage]                   = useState("dashboard");
  const [apiStatus, setApiStatus]         = useState("connecting");
  const [stats, setStats]                 = useState(null);
  const [history, setHistory]             = useState([]);
  const [modelInfo, setModelInfo]         = useState(null);
  const [featureImportance, setFI]        = useState(null);
  const [toast, setToast]                 = useState(null);
  const [notif]                           = useState(3);

  const showToast = useCallback((msg, type="info") => setToast({msg,type}), []);

  /* Poll API */
  const refreshData = useCallback(async () => {
    try {
      const [hRes, sRes, fiRes, mRes] = await Promise.all([
        fetch(API+"/history"),
        fetch(API+"/stats"),
        fetch(API+"/feature-importance"),
        fetch(API+"/model-info"),
      ]);
      setHistory((await hRes.json()).predictions || []);
      setStats(await sRes.json());
      setFI((await fiRes.json()).feature_importance || null);
      setModelInfo(await mRes.json());
      setApiStatus("ok");
    } catch {
      setApiStatus("error");
    }
  }, []);

  /* Initial check */
  useEffect(()=>{
    refreshData();
    const t = setInterval(refreshData, 15000);
    return ()=>clearInterval(t);
  },[refreshData]);

  const onNewPrediction = useCallback(()=>{ refreshData(); }, [refreshData]);

  function renderPage() {
    if (page==="dashboard") return <DashboardPage stats={stats} history={history} apiStatus={apiStatus}/>;
    if (page==="predict")   return <PredictPage onNewPrediction={onNewPrediction} showToast={showToast}/>;
    if (page==="analytics") return <AnalyticsPage modelInfo={modelInfo} featureImportance={featureImportance}/>;
    if (page==="customers") return <CustomersPage history={history}/>;
    if (page==="settings")  return <SettingsPage modelInfo={modelInfo}/>;
    return <DashboardPage stats={stats} history={history} apiStatus={apiStatus}/>;
  }

  return (
    <div style={{display:"flex",fontFamily:"'Inter',sans-serif"}}>
      <Sidebar page={page} setPage={setPage} apiStatus={apiStatus}/>
      <div className="main-wrap">
        <Topbar page={page} notif={notif}/>
        <main style={{flex:1,overflowY:"auto"}}>
          {renderPage()}
        </main>
      </div>
      {toast && <Toast msg={toast.msg} type={toast.type} onClose={()=>setToast(null)}/>}
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App/>);
</script>
</body>
</html>"""

out = pathlib.Path(r"c:\Users\banga\OneDrive\New folder\ECOMMMER\customer-churn-prediction\frontend\index.html")
out.write_text(HTML, encoding="utf-8")
print(f"Frontend written: {out.stat().st_size:,} bytes")
