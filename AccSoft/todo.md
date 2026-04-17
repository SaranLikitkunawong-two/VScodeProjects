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
- [ ] Add/Edit account should open as a modal overlay on the accounts list page — user should see existing accounts while filling in the form
- [ ] Actions (deactivate/reactivate, delete, edit) should preserve page scroll position
- [ ] Implement 3-level hierarchy: Level 1 = type, Level 2 = parent account, Level 3 = subaccount. Only Level 3 allows transaction posting. Render as indented tree; Levels 1–2 show aggregated balances from descendants only.

---

## Session 3 — Transaction Entry & General Ledger
**Goal:** Enter double-entry transactions and view the general ledger.  
**Status:** Code complete — awaiting browser verification.

### Verify
**Setup:** Open CMD → activate venv → `set FLASK_APP=run.py` → `flask run`

**Transaction list**
- [ ] Navigate to `http://127.0.0.1:5000/transactions/` — page loads with empty state and "+ New Transaction" button
- [ ] "Transactions" and "Ledger" links appear in the nav bar

**Add transaction — happy path**
- [ ] Click "+ New Transaction" → form loads with 2 pre-filled lines (one debit, one credit)
- [ ] Enter: Date = today, Description = "Office supplies", Reference = "INV-001"
- [ ] Line 1: account = any Expense account, type = Debit, amount = 50.00
- [ ] Line 2: account = any Asset/Bank account, type = Credit, amount = 50.00
- [ ] Running totals show Debits $50.00 / Credits $50.00 with no warning
- [ ] Click Save → redirects to transaction list with success flash message
- [ ] Transaction appears in the list with correct date, description, amount $50.00

**Validation — debits ≠ credits**
- [ ] Enter Line 1 Debit $100.00 / Line 2 Credit $90.00 → "Debits must equal credits" warning appears in real time
- [ ] Submit anyway → server rejects it and shows error flash (does not save)

**Validation — missing fields**
- [ ] Submit with no date → error: "Date is required."
- [ ] Submit with no description → error: "Description is required."
- [ ] Submit with amount = 0 → error: "amount must be greater than zero."

**Dynamic line rows**
- [ ] Click "+ Add line" → third row appears; totals update
- [ ] Click × on a row → row removed; totals update
- [ ] Try to remove a row when only 2 remain → alert shown, row not removed

**Edit transaction**
- [ ] Click Edit → form loads with correct date, description, and lines pre-filled
- [ ] Change description and save → list shows updated description

**Delete transaction**
- [ ] Click Delete → confirm dialog; confirm → transaction removed, success flash shown
- [ ] Re-add a transaction for ledger tests below

**General ledger**
- [ ] Navigate to `http://127.0.0.1:5000/transactions/ledger` — filter bar shown, no table yet
- [ ] Select the Bank/Asset account → ledger table appears with correct date, description, debit/credit, running balance
- [ ] Filter by date range that excludes the transaction → "No entries" message
- [ ] Filter by date range that includes it → row reappears
- [ ] Description is a link → clicking opens the edit form for that transaction

**Re-test Session 2 — delete restriction**
- [ ] Go to Accounts → try to delete the account used in the transaction above
- [ ] Error shown: "Cannot delete — it has linked transactions. Deactivate it instead."

---

## Session 4 — File Attachments & Dashboard
**Goal:** Attach invoices/receipts to transactions; working dashboard.

### Steps
- [ ] File upload on transaction form (JPG, PNG, PDF accepted)
- [ ] Store file in `app/static/uploads/` with UUID filename
- [ ] View attachment inline (images) or download link (PDFs)
- [ ] Multiple attachments per transaction
- [ ] Dashboard page:
  - Account balances summary (grouped by type)
  - Recent 10 transactions
  - Quick-add transaction button

### Verify
- Upload a JPG receipt to a transaction → visible on transaction detail page
- Upload a PDF invoice → download link works
- Dashboard shows correct balances after transactions entered in Session 3

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
| 4 | Attachments + dashboard | Not started |
| 5 | OCR pipeline | Not started |
| 6 | Bank reconciliation | Not started |
| 7 | Reports + CSV | Not started |
| 8 | VPS deployment | Not started |
