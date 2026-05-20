# Future Forward Planning — Design Document

## Overview

**Future Forward Planning** is an NDIS plan management business and web portal built for Australian NDIS participants, service providers, and the plan manager (admin). The tech stack is Next.js 15 (App Router), Supabase (Postgres + Auth + Storage + Realtime), Tailwind CSS v4, shadcn/ui, Recharts, and Google Document AI for OCR.

---

## Business Context

- **Plan Manager**: Saran Likitkunawong (CA ANZ, Melbourne)
- **Revenue model**: ~$124.57/month per participant (2026 NDIS rates), funded from participant's "Improved Life Choices" budget — zero out-of-pocket cost to the participant
- **Target**: 30–50 participants Year 1, 100+ by Year 2
- **Structure**: Sole trader → transition to Pty Ltd at ~50+ clients (~$80–120K revenue)
- **Hosting costs at scale (100 clients)**: ~$65–85/month (Vercel + Supabase + Google Cloud + Railway + Cloudflare)

---

## User Roles

| Role | Who | Key Capabilities |
|---|---|---|
| **Admin** | Plan manager (Saran) | Manage participants/providers, review invoices, generate PACE files, analytics |
| **Participant** | NDIS clients | View budget by category, transaction history, monthly trends |
| **Provider** | Service organisations | Upload invoices, track invoice status, receive payment notifications |

---

## Application Modules

### Module 1 — Provider Invoice Submission Portal
- Drag-and-drop PDF/image upload → Supabase Storage
- Google Document AI (OCR) extracts: supplier name & ABN, invoice number, date, amounts, line items
- Confidence ≥ 85% → soft-filled fields; < 85% → highlighted for manual correction
- Provider confirms/corrects, selects NDIS support category + line item code
- Price limit validation against PAPL (flags if unit price exceeds limit)
- Submits to admin review queue → email notification to admin

### Module 2 — Admin Dashboard
- **Invoice Queue**: sortable list (pending → approved → rejected → claimed → paid)
- **Invoice Review**: side-by-side PDF viewer + editable parsed fields
- **Participant Budget Board**: grid with allocated/spent progress bars per participant
- **PACE Bulk File Generator**: select approved invoices → download NDIA-compliant CSV
- **Claims History**: submitted PACE batches with NDIA status
- **Participant Management**: CRUD (NDIS number, plan dates, category budgets)
- **Provider Management**: CRUD (ABN, bank details, linked participants)
- **Metabase Analytics**: embedded dashboards (portfolio overview, invoice pipeline, provider analytics)

### Module 3 — Participant Dashboard
- Budget overview cards: total remaining ($/%); total spent with pace badge; days remaining; projected balance
- Monthly spending trend: 12-month stacked area chart by support category
- Category breakdown: donut chart + progress bars (amber ≥ 80%, red ≥ 100%)
- Recent transactions: filterable table of last 20 transactions
- Real-time updates via Supabase channel subscription

### Module 4 — Notifications & Automation
- Email: provider on approval/rejection; admin on new submission
- Weekly budget summary to participant (Monday)
- Low budget alert (< 20% remaining) → participant + admin
- Plan end date reminder (30-day, 7-day)

### Module 5 — PACE Bulk Payment File
- NDIA-compliant CSV for myPlace portal upload
- Required columns: RegistrationNumber, NDISNumber, SupportNumber, ClaimType, ClaimReference, Quantity, Hours, UnitPrice, GSTCode (P1), SupportFrom, SupportTo, AuthorisedBy, ParticipantApproved

---

## Invoice Processing Workflow

```
1. Provider uploads invoice (PDF/image)
2. Google Document AI OCR → extracts fields
3. Provider confirms/corrects fields, selects line item code
4. Auto-validation: ABN match, plan period, price limits, budget balance
5. Admin reviews (PDF + fields side-by-side) → Approve or Reject
   └─ Approval: budget deducted; email to provider
   └─ Rejection: rejection_reason stored; email to provider
6. Admin selects approved invoices → generates PACE CSV
7. Admin uploads CSV to NDIA myPlace portal
8. NDIA processes, releases funds → invoice status = 'claimed' → 'paid'
9. Admin pays provider from NDIA account
```

---

## Data Models

### Core Entities

```typescript
// Users / Profiles
Profile { id, role: 'admin'|'participant'|'provider', full_name, email, phone, abn }

// Participants
Participant { id, ndis_number, full_name, dob, email, phone, plan_start_date, plan_end_date, is_active }

// Providers
Provider { id, business_name, abn, email, phone, bsb, account_number, account_name, is_active }

// Provider ↔ Participant (many-to-many)
ProviderParticipant { provider_id, participant_id }

// Plan budget per category
PlanBudget { participant_id, support_category_id, allocated_amount, plan_start_date, plan_end_date }

// NDIS Price Guide items (seeded from PAPL)
PriceGuideItem { support_item_number, name, category_id, unit, price_limit_act_nsw_qld_vic, price_limit_other, ... }
```

### Invoice & Claims

```typescript
Invoice {
  id, participant_id, provider_id,
  file_path, file_name, file_size_bytes,
  ocr_confidence, ocr_raw_json,
  invoice_number, invoice_date, due_date, supplier_name, supplier_abn,
  subtotal, gst_amount, total_amount,
  support_category_id,
  status: 'pending'|'ocr_processing'|'needs_review'|'approved'|'rejected'|'claimed'|'paid',
  rejection_reason, reviewed_by, reviewed_at,
  claim_batch_id, claimed_at, paid_at
}

InvoiceLineItem {
  invoice_id, support_item_number, description,
  support_date_from, support_date_to,
  quantity, unit: 'H'|'E'|'D', unit_price, total,
  gst_code: 'P1', price_exceeds_limit, validation_notes
}

ClaimBatch {
  id, batch_reference, created_by,
  invoice_count, total_value, file_path,
  status: 'draft'|'submitted'|'processed'|'rejected',
  submitted_at, ndia_response
}

Notification {
  user_id, type, title, message, link, is_read
}
```

### Budget Computation (TypeScript, not SQL)

| Field | Formula |
|---|---|
| `spent_amount` | Sum of paid transaction amounts for category |
| `utilisation_pct` | (spent / allocated) × 100 |
| `days_elapsed` | (today − plan_start) / ms_per_day |
| `pct_time_elapsed` | (days_elapsed / total_days) × 100 |
| `burn_rate` | total_spent / days_elapsed |
| `projected_balance` | remaining − (burn_rate × days_remaining) |

### Row Level Security (Supabase)

| Table | Admin | Participant | Provider |
|---|---|---|---|
| participants | All | Own record | — |
| providers | All | — | Own record |
| invoices | All | Own NDIS number | Own submissions |
| plan_budgets | All | Own | — |
| price_guide_items | All | Public read | Public read |

---

## Public Website (Marketing)

### Pages

| Route | Purpose |
|---|---|
| `/` (Home) | Hero + budget calculator + "How we help" + "What is plan management" + About + CTA |
| `/news` | NDIS article grid with category filters |
| `/signup` | Waitlist registration form |

### Home Page Sections

1. **Hero** — Headline, lede, 2 CTAs, metadata bullets, hero art (3 variants: Plan / Chart / Grid)
2. **Budget Calculator** — 4-tab interactive calculator (Total Plan / Core / Capacity / Capital)
3. **How We Help** — 3 numbered cards (Pay providers; Keep budget visible; Answer when you call)
4. **What is Plan Management** — 2-column: explainer + checklist (6 items)
5. **About** — 2-column: headline + body + 3 stats (Founded, Based in, Team)
6. **CTA Band** — "Join the waitlist" on slate blue
7. **Footer** — 4-column (brand, product links, resources, contact)

### Sign Up Form

- Fields: first name (required), email (required, validated), phone (optional)
- Error states: border-alert + icon + message
- Success state: checkmark + personalised confirmation + 2 buttons

---

## Design System

### Color Palette

```
60% Slate Blue primary
  #3F51B5  (base)
  #2C3A83  (slate-900 — darkest)
  #3646A0  (slate-700)
  #8E98CC  (slate-300)
  #E5E8F4  (slate-100)
  #F1F3FA  (slate-50)

30% Background
  #F5F5F5  (off-white)
  #FFFFFF  (white)

10% Teal accent
  #00897B  (base)
  #00695C  (teal-700)
  #D5EAE7  (teal-100)

Neutrals
  #1B1F2A  (ink — primary text)
  #3A3F4B  (ink-2)
  #5C6370  (ink-3)
  #8A909B  (ink-4)
  #E4E5EA  (line — borders)
  #CDD0D9  (line-strong)

Status
  Warning:  bg #FFF4E0  /  text #8A5A00
  OK:       bg #E0F2EF  /  text #00695C
  Alert:    bg #FBE6E3  /  text #9A2A1E
```

### Typography

| Style | Size | Weight | Notes |
|---|---|---|---|
| H1 | clamp(36px, 4.6vw, 56px) | 600 | letter-spacing -0.025em |
| H2 | clamp(26px, 2.6vw, 34px) | 600 | |
| H3 | 20px | 600 | |
| H4 | 16px | 600 | ink-2 color |
| Body | 16px | 400 | line-height 1.55 |
| Lede | clamp(17px, 1.3vw, 19px) | 400 | intro paragraph |
| Eyebrow | 12px | 600 | 0.12em spacing, uppercase, teal |
| Font | Inter, system-ui | | |

### Component Tokens

**Buttons**
- Base: `padding: 12px 20px; border-radius: 10px; min-height: 44px`
- `.btn-primary`: teal bg, white text, shadow
- `.btn-secondary`: white bg, line border, ink text
- `.btn-ghost`: transparent, slate text
- `.btn-on-slate`: white bg on dark sections
- `.btn-lg`: `14px 24px; min-height: 52px`

**Cards**
- White bg, 1px line border, 10px border-radius, `.card-pad` = 28px

**Badges / Chips**
- `.chip`: `4px 10px; border-radius: 999px; slate-50 bg`
- `.chip-teal`, `.chip-warn`, `.chip-ok`, `.chip-alert`

**Progress Bars**
- 8px height, teal fill, transitions 0.3s ease
- Amber at ≥ 80%, red at ≥ 100%

**Inputs**
- `padding: 12px 14px; min-height: 48px; border-radius: 10px`
- Focus: teal outline + shadow
- Error: alert-ink border + shadow + icon + message below

### Layout

- Container: max-width 1180px, 24px gutter
- Section padding: 96px vertical (64px mobile)
- Breakpoints: ≤ 640px mobile | ≤ 900px tablet | ≥ 1180px desktop

---

## Frontend Architecture (Next.js 15)

### Component Hierarchy

```
Shell (Nav + Footer + Tweaks panel)
├── HomePage
│   ├── Hero + HeroArt (Plan | Chart | Grid variants)
│   ├── BudgetCalculator (4-tab: Total | Core | Capacity | Capital)
│   ├── How We Help cards
│   ├── What is Plan Management
│   ├── About
│   └── CTA Band
├── NewsPage
│   ├── News hero
│   ├── Filter chips (All | Regulatory | Budget updates | ...)
│   └── Article grid (featured 3-col + standard cards)
└── SignupPage
    ├── Copy + checklist (left)
    └── Form card / Success state (right)
```

### Data Fetching Pattern

- **Server Components**: fetch data in `page.tsx`, pass as props
- **Client Components**: charts, forms, real-time listeners
- **Parallel queries**: `Promise.all()` for independent Supabase calls
- **Real-time**: `supabase.channel()` subscription → `router.refresh()` on DB change

---

## Tech Stack

| Layer | Choice | Notes |
|---|---|---|
| Framework | Next.js 15 | App Router, TypeScript, Server Components |
| Styling | Tailwind CSS v4 | |
| UI | shadcn/ui | Card, Badge, Progress, Table, Chart |
| Charts | Recharts | Stacked area, donut, line |
| Icons | Lucide React | |
| Dates | date-fns v4 | |
| PDF Viewer | react-pdf | Invoice review in-browser |
| Database | Supabase (PostgreSQL) | AU Sydney region, RLS, Realtime |
| Auth | Supabase Auth | Email + magic link |
| Storage | Supabase Storage | Private buckets, signed URLs |
| OCR | Google Document AI | $0.01/page; GPT-4o Vision as fallback |
| Email | Resend | Transactional, 3,000/month free |
| Analytics | Metabase (self-hosted) | Embedded dashboards via signed JWT |
| Hosting | Vercel | Next.js + API routes |
| Metabase host | Railway | Docker |
| DNS | Cloudflare | |

---

## Security & Compliance

- **RLS**: Enforced at Postgres level — participants cannot query other participants' data
- **Signed URLs**: Invoice PDFs only accessible via time-limited signed URLs
- **JWT**: Stored in HTTP-only cookie, never localStorage
- **Data residency**: Supabase Sydney region (Australian Privacy Act)
- **Retention**: Invoices + PDFs kept 7 years (ATO), then deleted
- **Anti-fraud**: ABN verification, duplicate invoice detection, banning register check
- **No referral fees / inducements**: PM-POL-016 compliance
- **Price enforcement**: Every line item validated against current PAPL

---

## Business Rules

- **Budget alert thresholds**: amber ≥ 80% utilisation; red ≥ 100%
- **Low balance alert**: < 20% remaining → email participant + admin
- **Category lock**: Core ↔ Capacity budgets are not interchangeable
- **Overspend guard**: Admin approval blocked if it would exceed allocated category budget
- **OCR confidence threshold**: < 85% → highlight fields for manual correction
- **PACE GST code**: `P1` (GST-free) for most disability services

---

## Build Roadmap

| Phase | Scope | Est. Hours |
|---|---|---|
| 0 | Setup: GitHub, Supabase, Google Cloud, domain, seed data | 8–12 |
| 1 | Admin CRUD: participants, providers, plan budgets, route middleware | 20–30 |
| 2 | Invoice submission: provider login, upload, OCR, review form, validation | 30–40 |
| 3 | Admin invoice review: queue, approve/reject, budget deduction, audit trail | 15–20 |
| 4 | PACE file generator: batch builder, CSV export, claims history | 10–15 |
| 5 | Participant portal: login, budget overview, charts, transactions, realtime | 10–15 |
| 6 | Automation: scheduled emails, notifications, mobile audit | 15–20 |
| Post-MVP | ABN API, Xero integration, white-label option | TBD |

**Total MVP**: ~108–152 hours (~3–4 months at 10 hrs/week)

---

## Go-to-Market

- **Launch**: Month 12 (post NDIS Commission registration)
- **Revenue at 30 clients**: ~$37.4K/year
- **Revenue at 100 clients**: ~$125.4K/year
- **Key acquisition channels**: Google Business Profile, NDIS directories (My Care Space, Clickability), support coordinator network, r/NDIS, LinkedIn
- **Competitive moat**: Real-time participant portal + OCR automation + CA-qualified plan manager responsiveness
