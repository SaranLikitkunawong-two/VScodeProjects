# AccSoft — Session Build Plan

> Each session is a self-contained context window. Start a new session by telling Claude:
> "I am building AccSoft, a personal accounting web app. Read planning.md and todo.md in VScode/accsoft/ then continue with Session X."

---

## Session 1 — Complete ✓
Project structure, venv, all DB models, Flask-Migrate, auth (login/logout), base HTML layout, seed script.  
Key facts: `DATABASE_URL=postgresql://postgres:WatermarkD21@127.0.0.1:5433/accsoft_dev` · seed creates 1 user + 11 default accounts · login: `admin@example.com` / `changeme123`

---

## Session 2 — Complete ✓ (UX improvements pending)
Chart of Accounts CRUD: grouped list by type, add/edit/deactivate/hard-delete, flash messages. All routes verified working in browser.

### Pending UX improvements (pick up when revisiting accounts)
- [x] Add/Edit account should open as a modal overlay on the accounts list page — user should see existing accounts while filling in the form
- [x] Actions (deactivate/reactivate, delete, edit) should preserve page scroll position
- [ ] Implement 3-level hierarchy: Level 1 = type, Level 2 = parent account, Level 3 = subaccount. Only Level 3 allows transaction posting. Render as indented tree; Levels 1–2 show aggregated balances from descendants only.

### User review required
- [ ] Verify modal opens correctly for Add and Edit — confirm accounts list is visible behind modal
- [ ] Verify scroll position is restored after Deactivate/Activate, Delete, and Save actions
- [ ] Verify Edit modal shows type as locked (disabled) for accounts that have transactions
- [ ] Verify type dropdown auto-suggests account code in Add mode

---

## Session 3 — Transaction Entry & General Ledger
**Goal:** Enter double-entry transactions and view the general ledger.  
**Status:** Code complete — awaiting browser verification.

### Pending UX improvements
- [ ] Add CSV export button to the transactions list page
- [ ] Transactions page: add a left-hand filter panel with:
  - Date range slicer (from / to date pickers)
  - Account slicer — search input with filtered dropdown, supports multi-select
  - Panel filters the transaction list in real time (or on apply)
- [ ] Replace account dropdown on transaction line rows with a search input that shows autocomplete suggestions (behaves like a dropdown on click, but also filters by typing)
- [ ] Date field on new transaction form: clicking anywhere on the input should open the calendar picker (not just the calendar icon)
- [ ] Transaction entry: support selecting multiple GL account lines at once via checkboxes
- [ ] Transaction entry: split amount column into separate Debit and Credit columns
- [ ] Add a balance effect column (+/−) calculated from account type and entry side:
  - Asset, Expense, Equity: Debit → +, Credit → −
  - Liability, Revenue: Debit → −, Credit → +
- [ ] Ledger page: apply the same separate Debit/Credit columns and balance effect column (+/−) as above
- [ ] Ledger date filter: add preset range buttons — Today, Yesterday, Last 7 Days, This Month, Last Month — that populate the from/to date fields when clicked

### Verify
**Setup:** Open CMD → activate venv → `set FLASK_APP=run.py` → `flask run`

**Transaction list**
- [x] Navigate to `http://127.0.0.1:5000/transactions/` — page loads with empty state and "+ New Transaction" button
- [x] "Transactions" and "Ledger" links appear in the nav bar

**Add transaction — happy path**
- [x] Click "+ New Transaction" → form loads with 2 pre-filled lines (one debit, one credit)
- [x] Enter: Date = today, Description = "Office supplies", Reference = "INV-001"
- [x] Line 1: account = any Expense account, type = Debit, amount = 50.00
- [x] Line 2: account = any Asset/Bank account, type = Credit, amount = 50.00
- [x] Running totals show Debits $50.00 / Credits $50.00 with no warning
- [x] Click Save → redirects to transaction list with success flash message
- [x] Transaction appears in the list with correct date, description, amount $50.00

**Add Transaction testing**
Validation works - does not submit if debit and credits doesn't balance, or if fields are missing. 


---

## Session 4 — File Attachments & Dashboard
**Goal:** Attach invoices/receipts to transactions; working dashboard.  
**Status:** Code complete — awaiting browser verification.

### Steps
- [x] File upload on transaction form (JPG, PNG, PDF accepted)
- [x] Store file in `app/static/uploads/` with UUID filename
- [x] View attachment inline (images) or download link (PDFs)
- [x] Multiple attachments per transaction
- [x] Dashboard page:
  - Account balances summary (grouped by type)
  - Recent 10 transactions
  - Quick-add transaction button

### Verify
- Upload a JPG receipt to a transaction → visible on transaction detail page
- Upload a PDF invoice → download link works
- Dashboard shows correct balances after transactions entered in Session 3

---

## Session 4.5 — Customers & Suppliers
**Goal:** Customer and supplier profiles to support invoicing and payment tracking.
**Status:** Code complete — awaiting browser verification.

### Steps
- [x] `customers` table: name, contact person, email, phone, address, ABN, notes, is_active
- [x] `suppliers` table: same fields as customers
- [x] Customer CRUD UI — list, add, edit, deactivate
- [x] Supplier CRUD UI — list, add, edit, deactivate
- [x] Link customers to AR transactions (Accounts Receivable)
- [x] Link suppliers to AP transactions (Accounts Payable)
- [x] Customer/supplier selector on transaction form (search with autocomplete)
- [x] Customer detail page — shows all linked transactions and outstanding balance
- [x] Supplier detail page — shows all linked transactions and outstanding balance

### Verify
- [ ] Add a customer → appears in customer list
- [ ] Add a supplier → appears in supplier list
- [ ] Create a transaction linked to a customer → appears on customer detail page
- [ ] Outstanding balance calculates correctly from linked AR transactions
- [ ] Deactivating a customer hides them from the transaction selector but preserves history

---

## Session 5 — OCR Pipeline
**Goal:** Upload an invoice → auto-extract fields → review → post to ledger.

### Steps
- [ ] Install and test pdfplumber (digital PDF text extraction)
- [ ] Install and test PaddleOCR (scanned PDF / image OCR)
- [ ] `ocr/pipeline.py` — detect input type, route to correct extractor
- [ ] `ocr/extractor.py` — invoice2data integration, YAML templates for common invoice formats
- [ ] `ocr/gl_suggester.py` — keyword + vendor lookup → suggested GL accounts
- [ ] OCR upload page — upload invoice → show extracted fields for review
- [ ] Review & confirm form — user edits extracted fields, selects/confirms GL accounts, posts transaction
- [ ] Save vendor mapping on confirm (so next invoice from same vendor auto-suggests)
- [ ] Flag unrecognised vendors for manual GL selection

### Verify
- Upload a digital PDF invoice → vendor, date, total extracted correctly
- Upload a photo of a receipt → OCR extracts key fields
- Known vendor → GL accounts pre-filled
- Unknown vendor → flagged, user picks manually, mapping saved for next time

---

## Session 6 — Bank Reconciliation
**Goal:** Match posted transactions against a bank statement.

### Steps
- [ ] Import bank statement (CSV upload — date, description, amount)
- [ ] Reconciliation view — two columns: bank transactions vs ledger transactions
- [ ] Match/unmatch transactions manually
- [ ] Flag unmatched items on both sides
- [ ] Mark reconciliation period as complete
- [ ] Reconciliation history

### Verify
- Import a sample bank statement CSV
- Match a ledger transaction to a bank line
- Unmatched items clearly flagged

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

## Session 8 — VPS Deployment (Hetzner)
**Goal:** App live on Hetzner VPS with HTTPS.

### Steps
- [ ] Provision Hetzner CX22 (Ubuntu 24.04)
- [ ] Install: Python, PostgreSQL, Nginx, Certbot, Git
- [ ] Clone repo to VPS
- [ ] Set up production `.env`
- [ ] Set up PostgreSQL on VPS, run migrations, seed accounts
- [ ] Configure Gunicorn as systemd service
- [ ] Configure Nginx as reverse proxy
- [ ] Issue Let's Encrypt SSL cert via Certbot
- [ ] Set up daily `pg_dump` backup (cron job)
- [ ] Test all features on live URL

### Verify
- Visit `https://yourdomain.com` → login page loads with valid SSL
- All Session 1–7 features work on production
- `pg_dump` backup runs and produces a valid file

---

## Status Tracker

| Session | Focus | Status |
|---|---|---|
| 1 | Project setup, models, auth | **Complete** |
| 2 | Chart of Accounts | **Complete** |
| 3 | Transaction entry + ledger | **Code complete — awaiting browser verify** |
| 4 | Attachments + dashboard | **Code complete — awaiting browser verify** |
| 4.5 | Customers & Suppliers | **Code complete — awaiting browser verify** |
| 5 | OCR pipeline | Not started |
| 6 | Bank reconciliation | Not started |
| 7 | Reports + CSV | Not started |
| 8 | VPS deployment | Not started |

## UX Suggestions (user-provided)

When you list UX suggestions here in the chat, they will be added below as checklist todos. Template:
- [ ] Short description — added on YYYY-MM-DD by user

Instructions: Post your UX suggestion in a single line; it will be appended to this section and saved to todo.md.

- [ ] Show balancing hint under transaction totals: when debits ≠ credits, display the amount needed to balance (e.g., Debits 100 / Credits 90 → show "+10" in smaller text beneath the lesser side) — added on 2026-04-17 by user
- [x] Dashboard balance display: fix "deficit" label and red DR/CR indicators to respect normal balance sides. Debit-normal accounts (asset, expense) carry a natural debit balance — a positive computed balance is normal and should never show "deficit" or red. Only flag unusual balances (e.g. an asset with a credit balance, or equity with a debit balance). Also fix the individual account suffix: the "DR" label currently appears when `balance < 0` on a debit-normal account, but that computed negative means a credit balance — the suffix should say "CR", not "DR". — added on 2026-04-17 by user

