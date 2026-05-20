# AccSoft — Session Build Plan

> Each session is a self-contained context window. Start a new session by telling Claude:
> "I am building AccSoft, a personal accounting web app. Read planning.md and todo.md in VScode/accsoft/ then continue with Session X."

---

## Sessions 1–5 — Complete ✓

- **S1:** Project setup, venv, DB models, Flask-Migrate, auth (login/logout), seed script.  
  DB: `postgresql://postgres:WatermarkD21@127.0.0.1:5433/accsoft_dev` · login: `admin@example.com` / `changeme123`
- **S2:** Chart of Accounts CRUD — grouped list by type, add/edit/deactivate/hard-delete, flash messages.
- **S3:** Double-entry transaction form, transaction list, general ledger. CSV export. Verified 2026-04-18.
- **S4:** File attachments (JPG/PNG/PDF, UUID storage, inline viewer/download). Dashboard with account balances + recent transactions. Verified 2026-04-18.
- **S4.5:** Customers & Suppliers CRUD, linked to transactions (AR/AP), detail pages with outstanding balance. Verified 2026-04-18.
- **S5:** OCR pipeline — pdfplumber extraction, regex field parser (vendor/date/invoice no/subtotal/GST/total), vendor & keyword GL suggester, upload → review → confirm → post flow. Unknown vendor flagged with save-mapping checkbox. Invoice preview modal on review page (PDF iframe, image tag). PaddleOCR deferred. Verified 2026-04-18.

> UX improvements and polish for completed sessions are tracked in `UX improvements.md`.

---

## Session 5 — OCR Pipeline
**Goal:** Upload an invoice → auto-extract fields → review → post to ledger.

### Steps
- [x] Install and test pdfplumber (digital PDF text extraction) — PaddleOCR skipped (deferred)
- [x] `ocr/pipeline.py` — detect input type, route pdfplumber for digital PDFs; images return empty (manual entry)
- [x] `ocr/extractor.py` — regex extraction: vendor, invoice_no, date, subtotal, gst, total
- [x] `ocr/gl_suggester.py` — vendor lookup → keyword fallback → suggested GL accounts
- [x] OCR upload page — upload invoice → run pipeline → store OcrResult → redirect to review
- [x] Review & confirm form — user edits extracted fields, selects/confirms GL accounts, posts transaction
- [x] Save vendor mapping on confirm (checkbox)
- [x] Flag unrecognised vendors for manual GL selection

### Verify
- Upload a digital PDF invoice → vendor, date, total extracted correctly
- Upload a photo of a receipt → OCR extracts key fields
- Known vendor → GL accounts pre-filled
- Unknown vendor → flagged, user picks manually, mapping saved for next time

---

## Session 5.5 — Bulk Invoice Upload
**Goal:** Upload multiple invoices at once → system processes each → user reviews and approves one by one.

### Steps
- [x] Bulk upload form — multi-file input, accepts PDF/JPG/PNG
- [x] `BulkUploadJob` model — tracks a batch: id, status (processing/completed), created_at
- [x] `BulkUploadItem` model — one row per file: job_id, attachment_id, ocr_result_id, status (pending/approved/auto_approved/skipped), transaction_id (null until approved)
- [x] On submit: save all files, create `OcrResult` per file (run pipeline immediately — files are small so sync is fine for now)
- [x] Batch queue page — list all items in the job with status badges (pending / approved / auto-approved / skipped)
- [x] Per-item review — same review form as Session 5 single upload, but with prev/next navigation between items in the batch
- [x] Approve posts the transaction and marks item approved; Skip marks it skipped (file still saved, no transaction)
- [x] Batch summary page — shown when all items are approved or skipped: count posted, count skipped, link to each transaction

### Design notes
- Reuse `ocr/pipeline.py`, `ocr/extractor.py`, `ocr/gl_suggester.py` unchanged
- Reuse the single-item review template with a batch nav bar added at the top
- No background worker needed — process all files synchronously on upload (add async/Celery later if batches grow large)
- Known vendors auto-approve only if confidence == 1.0 AND vendor mapping exists — otherwise always require manual review

### Verify
- Upload 3 invoices at once → batch queue shows 3 items
- Navigate prev/next through items in the review form
- Approve all → batch summary shows 3 transactions posted
- Skip one → no transaction created, file still accessible from batch summary

---

## Session 6 — Bank Reconciliation
**Goal:** Match posted transactions against a bank statement.

### Data Models (`models/reconciliation.py`)

**`BankStatement`** — one record per CSV import
- `id` (UUID PK), `account_id` (FK → Account), `filename`, `imported_at`, `statement_date` (period end, optional)

**`BankStatementLine`** — immutable rows from CSV
- `id`, `bank_statement_id` (FK), `date`, `description`, `amount` (Decimal), `reference` (nullable), `balance` (nullable), `external_id` (nullable — for deduplication), `is_matched` (bool)

**`ReconciliationSession`** — one per reconciliation period
- `id`, `account_id` (FK), `bank_statement_id` (FK), `period_start`, `period_end`, `status` (enum: `open / in_review / complete / reopened`), `opening_balance`, `closing_balance` (nullable), `created_at`, `completed_at` (nullable), `notes`

**`ReconciliationMatch`** — join table, true many-to-many between bank lines and ledger transactions
- `id`, `session_id` (FK), `bank_statement_line_id` (FK), `transaction_id` (FK), `matched_at`, `matched_by` (FK → User)

### Blueprint Structure

```
blueprints/reconciliation/
    __init__.py      ← exports reconciliation_bp
    routes.py        ← route handlers
    service.py       ← all business logic
templates/reconciliation/
    list.html        ← all sessions with status badges
    new.html         ← create session + CSV upload
    detail.html      ← two-column reconciliation screen
    history.html     ← audit trail of matches
```

### Routes

| Method | URL | Purpose |
|---|---|---|
| GET | `/reconciliation/` | List all sessions |
| GET/POST | `/reconciliation/new` | Create session, import CSV |
| GET | `/reconciliation/<id>` | Main reconciliation screen |
| POST | `/reconciliation/<id>/match` | Create match (bank lines ↔ transactions) |
| POST | `/reconciliation/<id>/unmatch` | Remove a match |
| POST | `/reconciliation/<id>/complete` | Lock session as complete |
| POST | `/reconciliation/<id>/reopen` | Reopen a completed session |

### Service Functions (`service.py`)

- `import_csv(file, account_id)` — parse CSV, validate columns, dedupe via `external_id`, create `BankStatement` + `BankStatementLine` records
- `get_unmatched_bank_lines(session)` — lines where `is_matched = False`
- `get_unmatched_transactions(session)` — `Transaction` rows for the same account + period not in any `ReconciliationMatch` for this session
- `create_match(session_id, line_ids, transaction_ids)` — writes `ReconciliationMatch` rows, sets `is_matched = True` on lines
- `remove_match(match_id)` — deletes match rows, resets `is_matched`
- `complete_session(session)` — validates all lines matched or skipped, sets status + `completed_at`
- `reopen_session(session)` — sets status to `reopened`, clears `completed_at`

### Reconciliation Screen Layout (`detail.html`)

Two-column layout with checkboxes on both sides. User selects one or many from each column then clicks **Match Selected**. A warning is shown if selected amounts differ significantly (to support split transactions without blocking the match).

```
[ Account: ANZ Cheque | Period: 1 Apr – 30 Apr | Status: open ]
[ Bank Total: $X | Ledger Total: $Y | Difference: $Z ]

┌─────────────────────────┬─────────────────────────┐
│  Bank Statement Lines   │   Ledger Transactions   │
│  (unmatched)            │   (unmatched)           │
│  ☐ 01 Apr  Rent  -1200 │  ☐ 01 Apr  Rent   1200  │
│  ☐ 05 Apr  AWS    -89  │  ☐ 05 Apr  AWS      89  │
└─────────────────────────┴─────────────────────────┘
[ Match Selected ]

─── Matched Items ────────────────────────────────────
  Bank: 01 Apr Rent $1200 ↔ Ledger: Rent $1200  [Unmatch]
```

### Locking

- `status = complete` → match/unmatch routes return a flash error, no changes allowed
- **Reopen** sets status to `reopened` and re-enables editing

### Steps
- [ ] `models/reconciliation.py` — BankStatement, BankStatementLine, ReconciliationSession, ReconciliationMatch
- [ ] Export new models in `models/__init__.py`
- [ ] `flask db migrate && flask db upgrade`
- [ ] `blueprints/reconciliation/__init__.py`
- [ ] `service.py` — CSV import first, then matching logic, then session state
- [ ] `routes.py` — list → new → detail → match/unmatch → complete/reopen
- [ ] Templates — list → new → detail → history
- [ ] Register blueprint in `app/__init__.py`, add nav link in `base.html`

### Verify
- Import a sample CSV → rows appear as bank statement lines
- Match one ledger transaction to one bank line → both disappear from unmatched columns
- Unmatched items visually flagged and counted in totals
- Complete a reconciliation period → status badge shows complete, edits locked, appears in history

---

## Session 7 — Reports & CSV Export
**Goal:** P&L, expense summary, balance summary, CSV exports.

### Steps
- [ ] Profit & Loss report (date range: revenue − expenses)
- [ ] Expense summary by account/category (date range)
- [ ] Account balance summary (all accounts, current balances)
- [ ] Export any report to CSV
- [ ] Print-friendly layout for reports

### Verify
- P&L for a date range matches manually calculated figures
- CSV export opens correctly in Excel

---

## Session 9 — CRM: Contacts Hub & Activity Log
**Goal:** Unified contacts hub combining customers and suppliers; internal notes and activity log per contact.

### Steps
- [ ] `ContactNote` model — `id`, `contact_type` (enum: `customer`/`supplier`), `contact_id` (UUID, not FK — resolved at query time), `note_type` (enum: `call`/`email`/`meeting`/`note`), `body` (TEXT), `created_at`
- [ ] `ContactTag` model — `id`, `name`, `colour` (hex); `ContactTagAssignment` join table — `tag_id`, `contact_type`, `contact_id`
- [ ] `flask db migrate && flask db upgrade`
- [ ] `/contacts` hub page — unified list of customers + suppliers, searchable, filterable by type/tag
- [ ] Add tag selector to customer + supplier add/edit forms
- [ ] Activity timeline on customer + supplier detail pages (notes, linked transactions)
- [ ] "Add note" form on detail pages (select note type, body, submit)
- [ ] Register blueprint + nav link in `base.html`

### Verify
- `/contacts` shows all customers and suppliers, type badges, searchable
- Add a tag to a customer → appears on list and detail page
- Log a call note on a supplier → appears in activity timeline on their detail page
- Linked transactions still appear on detail page as before

---

## Session 10 — CRM: NDIS Participant Profiles
**Goal:** NDIS-specific profile layer on top of existing Customer records.

### Steps
- [ ] `Participant` model — `id`, `customer_id` (FK → Customer, one-to-one), `ndis_number` (VARCHAR), `date_of_birth` (DATE, nullable), `plan_start_date` (DATE), `plan_end_date` (DATE), `monthly_management_fee` (NUMERIC 12,2), `lac_name` (VARCHAR, nullable), `lac_email` (VARCHAR, nullable), `lac_phone` (VARCHAR, nullable), `status` (enum: `active`/`expiring_soon`/`expired`/`inactive`), `notes` (TEXT)
- [ ] `flask db migrate && flask db upgrade`
- [ ] `/participants` list — NDIS number, plan dates, status badge (Active / Expiring <30d / Expired), monthly fee
- [ ] Add/edit participant form — linked to an existing customer, or create inline
- [ ] Participant detail page — NDIS fields + inherited customer contact info + activity timeline + linked transactions
- [ ] Nightly status recalculation: cron-style function (called on page load) to set `expiring_soon` / `expired` from `plan_end_date`
- [ ] Register blueprint + nav link

### Verify
- Create a participant linked to an existing customer → NDIS fields saved
- Participant with `plan_end_date` within 30 days → badge shows "Expiring Soon"
- Participant detail shows linked invoices/transactions

---

## Session 11 — CRM: Plan Budget Tracking
**Goal:** Track NDIS plan budgets by support category and monitor spend against allocation.

### Steps
- [ ] `SupportCategory` model — `id`, `name` (Core Supports / Capacity Building / Capital Supports), `ndis_code` (VARCHAR), `gst_applicable` (BOOLEAN, default False — most NDIS supports are GST-free)
- [ ] `ParticipantBudget` model — `id`, `participant_id` (FK), `support_category_id` (FK), `plan_year` (INT, e.g. 2026), `allocated_amount` (NUMERIC 12,2), `notes`
- [ ] Add `support_category_id` (nullable FK → SupportCategory) and `participant_id` (nullable FK → Participant) to `transactions` table
- [ ] `flask db migrate && flask db upgrade`
- [ ] Budget entry form on participant detail page — add/edit allocations per category per plan year
- [ ] Budget utilisation panel: for each category, show allocated / spent (sum of linked transactions) / remaining / % bar; highlight >80% in amber, >100% in red
- [ ] Dashboard card: "Participants near budget limit" (>80% in any category)
- [ ] Support category seeder (Core Supports, Capacity Building, Capital Supports)

### Verify
- Add budget allocation of $10,000 Core Supports for a participant
- Link two transactions (total $8,200) to that participant + category
- Budget panel shows $8,200 spent / $1,800 remaining / 82% (amber highlight)
- Dashboard card lists that participant

---

## Session 12 — CRM: Provider Profiles & Service Agreements
**Goal:** NDIS provider data on supplier records; service agreement tracking linking providers to participants.

### Steps
- [ ] `ProviderProfile` model — `id`, `supplier_id` (FK → Supplier, one-to-one), `ndis_registration_number` (VARCHAR, nullable), `registration_groups` (JSONB array of strings), `service_regions` (VARCHAR, nullable), `notes`
- [ ] `ServiceAgreement` model — `id`, `provider_id` (FK → Supplier), `participant_id` (FK → Participant), `support_category_id` (FK → SupportCategory), `start_date`, `end_date`, `agreed_rate` (NUMERIC 10,4), `rate_unit` (enum: `hour`/`session`/`km`/`item`), `status` (enum: `active`/`expired`/`cancelled`), `notes`
- [ ] Add optional `service_agreement_id` (FK → ServiceAgreement) to `transactions`
- [ ] `flask db migrate && flask db upgrade`
- [ ] Provider profile tab/section on supplier detail page — add/edit NDIS fields
- [ ] `/service-agreements` list — filterable by provider, participant, status, expiry
- [ ] Add/edit service agreement form
- [ ] Link a transaction to a service agreement on the transaction form (optional dropdown)
- [ ] Register blueprint + nav link

### Verify
- Add NDIS registration details to an existing supplier → saved and shown on their detail page
- Create a service agreement between a provider and participant → appears in `/service-agreements`
- Post a transaction linked to that service agreement → shows on agreement detail page

---

## Session 13 — CRM: Reports & Alerts
**Goal:** CRM-specific reports — plan summaries, budget burn rates, provider payments, renewal alerts.

### Steps
- [ ] **Participant Plan Summary** — per participant: support categories, allocated vs spent vs remaining; CSV export
- [ ] **Budget Burn Rate** — monthly spend by support category across all participants (bar/table); date range filter; CSV export
- [ ] **Upcoming Renewals** — participants with `plan_end_date` within 0–90 days, sorted ascending; CSV export
- [ ] **Provider Payment Summary** — total paid per provider by date range, broken down by support category; CSV export
- [ ] Add CRM reports to `/reports` page (new tab or section alongside financial reports)
- [ ] Budget alert emails/notifications — deferred; for now surface alerts only on dashboard

### Verify
- Participant Plan Summary matches manually calculated figures from Session 11 budget data
- Upcoming Renewals correctly shows participants with plan expiry within 90 days
- All four reports export to CSV correctly

---

## Session 14 — VPS Deployment (Hetzner)
**Goal:** App live on Hetzner VPS with HTTPS.

### Steps
- [ ] Provision Hetzner CX22 (Ubuntu 24.04)
- [ ] Install: Python, PostgreSQL, Nginx, Certbot, Git
- [ ] Clone repo to VPS, set up production `.env`
- [ ] Set up PostgreSQL on VPS, run migrations, seed accounts + support categories
- [ ] Configure Gunicorn as systemd service
- [ ] Configure Nginx as reverse proxy
- [ ] Issue Let's Encrypt SSL cert via Certbot
- [ ] Set up daily `pg_dump` backup (cron job)
- [ ] Test all features on live URL

### Verify
- Visit `https://yourdomain.com` → login page loads with valid SSL
- All Session 1–13 features work on production
- `pg_dump` backup runs and produces a valid file

---

## Status Tracker

| Session | Focus | Status |
|---|---|---|
| 1 | Project setup, models, auth | **Complete** |
| 2 | Chart of Accounts | **Complete** |
| 3 | Transaction entry + ledger | **Complete** |
| 4 | Attachments + dashboard | **Complete** |
| 4.5 | Customers & Suppliers | **Complete** |
| 5 | OCR pipeline | **Complete** |
| 5.5 | Bulk invoice upload | **Complete** |
| 6 | Bank reconciliation | **Ready for testing** |
| 7 | Reports + CSV | Not started |
| 8 | VPS deployment | Pushed to Session 14 |
| 9 | CRM: Contacts hub + activity log | Not started |
| 10 | CRM: NDIS participant profiles | Not started |
| 11 | CRM: Plan budget tracking | Not started |
| 12 | CRM: Provider profiles + service agreements | Not started |
| 13 | CRM: CRM reports + alerts | Not started |
| 14 | VPS deployment | Not started |
