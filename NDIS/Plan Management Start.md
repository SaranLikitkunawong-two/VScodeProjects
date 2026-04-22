# NDIS Plan Management Business — Full Planning Document
> **Owner:** Saran Likitkunawong | CAANZ Full Member | Melbourne, VIC
> **Date:** April 2026

TFN 958 027 530
ABN 20 931 095 007

---

Week 1:    Register business name + GST ✅ + business bank account (Westpac Business One) ✅ + Xero
Week 1–2:  Get professional indemnity + public liability insurance
Week 1–2:  Set up myID (Standard/Strong level) ✅
Week 1–2:  Apply for NDIS Worker Screening clearance (takes 2–6 weeks)
Week 2–4:  Write policy suite
Week 3–4:  Engage AQA, get quotes, book audit
Week 4–5:  Submit NDIS Commission registration application
Week 4–12: Build portal Phase 0 + 1 (skeleton + admin/participant data)
Week 8–12: Verification audit completed, registration certificate issued
Week 12+:  First client onboarded 🎉

## Table of Contents
1. [Business Structure: Sole Trader vs Pty Ltd](#1-business-structure-sole-trader-vs-pty-ltd)
2. [Best-of-Market NDIS Plan Management Software](#2-best-of-market-ndis-plan-management-software)
3. [Decision: Build Your Own Portal](#3-decision-build-your-own-portal)
4. [Custom Portal — Product Specification](#4-custom-portal--product-specification)
5. [Tech Stack Decision](#5-tech-stack-decision)
6. [Database Schema](#6-database-schema)
7. [OCR & Invoice Intelligence Layer](#7-ocr--invoice-intelligence-layer)
8. [Infrastructure & Hosting](#8-infrastructure--hosting)
9. [Project File Structure](#9-project-file-structure)
10. [Feature Build Roadmap (Phase-by-Phase)](#10-feature-build-roadmap-phase-by-phase)
11. [Security & Compliance](#11-security--compliance)
12. [Cost Model](#12-cost-model)
13. [Scaling Plan](#13-scaling-plan)

---

## 1. Business Structure: Sole Trader vs Pty Ltd

### Quick Summary
For your stated priority — **reach critical mass fast, then scale** — starting as a sole trader is the right call. Here is the full trade-off analysis.

---

### Sole Trader

| Factor | Detail |
|--------|--------|
| **Setup cost** | Free (just register ABN + business name ~$44/3yr) |
| **Setup time** | Same day via ABR website |
| **Tax** | Taxed at personal marginal rates |
| **Accounting** | Report income on personal tax return — no separate company return |
| **Liability** | **Unlimited** — personal assets (house, car, savings) are exposed |
| **ASIC fees** | None |
| **NDIS eligibility** | ✅ Sole traders can be registered NDIS providers |
| **Closing down** | Simply stop trading; notify ATO/ABR |

**Pros for your situation:**
- Zero delay to first client — register ABN and you are trading
- Simplest bookkeeping; use Xero or MYOB with minimal setup
- As CAANZ, you can handle your own tax return
- At sub-$120K profit, your marginal tax rate is manageable

**Cons to be aware of:**
- Unlimited personal liability is real — **offset this with professional indemnity and public liability insurance (non-negotiable)**
- At $120K+ profit, you lose more to tax vs a company paying 25% flat rate
- No ability to split income via dividends (important for family tax planning)
- Perception: some support coordinators may prefer to refer to a registered company

---

### Pty Ltd Company

| Factor | Detail |
|--------|--------|
| **Setup cost** | ~$576 ASIC registration fee |
| **Annual ASIC fee** | ~$310/year |
| **Tax rate** | 25% (base rate entity) flat — vs your personal rate of 32.5–47% |
| **Tax return** | Separate company tax return required each year |
| **Liability** | Limited to company assets (some personal exposure via director duties) |
| **Hiring** | Easier to structure staff remuneration + share equity |
| **Credibility** | Better for tendering, referrals, enterprise clients |
| **Closing down** | ASIC deregistration process required |

**Pros:**
- Protect personal assets as client base grows
- At 50+ clients (~$62K+/year), the 25% company tax rate vs your marginal rate saves thousands
- Can pay yourself salary + dividends to optimise tax
- Easier to bring in a business partner or sell the business later

**Cons:**
- ~$886 extra cost in year one before you have a single client
- Separate BAS, company tax return, and potential Division 7A obligations
- Director penalties if obligations breached

---

### Recommendation: Start Sole Trader → Transition at ~$80–120K Revenue

```
PHASE 1 (0–18 months): Sole Trader
  - Register ABN + business name + GST (if expecting >$75K)
  - Get professional indemnity ($1M+ cover) + public liability insurance
  - Focus 100% on getting to 30-50 participants

PHASE 2 (18–36 months): Incorporate Pty Ltd
  - When annual revenue hits $80–120K, engage your accountant
  - Incorporate Pty Ltd and transfer business activities
  - Xero company file migration is straightforward
```

**Tax crossover point for sole trader → company:**
- If your effective marginal rate is 39% (including Medicare) and company rate is 25%,
  every $1 of profit above ~$120K costs you ~14c more as a sole trader.
- At 50 clients × $104.45/month × 12 = $62,670/year — still in the sole trader comfort zone.
- At 100 clients → $125,340/year — time to incorporate.

---

## 2. Best-of-Market NDIS Plan Management Software

> Researched April 2026. Use these as your bridge while you build your own portal, or as competitive benchmarks.

### Comparison Table

| Platform | Best For | PACE/PRODA | Invoice Processing | Participant Portal | Price (est.) |
|----------|----------|------------|-------------------|-------------------|-------------|
| **MYP Corp** | Dedicated plan managers | ✅ Bulk payment requests, myPlace integration | Manual + bulk | Basic | Quote only |
| **ShiftCare** | Small-mid providers growing beyond PM | ✅ | Automated billing | ✅ Family portal | ~$9/user/month |
| **Brevity** | Multi-funder, complex orgs | ✅ | Excellent | ✅ | ~$200/org/month |
| **SupportAbility** | Complex support coordination | ✅ | Strong | ✅ | ~$20/participant/month |
| **Lumary** | Large enterprise providers | ✅ | Excellent, Salesforce-based | ✅ | ~$30+/user/month |
| **Careview** | SIL/group homes | ✅ | Good | Limited | Custom quote |
| **Imploy** | All-in-one NDIS + aged care | ✅ | AI-assisted | ✅ | $8–20/user/month |

### Key Insights for a Startup Plan Manager

- **MYP Corp** is the closest to what you need for pure plan management, but is quote-priced and built for established orgs.
- **ShiftCare** at $9/user/month is the best commercial starting point, but its invoice UX is generic.
- **None of these** provide an OCR invoice reader or a branded provider-facing submission portal.
- **Building your own** creates a genuine competitive advantage: a slick, modern portal that providers love using, reducing your admin time dramatically.

### Recommended Bridge Strategy

```
Month 1–3:   Use Xero + Excel/Google Sheets + myPlace manually
              (5–15 clients = manageable by hand)

Month 3–12:  Migrate to ShiftCare (~$9/user/month) for compliance
              + budget tracking while building your custom portal

Month 12+:   Migrate providers to your custom portal
              Keep ShiftCare for rostering/compliance if needed
              OR replace entirely with your portal
```

---

## 3. Decision: Build Your Own Portal

### Why Build?

| What you get | Commercial software | Your custom portal |
|---|---|---|
| Branded provider submission portal | ❌ Generic | ✅ Your brand |
| OCR invoice auto-fill | ❌ None | ✅ AI-powered |
| NDIS-specific invoice validation | Partial | ✅ Full custom rules |
| PACE bulk payment file generator | ✅ (MYP only) | ✅ Build once |
| Participant budget dashboard | Basic | ✅ Real-time |
| Monthly fee | $200–$600/month | ~$20–50/month infra |
| Data ownership | Vendor's cloud | ✅ Yours |
| Competitive moat | None | ✅ Yes |

### Realistic Build Scope (MVP)

The MVP is **not** trying to replace all of ShiftCare. It targets the specific pain point:
> *"Providers submit invoices. You review, validate, and generate PACE payment files."*

Everything else (compliance docs, staff rostering, etc.) can remain in a bridge tool initially.

---

## 4. Custom Portal — Product Specification

### Users / Roles

| Role | Description |
|------|-------------|
| `admin` | You (plan manager) — full access to everything |
| `participant` | NDIS participant — view their own budget and transaction history |
| `provider` | Service provider — submit invoices, track status |

---

### Module 1: Provider Invoice Submission Portal

**Flow:**
1. Provider receives invite link via email
2. Provider logs in (email + password, or magic link)
3. Provider selects participant from dropdown (filtered to their approved participants)
4. Provider uploads invoice (PDF or image)
5. **OCR engine processes the document and pre-fills fields:**
   - Supplier name
   - ABN
   - Invoice number
   - Invoice date
   - Due date
   - Line items (description, unit price, qty, total)
   - GST amount
   - Total amount
6. Provider reviews and confirms or corrects OCR output
7. Provider selects NDIS support category and line item code from dropdown
8. Provider submits → invoice goes into plan manager's review queue

---

### Module 2: Plan Manager Dashboard (Admin)

**Views:**
- **Invoice Queue** — paginated list of pending invoices with priority flags
- **Invoice Detail** — side-by-side view of original PDF (left) + parsed fields (right) for fast review
- **Participant Budget Board** — grid of all participants with budget bars (budgeted vs. spent vs. claimed)
- **Bulk Payment Generator** — select approved invoices → generate PACE bulk upload CSV/XML
- **Claims History** — log of all submitted bulk payment requests with NDIA status
- **Participant Management** — add/edit participants, plan dates, support category budgets
- **Provider Management** — add/edit providers, their ABN, bank details, linked participants

---

### Module 3: Participant Dashboard

**Views:**
- Budget overview (remaining vs. spent per support category)
- Transaction history (all processed invoices)
- Support provider list
- Plan dates and renewal alerts

---

### Module 4: Notifications & Automation

- Email to provider when invoice is approved/rejected (with reason)
- Email to admin when new invoice submitted
- Weekly budget summary email to participants
- Alert when participant budget < 20% remaining
- Alert when plan end date < 30 days away

---

### Module 5: PACE Bulk Payment File Generator

The NDIA's myPlace portal accepts bulk payment requests as a structured CSV upload.

**Required fields per claim line:**
- Registration number (your NDIS provider number)
- NDIS number (participant)
- Support item number (NDIS line item code)
- Claim type
- Date of support (from/to)
- Quantity / hours
- Unit price
- GST code (P1 = no GST for most disability services)
- Total

**Feature:** Select all approved invoices → click "Generate PACE File" → download CSV ready for myPlace upload.

---

## 5. Tech Stack Decision

### Chosen Stack

```
Frontend:     Next.js 15 (App Router, TypeScript)
Backend:      Next.js Server Actions + API Routes
Database:     Supabase (PostgreSQL + Row Level Security)
Auth:         Supabase Auth (email/password + magic link)
File Storage: Supabase Storage (invoice PDFs/images)
OCR Engine:   Google Document AI — Invoice Parser
Email:        Resend (transactional emails)
Hosting:      Vercel (frontend + serverless functions)
              Supabase (managed Postgres, AU region)
Styling:      Tailwind CSS v4
Icons:        Lucide React
PDF Viewer:   react-pdf
```

### Why This Stack?

| Decision | Rationale |
|----------|-----------|
| **Next.js** | You already know React/TS. App Router gives server components for secure data fetching. |
| **Supabase** | Built-in Auth + Postgres + Storage + Row Level Security. AU region (Sydney). Free tier handles 0–500MB DB, 1GB storage. |
| **Google Document AI** | Best-in-class invoice parsing. $0.01 per page. At 500 invoices/month = $5. Negligible cost. |
| **Vercel** | Zero-config Next.js hosting. Free hobby tier → $20/month Pro when you have paying users. |
| **Resend** | Simple transactional email API. Free for 3,000 emails/month. |

### Alternative OCR Options Evaluated

| Option | Accuracy | Cost | Verdict |
|--------|----------|------|---------|
| **Google Document AI** | ⭐⭐⭐⭐⭐ | $0.01/page | ✅ **Recommended** |
| OpenAI GPT-4o Vision | ⭐⭐⭐⭐ | ~$0.01-0.02/img | Good fallback for unusual formats |
| Azure Document Intelligence | ⭐⭐⭐⭐⭐ | $0.01/page | Equivalent, slightly harder setup |
| Veryfi API | ⭐⭐⭐⭐ | $500/month | Way too expensive at startup |
| Tesseract.js (open source) | ⭐⭐ | Free | Inaccurate on real invoices |

**Implementation:** Google Document AI as primary → GPT-4o Vision as fallback for documents with <80% confidence score.

---

## 6. Database Schema

```sql
-- ============================================================
-- CORE ENTITIES
-- ============================================================

-- Plan Manager / Admin users (managed by Supabase Auth)
CREATE TABLE profiles (
  id           UUID PRIMARY KEY REFERENCES auth.users(id),
  role         TEXT NOT NULL CHECK (role IN ('admin', 'participant', 'provider')),
  full_name    TEXT NOT NULL,
  email        TEXT NOT NULL,
  phone        TEXT,
  abn          TEXT,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- NDIS Participants
CREATE TABLE participants (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id      UUID REFERENCES profiles(id),  -- linked login if participant has portal access
  ndis_number     TEXT NOT NULL UNIQUE,
  full_name       TEXT NOT NULL,
  dob             DATE,
  email           TEXT,
  phone           TEXT,
  plan_start_date DATE NOT NULL,
  plan_end_date   DATE NOT NULL,
  is_active       BOOLEAN DEFAULT TRUE,
  notes           TEXT,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- Service Providers
CREATE TABLE providers (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  profile_id   UUID REFERENCES profiles(id),  -- linked login
  business_name TEXT NOT NULL,
  abn          TEXT NOT NULL,
  email        TEXT NOT NULL,
  phone        TEXT,
  bsb          TEXT,
  account_number TEXT,
  account_name TEXT,
  is_active    BOOLEAN DEFAULT TRUE,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Provider <-> Participant relationship (a provider can service multiple participants)
CREATE TABLE provider_participants (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  provider_id    UUID NOT NULL REFERENCES providers(id),
  participant_id UUID NOT NULL REFERENCES participants(id),
  UNIQUE (provider_id, participant_id)
);

-- ============================================================
-- NDIS BUDGET & PRICING
-- ============================================================

-- NDIS Support Categories (from NDIS Price Guide)
CREATE TABLE support_categories (
  id            SERIAL PRIMARY KEY,
  code          TEXT NOT NULL UNIQUE,   -- e.g. "01", "07", "09", "15"
  name          TEXT NOT NULL,          -- e.g. "Daily Activities", "Support Coordination"
  budget_type   TEXT NOT NULL CHECK (budget_type IN ('core', 'capacity_building', 'capital'))
);

-- NDIS Price Guide Line Items
CREATE TABLE price_guide_items (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  support_item_number  TEXT NOT NULL UNIQUE,  -- e.g. "01_011_0107_1_1"
  name                 TEXT NOT NULL,
  category_id          INTEGER REFERENCES support_categories(id),
  unit                 TEXT NOT NULL,          -- "H" (hour), "E" (each), "D" (day)
  price_limit_act_nsw_qld_vic NUMERIC(10,2),
  price_limit_other    NUMERIC(10,2),
  price_limit_remote   NUMERIC(10,2),
  price_limit_very_remote NUMERIC(10,2),
  effective_from       DATE NOT NULL,
  effective_to         DATE,
  created_at           TIMESTAMPTZ DEFAULT NOW()
);

-- Participant Plan Budgets (per support category per plan period)
CREATE TABLE plan_budgets (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  participant_id        UUID NOT NULL REFERENCES participants(id),
  support_category_id   INTEGER NOT NULL REFERENCES support_categories(id),
  allocated_amount      NUMERIC(12,2) NOT NULL,
  plan_start_date       DATE NOT NULL,
  plan_end_date         DATE NOT NULL,
  UNIQUE (participant_id, support_category_id, plan_start_date)
);

-- ============================================================
-- INVOICES
-- ============================================================

CREATE TABLE invoices (
  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  participant_id      UUID NOT NULL REFERENCES participants(id),
  provider_id         UUID NOT NULL REFERENCES providers(id),

  -- Source document
  file_path           TEXT NOT NULL,   -- Supabase Storage path
  file_name           TEXT NOT NULL,
  file_size_bytes     INTEGER,

  -- OCR / parsed fields
  ocr_confidence      NUMERIC(5,2),    -- 0–100, from Document AI
  ocr_raw_json        JSONB,           -- full raw response stored for audit

  -- Invoice details (populated by OCR, confirmed by provider)
  invoice_number      TEXT,
  invoice_date        DATE,
  due_date            DATE,
  supplier_name       TEXT,
  supplier_abn        TEXT,
  subtotal            NUMERIC(12,2),
  gst_amount          NUMERIC(12,2),
  total_amount        NUMERIC(12,2) NOT NULL,

  -- NDIS specifics (selected by provider or admin)
  support_category_id INTEGER REFERENCES support_categories(id),

  -- Workflow status
  status              TEXT NOT NULL DEFAULT 'pending'
                      CHECK (status IN (
                        'pending',        -- submitted, awaiting review
                        'ocr_processing', -- being processed by AI
                        'needs_review',   -- OCR done, low confidence
                        'approved',       -- approved by plan manager
                        'rejected',       -- rejected by plan manager
                        'claimed',        -- included in PACE bulk file
                        'paid'            -- payment confirmed
                      )),
  rejection_reason    TEXT,
  reviewed_by         UUID REFERENCES profiles(id),
  reviewed_at         TIMESTAMPTZ,

  -- PACE claim tracking
  claim_batch_id      UUID REFERENCES claim_batches(id),
  claimed_at          TIMESTAMPTZ,
  paid_at             TIMESTAMPTZ,

  notes               TEXT,
  created_at          TIMESTAMPTZ DEFAULT NOW(),
  updated_at          TIMESTAMPTZ DEFAULT NOW()
);

-- Invoice line items (each service item within an invoice)
CREATE TABLE invoice_line_items (
  id                    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  invoice_id            UUID NOT NULL REFERENCES invoices(id) ON DELETE CASCADE,
  support_item_number   TEXT REFERENCES price_guide_items(support_item_number),
  description           TEXT NOT NULL,
  support_date_from     DATE,
  support_date_to       DATE,
  quantity              NUMERIC(10,2),
  unit                  TEXT,          -- "H", "E", "D"
  unit_price            NUMERIC(10,4),
  total                 NUMERIC(12,2) NOT NULL,
  gst_code              TEXT DEFAULT 'P1',  -- P1 = GST free (most NDIS services)

  -- Validation flags
  price_exceeds_limit   BOOLEAN DEFAULT FALSE,
  validation_notes      TEXT
);

-- ============================================================
-- PACE CLAIM BATCHES
-- ============================================================

CREATE TABLE claim_batches (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  batch_reference TEXT NOT NULL UNIQUE,  -- e.g. "BATCH-2026-04-001"
  created_by      UUID NOT NULL REFERENCES profiles(id),
  invoice_count   INTEGER NOT NULL,
  total_value     NUMERIC(14,2) NOT NULL,
  file_path       TEXT,                  -- path to generated PACE CSV file
  status          TEXT NOT NULL DEFAULT 'draft'
                  CHECK (status IN ('draft', 'submitted', 'processed', 'rejected')),
  submitted_at    TIMESTAMPTZ,
  processed_at    TIMESTAMPTZ,
  ndia_response   JSONB,
  created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- NOTIFICATIONS
-- ============================================================

CREATE TABLE notifications (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id      UUID NOT NULL REFERENCES profiles(id),
  type         TEXT NOT NULL,      -- 'invoice_submitted', 'invoice_approved', 'budget_low', etc.
  title        TEXT NOT NULL,
  message      TEXT NOT NULL,
  link         TEXT,               -- relative URL to relevant page
  is_read      BOOLEAN DEFAULT FALSE,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- ROW LEVEL SECURITY POLICIES (summary)
-- ============================================================
-- profiles:       Users see only their own profile. Admin sees all.
-- participants:   Admin sees all. Participant sees only their own record.
-- providers:      Admin sees all. Provider sees only their own record.
-- invoices:       Admin sees all. Provider sees invoices they submitted.
--                 Participant sees invoices for their NDIS number.
-- plan_budgets:   Admin sees all. Participant sees their own budgets.
-- claim_batches:  Admin only.
-- price_guide:    Public read (no RLS needed).
```

---

## 7. OCR & Invoice Intelligence Layer

### Architecture

```
Provider uploads PDF/image
        ↓
Supabase Storage (secure bucket)
        ↓
Next.js Server Action triggers processing
        ↓
┌─────────────────────────────────────┐
│  Google Document AI Invoice Parser  │
│  - Extracts 50+ structured fields   │
│  - Returns confidence per field     │
│  - $0.01 per page                   │
└─────────────────────────────────────┘
        ↓
Confidence ≥ 85%?
  YES → Pre-fill form, mark "ready to confirm"
  NO  → Pre-fill form, highlight uncertain fields for manual review
        ↓
Store raw OCR JSON in invoices.ocr_raw_json (for audit trail)
        ↓
Validate against NDIS Price Guide
  - Check unit price ≤ price limit for the selected line item
  - Flag if ABN does not match registered provider ABN
  - Flag if invoice date is outside participant's plan period
        ↓
Provider confirms / corrects → submits
        ↓
Invoice enters admin review queue
```

### Google Document AI — Key Extracted Fields

| Field | Document AI JSON Key |
|-------|---------------------|
| Invoice ID | `invoice_id` |
| Invoice date | `invoice_date` |
| Due date | `due_date` |
| Supplier name | `supplier_name` |
| Supplier ABN | `supplier_tax_id` |
| Line item description | `line_item/description` |
| Line item quantity | `line_item/quantity` |
| Line item unit price | `line_item/unit_price` |
| Line item total | `line_item/amount` |
| Subtotal | `net_amount` |
| GST | `total_tax_amount` |
| Total | `total_amount` |

### Implementation (Next.js Server Action)

```typescript
// app/actions/processInvoice.ts
'use server'

import { DocumentProcessorServiceClient } from '@google-cloud/documentai'
import { createClient } from '@/lib/supabase/server'

const docAIClient = new DocumentProcessorServiceClient()
const PROCESSOR_ID = process.env.GOOGLE_DOC_AI_PROCESSOR_ID!
const PROJECT_ID = process.env.GOOGLE_CLOUD_PROJECT_ID!
const LOCATION = 'us' // or 'eu'

export async function processInvoice(invoiceId: string, filePath: string) {
  const supabase = createClient()

  // 1. Download file from Supabase Storage
  const { data: fileData } = await supabase.storage
    .from('invoices')
    .download(filePath)

  const buffer = await fileData!.arrayBuffer()
  const base64 = Buffer.from(buffer).toString('base64')

  // 2. Send to Google Document AI
  const processorName = `projects/${PROJECT_ID}/locations/${LOCATION}/processors/${PROCESSOR_ID}`

  const [result] = await docAIClient.processDocument({
    name: processorName,
    rawDocument: {
      content: base64,
      mimeType: 'application/pdf',
    },
  })

  const document = result.document!
  const entities = document.entities || []

  // 3. Parse entities into structured fields
  const parsed = parseDocumentAIEntities(entities)

  // 4. Validate against NDIS price limits
  const validationFlags = await validateInvoice(parsed, supabase)

  // 5. Update invoice record
  await supabase.from('invoices').update({
    ocr_raw_json: result,
    ocr_confidence: parsed.overallConfidence,
    invoice_number: parsed.invoiceId,
    invoice_date: parsed.invoiceDate,
    due_date: parsed.dueDate,
    supplier_name: parsed.supplierName,
    supplier_abn: parsed.supplierAbn,
    subtotal: parsed.subtotal,
    gst_amount: parsed.gstAmount,
    total_amount: parsed.total,
    status: parsed.overallConfidence >= 85 ? 'pending' : 'needs_review',
  }).eq('id', invoiceId)

  // 6. Insert line items
  if (parsed.lineItems.length > 0) {
    await supabase.from('invoice_line_items').insert(
      parsed.lineItems.map(item => ({
        invoice_id: invoiceId,
        ...item,
        ...validationFlags[item.index],
      }))
    )
  }

  return { success: true, confidence: parsed.overallConfidence }
}
```

### PACE Bulk Payment File Generator

```typescript
// lib/pace/generateBulkFile.ts

import { createObjectCsvWriter } from 'csv-writer'

interface ClaimLine {
  registrationNumber: string   // Your NDIS provider registration number
  ndisNumber: string           // Participant NDIS number
  supportNumber: string        // NDIS line item code
  claimType: string            // Usually 'NDIS'
  claimReference: string       // Your invoice number
  quantity: number
  hours: number | null
  unitPrice: number
  gstCode: string              // 'P1' = no GST
  authorisedBy: string
  participantApproved: string
  inKind: string
  supportFrom: string          // YYYY-MM-DD
  supportTo: string            // YYYY-MM-DD
  cancellationReason: string
}

export async function generatePACEBulkFile(
  batchId: string,
  lines: ClaimLine[]
): Promise<string> {
  const fileName = `pace-bulk-${batchId}-${Date.now()}.csv`
  const filePath = `/tmp/${fileName}`

  const writer = createObjectCsvWriter({
    path: filePath,
    header: [
      { id: 'registrationNumber', title: 'RegistrationNumber' },
      { id: 'ndisNumber', title: 'NDISNumber' },
      { id: 'supportNumber', title: 'SupportNumber' },
      { id: 'claimType', title: 'ClaimType' },
      { id: 'claimReference', title: 'ClaimReference' },
      { id: 'quantity', title: 'Quantity' },
      { id: 'hours', title: 'Hours' },
      { id: 'unitPrice', title: 'UnitPrice' },
      { id: 'gstCode', title: 'GSTCode' },
      { id: 'authorisedBy', title: 'AuthorisedBy' },
      { id: 'participantApproved', title: 'ParticipantApproved' },
      { id: 'inKind', title: 'InKind' },
      { id: 'supportFrom', title: 'SupportFrom' },
      { id: 'supportTo', title: 'SupportTo' },
      { id: 'cancellationReason', title: 'CancellationReason' },
    ],
  })

  await writer.writeRecords(lines)
  return filePath
}
```

---

## 8. Infrastructure & Hosting

### Services & Costs

| Service | Purpose | Free Tier | Paid Tier |
|---------|---------|-----------|-----------|
| **Vercel** | Next.js hosting | Hobby: free | Pro: $20/month |
| **Supabase** | DB + Auth + Storage | 500MB DB, 1GB storage, 50K MAU | Pro: $25/month |
| **Google Cloud** | Document AI OCR | $300 credit (new) | ~$0.01/page |
| **Resend** | Transactional email | 3,000 emails/month | $20/month for 50K |
| **Custom domain** | yourcompanyname.com.au | — | ~$20/year |

**Total infrastructure cost at 0–30 clients: ~$0–$20/month**
**Total at 100+ clients: ~$65–$85/month**

### Supabase Region

Use **ap-southeast-1 (Singapore)** or the closest available Australian region. As of 2026, Supabase has an Australian data centre. Confirm at dashboard.supabase.com when creating project. **Australian data residency is important for NDIS compliance under Australian Privacy Act.**

### Environment Variables

```bash
# .env.local
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...   # Server only — never expose to client

GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_DOC_AI_PROCESSOR_ID=your-processor-id
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

RESEND_API_KEY=re_xxxx

NEXT_PUBLIC_APP_URL=https://yourportal.com.au
NDIS_PROVIDER_REGISTRATION_NUMBER=4-XXXXXXX  # Your NDIS registration number
```

### Deployment Pipeline

```
GitHub Repository
      ↓
Push to main branch
      ↓
Vercel auto-deploys (preview URL for PRs, production for main)
      ↓
Supabase migrations run via: npx supabase db push
```

---

## 9. Project File Structure

```
ndis-portal/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx              # Login page
│   │   ├── register/
│   │   │   └── page.tsx              # Invite-based registration
│   │   └── layout.tsx
│   │
│   ├── (portal)/
│   │   ├── layout.tsx                # Portal shell with nav + sidebar
│   │   │
│   │   ├── admin/                    # ADMIN ONLY ROUTES
│   │   │   ├── page.tsx              # Admin dashboard
│   │   │   ├── invoices/
│   │   │   │   ├── page.tsx          # Invoice queue
│   │   │   │   └── [id]/page.tsx     # Invoice review (PDF + form side-by-side)
│   │   │   ├── participants/
│   │   │   │   ├── page.tsx          # Participant list
│   │   │   │   └── [id]/page.tsx     # Participant detail + budget view
│   │   │   ├── providers/
│   │   │   │   ├── page.tsx          # Provider management
│   │   │   │   └── [id]/page.tsx     # Provider detail
│   │   │   ├── claims/
│   │   │   │   ├── page.tsx          # Claim batches list
│   │   │   │   └── new/page.tsx      # Create new PACE bulk file
│   │   │   └── reports/
│   │   │       └── page.tsx          # Reports
│   │   │
│   │   ├── provider/                 # PROVIDER ROUTES
│   │   │   ├── page.tsx              # Provider dashboard (invoice history)
│   │   │   └── invoices/
│   │   │       ├── new/page.tsx      # Submit new invoice (upload + OCR review)
│   │   │       └── [id]/page.tsx     # Invoice status view
│   │   │
│   │   └── participant/              # PARTICIPANT ROUTES
│   │       ├── page.tsx              # Budget overview
│   │       └── transactions/
│   │           └── page.tsx          # Transaction history
│   │
│   └── api/
│       ├── webhooks/
│       │   └── invoice-ocr/route.ts  # Webhook to trigger OCR after upload
│       └── pace/
│           └── generate/route.ts     # PACE bulk file generation endpoint
│
├── components/
│   ├── ui/                           # Generic UI (Button, Card, Badge, etc.)
│   ├── invoice/
│   │   ├── InvoiceUploader.tsx       # Drag-and-drop uploader with progress
│   │   ├── InvoiceOCRReview.tsx      # Side-by-side PDF viewer + editable fields
│   │   ├── InvoiceStatusBadge.tsx
│   │   └── InvoiceQueue.tsx          # Admin review queue
│   ├── budget/
│   │   ├── BudgetBar.tsx             # Visual budget usage indicator
│   │   └── BudgetSummary.tsx
│   └── pace/
│       └── ClaimBatchBuilder.tsx     # Select invoices → generate bulk file
│
├── lib/
│   ├── supabase/
│   │   ├── client.ts                 # Browser client
│   │   └── server.ts                 # Server client (cookies)
│   ├── documentai/
│   │   ├── client.ts
│   │   ├── parseEntities.ts          # Map Document AI response → our schema
│   │   └── validation.ts             # NDIS price limit validation
│   ├── pace/
│   │   └── generateBulkFile.ts       # PACE CSV generator
│   └── email/
│       └── templates.ts              # Resend email templates
│
├── actions/
│   ├── invoices.ts                   # Server actions: submit, approve, reject
│   ├── participants.ts
│   ├── providers.ts
│   └── claims.ts
│
├── types/
│   └── database.ts                   # TypeScript types (generated from Supabase)
│
├── supabase/
│   ├── migrations/                   # Database migrations
│   └── seed.sql                      # NDIS support categories + price guide seed data
│
├── middleware.ts                      # Auth + role-based route protection
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

---

## 10. Feature Build Roadmap (Phase-by-Phase)

### Phase 0 — Setup (Week 1–2)

- [ ] Create GitHub repository
- [ ] Initialise Next.js 15 project with TypeScript + Tailwind
- [ ] Set up Supabase project (AU region)
- [ ] Configure Supabase Auth (email + magic link)
- [ ] Run initial database migrations (schema above)
- [ ] Set up Google Cloud project + enable Document AI Invoice Parser
- [ ] Configure Vercel deployment (link to GitHub)
- [ ] Set up custom domain (e.g., `portal.yourcompany.com.au`)
- [ ] Configure Resend for transactional emails
- [ ] Seed NDIS support categories and 2025–26 price guide data

**Deliverable:** Deployed skeleton with login page and empty dashboard shell.

---

### Phase 1 — Core Admin & Data (Week 3–5)

- [ ] Participant management CRUD (add, edit, deactivate)
- [ ] Plan budget entry per participant per support category
- [ ] Provider management CRUD
- [ ] Provider ↔ Participant relationship management
- [ ] Admin dashboard — participant grid with budget bars
- [ ] Basic navigation + role-based route middleware

**Deliverable:** Admin can manage all participants and providers. No invoices yet.

---

### Phase 2 — Invoice Submission Portal (Week 6–9)

- [ ] Provider login flow (invite link → set password)
- [ ] Provider dashboard (list their invoices + status)
- [ ] Invoice upload component (PDF/JPG/PNG, drag-and-drop, 10MB limit)
- [ ] Supabase Storage integration (private bucket, signed URLs for PDF viewing)
- [ ] Google Document AI integration (Server Action triggered on upload)
- [ ] OCR review form (PDF viewer left, editable fields right)
- [ ] Support category + line item code selector (autocomplete from price guide)
- [ ] NDIS price limit validation (flag if unit price > price guide limit)
- [ ] Invoice submission → enters admin review queue
- [ ] Email notification to admin on new invoice submission

**Deliverable:** Providers can upload and submit invoices with OCR auto-fill.

---

### Phase 3 — Admin Invoice Review (Week 10–12)

- [ ] Invoice queue view (sortable by participant, provider, date, amount, status)
- [ ] Invoice review page (PDF viewer + all fields, approve/reject with reason)
- [ ] Budget deduction on approval (update plan_budgets running total)
- [ ] Budget overspend guard (warn if approval would exceed allocated budget)
- [ ] Email to provider on approval/rejection
- [ ] Invoice status history / audit trail

**Deliverable:** Full invoice review workflow operational. Real invoices can flow through.

---

### Phase 4 — PACE Claim File Generator (Week 13–15)

- [ ] Claim batch builder (select approved invoices, preview total)
- [ ] PACE CSV file generator (correct NDIA column format)
- [ ] Batch tracking (mark as submitted, record submission date)
- [ ] Claims history view
- [ ] Mark invoices as "claimed" and "paid" when NDIA pays
- [ ] Budget "claimed" vs "paid" tracking

**Deliverable:** One-click generation of NDIA-ready bulk payment file. Core business function complete.

---

### Phase 5 — Participant Portal (Week 16–17)

- [ ] Participant login (invite link)
- [ ] Budget overview (progress bars by support category)
- [ ] Transaction history (all processed invoices, date, provider, amount)
- [ ] Plan renewal date alert banner
- [ ] Budget < 20% warning alert

**Deliverable:** Participants can log in and see their budget and transactions.

---

### Phase 6 — Automation & Polish (Week 18–20)

- [ ] Weekly budget summary email (automated, every Monday)
- [ ] Plan end date reminder (30-day and 7-day alerts to admin)
- [ ] Budget depletion alert (email to admin + participant at 20% remaining)
- [ ] In-app notifications (bell icon with unread count)
- [ ] Dashboard charts (budget usage trends, invoices processed per month)
- [ ] CSV data export for participant transaction history
- [ ] Mobile responsiveness audit + fixes

**Deliverable:** Production-ready portal with proactive notifications.

---

### Phase 7 — Advanced (Future / Post Critical Mass)

- [ ] Bulk import of price guide updates (annual July refresh)
- [ ] Service agreement management (upload and track signed agreements)
- [ ] NDIS plan review preparation report (generate summary for LAC meetings)
- [ ] Multiple plan managers (multi-user admin with roles)
- [ ] Provider ABN verification (ABR API lookup)
- [ ] GPT-4o fallback for low-confidence OCR documents
- [ ] Xero integration (sync approved invoices as bills)
- [ ] White-label option (sell portal access to other small plan managers)

---

## 11. Security & Compliance

### Authentication & Access Control

```typescript
// middleware.ts — Role-based route protection
import { createMiddlewareClient } from '@supabase/auth-helpers-nextjs'
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export async function middleware(req: NextRequest) {
  const res = NextResponse.next()
  const supabase = createMiddlewareClient({ req, res })
  const { data: { session } } = await supabase.auth.getSession()

  const pathname = req.nextUrl.pathname

  if (!session) {
    return NextResponse.redirect(new URL('/login', req.url))
  }

  // Get user role
  const { data: profile } = await supabase
    .from('profiles')
    .select('role')
    .eq('id', session.user.id)
    .single()

  // Route protection
  if (pathname.startsWith('/admin') && profile?.role !== 'admin') {
    return NextResponse.redirect(new URL('/unauthorised', req.url))
  }
  if (pathname.startsWith('/provider') && profile?.role !== 'provider') {
    return NextResponse.redirect(new URL('/unauthorised', req.url))
  }
  if (pathname.startsWith('/participant') && profile?.role !== 'participant') {
    return NextResponse.redirect(new URL('/unauthorised', req.url))
  }

  return res
}
```

### Privacy & Data Security Checklist

- [ ] **Supabase Row Level Security** enabled on ALL tables — no table should have RLS disabled
- [ ] **Invoice file storage** in private bucket — only accessible via signed URLs generated server-side
- [ ] **NDIS numbers** never logged to console or error tracking tools
- [ ] **Australian data residency** — confirm Supabase project in Sydney/AU region
- [ ] **TLS everywhere** — Vercel and Supabase enforce HTTPS by default
- [ ] **Service account keys** (Google Cloud) stored as environment variables, never committed to git
- [ ] **Privacy Policy** published on portal covering: data collected, purpose, storage location, retention period
- [ ] **Terms of Service** for provider and participant portal users
- [ ] **Audit log** — all invoice status changes recorded with timestamp and user ID
- [ ] **Data retention policy** — invoices and documents retained for 7 years (ATO requirement)
- [ ] **Backup strategy** — Supabase Pro includes daily automated backups; test restore quarterly

### NDIS-Specific Compliance

- Every invoice processed must be stored with its original PDF — do not delete source documents
- `ocr_raw_json` field preserves the complete Document AI response for audit purposes
- All price guide validations must be logged in `invoice_line_items.validation_notes`
- PACE bulk files should be archived (stored in Supabase Storage) even after submission

---

## 12. Cost Model

### Infrastructure Running Costs

| Stage | Clients | Monthly Infra Cost |
|-------|---------|-------------------|
| Pre-launch (dev) | 0 | $0 (all free tiers) |
| Early (0–30 clients) | 1–30 | ~$0–20 |
| Growth (30–100 clients) | 30–100 | ~$45–65 |
| Scale (100–300 clients) | 100–300 | ~$85–120 |

*Breakdown at 100 clients: Vercel Pro $20 + Supabase Pro $25 + Google Doc AI ~$5 + Resend $0 + domain $2 = ~$52/month*

### Revenue vs. Infra Cost at Scale

| Clients | Monthly Revenue (@ $104.45/client) | Monthly Infra | Gross Margin |
|---------|------------------------------------|---------------|--------------|
| 10 | $1,044 | ~$0 | 100% |
| 30 | $3,133 | ~$20 | 99.4% |
| 50 | $5,222 | ~$45 | 99.1% |
| 100 | $10,445 | ~$65 | 99.4% |
| 200 | $20,890 | ~$100 | 99.5% |

Infrastructure is essentially a rounding error in the cost model.

### Development Time Investment

| Phase | Estimated Hours |
|-------|----------------|
| Phase 0 — Setup | 8–12 hours |
| Phase 1 — Core admin | 20–30 hours |
| Phase 2 — Invoice submission + OCR | 30–40 hours |
| Phase 3 — Admin review workflow | 15–20 hours |
| Phase 4 — PACE file generator | 10–15 hours |
| Phase 5 — Participant portal | 10–15 hours |
| Phase 6 — Automation + polish | 15–20 hours |
| **Total MVP (Phase 0–6)** | **~108–152 hours** |

At 10 hours/week evenings and weekends: **~3–4 months to MVP**.

---

## 13. Scaling Plan

### Technical Scaling

When you reach 200+ clients, the following enhancements become worthwhile:

- **Background job queue** (Supabase Edge Functions + pg_cron) for OCR processing — avoids timeout on large PDF batches
- **Supabase connection pooling** (PgBouncer, already included in Pro tier) — enable for high-concurrency
- **CDN for invoice files** — Supabase Storage already uses a CDN layer
- **Rate limiting on upload endpoint** — prevent abuse (Vercel Edge Config)

### Business Scaling

When you incorporate as Pty Ltd (at ~$80–120K revenue):

- Portal becomes a business asset on the balance sheet
- You can hire a part-time operations assistant and give them a `staff` role in the portal
- Consider licensing portal access to other sole-trader plan managers ($50–200/month SaaS) — the white-label future path
- The PACE file generator + OCR combination is unique IP with genuine commercial value

### Critical Path to First Client

```
Week 1:    Register ABN + business name + GST
Week 1:    Get professional indemnity insurance
Week 1–4:  NDIS registration audit (verification pathway)
Week 2:    Set up Xero (bridge accounting)
Week 2:    Build Supabase + Next.js skeleton (Phase 0)
Week 3–8:  NDIS Commission review period
Week 4–8:  Build Phase 1 + Phase 2 (admin + invoice submission)
Week 8:    Receive NDIS registration certificate
Week 8:    First outreach to support coordinators
Week 10:   First client onboarded → use portal Phase 1–2
Week 12:   Phase 3 complete → full invoice review in portal
Week 15:   Phase 4 complete → PACE file generated from portal
```

---

*Last updated: April 2026*
*Stack: Next.js 15 · Supabase · Google Document AI · Vercel · Resend*
