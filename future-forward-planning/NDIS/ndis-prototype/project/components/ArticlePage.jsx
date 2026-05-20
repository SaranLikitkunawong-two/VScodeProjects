/* Individual article pages — breadcrumbs, dot-point content, related carousel */

const ARTICLE_DATA = {
  'pricing-2026': {
    title: 'What the 2026 NDIS pricing arrangements mean for participants',
    cat: 'Regulatory',
    date: '14 April 2026',
    read: '6 min read',
    image: 'https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=1200&q=80&auto=format&fit=crop',
    imageAlt: 'Person reviewing policy documents at a professional desk',
    intro: 'A plain-English summary of the updated price guide, the support categories affected, and what participants should ask their plan manager before their next invoice cycle.',
    points: [
      'NDIS releases an updated price guide annually; the 2026 version took effect 1 July 2026',
      'Price limits increased by 3.2% across most support categories — an inflation (CPI) adjustment',
      'Core supports (01_xxx codes) saw the highest increases, particularly daily activities and community participation',
      'Capacity building: therapy supports now have separate rates for face-to-face versus telehealth delivery',
      'New line items added for assistive technology trials and formal assessment hours',
      'Consumables category expanded — several over-the-counter items previously excluded are now claimable',
      'What participants should ask their plan manager: Are my current budgets still sufficient at the new rates? Do any of my regular supports now have a different price cap?',
      'Plan managers must update their systems to reflect new price limits by 1 July 2026',
      'Participants on longer plans (e.g. 2-year plans started in 2025) may need a plan review if budgets become tight under the new rates',
      'The NDIA provides a comparison tool to view old vs new price limits at the support item level',
      'Key takeaway: most participants will notice no direct change — the administrative update is absorbed by your plan manager',
    ],
    related: ['pacing-core', 'improved-life-choices', 'invoice-records'],
  },

  'pacing-core': {
    title: 'Pacing your core supports through the final quarter',
    cat: 'Budget updates',
    date: '02 April 2026',
    read: '4 min read',
    image: 'https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=1200&q=80&auto=format&fit=crop',
    imageAlt: 'Financial charts and budget planning documents spread on a desk',
    intro: 'Three simple checks to run on your core supports budget before the end of financial year — and when to request a plan variation.',
    points: [
      'Core supports are the most flexible budget category — providers can often be swapped without prior NDIA approval',
      'End of financial year (April–June) is when most participants first notice underspend or overspend risks',
      'Check 1: Compare your actual spend to date against your expected spend (budget ÷ plan months × months elapsed)',
      'Check 2: Identify committed invoices that have been approved by your plan manager but not yet paid or claimed with NDIA',
      'Check 3: List upcoming services not yet invoiced — these are invisible commitments against your remaining balance',
      'Underspend: unspent core supports funds do NOT roll over at plan end — they return to the NDIA',
      'Plan variations: if you are likely to exhaust core supports before plan end, contact your LAC or ECEI to request a variation early',
      'Common causes of end-of-year budget crunch: provider price increases mid-year, additional therapy hours in the second half, unplanned consumables',
      'Simple formula: remaining budget ÷ months left = your safe monthly spend ceiling',
      'Ask your plan manager for a monthly burn report to see your actual versus projected trajectory',
      'Core supports sub-categories (daily activities, community participation, consumables) are flexible within Core — you can redirect spend between them without a plan review',
    ],
    related: ['pricing-2026', 'monthly-statement', 'improved-life-choices'],
  },

  'switching-plan-manager': {
    title: 'Switching plan managers mid-plan: what to expect',
    cat: 'Participant guidance',
    date: '28 March 2026',
    read: '5 min read',
    image: 'https://images.unsplash.com/photo-1521791136064-7986c2920216?w=1200&q=80&auto=format&fit=crop',
    imageAlt: 'Two people shaking hands across a desk in a professional meeting',
    intro: 'Participants can change plan managers at any point in their plan. Here\'s the process, typical timelines, and how to avoid double-invoicing.',
    points: [
      'You have the legal right to change plan managers at any time — no lock-in periods are permitted under NDIS rules',
      'Step 1: Choose your new plan manager and confirm they are registered with the NDIS Commission and have capacity to take you on',
      'Step 2: Complete a change-of-provider form with your new plan manager — they will typically handle all the paperwork on your behalf',
      'Step 3: Notify your current plan manager in writing — most prefer 2–4 weeks notice, though this is a courtesy, not a legal requirement',
      'Step 4: The NDIA updates your plan in the PACE system to reflect the new plan manager — typically within 2–5 business days',
      'Pending invoices: your current plan manager should process all outstanding invoices before the transition — confirm this explicitly in writing',
      'Double-invoicing risk: give your providers the exact handover date so they send future invoices to the correct plan manager',
      'Budget transfer: your remaining budget balance carries over automatically — only the plan management (ILC) line item is redirected to the new provider',
      'Records that do not transfer: admin files, provider contact notes, or internal records held by your previous plan manager',
      'Red flags to watch for: plan managers who charge exit fees (not permitted under NDIS rules), delay the transition, or fail to finalise outstanding claims before handover',
    ],
    related: ['monthly-statement', 'improved-life-choices', 'invoices-held'],
  },

  'invoice-records': {
    title: 'Invoice record-keeping after the 2026 reforms',
    cat: 'Compliance',
    date: '21 March 2026',
    read: '3 min read',
    image: 'https://images.unsplash.com/photo-1568992688413-7b0bc7e6fef9?w=1200&q=80&auto=format&fit=crop',
    imageAlt: 'Organised filing folders and documents on a clean white desk',
    intro: 'The NDIA has tightened documentation expectations for plan-managed invoices. Here\'s what providers and participants should keep on file.',
    points: [
      'Since mid-2025, the NDIA has significantly increased audit activity on plan-managed invoice claims',
      'Providers must retain: the original tax invoice, a signed service agreement, and delivery records (attendance notes, shift logs, session notes)',
      'Participants (via their plan manager) must keep all paid invoices for 7 years from the date of payment — this is an ATO requirement',
      'Every valid invoice must include: supplier ABN, a unique invoice number, invoice date, itemised description of the support, NDIS line item code, quantity, unit price, and GST status',
      'New from 2026: invoices for high-cost items (greater than $5,000 per line item) now require a supporting quote or formal assessment report',
      'Plan managers must be able to produce all relevant records within 5 business days of receiving an NDIA audit request',
      'Electronic storage is fully acceptable — physical paper copies are not required, but PDFs must be legible and easily retrievable',
      'Participants can request a complete copy of their invoice history from their plan manager at any time — this is your right',
      'Common audit triggers: claims outside plan dates, duplicate line items across batches, unit prices above PAPL limits, provider not registered for the claimed support category',
    ],
    related: ['invoices-held', 'pricing-2026', 'switching-plan-manager'],
  },

  'invoices-held': {
    title: 'Why some invoices get held: a quick walkthrough',
    cat: 'Invoicing',
    date: '10 March 2026',
    read: '4 min read',
    image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=1200&q=80&auto=format&fit=crop',
    imageAlt: 'Person at a desk carefully reviewing and annotating a document',
    intro: 'The most common reasons plan-managed invoices are paused, how we resolve them, and what participants can do to speed things up.',
    points: [
      '"Held" means the invoice has been received by your plan manager but not yet approved for NDIA claim submission',
      'Most common reason: the unit price on the invoice exceeds the NDIS price limit (PAPL) for that support item — the provider needs to reissue at the correct rate',
      'Invoice date falls outside the participant\'s current plan period — supports must be delivered and invoiced within the active plan dates',
      'Support item number on the invoice doesn\'t match the service description — a mismatch triggers a manual review',
      'The participant\'s budget for that support category is at or near zero — the plan manager cannot approve a claim that would exceed the allocated amount',
      'ABN on the invoice doesn\'t match the ABN on file for that registered provider',
      'Invoice appears to be a duplicate of one already paid or claimed in a previous PACE batch',
      'What plan managers do: contact the provider with a specific reason and a request for a corrected invoice or supporting documentation',
      'Simple corrections (typographical ABN error, wrong invoice date) typically resolve within 1–2 business days',
      'Pricing disputes or missing documentation may take longer — the provider needs to engage with the NDIA or reissue the invoice',
      'What participants need to do: in most cases, nothing — your plan manager handles resolution; you will see the invoice status as "on hold" in your portal',
      'Prevention: ensure your providers have the current NDIS Price Arrangement and Price Limits document before submitting invoices each year',
    ],
    related: ['invoice-records', 'monthly-statement', 'pricing-2026'],
  },

  'monthly-statement': {
    title: 'Reading your monthly statement without the jargon',
    cat: 'Participant guidance',
    date: '26 February 2026',
    read: '5 min read',
    image: 'https://images.unsplash.com/photo-1579621970563-ebec7e6e4f85?w=1200&q=80&auto=format&fit=crop',
    imageAlt: 'Person reviewing a financial statement on a laptop with printed documents nearby',
    intro: 'A guided tour of the numbers that matter on your monthly plan statement — category balances, claim status, and what "committed" really means.',
    points: [
      'Your monthly plan statement is a snapshot of your budget as at the last day of the reporting month',
      '"Total allocated" — the total amount in your current NDIS plan for each support category',
      '"Spent (paid)" — invoices that have been fully paid to providers; this money has left the NDIA system',
      '"Claimed" — invoices submitted to the NDIA via a PACE batch but not yet paid out (typically 2–5 business days to process)',
      '"Committed" — invoices approved by your plan manager but not yet included in a PACE submission batch',
      '"Remaining" — your allocated amount minus claimed and paid totals; does not yet account for uncommitted invoices in the queue',
      '"Uncommitted" invoices are sitting in your plan manager\'s review queue and have not yet been approved or submitted — they will reduce your remaining balance once processed',
      'The pace badge ("On track", "Watch", "At risk") compares your spending rate to how far through your plan period you are',
      '"On track" means your spending rate aligns with your plan timeline',
      '"Watch" means you are spending faster than expected — at this rate you may exhaust the budget before plan end',
      '"At risk" means you are projected to either run out before plan end, or significantly underspend (which may indicate unmet needs)',
      'If you see invoices marked "Rejected" on your statement, your plan manager should have already sent you or your provider a written explanation',
    ],
    related: ['switching-plan-manager', 'pacing-core', 'invoices-held'],
  },

  'improved-life-choices': {
    title: 'Changes to Improved Life Choices: what plan managers watch for',
    cat: 'Regulatory',
    date: '18 February 2026',
    read: '5 min read',
    image: 'https://images.unsplash.com/photo-1434626881859-086134fd7db8?w=1200&q=80&auto=format&fit=crop',
    imageAlt: 'NDIS plan documents on a desk with a pen ready to sign',
    intro: 'A short explainer on the support category that funds plan management, and why getting the right wording on your plan matters at review time.',
    points: [
      '"Improved Life Choices" (ILC) is the NDIS support category that funds plan management services',
      'It sits under Capacity Building (Category 07) — entirely separate from Core and Capital supports',
      'Your plan must explicitly include an ILC allocation for plan-managed funding to be possible; it is not added automatically',
      '2026 ILC rate: approximately $124.57 per month per participant (includes the monthly management fee)',
      'Establishment fee (charged once at the start of a new plan management arrangement): approximately $233.56',
      'Common issue at plan review: if the NDIA planner or LAC does not include ILC in the renewed plan, the participant cannot continue with a plan manager',
      'Plan managers actively monitor plan review dates and expiring ILC allocations to flag this risk early for each participant',
      'Participants should specifically request ILC at their plan review meeting if they wish to continue with plan management',
      'Wording to use at plan review: "I would like to continue with plan management services under the Improved Life Choices support category"',
      'ILC funds are a restricted-use category — they can only be used to pay plan management fees, nothing else',
      'Plan managers cannot charge above the NDIA rate for ILC — any costs above the price limit must be absorbed by the plan manager, never passed to the participant',
    ],
    related: ['pricing-2026', 'switching-plan-manager', 'pacing-core'],
  },
};

/* Small card used in the related articles carousel */
function RelatedCard({ slug }) {
  const a = ARTICLE_DATA[slug];
  if (!a) return null;
  const go = (e) => { e.preventDefault(); window.navigate('article', slug); };
  return (
    <article className="related-card" onClick={go} role="link" tabIndex={0}
             onKeyDown={(e) => e.key === 'Enter' && go(e)}>
      <div className="related-card-img">
        <img src={a.image} alt={a.imageAlt} loading="lazy"/>
      </div>
      <div className="related-card-body">
        <span className="chip chip-teal" style={{fontSize: 11}}>{a.cat}</span>
        <h3>{a.title}</h3>
        <span className="related-card-meta">{a.date} · {a.read}</span>
      </div>
    </article>
  );
}

function Breadcrumbs({ title }) {
  const goHome = (e) => { e.preventDefault(); window.navigate('home'); };
  const goNews = (e) => { e.preventDefault(); window.navigate('news'); };
  return (
    <nav className="breadcrumbs" aria-label="Breadcrumb">
      <a href="#/" className="breadcrumb-link" onClick={goHome}>Home</a>
      <span className="breadcrumb-sep" aria-hidden>/</span>
      <a href="#/news" className="breadcrumb-link" onClick={goNews}>News</a>
      <span className="breadcrumb-sep" aria-hidden>/</span>
      <span className="breadcrumb-current" aria-current="page">{title}</span>
    </nav>
  );
}

function ArticlePage({ slug }) {
  const article = ARTICLE_DATA[slug];

  React.useEffect(() => {
    if (!article) window.navigate('news');
  }, [slug]);

  if (!article) return null;

  return (
    <main id="main">
      {/* Breadcrumbs */}
      <div className="breadcrumb-bar">
        <div className="container">
          <Breadcrumbs title={article.title}/>
        </div>
      </div>

      {/* Hero image */}
      <div className="article-hero">
        <img src={article.image} alt={article.imageAlt} className="article-hero-img"/>
        <div className="article-hero-overlay">
          <div className="container">
            <span className="chip chip-teal">{article.cat}</span>
            <h1 className="article-hero-title">{article.title}</h1>
            <div className="article-hero-meta">
              <span>{article.date}</span>
              <span className="dot" aria-hidden></span>
              <span>{article.read}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Article body */}
      <div className="container">
        <div className="article-body-wrap">
          <p className="lede article-intro">{article.intro}</p>
          <ul className="article-points" aria-label="Key points">
            {article.points.map((point, i) => (
              <li key={i}>{point}</li>
            ))}
          </ul>

          {/* Back to news */}
          <div className="article-back">
            <a href="#/news" className="btn btn-secondary"
               onClick={(e) => { e.preventDefault(); window.navigate('news'); }}>
              ← Back to News
            </a>
          </div>
        </div>
      </div>

      {/* Related articles */}
      <section className="related-section" aria-label="Related articles">
        <div className="container">
          <h2 className="related-heading">Related articles</h2>
          <div className="related-grid">
            {article.related.map(s => <RelatedCard key={s} slug={s}/>)}
          </div>
        </div>
      </section>

      <Footer/>
    </main>
  );
}

Object.assign(window, { ArticlePage, ARTICLE_DATA });
