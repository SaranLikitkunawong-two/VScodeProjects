/* Plan budget calculator — segmented (Total / Core / Capacity / Capital) */

function formatAUD(n) {
  if (!isFinite(n)) return '—';
  const v = Math.round(n);
  return (v < 0 ? '-$' : '$') + Math.abs(v).toLocaleString('en-AU');
}

const SEGMENTS = [
  { id: 'total',    label: 'Total plan',     color: '#3F51B5', share: 1.00 },
  { id: 'core',     label: 'Core supports',  color: '#00897B', share: 0.80,
    blurb: 'Day-to-day, run-rate spending — assistance, consumables, social participation.' },
  { id: 'capacity', label: 'Capacity building', color: '#7986CB', share: 0.10,
    blurb: 'Therapies, skill-building, and supports that build long-term independence.' },
  { id: 'capital',  label: 'Capital supports', color: '#00695C', share: 0.10,
    blurb: 'One-off purchases — equipment, assistive technology, home modifications.' },
];

/* Status helper for run-rate segments (Core, Capacity) */
function paceStatus(annualBudget, monthly, months, elapsed) {
  if (annualBudget <= 0 || monthly <= 0) {
    return { tone: 'neutral', label: 'Awaiting inputs',
      note: 'Enter the annual cap and your typical monthly spend to see a projection.' };
  }
  const projected = monthly * months;
  const pace = projected / annualBudget;
  if (pace <= 1.02) return { tone: 'ok',    label: 'On track',
    note: `At ${formatAUD(monthly)}/mo you'll finish the year with funds to spare.` };
  if (pace <= 1.15) return { tone: 'warn',  label: 'Watch spending',
    note: `Projected spend is ${Math.round((pace-1)*100)}% over budget. A small adjustment brings you back on track.` };
  return { tone: 'alert', label: 'Review needed',
    note: `At current pace you'll exceed budget by ${formatAUD(projected - annualBudget)}. Consider a plan review.` };
}

/* Status helper for capital (lump-sum) */
function capitalStatus(budget, committed, planned) {
  if (budget <= 0) return { tone: 'neutral', label: 'Awaiting inputs',
    note: 'Enter your annual capital pool to see what\u2019s left for upcoming purchases.' };
  const total = committed + planned;
  if (total <= budget * 0.9)  return { tone: 'ok',    label: 'Headroom available',
    note: `You'll have ${formatAUD(budget - total)} left after planned purchases.` };
  if (total <= budget)        return { tone: 'warn',  label: 'Close to cap',
    note: `Planned purchases will use ${Math.round((total/budget)*100)}% of your capital pool.` };
  return { tone: 'alert', label: 'Over cap',
    note: `Planned purchases exceed your capital pool by ${formatAUD(total - budget)}.` };
}

const TONE_CHIP = {
  neutral: 'chip',
  ok:      'chip chip-ok',
  warn:    'chip chip-warn',
  alert:   'chip chip-alert',
};
const TONE_PROGRESS = {
  neutral: '',
  ok:      '',
  warn:    'warn',
  alert:   'alert',
};

function BudgetCalculator() {
  // Plan-wide inputs
  const [planTotal, setPlanTotal] = React.useState('60000');
  const [months, setMonths]       = React.useState('12');
  const [elapsed, setElapsed]     = React.useState('5');
  const [active, setActive]       = React.useState('total');

  // Per-segment monthly run-rate (Core, Capacity) and capital state
  const [coreMonthly, setCoreMonthly]         = React.useState('3800');
  const [capacityMonthly, setCapacityMonthly] = React.useState('420');
  const [capitalCommitted, setCapitalCommitted] = React.useState('2400');
  const [capitalPlanned, setCapitalPlanned]     = React.useState('1500');

  const planTotalN = Number(planTotal) || 0;
  const m  = Math.max(1, Number(months) || 1);
  const elapsedM = Math.min(m, Math.max(0, Number(elapsed) || 0));

  // Derived annual caps per segment
  const coreCap     = planTotalN * 0.80;
  const capacityCap = planTotalN * 0.10;
  const capitalCap  = planTotalN * 0.10;

  // Run-rate spent / projected
  const coreSpent     = (Number(coreMonthly) || 0) * elapsedM;
  const coreProjected = (Number(coreMonthly) || 0) * m;
  const capacitySpent     = (Number(capacityMonthly) || 0) * elapsedM;
  const capacityProjected = (Number(capacityMonthly) || 0) * m;

  const capitalCommittedN = Number(capitalCommitted) || 0;
  const capitalPlannedN   = Number(capitalPlanned) || 0;

  // Aggregate "spent so far" across plan = run-rate to date + capital committed
  const totalSpent = coreSpent + capacitySpent + capitalCommittedN;

  return (
    <div className="calc-wrap" aria-label="Plan budget calculator">
      {/* Header */}
      <div className="calc-header">
        <div>
          <h3>Plan budget calculator</h3>
          <div className="meta">Estimate only — figures aren't stored or shared.</div>
        </div>
        <div className="calc-plan-meta">
          <label htmlFor="calc-plan-total" className="calc-mini-label">Annual plan</label>
          <div className="input-prefix calc-mini-input">
            <span className="prefix">$</span>
            <input id="calc-plan-total" type="number" inputMode="numeric" min="0" step="1000"
                   className="input"
                   value={planTotal}
                   onChange={e => setPlanTotal(e.target.value)}/>
          </div>
        </div>
      </div>

      {/* Segment tabs */}
      <div className="seg-tabs" role="tablist" aria-label="Budget segments">
        {SEGMENTS.map(s => (
          <button key={s.id}
                  role="tab"
                  aria-selected={active === s.id}
                  className={`seg-tab ${active === s.id ? 'on' : ''}`}
                  onClick={() => setActive(s.id)}>
            <span className="seg-dot" style={{background: s.color}}></span>
            <span className="seg-label">{s.label}</span>
            {s.id !== 'total' && (
              <span className="seg-share">{Math.round(s.share*100)}%</span>
            )}
          </button>
        ))}
      </div>

      {/* Body — varies by active segment */}
      {active === 'total'    && (
        <TotalView
          planTotal={planTotalN}
          months={m}
          elapsed={elapsedM}
          setElapsed={setElapsed}
          setMonths={setMonths}
          coreCap={coreCap} coreSpent={coreSpent} coreProjected={coreProjected} coreMonthly={Number(coreMonthly)||0}
          capacityCap={capacityCap} capacitySpent={capacitySpent} capacityProjected={capacityProjected} capacityMonthly={Number(capacityMonthly)||0}
          capitalCap={capitalCap} capitalCommitted={capitalCommittedN} capitalPlanned={capitalPlannedN}
          totalSpent={totalSpent}
          jumpTo={setActive}
        />
      )}
      {active === 'core'     && (
        <RunRateView
          segment={SEGMENTS[1]}
          annualCap={coreCap}
          months={m} elapsed={elapsedM}
          monthly={coreMonthly} setMonthly={setCoreMonthly}
          setElapsed={setElapsed}
          spent={coreSpent} projected={coreProjected}
          unitLabel="month"
          intro="Core supports run on a monthly cadence — set your typical monthly spend to project the year."
        />
      )}
      {active === 'capacity' && (
        <RunRateView
          segment={SEGMENTS[2]}
          annualCap={capacityCap}
          months={m} elapsed={elapsedM}
          monthly={capacityMonthly} setMonthly={setCapacityMonthly}
          setElapsed={setElapsed}
          spent={capacitySpent} projected={capacityProjected}
          unitLabel="month"
          intro="Capacity building is also run-rate — therapy sessions and skill-building bookings tend to recur monthly."
        />
      )}
      {active === 'capital'  && (
        <CapitalView
          segment={SEGMENTS[3]}
          annualCap={capitalCap}
          committed={capitalCommitted} setCommitted={setCapitalCommitted}
          planned={capitalPlanned} setPlanned={setCapitalPlanned}
        />
      )}
    </div>
  );
}

/* ---------- Total view: overview of all three segments ---------- */
function TotalView({
  planTotal, months, elapsed, setElapsed, setMonths,
  coreCap, coreSpent, coreProjected, coreMonthly,
  capacityCap, capacitySpent, capacityProjected, capacityMonthly,
  capitalCap, capitalCommitted, capitalPlanned,
  totalSpent, jumpTo
}) {
  const remaining   = planTotal - totalSpent;
  const remainingPct = planTotal > 0 ? Math.max(0, Math.min(100, (remaining/planTotal)*100)) : 0;

  const corePace     = paceStatus(coreCap,     coreMonthly,     months, elapsed);
  const capacityPace = paceStatus(capacityCap, capacityMonthly, months, elapsed);
  const capitalPace  = capitalStatus(capitalCap, capitalCommitted, capitalPlanned);

  // Overall rollup tone — worst of the three
  const order = { neutral: 0, ok: 1, warn: 2, alert: 3 };
  const worst = [corePace, capacityPace, capitalPace].reduce((a,b) => order[b.tone] > order[a.tone] ? b : a);

  return (
    <div className="calc-body calc-body-total">
      <div className="calc-inputs">
        <div className="field">
          <label htmlFor="calc-months">Plan period (months)</label>
          <input id="calc-months" type="number" inputMode="numeric" min="1" max="36" step="1"
                 className="input" value={months}
                 onChange={e => setMonths(e.target.value)}/>
        </div>
        <div className="field" style={{marginBottom: 0}}>
          <label htmlFor="calc-elapsed">Months into plan</label>
          <input id="calc-elapsed" type="range" min="0" max={months} step="1"
                 value={elapsed}
                 onChange={e => setElapsed(e.target.value)}
                 style={{width:'100%', accentColor:'var(--teal)'}}/>
          <div className="status-row">
            <span>Month 0</span>
            <span><strong style={{color:'var(--ink)'}}>{elapsed}</strong> of {months}</span>
            <span>Month {months}</span>
          </div>
        </div>

        <div className="seg-summary-list">
          <SegSummary
            color={SEGMENTS[1].color}
            name="Core supports"
            cap={coreCap}
            used={coreSpent}
            sub={coreMonthly > 0 ? `${formatAUD(coreMonthly)} / month` : 'Set a monthly run-rate'}
            tone={corePace.tone}
            onClick={() => jumpTo('core')}
          />
          <SegSummary
            color={SEGMENTS[2].color}
            name="Capacity building"
            cap={capacityCap}
            used={capacitySpent}
            sub={capacityMonthly > 0 ? `${formatAUD(capacityMonthly)} / month` : 'Set a monthly run-rate'}
            tone={capacityPace.tone}
            onClick={() => jumpTo('capacity')}
          />
          <SegSummary
            color={SEGMENTS[3].color}
            name="Capital supports"
            cap={capitalCap}
            used={capitalCommitted}
            sub={capitalPlanned > 0 ? `${formatAUD(capitalPlanned)} planned` : 'One-off purchases'}
            tone={capitalPace.tone}
            onClick={() => jumpTo('capital')}
          />
        </div>
      </div>

      <div className="calc-outputs">
        <div className="output-row">
          <span className="k">Annual plan total</span>
          <span className="v">{formatAUD(planTotal)}</span>
        </div>
        <div className="output-row">
          <span className="k">Spent / committed</span>
          <span className="v">{formatAUD(totalSpent)}</span>
        </div>
        <div className="output-row">
          <span className="k">Remaining</span>
          <span className="v">{formatAUD(remaining)}</span>
        </div>

        <div style={{marginTop: 18}}>
          <div style={{display:'flex', justifyContent:'space-between', fontSize: 13, color:'var(--ink-3)'}}>
            <span>Funds remaining</span>
            <span>{Math.round(remainingPct)}%</span>
          </div>
          <div className={`progress ${TONE_PROGRESS[worst.tone]}`}>
            <span style={{width: remainingPct+'%'}}></span>
          </div>
        </div>

        <div style={{marginTop: 16, display:'flex', alignItems:'center', gap: 10}}>
          <span className={TONE_CHIP[worst.tone]}>{worst.label}</span>
          <span style={{fontSize: 13, color: 'var(--ink-3)'}}>across all segments</span>
        </div>

        <p style={{fontSize: 13, color:'var(--ink-3)', marginTop: 14, marginBottom: 0, lineHeight: 1.5}}>
          {worst.note}
        </p>
      </div>
    </div>
  );
}

function SegSummary({ color, name, cap, used, sub, tone, onClick }) {
  const pct = cap > 0 ? Math.max(0, Math.min(100, (used/cap)*100)) : 0;
  return (
    <button type="button" className="seg-summary" onClick={onClick}>
      <div className="seg-summary-hd">
        <span className="seg-dot" style={{background: color}}></span>
        <span className="seg-summary-name">{name}</span>
        <span className={`${TONE_CHIP[tone]} seg-summary-chip`}>
          {Math.round(pct)}% used
        </span>
      </div>
      <div className="seg-summary-bar">
        <span style={{width: pct+'%', background: color}}></span>
      </div>
      <div className="seg-summary-meta">
        <span>{formatAUD(used)} of {formatAUD(cap)}</span>
        <span className="seg-summary-sub">{sub}</span>
      </div>
    </button>
  );
}

/* ---------- Run-rate view: Core / Capacity ---------- */
function RunRateView({ segment, annualCap, months, elapsed, monthly, setMonthly, setElapsed, spent, projected, unitLabel, intro }) {
  const monthlyN = Number(monthly) || 0;
  const remaining = annualCap - spent;
  const remainingPct = annualCap > 0 ? Math.max(0, Math.min(100, (remaining/annualCap)*100)) : 0;
  const status = paceStatus(annualCap, monthlyN, months, elapsed);
  const avgMonthlyBudget = annualCap / Math.max(1, months);

  return (
    <div className="calc-body">
      <div className="calc-inputs">
        <div className="seg-intro" style={{borderLeftColor: segment.color}}>
          <div className="seg-intro-hd">
            <span className="seg-dot" style={{background: segment.color}}></span>
            <strong>{segment.label}</strong>
            <span className="seg-share-pill">{Math.round(segment.share*100)}% of plan</span>
          </div>
          <p>{intro}</p>
        </div>

        <div className="field">
          <label htmlFor="rr-monthly">Estimated spend per {unitLabel}</label>
          <div className="input-prefix">
            <span className="prefix">$</span>
            <input id="rr-monthly" type="number" inputMode="numeric" min="0" step="50"
                   className="input" value={monthly}
                   onChange={e => setMonthly(e.target.value)}/>
          </div>
          <div className="hint" style={{marginTop: 6}}>
            On-budget would be ~{formatAUD(avgMonthlyBudget)} / {unitLabel}.
          </div>
        </div>

        <div className="field" style={{marginBottom: 0}}>
          <label htmlFor="rr-elapsed">Months into plan</label>
          <input id="rr-elapsed" type="range" min="0" max={months} step="1"
                 value={elapsed}
                 onChange={e => setElapsed(e.target.value)}
                 style={{width:'100%', accentColor: segment.color}}/>
          <div className="status-row">
            <span>Month 0</span>
            <span><strong style={{color:'var(--ink)'}}>{elapsed}</strong> of {months}</span>
            <span>Month {months}</span>
          </div>
        </div>
      </div>

      <div className="calc-outputs">
        <div className="output-row">
          <span className="k">{segment.label} cap (annual)</span>
          <span className="v">{formatAUD(annualCap)}</span>
        </div>
        <div className="output-row">
          <span className="k">Spent so far</span>
          <span className="v">{formatAUD(spent)}</span>
        </div>
        <div className="output-row">
          <span className="k">Remaining</span>
          <span className="v">{formatAUD(remaining)}</span>
        </div>
        <div className="output-row">
          <span className="k">Projected full-year spend</span>
          <span className="v">{formatAUD(projected)}</span>
        </div>

        <div style={{marginTop: 18}}>
          <div style={{display:'flex', justifyContent:'space-between', fontSize: 13, color:'var(--ink-3)'}}>
            <span>Funds remaining</span>
            <span>{Math.round(remainingPct)}%</span>
          </div>
          <div className={`progress ${TONE_PROGRESS[status.tone]}`}>
            <span style={{width: remainingPct+'%', background: status.tone === 'ok' || status.tone === 'neutral' ? segment.color : undefined}}></span>
          </div>
        </div>

        <div style={{marginTop: 16, display:'flex', alignItems:'center', gap: 10}}>
          <span className={TONE_CHIP[status.tone]}>{status.label}</span>
        </div>
        <p style={{fontSize: 13, color:'var(--ink-3)', marginTop: 10, marginBottom: 0, lineHeight: 1.5}}>
          {status.note}
        </p>
      </div>
    </div>
  );
}

/* ---------- Capital view: lump-sum, no run-rate ---------- */
function CapitalView({ segment, annualCap, committed, setCommitted, planned, setPlanned }) {
  const committedN = Number(committed) || 0;
  const plannedN   = Number(planned)   || 0;
  const totalCommit = committedN + plannedN;
  const remaining = annualCap - totalCommit;
  const remainingPct = annualCap > 0 ? Math.max(0, Math.min(100, (remaining/annualCap)*100)) : 0;
  const status = capitalStatus(annualCap, committedN, plannedN);

  // Stacked-bar segments
  const committedPct = annualCap > 0 ? Math.min(100, (committedN/annualCap)*100) : 0;
  const plannedPct   = annualCap > 0 ? Math.min(100 - committedPct, (plannedN/annualCap)*100) : 0;

  return (
    <div className="calc-body">
      <div className="calc-inputs">
        <div className="seg-intro" style={{borderLeftColor: segment.color}}>
          <div className="seg-intro-hd">
            <span className="seg-dot" style={{background: segment.color}}></span>
            <strong>{segment.label}</strong>
            <span className="seg-share-pill">{Math.round(segment.share*100)}% of plan</span>
          </div>
          <p>Capital supports are one-off purchases — assistive tech, equipment, modifications.
             Track them as discrete amounts against your annual pool, not a monthly run-rate.</p>
        </div>

        <div className="field">
          <label htmlFor="cap-committed">Committed / spent so far</label>
          <div className="input-prefix">
            <span className="prefix">$</span>
            <input id="cap-committed" type="number" inputMode="numeric" min="0" step="50"
                   className="input" value={committed}
                   onChange={e => setCommitted(e.target.value)}/>
          </div>
          <div className="hint" style={{marginTop: 6}}>Equipment already paid for or under quote.</div>
        </div>

        <div className="field" style={{marginBottom: 0}}>
          <label htmlFor="cap-planned">Planned upcoming purchases</label>
          <div className="input-prefix">
            <span className="prefix">$</span>
            <input id="cap-planned" type="number" inputMode="numeric" min="0" step="50"
                   className="input" value={planned}
                   onChange={e => setPlanned(e.target.value)}/>
          </div>
          <div className="hint" style={{marginTop: 6}}>e.g. assistive tech you intend to order this plan year.</div>
        </div>
      </div>

      <div className="calc-outputs">
        <div className="output-row">
          <span className="k">Capital pool (annual)</span>
          <span className="v">{formatAUD(annualCap)}</span>
        </div>
        <div className="output-row">
          <span className="k">Committed</span>
          <span className="v">{formatAUD(committedN)}</span>
        </div>
        <div className="output-row">
          <span className="k">Planned</span>
          <span className="v">{formatAUD(plannedN)}</span>
        </div>
        <div className="output-row">
          <span className="k">Remaining after planned</span>
          <span className="v">{formatAUD(remaining)}</span>
        </div>

        <div style={{marginTop: 18}}>
          <div style={{display:'flex', justifyContent:'space-between', fontSize: 13, color:'var(--ink-3)'}}>
            <span>Capital pool allocation</span>
            <span>{Math.round(remainingPct)}% free</span>
          </div>
          <div className="stack-bar" aria-hidden>
            <span className="stack-committed" style={{width: committedPct+'%', background: segment.color}}></span>
            <span className="stack-planned"   style={{width: plannedPct+'%',   background: segment.color, opacity: 0.45}}></span>
          </div>
          <div className="stack-legend">
            <span><span className="legend-sq" style={{background: segment.color}}></span>Committed</span>
            <span><span className="legend-sq" style={{background: segment.color, opacity: 0.45}}></span>Planned</span>
            <span><span className="legend-sq" style={{background: 'var(--line)'}}></span>Free</span>
          </div>
        </div>

        <div style={{marginTop: 16, display:'flex', alignItems:'center', gap: 10}}>
          <span className={TONE_CHIP[status.tone]}>{status.label}</span>
        </div>
        <p style={{fontSize: 13, color:'var(--ink-3)', marginTop: 10, marginBottom: 0, lineHeight: 1.5}}>
          {status.note}
        </p>
      </div>
    </div>
  );
}

Object.assign(window, { BudgetCalculator });
