/* Hero art variants — all built from CSS/SVG, no imagery. */

function HeroArtPlan() {
  const rows = [
    { name: 'Core supports',         pct: 62, amt: '$18,420', color: '#00897B' },
    { name: 'Capacity building',     pct: 41, amt: '$7,180',  color: '#7986CB' },
    { name: 'Capital supports',      pct: 28, amt: '$2,940',  color: '#B6E3DD' },
    { name: 'Consumables & travel',  pct: 55, amt: '$1,210',  color: '#C5CAE9' },
  ];
  return (
    <div className="plan-stack">
      <div style={{display:'flex', justifyContent:'space-between', alignItems:'center', marginBottom: 14, color:'rgba(255,255,255,0.75)', fontSize: 12, letterSpacing:'0.08em', textTransform:'uppercase'}}>
        <span>Plan summary</span>
        <span>FY 25/26</span>
      </div>
      {rows.map(r => (
        <div className="plan-line" key={r.name}>
          <div style={{flex:1}}>
            <div style={{display:'flex', alignItems:'center', gap:10, justifyContent:'space-between'}}>
              <div style={{display:'flex', alignItems:'center', gap:10}}>
                <span className="swatch" style={{background: r.color}}></span>
                <span>{r.name}</span>
              </div>
              <span className="amt">{r.amt}</span>
            </div>
            <div className="bar"><span style={{width: r.pct+'%', background: r.color}}></span></div>
          </div>
        </div>
      ))}
      <div className="plan-totals">
        <div>
          <div className="k">Avg / month</div>
          <div className="v">$2,479</div>
        </div>
        <div>
          <div className="k">Status</div>
          <div className="v" style={{display:'flex', alignItems:'center', gap:8}}>
            <span style={{width:8, height:8, borderRadius:'50%', background:'#5CE1C1'}}></span>
            On track
          </div>
        </div>
      </div>
    </div>
  );
}

function HeroArtChart() {
  // 12-month spend vs budget line chart, pure SVG
  const budget = Array.from({length: 12}, (_,i) => 100 - (i * (100/12)));
  const spend = [96, 87, 79, 74, 66, 60, 55, 50, 44, 38, 32, 24];
  const w = 520, h = 300, pad = 28;
  const x = i => pad + (i/(11)) * (w - pad*2);
  const y = v => h - pad - (v/100) * (h - pad*2);
  const toPath = arr => arr.map((v,i) => (i===0?'M':'L') + x(i).toFixed(1) + ' ' + y(v).toFixed(1)).join(' ');
  return (
    <div style={{width:'100%', height:'100%'}}>
      <div style={{display:'flex', justifyContent:'space-between', marginBottom: 8, color:'rgba(255,255,255,0.75)', fontSize: 12, letterSpacing:'0.08em', textTransform:'uppercase'}}>
        <span>Budget runway</span>
        <span>12 months</span>
      </div>
      <svg viewBox={`0 0 ${w} ${h}`} width="100%" style={{display:'block'}}>
        {[0,25,50,75,100].map(p => (
          <line key={p} x1={pad} x2={w-pad} y1={y(p)} y2={y(p)} stroke="rgba(255,255,255,0.1)"/>
        ))}
        <path d={toPath(budget)} stroke="rgba(255,255,255,0.5)" strokeWidth="1.5" strokeDasharray="4 4" fill="none"/>
        <path d={toPath(spend)} stroke="#00897B" strokeWidth="3" fill="none"/>
        <path d={toPath(spend) + ` L ${x(11)} ${y(0)} L ${x(0)} ${y(0)} Z`} fill="rgba(0,137,123,0.22)"/>
        {spend.map((v,i) => i%3===0 ? <circle key={i} cx={x(i)} cy={y(v)} r="3.5" fill="#fff"/> : null)}
        <text x={pad} y={h-8} fill="rgba(255,255,255,0.6)" fontSize="10">Jul</text>
        <text x={w-pad} y={h-8} textAnchor="end" fill="rgba(255,255,255,0.6)" fontSize="10">Jun</text>
      </svg>
      <div className="plan-totals" style={{marginTop:14}}>
        <div><div className="k">Plan remaining</div><div className="v">$6,842</div></div>
        <div><div className="k">Days left</div><div className="v">73</div></div>
      </div>
    </div>
  );
}

function HeroArtGrid() {
  const tiles = [
    { k: 'Invoices paid', v: '147' },
    { k: 'This month',    v: '$3,204' },
    { k: 'Providers',     v: '12' },
    { k: 'Plan remaining',v: '$6,842' },
  ];
  return (
    <div>
      <div style={{display:'flex', justifyContent:'space-between', marginBottom: 14, color:'rgba(255,255,255,0.75)', fontSize: 12, letterSpacing:'0.08em', textTransform:'uppercase'}}>
        <span>Monthly snapshot</span>
        <span>March 2026</span>
      </div>
      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:10, marginBottom: 14}}>
        {tiles.map(t => (
          <div key={t.k} style={{padding: 14, borderRadius: 10, background:'rgba(255,255,255,0.08)', border:'1px solid rgba(255,255,255,0.1)'}}>
            <div style={{fontSize: 11, color:'rgba(255,255,255,0.6)', textTransform:'uppercase', letterSpacing:'0.08em'}}>{t.k}</div>
            <div style={{fontSize: 22, fontWeight: 600, color:'#fff', marginTop: 4, letterSpacing:'-0.01em'}}>{t.v}</div>
          </div>
        ))}
      </div>
      <div style={{padding: 14, borderRadius: 10, background:'rgba(255,255,255,0.08)', border:'1px solid rgba(255,255,255,0.1)'}}>
        <div style={{display:'flex', justifyContent:'space-between', fontSize: 12, color:'rgba(255,255,255,0.7)', marginBottom: 8}}>
          <span>Core supports</span><span>62% used</span>
        </div>
        <div style={{height: 8, background:'rgba(255,255,255,0.15)', borderRadius: 999, overflow:'hidden'}}>
          <div style={{width:'62%', height:'100%', background:'#00897B'}}></div>
        </div>
      </div>
    </div>
  );
}

function HeroArt({ variant }) {
  return (
    <div className="hero-art">
      {variant === 'chart' ? <HeroArtChart/> :
       variant === 'grid'  ? <HeroArtGrid/>  :
                             <HeroArtPlan/>}
    </div>
  );
}

Object.assign(window, { HeroArt });
