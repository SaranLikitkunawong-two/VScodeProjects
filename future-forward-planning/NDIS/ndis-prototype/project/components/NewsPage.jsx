/* News / updates page */

const ARTICLES = [
  {
    slug: 'pricing-2026',
    featured: true,
    cat: 'Regulatory',
    title: 'What the 2026 NDIS pricing arrangements mean for participants',
    date: '14 April 2026',
    read: '6 min read',
    excerpt: 'A plain-English summary of the updated price guide, the support categories affected, and what participants should ask their plan manager before their next invoice cycle.',
    cover: 'docs',
  },
  {
    slug: 'pacing-core',
    cat: 'Budget updates',
    title: 'Pacing your core supports through the final quarter',
    date: '02 April 2026',
    read: '4 min read',
    excerpt: 'Three simple checks to run on your core supports budget before end of financial year — and when to request a plan variation.',
    cover: 'chart',
  },
  {
    slug: 'switching-plan-manager',
    cat: 'Participant guidance',
    title: 'Switching plan managers mid-plan: what to expect',
    date: '28 March 2026',
    read: '5 min read',
    excerpt: 'Participants can change plan managers at any point in their plan. Here\u2019s the process, typical timelines, and how to avoid double-invoicing.',
    cover: 'swap',
  },
  {
    slug: 'invoice-records',
    cat: 'Compliance',
    title: 'Invoice record-keeping after the 2026 reforms',
    date: '21 March 2026',
    read: '3 min read',
    excerpt: 'The NDIA has tightened documentation expectations for plan-managed invoices. Here\u2019s what providers and participants should keep on file.',
    cover: 'doc',
  },
  {
    slug: 'invoices-held',
    cat: 'Invoicing',
    title: 'Why some invoices get held: a quick walkthrough',
    date: '10 March 2026',
    read: '4 min read',
    excerpt: 'The most common reasons plan-managed invoices are paused, how we resolve them, and what participants can do to speed things up.',
    cover: 'pause',
  },
  {
    slug: 'monthly-statement',
    cat: 'Participant guidance',
    title: 'Reading your monthly statement without the jargon',
    date: '26 February 2026',
    read: '5 min read',
    excerpt: 'A guided tour of the numbers that matter on your monthly plan statement — category balances, claim status, and what "committed" really means.',
    cover: 'sheet',
  },
  {
    slug: 'improved-life-choices',
    cat: 'Regulatory',
    title: 'Changes to Improved Life Choices: what plan managers watch for',
    date: '18 February 2026',
    read: '5 min read',
    excerpt: 'A short explainer on the category that funds plan management, and why getting the right wording on your plan matters at review time.',
    cover: 'note',
  },
];

const COVER_COLORS = {
  docs:  ['#E5E8F4','#3F51B5'],
  chart: ['#D5EAE7','#00897B'],
  swap:  ['#E5E8F4','#3F51B5'],
  doc:   ['#F1F3FA','#3F51B5'],
  pause: ['#D5EAE7','#00897B'],
  sheet: ['#E5E8F4','#3F51B5'],
  note:  ['#D5EAE7','#00897B'],
};

function ArticleCover({ kind }) {
  const [bg, fg] = COVER_COLORS[kind] || ['#E5E8F4','#3F51B5'];
  // Abstract SVG — bars, lines, dots. No medical/childish imagery.
  return (
    <div className="article-cover" style={{background: bg}}>
      <svg width="100%" height="100%" viewBox="0 0 320 180" preserveAspectRatio="xMidYMid slice" aria-hidden>
        {kind === 'docs' && (
          <g>
            <rect x="40"  y="34" width="140" height="112" rx="8" fill="#fff" stroke={fg} strokeOpacity="0.25"/>
            <rect x="60"  y="20" width="140" height="112" rx="8" fill="#fff" stroke={fg} strokeOpacity="0.5"/>
            <rect x="80"  y="8"  width="140" height="112" rx="8" fill="#fff" stroke={fg}/>
            <rect x="96"  y="26" width="108" height="8" rx="3" fill={fg} opacity="0.85"/>
            <rect x="96"  y="42" width="80"  height="6" rx="3" fill={fg} opacity="0.35"/>
            <rect x="96"  y="56" width="92"  height="6" rx="3" fill={fg} opacity="0.35"/>
            <rect x="96"  y="70" width="70"  height="6" rx="3" fill={fg} opacity="0.35"/>
            <rect x="96"  y="88" width="108" height="20" rx="4" fill={fg} opacity="0.12"/>
          </g>
        )}
        {kind === 'chart' && (
          <g>
            <line x1="40" y1="140" x2="280" y2="140" stroke={fg} strokeOpacity="0.25"/>
            <line x1="40" y1="100" x2="280" y2="100" stroke={fg} strokeOpacity="0.15"/>
            <line x1="40" y1="60"  x2="280" y2="60"  stroke={fg} strokeOpacity="0.15"/>
            <path d="M40 120 L80 108 L120 92 L160 76 L200 64 L240 50 L280 42" stroke={fg} strokeWidth="3" fill="none" strokeLinecap="round"/>
            <path d="M40 120 L80 108 L120 92 L160 76 L200 64 L240 50 L280 42 L280 140 L40 140 Z" fill={fg} fillOpacity="0.15"/>
            {[40,80,120,160,200,240,280].map((x,i)=> <circle key={i} cx={x} cy={[120,108,92,76,64,50,42][i]} r="3.5" fill="#fff" stroke={fg} strokeWidth="2"/>)}
          </g>
        )}
        {kind === 'swap' && (
          <g>
            <rect x="60" y="50" width="80" height="80" rx="10" fill="#fff" stroke={fg}/>
            <rect x="180" y="50" width="80" height="80" rx="10" fill="#fff" stroke={fg}/>
            <path d="M140 78 L180 78 M170 68 L180 78 L170 88" stroke={fg} strokeWidth="2.2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
            <path d="M180 102 L140 102 M150 92 L140 102 L150 112" stroke={fg} strokeWidth="2.2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
            <rect x="72" y="68" width="56" height="6" rx="3" fill={fg} opacity="0.6"/>
            <rect x="72" y="82" width="40" height="6" rx="3" fill={fg} opacity="0.25"/>
            <rect x="192" y="68" width="56" height="6" rx="3" fill={fg} opacity="0.6"/>
            <rect x="192" y="82" width="40" height="6" rx="3" fill={fg} opacity="0.25"/>
          </g>
        )}
        {kind === 'doc' && (
          <g>
            <rect x="100" y="30" width="120" height="130" rx="8" fill="#fff" stroke={fg}/>
            <rect x="116" y="48" width="88"  height="8" rx="3" fill={fg} opacity="0.85"/>
            {[66,80,94,108,122,136].map((y,i)=> <rect key={i} x="116" y={y} width={88 - (i*4)} height="4" rx="2" fill={fg} opacity="0.3"/>)}
            <circle cx="220" cy="44" r="14" fill={fg} opacity="0.15"/>
            <path d="M213 44 l5 5 l10 -10" stroke={fg} strokeWidth="2.4" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
          </g>
        )}
        {kind === 'pause' && (
          <g>
            <rect x="60" y="40" width="200" height="100" rx="10" fill="#fff" stroke={fg} strokeOpacity="0.3"/>
            <rect x="80" y="60" width="160" height="8" rx="3" fill={fg} opacity="0.85"/>
            <rect x="80" y="80" width="120" height="6" rx="3" fill={fg} opacity="0.3"/>
            <rect x="80" y="94" width="100" height="6" rx="3" fill={fg} opacity="0.3"/>
            <circle cx="220" cy="108" r="16" fill={fg} opacity="0.15"/>
            <rect x="214" y="100" width="4" height="16" rx="1.5" fill={fg}/>
            <rect x="222" y="100" width="4" height="16" rx="1.5" fill={fg}/>
          </g>
        )}
        {kind === 'sheet' && (
          <g>
            <rect x="60" y="34" width="200" height="112" rx="8" fill="#fff" stroke={fg}/>
            {[54,74,94,114,134].map((y,i)=>
              <g key={i}>
                <line x1="60" y1={y} x2="260" y2={y} stroke={fg} strokeOpacity="0.15"/>
                <rect x="76"  y={y-10} width="50" height="6" rx="3" fill={fg} opacity={0.45 - i*0.05}/>
                <rect x="140" y={y-10} width="30" height="6" rx="3" fill={fg} opacity="0.25"/>
                <rect x="180" y={y-10} width="40" height="6" rx="3" fill={fg} opacity="0.25"/>
                <rect x="230" y={y-10} width={22 + i*4} height="6" rx="3" fill={fg} opacity={0.35 + i*0.1}/>
              </g>
            )}
          </g>
        )}
        {kind === 'note' && (
          <g>
            <rect x="80" y="30" width="160" height="120" rx="8" fill="#fff" stroke={fg}/>
            <circle cx="104" cy="54" r="6" fill={fg}/>
            <rect x="118" y="50" width="100" height="8" rx="3" fill={fg} opacity="0.8"/>
            <rect x="96"  y="74" width="128" height="6" rx="3" fill={fg} opacity="0.3"/>
            <rect x="96"  y="88" width="112" height="6" rx="3" fill={fg} opacity="0.3"/>
            <rect x="96" y="108" width="60" height="20" rx="4" fill={fg} opacity="0.2"/>
          </g>
        )}
      </svg>
    </div>
  );
}

function ArticleCard({ a, featured }) {
  return (
    <article className={`article ${featured?'featured-article':''}`}>
      <ArticleCover kind={a.cover}/>
      <div className="article-body">
        <div className="article-meta">
          <span className="chip chip-teal">{a.cat}</span>
          <span className="dot"></span>
          <span>{a.date}</span>
          <span className="dot"></span>
          <span>{a.read}</span>
        </div>
        <h3>{a.title}</h3>
        <p>{a.excerpt}</p>
        <a href={`#/news/${a.slug}`} className="read-more"
           onClick={(e)=>{ e.preventDefault(); window.navigate('article', a.slug); }}>
          Read more <Icon.arrow/>
        </a>
      </div>
    </article>
  );
}

function NewsPage() {
  const cats = ['All', ...Array.from(new Set(ARTICLES.map(a => a.cat)))];
  const [filter, setFilter] = React.useState('All');
  const filtered = filter === 'All' ? ARTICLES : ARTICLES.filter(a => a.cat === filter);

  return (
    <main id="main">
      <section className="news-hero">
        <div className="container">
          <span className="eyebrow eyebrow-on-slate">News &amp; updates</span>
          <h1>Stay informed with NDIS updates.</h1>
          <p className="lede">
            Plain-English summaries of the pricing changes, compliance shifts, and participant
            guidance we think are worth your time.
          </p>
        </div>
      </section>

      <div className="container">
        <div className="news-controls" role="toolbar" aria-label="Filter articles">
          <div className="filter-chips">
            {cats.map(c =>
              <button key={c}
                      className={`filter-chip ${filter===c?'active':''}`}
                      onClick={()=>setFilter(c)}>
                {c}
              </button>
            )}
          </div>
          <div style={{color: 'var(--ink-3)', fontSize: 13, padding: '0 6px'}}>
            {filtered.length} article{filtered.length===1?'':'s'}
          </div>
        </div>

        <div className="news-grid" style={{paddingBottom: 96}}>
          {filtered.map((a, i) =>
            <ArticleCard key={a.title} a={a} featured={a.featured && filter==='All'} />
          )}
        </div>
      </div>

      <Footer/>
    </main>
  );
}

Object.assign(window, { NewsPage });
