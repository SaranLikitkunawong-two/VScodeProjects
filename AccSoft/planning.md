# AccSoft — Accounting Software Planning

## Skill Reference Files

These files in `SKILLS/` define the rules and patterns to follow when building AccSoft. **Refer to the relevant file before implementing any feature in its domain.**

| File | When to consult |
|---|---|
| [`SKILLS/Architecture.md`](SKILLS/Architecture.md) | Project structure, layer responsibilities, Flask patterns, database conventions, OCR pipeline design, deployment — consult before any structural or cross-cutting work |
| [`SKILLS/Flask.md`](SKILLS/Flask.md) | Application factory, blueprints, route design, config, error handling, logging, testing, file uploads — consult whenever writing or reviewing Flask code |
| [`SKILLS/Accounting.md`](SKILLS/Accounting.md) | Double-entry rules, Australian GST/BAS, transaction patterns, chart of accounts conventions, reconciliation, reporting — consult whenever implementing any accounting logic or UI |

---

## Overview
A personal web-based accounting portal for a small service business. Accessible from any browser via login. Handles expense/income tracking, general ledger, bank reconciliation, and file attachments (invoices, receipts, photos).

---

## Tech Stack

| Layer | Choice | Reason |
|---|---|---|
| Backend | Python + Flask | Simple, readable, easy to maintain |
| Database | PostgreSQL | Familiar, robust, relational |
| ORM | SQLAlchemy | Maps Python objects to DB tables |
| File Storage | Local filesystem on VPS (or S3-compatible later) | Simple to start, easy to migrate |
| Auth | Flask-Login | Session-based login, lightweight |
| Frontend | HTML + Tailwind CSS + minimal JS | No heavy framework, fast to build |
| Hosting | Hetzner VPS (~$5-6/month) | Cheap, reliable, 99.9% uptime |
| SSL | Let's Encrypt (Certbot) | Free, auto-renewing HTTPS |
| Domain | Optional (~$12/year) | e.g. mybusiness.com |
| OCR | pdfplumber + PaddleOCR + invoice2data | See OCR section below |
| GL Suggestions | Keyword rules + Claude API fallback | See OCR section below |

---

## Features

### Phase 1 — Core (Build First)
- [x] User authentication (login/logout, single user)
- [x] Chart of Accounts (create/edit/deactivate accounts)
- [x] Transaction entry (double-entry: debit/credit)
- [x] Income & expense categorization
- [x] File attachments per transaction (invoices, receipts, photos)
- [x] General ledger view (all transactions by account)
- [x] Basic dashboard (account balances, recent transactions)

### Phase 2 — Reconciliation & Reporting
- [ ] Bank reconciliation (match transactions to bank statement)
- [ ] Profit & Loss report (by date range)
- [ ] Expense summary by category
- [ ] Account balance summary
- [ ] Export to CSV

### Phase 2.5 — OCR & Automated Invoice Processing
- [x] Upload invoice/receipt → extract fields automatically (vendor, date, total, tax)
- [x] Review & confirm extracted fields before posting
- [x] Suggested GL account mapping based on vendor/description
- [x] User can correct suggestions; corrections are remembered per vendor (save-mapping checkbox)
- [x] Support: digital PDFs (pdfplumber)
- [ ] Support: scanned PDFs / JPG/PNG photos via OCR — deferred (PaddleOCR not yet installed)
- [ ] Bulk invoice upload — multiple files at once, queue-style review (Session 5.5, planned)

### Phase 2.6 — Customers & Suppliers
- [x] Customer profiles: name, contact, email, phone, address, ABN, notes
- [x] Supplier profiles: same fields
- [x] Link customers to AR transactions; link suppliers to AP transactions
- [x] Customer/supplier detail page showing linked transactions and outstanding balance
- [x] Customer/supplier selector on transaction form

### Phase 3 — Maybe Later
- [ ] Tax report export
- [ ] Migrate file storage to Cloudflare R2 / AWS S3
- [ ] Migrate hosting to self-hosted machine
- [ ] Multi-currency support
- [ ] Claude API fallback for GL suggestions (unrecognised vendor/description → AI suggests account from chart of accounts)

### Phase 4 — NDIS Portal Integration
AccSoft will act as the accounting backend for the NDIS Plan Management portal (separate Next.js + Supabase app).

**How it works:**
- NDIS portal exposes a webhook trigger on invoice approval
- NDIS portal POSTs invoice data to AccSoft's REST API endpoint
- AccSoft creates a `supplier_bill` transaction automatically — no manual entry needed

**AccSoft changes required:**
- [ ] Expose a REST API endpoint: `POST /api/bills/create` (API key authenticated)
- [ ] Accept JSON payload with invoice fields (see below)
- [ ] Auto-match or create supplier record based on ABN
- [ ] Post double-entry: Debit NDIS Client Expense account → Credit Accounts Payable
- [ ] Link original invoice PDF (download from NDIS portal Supabase Storage URL, store as attachment)
- [ ] Return `{ transaction_id, status }` to NDIS portal for confirmation

**Expected payload from NDIS portal:**
```json
{
  "provider_name": "ABC Support Services",
  "provider_abn": "12 345 678 901",
  "invoice_number": "INV-001",
  "invoice_date": "2026-04-20",
  "support_category": "Daily Activities",
  "subtotal": 450.00,
  "gst_amount": 0.00,
  "total_amount": 450.00,
  "participant_name": "John Smith",
  "ndis_number": "430 123 456",
  "file_url": "https://supabase-storage-url/invoices/abc.pdf"
}
```

**New GL accounts needed (to add to seed/CoA):**
- `4100` NDIS Plan Management Fees (Revenue — monthly management fee per participant)
- `5400` NDIS Client Disbursements (Expense — provider payments on behalf of participants)

---

## Chart of Accounts

### Account Hierarchy (3 levels)

Accounts exist at exactly one of three levels. Only Level 3 (subaccounts) may have transactions posted to them. Levels 1 and 2 are consolidation-only — their balances are always derived by summing their descendants.

| Level | Name | Example | Posting allowed? |
|---|---|---|---|
| 1 | Type | Expenses | No — consolidation only |
| 2 | Parent account | Software Subscriptions | No — consolidation only |
| 3 | Subaccount | Adobe Creative Cloud | Yes |

- A Level 2 parent account must belong to a Level 1 type.
- A Level 3 subaccount must belong to a Level 2 parent account.
- Transaction entry dropdowns show only Level 3 subaccounts.

### Account Code Ranges (fixed convention)
| Range | Type (Level 1) |
|---|---|
| 1000–1999 | Assets |
| 2000–2999 | Liabilities |
| 3000–3999 | Equity |
| 4000–4999 | Revenue |
| 5000–5999 | Expenses |

Code convention:
- Level 1 (type): no code — identified by the type enum
- Level 2 (parent): e.g. `5100` — first available round number in the type's range
- Level 3 (subaccount): e.g. `5101`, `5102` — sequential under the parent

### Starter Accounts (minimal default on first login)
| Code | Name | Level | Parent |
|---|---|---|---|
| — | Asset | 1 (type) | — |
| 1000 | Bank & Cash | 2 (parent) | Asset |
| 1001 | Cheque Account | 3 (subaccount) | Bank & Cash |
| 1100 | Receivables | 2 (parent) | Asset |
| 1101 | Accounts Receivable | 3 (subaccount) | Receivables |
| — | Liability | 1 (type) | — |
| 2000 | Payables | 2 (parent) | Liability |
| 2001 | Accounts Payable | 3 (subaccount) | Payables |
| 2100 | Tax Liabilities | 2 (parent) | Liability |
| 2101 | GST / Tax Payable | 3 (subaccount) | Tax Liabilities |
| — | Equity | 1 (type) | — |
| 3000 | Owner's Equity | 2 (parent) | Equity |
| 3001 | Capital Contributions | 3 (subaccount) | Owner's Equity |
| 3100 | Retained Earnings | 2 (parent) | Equity |
| 3101 | Current Year Earnings | 3 (subaccount) | Retained Earnings |
| — | Revenue | 1 (type) | — |
| 4000 | Service Revenue | 2 (parent) | Revenue |
| 4001 | Consulting Income | 3 (subaccount) | Service Revenue |
| — | Expense | 1 (type) | — |
| 5000 | General Expenses | 2 (parent) | Expense |
| 5001 | Miscellaneous | 3 (subaccount) | General Expenses |
| 5100 | Office Expenses | 2 (parent) | Expense |
| 5101 | Stationery & Supplies | 3 (subaccount) | Office Expenses |
| 5200 | Professional Fees | 2 (parent) | Expense |
| 5201 | Accounting & Legal | 3 (subaccount) | Professional Fees |
| 5300 | Travel & Transport | 2 (parent) | Expense |
| 5301 | Fuel & Parking | 3 (subaccount) | Travel & Transport |

### Chart of Accounts UI Rules
- Accounts displayed as an indented tree: Level 1 → Level 2 → Level 3
- Accounts grouped and colour-coded by type on the management page
- **Add account**: must specify level and (for levels 2–3) parent; code auto-suggested as next available under the parent (user can override)
- **Delete account**: only allowed if account has no transactions and no children; otherwise deactivate (soft delete)
- **Deactivate**: hides account from transaction entry dropdowns but preserves history; deactivating a parent cascades to all children
- **Edit**: name, code, and description editable at any time; type and level are locked once transactions or children exist
- **Posting restriction**: transaction entry forms must only show Level 3 subaccounts in account dropdowns

---

## Data Model (Core Tables)

### `users`
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| email | VARCHAR | Login email |
| password_hash | VARCHAR | Hashed password |
| created_at | TIMESTAMP | |

### `accounts`
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| name | VARCHAR | e.g. "Software Subscriptions", "Adobe Creative Cloud" |
| type | ENUM | asset, liability, equity, revenue, expense |
| code | VARCHAR | e.g. "5100", "5101" — null for Level 1 type nodes |
| description | TEXT | |
| level | SMALLINT | 1 = type, 2 = parent account, 3 = subaccount |
| parent_account_id | UUID | FK → accounts (null for Level 1); Level 2 → Level 1, Level 3 → Level 2 |
| allow_posting | BOOLEAN | True only for Level 3 subaccounts |
| is_active | BOOLEAN | Soft delete |
| created_at | TIMESTAMP | |

### `transactions`
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| date | DATE | Transaction date |
| description | TEXT | What it was for |
| reference | VARCHAR | Invoice number, receipt ref, etc. |
| created_at | TIMESTAMP | |

### `transaction_lines`
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| transaction_id | UUID | FK → transactions |
| account_id | UUID | FK → accounts |
| type | ENUM | debit / credit |
| amount | NUMERIC(12,2) | |

### `attachments`
| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| transaction_id | UUID | FK → transactions |
| filename | VARCHAR | Original filename |
| storage_path | VARCHAR | Path on server |
| mime_type | VARCHAR | image/jpeg, application/pdf, etc. |
| uploaded_at | TIMESTAMP | |

---

## OCR & Automated Invoice Processing

### The Problem
Invoices arrive as digital PDFs, scanned PDFs, or photo receipts. We need to:
1. Extract key fields (vendor, date, invoice number, line items, totals, tax)
2. Suggest which GL accounts to debit/credit

### Recommended Library Stack

| Input Type | Library | Why |
|---|---|---|
| Digital PDF (text embedded) | **pdfplumber** | Native text extraction, excellent table detection, no OCR needed |
| Scanned PDF or image (JPG/PNG) | **PaddleOCR** (PP-OCRv5) | Best accuracy on CPU (94.5%), fits in 4GB RAM, Apache 2.0 |
| Field extraction (all types) | **invoice2data** | Only library with built-in invoice field extraction via YAML templates |

**Why not the others:**
- `pytesseract` — ~80% accuracy, fine as fallback but PaddleOCR is meaningfully better
- `EasyOCR` — 1-2GB memory alone, too heavy for our VPS
- `Surya` / `doctr` — GPU-optimised, poor CPU performance
- `AWS Textract` / `Google Vision` — not open-source, costs per API call

### How It Works (Pipeline) — as built

```
Upload invoice/receipt
        │
        ▼
Is it a digital PDF? ──Yes──▶ pdfplumber (extract raw text)
        │                             │
        No (image)                    ▼
        ▼                     extractor.py (regex parser)
Return empty text                     │   vendor, date, invoice_no,
(manual entry)                        │   subtotal, GST, total
                                      ▼
                             GL Suggestion Engine
                              1. vendor_mappings (exact match)
                              2. keyword_mappings (keyword scan)
                              3. Flag unknown → manual selection
                                        │
                                        ▼
                             User reviews & edits on review page
                             (invoice preview modal available)
                                        │
                                        ▼
                             Confirm → transaction posted to ledger
                             Attachment linked to transaction
                             Vendor mapping saved (if checkbox ticked)
```

> **invoice2data** is installed but not used as the primary extractor — regex parsing in `extractor.py` is faster and more predictable for the field set we need. invoice2data YAML templates remain an option for future structured invoice formats.

> **PaddleOCR** — deferred. Image uploads are accepted but return empty text; the user fills fields manually. Install `paddlepaddle` + `paddleocr` from `requirements-ocr.txt` when ready to add image OCR.

### GL Suggestion Engine

Two-tier approach:

**Tier 1 — Keyword Rules (fast, free, no API)**
- `vendor_mappings` table: exact vendor name (case-insensitive) → default GL debit account
- `keyword_mappings` table: keyword in `vendor + description` text → GL account, ordered by priority
  - e.g. "electricity", "power bill" → Utilities Expense
  - e.g. "office supplies", "stationery" → Office Expense
  - e.g. "consulting", "professional fee" → Professional Services Expense
- Credit account defaults to the first active Accounts Payable account
- When user confirms with "save mapping" checked, `gl_suggester.save_vendor_mapping()` upserts the vendor → debit account mapping

**Tier 2 — Unrecognised vendors/descriptions**
- If no vendor or keyword match found, fields are left blank and a warning banner is shown
- User selects accounts manually; mapping saved on confirm if checkbox is ticked

### New DB Tables for OCR

#### `vendor_mappings`
| Column | Type | Notes |
|---|---|---|
| id | UUID | |
| vendor_name | VARCHAR | Normalised vendor name |
| default_account_id | UUID | FK → accounts |
| created_at | TIMESTAMP | |

#### `keyword_mappings`
| Column | Type | Notes |
|---|---|---|
| id | UUID | |
| keyword | VARCHAR | e.g. "electricity", "rent" |
| account_id | UUID | FK → accounts |
| priority | INTEGER | Higher = checked first |

#### `ocr_results`
| Column | Type | Notes |
|---|---|---|
| id | UUID | |
| attachment_id | UUID | FK → attachments |
| raw_text | TEXT | Full OCR output |
| extracted_fields | JSONB | Structured fields (vendor, date, total, etc.) |
| confidence | FLOAT | OCR confidence score |
| processed_at | TIMESTAMP | |

---

## Hosting Setup (Hetzner VPS)

1. Provision Hetzner CX22 (~$5-6/month, 2 vCPU, 4GB RAM, 40GB SSD)
2. Ubuntu 24.04 LTS
3. Install: Python, PostgreSQL, Nginx, Certbot
4. Nginx as reverse proxy → Flask app (via Gunicorn)
5. Let's Encrypt SSL certificate
6. Daily PostgreSQL backups (`pg_dump` → stored locally + optionally offsite)

---

## Migration Path (VPS → Self-hosted, when ready)
1. `pg_dump` database on VPS → restore on local machine
2. Copy `/uploads` file directory to local machine
3. Update domain DNS A record to your static IP
4. Replicate Nginx + Gunicorn setup on local machine
5. Cancel VPS

---

## Dependencies & Software

### System Requirements (local dev machine)
| Software | Version | Purpose |
|---|---|---|
| Python | 3.13.12 (installed) | Runtime |
| PostgreSQL | 18 (installed) | Database |
| Git | Latest | Version control |
| pip + venv | Bundled with Python | Package & env management |

> **Windows notes:** Use Command Prompt (not PowerShell) — activate venv with `venv\Scripts\activate.bat`. Use pgAdmin Query Tool to run raw SQL (e.g. `CREATE DATABASE accsoft_dev;`) — pgAdmin's GUI dialogs have bugs on PG18. OCR packages (`paddlepaddle`, `paddleocr`, `invoice2data`, `pdfplumber`) are in `requirements-ocr.txt` — install separately in Session 5.
>
> **PostgreSQL PATH (Windows):** Add `C:\Program Files\PostgreSQL\18\bin` to System PATH via `Win+R → sysdm.cpl → Advanced → Environment Variables → System variables → Path`. Must open a new CMD/VS Code window after saving for the change to take effect. VS Code terminal inherits PATH at launch — restart VS Code to pick up changes.
>
> **pgAdmin notes:** "pgAdmin 4" and "pgAdmin 4 v6" are the same app. Two server registrations (PostgreSQL 14 and PostgreSQL 18) may appear — use PostgreSQL 18. These are pgAdmin bookmarks only, not separate installations. To reset the postgres password: connect to PostgreSQL 18 → Query Tool → `ALTER USER postgres WITH PASSWORD 'yourpassword';`
>
> **Two PostgreSQL versions installed:** PostgreSQL 14 runs on port **5432**, PostgreSQL 18 runs on port **5433**. Always use port 5433 in `DATABASE_URL`. The `accsoft_dev` database lives on PostgreSQL 18. When connecting via psql or pgAdmin, always target port 5433.
>
> **`flask db migrate` must be run before `flask db upgrade`** — if `migrations/versions/` is empty, `flask db upgrade` silently does nothing. Run `flask db migrate -m "message"` first to generate the migration file, then `flask db upgrade` to apply it.

### Python Packages (`requirements.txt`)
| Package | Purpose |
|---|---|
| Flask | Web framework |
| Flask-Login | Session-based authentication |
| Flask-SQLAlchemy | ORM (Python ↔ PostgreSQL) |
| Flask-Migrate | Database migrations (via Alembic) |
| psycopg2-binary | PostgreSQL driver |
| python-dotenv | Load `.env` config variables |
| Werkzeug | Password hashing (bundled with Flask) |
| gunicorn | WSGI server (used in production/VPS) |
| pdfplumber | Extract text from digital PDFs (installed Session 5) |
| invoice2data | Invoice field extraction — installed, available for YAML templates |
| Pillow | Image processing (installed Session 5) |
| paddlepaddle | Core engine for PaddleOCR — **not yet installed** (deferred) |
| paddleocr | OCR for scanned PDFs and image receipts — **not yet installed** (deferred) |

### Frontend
| Tool | How | Purpose |
|---|---|---|
| Tailwind CSS | CDN (dev) → standalone CLI (prod) | Styling |

> Tailwind via CDN requires no Node.js install. Switch to the standalone Tailwind CLI binary before VPS deployment for optimised CSS.

### Optional Dev Tools
| Tool | Purpose |
|---|---|
| pgAdmin or DBeaver | GUI to inspect PostgreSQL database |
| Postman | Test Flask API routes manually |

---

## Project Structure

### Tree (current — as of Session 6)
```
accsoft/
├── app/
│   ├── __init__.py           # App factory — registers all 9 blueprints
│   ├── extensions.py         # db, migrate, login_manager instances
│   ├── models/
│   │   ├── user.py
│   │   ├── account.py                # 3-level hierarchy (hierarchy / allows_posting / level_0/1 FKs)
│   │   ├── transaction.py            # Transaction (with kind enum + related_transaction_id) + TransactionLine
│   │   ├── attachment.py
│   │   ├── customer.py
│   │   ├── supplier.py
│   │   ├── vendor_mapping.py         # Vendor name → default GL debit account
│   │   ├── keyword_mapping.py        # Keyword → GL account (priority-ordered)
│   │   ├── ocr_result.py             # Raw text + extracted fields per attachment
│   │   ├── bulk_upload.py            # BulkUploadJob + BulkUploadItem
│   │   └── reconciliation.py         # BankStatement, BankStatementLine, ReconciliationSession, ReconciliationMatch
│   ├── blueprints/
│   │   ├── auth/                     # routes.py, forms.py
│   │   ├── dashboard/                # routes.py
│   │   ├── accounts/                 # routes.py + service.py — CoA CRUD, tree build, parent resolution
│   │   ├── transactions/             # routes.py + service.py — entry, list, ledger, CSV export, credit-note flows
│   │   ├── attachments/              # routes.py — upload/view/delete
│   │   ├── customers/                # routes.py
│   │   ├── suppliers/                # routes.py
│   │   ├── ocr/                      # routes.py + pipeline.py + extractor.py + gl_suggester.py
│   │   ├── reconciliation/           # routes.py + service.py — session/CSV import/match/complete
│   │   └── reports/                  # __init__.py only — Session 7 will fill
│   ├── templates/                    # See "Template map" below
│   ├── static/uploads/               # Attached invoices/receipts/photos (UUID filenames)
│   └── utils/                        # (empty — reserved)
├── migrations/                       # Flask-Migrate auto-generated
├── tests/
├── config.py                         # Dev/prod config
├── requirements.txt                  # Core deps
├── requirements-ocr.txt              # OCR deps (paddlepaddle/paddleocr deferred)
├── seed.py                           # Starter CoA + admin user
└── run.py                            # Entry point (exposes `app` for flask CLI)
```

### Codebase reference — where to look first

| Area | Routes | Service / helpers | Templates | Key models |
|---|---|---|---|---|
| Auth | `auth/routes.py` | `auth/forms.py` | `templates/auth/` | `User` |
| Dashboard | `dashboard/routes.py` | — | `templates/dashboard/index.html` | — |
| Chart of Accounts | `accounts/routes.py` | `accounts/service.py` (tree build, code suggestion) | `templates/accounts/list.html` (tree + slide-in sidebar form) | `Account` (3-level, `hierarchy`, `allows_posting`, `level_0_account_id`, `level_1_account_id`) |
| Transactions | `transactions/routes.py` | `transactions/service.py` (query, balance) | `transactions/form.html` (journal editor + auto-balance JS), `transactions/list.html` (filter sidebar + kind badges), `transactions/ledger.html`, `transactions/credit_note_picker.html` | `Transaction`, `TransactionLine`, `TRANSACTION_KINDS` |
| Attachments | `attachments/routes.py` | — | (embedded in `transactions/form.html`) | `Attachment` |
| Customers / Suppliers | `customers/routes.py`, `suppliers/routes.py` | — | `templates/customers/*.html`, `templates/suppliers/*.html` | `Customer`, `Supplier` |
| OCR — single/bulk | `ocr/routes.py` (`/ocr/upload` redirects to bulk) | `ocr/pipeline.py` (pdfplumber; image → empty), `ocr/extractor.py` (regex parser), `ocr/gl_suggester.py` | `ocr/bulk_upload.html`, `ocr/bulk_queue.html`, `ocr/bulk_review.html`, `ocr/bulk_summary.html`, `ocr/review.html`, `ocr/upload.html` | `OcrResult`, `BulkUploadJob`, `BulkUploadItem`, `VendorMapping`, `KeywordMapping` |
| Reconciliation | `reconciliation/routes.py` | `reconciliation/service.py` (CSV import, unmatched queries, matching, complete/reopen) | `reconciliation/list.html`, `reconciliation/new.html`, `reconciliation/detail.html` (two-column match UI), `reconciliation/history.html` | `BankStatement`, `BankStatementLine`, `ReconciliationSession`, `ReconciliationMatch` |
| Reports | (empty, Session 7) | — | — | — |

### Conventions to know before editing
- **Blueprint pattern**: every blueprint exports `<name>_bp`; `app/__init__.py` imports and registers all of them. Add new ones there.
- **URL prefixes** are set on the Blueprint, not per-route (see `url_prefix="/transactions"` etc.).
- **Service layer** (`accounts/service.py`, `transactions/service.py`, `reconciliation/service.py`): all DB queries live here; routes only orchestrate. Follow this split when adding features.
- **Template inheritance**: everything extends `templates/base.html`. Flash messages, nav, and Tailwind CDN are defined there — don't duplicate them. Nav link injection belongs in `base.html`.
- **Styling**: Tailwind via CDN (no Node). `font-mono` is overridden to Open Sans (see `base.html`) — use it on all amounts.
- **Transaction `kind`**: one of `manual_journal`, `customer_invoice`, `supplier_bill`, `customer_credit_note`, `supplier_credit_note`. Form templates branch on this.
- **Account posting guard**: transaction dropdowns must only show accounts where `allows_posting=True` (currently Level-0 leaves).
- **File uploads**: go to `app/static/uploads/` with UUID filenames; original name kept in `Attachment.filename`.
- **Scroll preservation**: the accounts list hides the page pre-paint and restores `sessionStorage['accountsScroll']` on `DOMContentLoaded` — replicate this pattern for any page with POST-then-redirect flows.
- **JS**: all inline in Jinja templates. No build step, no SPA framework.
- **Migrations**: run `flask db migrate -m "message"` before `flask db upgrade`. Both must complete or the schema silently diverges.

---

## Build Order
1. Project structure + virtual environment + dependencies
2. PostgreSQL local DB + Flask app factory + config
3. Database models + Flask-Migrate
4. Auth (login/logout)
5. Base HTML layout (Tailwind)
6. Chart of Accounts CRUD + seed starter accounts
7. Transaction entry + general ledger view
8. File attachment upload/view
9. Dashboard (balances + recent transactions)
10. OCR pipeline (pdfplumber + PaddleOCR + invoice2data)
11. GL suggestion engine (keyword/vendor rules)
12. Bank reconciliation
13. Reports + CSV export
14. VPS deployment (Hetzner + Nginx + Gunicorn + SSL)
