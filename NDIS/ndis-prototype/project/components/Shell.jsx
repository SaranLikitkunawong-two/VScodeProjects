/* Shared small UI pieces: Nav, Footer, Brand, Tweaks, icons */

const Icon = {
  arrow: (props) => (
    <svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden {...props}>
      <path d="M4 10h12M11 5l5 5-5 5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  check: (props) => (
    <svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden {...props}>
      <path d="M4 10.5l4 4 8-9" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
  ),
  close: (props) => (
    <svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden {...props}>
      <path d="M5 5l10 10M15 5L5 15" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    </svg>
  ),
  info: (props) => (
    <svg width="14" height="14" viewBox="0 0 20 20" fill="none" aria-hidden {...props}>
      <circle cx="10" cy="10" r="8" stroke="currentColor" strokeWidth="1.6"/>
      <path d="M10 9v5M10 6.5v.5" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round"/>
    </svg>
  ),
};

function Brand({ className = 'brand' }) {
  return (
    <a className={className} href="#/" onClick={(e)=>{e.preventDefault(); window.navigate('home');}}>
      <span className="brand-mark" aria-hidden></span>
      <span>Future Forward Planning</span>
    </a>
  );
}

function Nav({ route }) {
  const go = (r, e) => { e.preventDefault(); window.navigate(r); };
  return (
    <header className="nav" role="banner">
      <div className="container nav-inner">
        <Brand />
        <nav className="nav-links" aria-label="Primary">
          <a className={`nav-link ${route==='home'?'active':''}`}   href="#/"       onClick={(e)=>go('home',e)}>Home</a>
          <a className={`nav-link ${route==='news'?'active':''}`}   href="#/news"   onClick={(e)=>go('news',e)}>News</a>
          <a className={`nav-link ${route==='signup'?'active':''}`} href="#/signup" onClick={(e)=>go('signup',e)}>Sign up</a>
          <a className="btn btn-primary nav-cta" href="#/signup" onClick={(e)=>go('signup',e)}>
            Join the waitlist <Icon.arrow />
          </a>
        </nav>
      </div>
    </header>
  );
}

function Footer() {
  const go = (r, e) => { e.preventDefault(); window.navigate(r); };
  return (
    <footer className="footer" role="contentinfo">
      <div className="container">
        <div className="cols">
          <div>
            <Brand className="brand" />
            <p className="fine" style={{marginTop:12}}>
              Independent NDIS plan management for Australian participants. Future Forward Planning
              pays your providers, tracks your plan, and keeps your records straight.
            </p>
          </div>
          <div>
            <h5>Product</h5>
            <a href="#/" onClick={(e)=>go('home',e)}>How we help</a>
            <a href="#/" onClick={(e)=>go('home',e)}>Budget tool</a>
            <a href="#/signup" onClick={(e)=>go('signup',e)}>Join the waitlist</a>
          </div>
          <div>
            <h5>Resources</h5>
            <a href="#/news" onClick={(e)=>go('news',e)}>News &amp; updates</a>
            <a href="#/news" onClick={(e)=>go('news',e)}>Participant guides</a>
            <a href="#/news" onClick={(e)=>go('news',e)}>For referrers</a>
          </div>
          <div>
            <h5>Contact</h5>
            <a href="mailto:hello@futureforwardplanning.example">hello@futureforwardplanning.example</a>
            <a href="tel:+61000000000">1800 000 000</a>
            <a href="#">Melbourne, VIC</a>
          </div>
        </div>
        <div className="bottom">
          <span>© 2026 Future Forward Planning Pty Ltd. ABN pending.</span>
          <span>Registered NDIS plan manager (coming soon)</span>
        </div>
      </div>
    </footer>
  );
}

/* ---------- Tweaks panel (edit-mode) ---------- */
function Tweaks({ active, tweaks, setTweaks, onClose }) {
  if (!active) return null;
  const update = (k, v) => {
    const next = { ...tweaks, [k]: v };
    setTweaks(next);
    try {
      window.parent.postMessage({ type: '__edit_mode_set_keys', edits: { [k]: v } }, '*');
    } catch (e) {}
  };
  return (
    <aside className="tweaks" aria-label="Tweaks panel">
      <div className="tweaks-hd">
        <span>Tweaks</span>
        <button onClick={onClose} aria-label="Close tweaks"><Icon.close/></button>
      </div>
      <div className="tweaks-bd">
        <div className="tweak-row">
          <label>Hero layout</label>
          <div className="seg">
            {['split','stacked'].map(v =>
              <button key={v} className={tweaks.heroLayout===v?'on':''} onClick={()=>update('heroLayout', v)}>
                {v === 'split' ? 'Split' : 'Stacked'}
              </button>
            )}
          </div>
        </div>
        <div className="tweak-row">
          <label>Hero visual</label>
          <div className="seg">
            {['plan','chart','grid'].map(v =>
              <button key={v} className={tweaks.heroArt===v?'on':''} onClick={()=>update('heroArt', v)}>
                {v === 'plan' ? 'Plan' : v === 'chart' ? 'Chart' : 'Grid'}
              </button>
            )}
          </div>
        </div>
        <div className="tweak-row">
          <label>Accent colour</label>
          <div className="swatches">
            {[
              ['#00897B','teal'],
              ['#2E7D6A','forest'],
              ['#0277BD','azure'],
              ['#5E35B1','violet'],
            ].map(([c, name]) =>
              <button key={c} title={name}
                      className={tweaks.accent===c?'on':''}
                      style={{background: c}}
                      onClick={()=>update('accent', c)}/>
            )}
          </div>
        </div>
        <div className="tweak-row">
          <label>Corner radius</label>
          <div className="seg">
            {['sharp','soft','round'].map(v =>
              <button key={v} className={tweaks.radius===v?'on':''} onClick={()=>update('radius', v)}>
                {v[0].toUpperCase()+v.slice(1)}
              </button>
            )}
          </div>
        </div>
      </div>
    </aside>
  );
}

Object.assign(window, { Icon, Brand, Nav, Footer, Tweaks });
