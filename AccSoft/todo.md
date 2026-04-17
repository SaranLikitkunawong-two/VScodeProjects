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

## Session 5.5 — Bulk Invoice Upload *(future)*
**Goal:** Upload multiple invoices at once → system processes each → user reviews and approves one by one.

### Steps
- [ ] Bulk upload form — multi-file input, accepts PDF/JPG/PNG
- [ ] `BulkUploadJob` model — tracks a batch: id, status (pending/processing/done), created_at
- [ ] `BulkUploadItem` model — one row per file: job_id, attachment_id, ocr_result_id, status (pending/approved/skipped), transaction_id (null until approved)
- [ ] On submit: save all files, create `OcrResult` per file (run pipeline immediately — files are small so sync is fine for now)
- [ ] Batch queue page — list all items in the job with status badges (extracted / needs review / approved / skipped)
- [ ] Per-item review — same review form as Session 5 single upload, but with prev/next navigation between items in the batch
- [ ] Approve posts the transaction and marks item approved; Skip marks it skipped (file still saved, no transaction)
- [ ] Batch summary page — shown when all items are approved or skipped: count posted, count skipped, link to each transaction

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
- [ ] Clone repo to VPS, set up production `.env`
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
| 3 | Transaction entry + ledger | **Complete** |
| 4 | Attachments + dashboard | **Complete** |
| 4.5 | Customers & Suppliers | **Complete** |
| 5 | OCR pipeline | **Complete** |
| 5.5 | Bulk invoice upload | Not started |
| 6 | Bank reconciliation | Not started |
| 7 | Reports + CSV | Not started |
| 8 | VPS deployment | Not started |
