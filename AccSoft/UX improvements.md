# AccSoft — UX Improvements

> UX items, polish tasks, and user-facing verifications that are not part of core feature delivery.
> Pick these up after a session's core functionality is verified.

---

## Accounts (Session 2)

### Done ✓
- Modal overlay for Add/Edit account — accounts list visible behind form
- Scroll position preserved after all actions (deactivate/reactivate, delete, edit/save)
- Scroll flicker fixed — document hidden before paint, restored at correct position via DOMContentLoaded
- Edit modal locks Type field (disabled) for accounts that have transactions — verified
- Type dropdown auto-suggests account code in Add mode — verified

### Done ✓
- [x] 3-level account hierarchy (0 = posting leaf, 1 = group, 2 = category). DB columns: hierarchy, allows_posting, level_0_account_id (FK→level-1 parent), level_1_account_id (FK→level-2 grandparent), gl_description. Tree rendered with indentation in accounts list. Sidebar has level selector + dynamic parent dropdowns. Transaction forms restricted to allows_posting=True accounts.
- [x] Change from modal to a sidebar so that the accounts list and the new account sidebar are both visible and scrollable at the same time. The sidebar comes out from the right side. ✓ Verified

---

## Transactions & Ledger (Session 3)

### Done ✓ (Session 3)
- CSV export button on transaction list (respects search filter)
- Account autocomplete on journal line rows (type-to-filter, click to select)
- Date field opens calendar picker on click anywhere in the input
- Journal lines split into separate Debit and Credit columns (replaces Type + Amount)
- Balance effect column (+/−) on each journal line, calculated from account normal balance side
- Balancing hint shows "$X.XX more needed on debits/credits" when unbalanced
- Ledger preset date range buttons: Today, Yesterday, Last 7 Days, This Month, Last Month

### Done ✓ (Session 5 — 2026-04-18)
- Left-hand filter sidebar on transaction list: date range (from/to) + account multi-select with live search
- Filters auto-apply on change (date picker or checkbox click) — no Apply button required
- Account filter has All / None shortcuts to select or clear all accounts at once
- Account filter and date range are respected by CSV export
- Multi-select GL lines on transaction entry form: checkbox column on each journal line, select-all header checkbox, "Delete selected" button (enforces 2-line minimum)

### Done ✓ (Session 7 polish — 2026-04-18)
- **Transaction form**: Auto-balance toggle (default on, persisted in localStorage) — prefilling one side auto-fills the opposite side of a single empty line with the diff; re-fires on subsequent edits. Manual "Auto balance" button still appears when the toggle is off
- **Transaction list**: Transaction type badge column (compact, colour-coded — Journal/Invoice/Bill/Credit Note)
- **Transaction list**: Transaction type filter in sidebar (multi-select with All/None, auto-submit, respected by CSV export)
- **OCR**: "Scan Invoice" and "Bulk Upload" merged into a single **Scan Invoice** entry point (bulk flow retained, accepts one or many files). Legacy `/ocr/upload` redirects to the unified page

### Done ✓ (Session 6 — 2026-04-18)
- **Ledger**: account filter moved to left sidebar (mirroring transactions list) — type-to-search, multi-select checkboxes, All/None shortcuts, date range + presets, auto-submit
- **Ledger**: combined table across all selected accounts — columns Date | Account (code+name) | Description | Reference | Debit | Credit, with total debit/credit footer
- **DB**: `transactions.kind` enum added (`manual_journal`, `customer_invoice`, `supplier_bill`, `customer_credit_note`, `supplier_credit_note`). Existing rows backfilled to `manual_journal`. Migration `163c28d490f0`
- **DB**: `transactions.related_transaction_id` nullable self-FK — links credit notes back to the originating invoice/bill
- **Transaction form**: kind-aware — shows kind badge in header, conditionally renders customer/supplier fields (hides the irrelevant side), enforces required party based on kind
- **Transaction form**: "Create Credit Note" button on invoice/bill edit pages; link back to original shown on credit-note edit pages
- **OCR pipeline**: posted transactions now tagged `kind=supplier_bill`
- **New routes**: `/transactions/invoices/new`, `/transactions/bills/new`, `/transactions/credit-notes/new` (with `?type=customer|supplier`), `/transactions/<id>/credit-note`

---

## Dashboard (Session 4)

### Done ✓
- Dashboard balance display: DR/CR suffix and "deficit" indicator now respect normal balance sides (debit-normal accounts are never flagged as deficit when balance is positive)

### Done ✓ (Session 6 — 2026-04-18)
- `+ New Transaction` button replaced with 3-option dropdown: Customer Invoice, Supplier Bill, Manual Journal (each with a short sub-label describing when to use it)
- Dropdown closes on outside click

---

## Global

### Done ✓
- Open Sans font for all numbers/amounts (font-mono elements app-wide) — via Tailwind config override
- Dashboard recent transactions: SVG paperclip icon for entries with attachments

---

## UX Suggestions Log

| Date | Item | Status |
|---|---|---|
| 2026-04-17 | Balancing hint under transaction totals | ✓ Done |
| 2026-04-17 | Dashboard DR/CR deficit indicator fix | ✓ Done |
| 2026-04-18 | Transaction filter panel (date range + account multi-select, auto-submit, All/None) | ✓ Done |
| 2026-04-18 | Multi-select GL lines with select-all and Delete selected | ✓ Done |
| 2026-04-18 | Scroll flicker fix on accounts list | ✓ Done |
| 2026-04-18 | Type field lock verified (accounts with transactions) | ✓ Done |
| 2026-04-18 | Open Sans for all numbers (font-mono app-wide) | ✓ Done |
| 2026-04-18 | Dashboard attachment indicator — SVG paperclip | ✓ Done |
| 2026-04-18 | Accounts modal → right-hand sticky sidebar (slide-in, both panels scrollable) | ✓ Done |
| 2026-04-18 | 3-level account hierarchy — DB schema + tree list + sidebar dropdowns + posting guard | ✓ Done |
| 2026-04-18 | Ledger: account filter → sidebar with multi-select + combined table | ✓ Done |
| 2026-04-18 | DB: `transactions.kind` enum + `related_transaction_id` self-FK | ✓ Done |
| 2026-04-18 | Dashboard: `+ New Transaction` split into 3-option dropdown | ✓ Done |
| 2026-04-18 | Lean customer-invoice / supplier-bill / credit-note flows (kind-aware form) | ✓ Done |
| 2026-04-18 | Credit note creation from invoice/bill (auto line reversal + related_transaction_id) | ✓ Done |
| 2026-04-18 | Transaction form: Auto-balance (automatic on edit, with off toggle) | ✓ Done |
| 2026-04-18 | Transactions list: Transaction-type badge column + type filter in sidebar | ✓ Done |
| 2026-04-18 | OCR: unified Scan Invoice + Bulk Upload into one page | ✓ Done |

---

## Suggested Future Improvements

### Invoices & Bills (follow-on to Lean)
- **Due dates** on customer invoices and supplier bills + "Overdue" badge on the list
- **Status** field: `draft / open / paid / void` (open = posted but unpaid; paid = settled via payment transaction)
- **Invoice numbering**: auto-increment sequence per kind (`INV-0001`, `BILL-0001`, `CN-0001`), configurable prefix
- **PDF generation** for customer invoices (print/email friendly, with business letterhead)
- **Line items UX** (the "Full" path): description/qty/unit price/GST line items above the journal view; system auto-generates Dr AR / Cr Income / Cr GST Collected
- **Payment application**: mark an invoice as paid by linking a bank-side transaction (ties into reconciliation)

### Credit notes
- **Credit note application**: link a credit note to a specific invoice/bill it's settling, then display "applied" vs "open" status
- **Validation**: warn (don't block) if credit note total exceeds the related invoice total
- **Show credit notes on the related invoice** — list them at the bottom with net outstanding amount
- **Prevent editing a credit note's `related_transaction_id` after posting** (currently not editable, but also not guarded if someone manipulates form)

### Ledger
- **Per-account running balance** column when only one account is selected (meaningful then; suppressed when multiple — current behaviour)
- **Filter by transaction kind** in the ledger sidebar (e.g. "show only invoices")
- **CSV export** from the ledger (list page has it — ledger doesn't yet)
- **Pagination** for ledgers with many entries (currently renders everything)

### Dashboard / lists
- **"Outstanding AR" / "Outstanding AP" cards** on the dashboard (now trivial because `kind` is queryable)
- **Customer/Supplier detail pages**: split into "Invoices", "Bills", "Credit Notes" tabs instead of one unified list

### Transactions
- **Import transactions from CSV** — "Import CSV" button on the transactions list. Clicking opens a dialog with two options:
  - **Download template** — downloads a blank CSV with the standardised header row
  - **Upload CSV** — user picks a file and submits
  Standard header row: `date, Account Code, Description, Debit Amount, Credit Amount`.
  One CSV row = one journal line. Rows sharing the same `date + Description` group into a single transaction. After parse, the file is validated using the existing manual-journal rules (2+ lines per txn, accounts exist + `allows_posting`, debits == credits per txn, amounts > 0). The user lands on a preview/confirm page showing each parsed transaction with its lines and any validation errors per-row; they click **Confirm Import** to post all valid transactions atomically, or fix the CSV and retry.

### Data integrity
- **DB check constraints**: a `customer_invoice`/`customer_credit_note` must have `customer_id` set; `supplier_bill`/`supplier_credit_note` must have `supplier_id` set (currently enforced at form layer only)
- **Audit trail**: `updated_at` / `updated_by` on Transaction so edits to posted transactions are traceable
- **Prevent editing kind** after creation (currently relies on UI not exposing a widget)

---

## Research-backed suggestions — 2026-04-18

> Observed from a read-through of `base.html`, dashboard, transactions list/form, ledger, OCR templates (`bulk_upload.html`, `bulk_queue.html`, `bulk_review.html`), reconciliation (`list.html`, `new.html`, `detail.html`), customers list/detail, and accounts list. Items already in the "Suggested Future Improvements" section above are not repeated here.

### Navigation (base.html)
- **Active-page indicator in top nav** — currently every link is plain hover-blue; users can't tell where they are. Add an underline / bold / colour shift when the route matches.
- **Mobile / narrow-window menu** — the horizontal nav overflows below ~900px (9 links + logo + logout). Collapse into a hamburger under a breakpoint.
- **Auto-dismissing flash messages** — they currently persist until the next navigation. Add a fade-out after ~5s (or a close-button) so success toasts don't pile up.
- **Global quick-jump search (Ctrl+K / `/`)** — a command-palette style overlay that matches transactions (description/reference), customers, suppliers, and accounts. Cheap to build and eliminates a lot of clicking as the dataset grows.

### Dashboard
- **Cash-on-hand card pinned at top** — sum of active Asset ▸ Bank & Cash subaccount balances. The current Account-Balances list buries this.
- **Unreconciled indicator per bank account** — e.g. "ANZ Cheque · 4 unreconciled lines →". Links straight into `/reconciliation/<id>`. Promotes the Reconciliation feature which is otherwise easy to forget.
- **Pending OCR-batch banner** — if `BulkUploadJob.status == 'processing'` exists, surface a "Resume batch review" banner at the top of the dashboard. Closing the tab currently leaves orphan items with no reminder.
- **Time-window toggle on Recent Transactions** — currently shows a fixed set; Month-to-date / Last 30d / Custom toggle makes it more useful.

### Transactions list
- **Live debounced search** — the input already triggers filter auto-submit for other fields, but text search still needs the Search button. Make it consistent (debounce 300ms on typing).
- **Sort by Amount / Type / Reference** — `sort` select only offers date asc/desc.
- **Bulk delete checkboxes on the list** — mirror the pattern already used inside the journal-line editor (select-all header, Delete selected).
- **"Duplicate" row action** — clone description/lines/kind with today's date, land on a new edit page. Big win for recurring manual journals and monthly bills.
- **Row-level "add attachment" quick-action** — drag-drop a file onto a row to attach, without opening the edit page.
- **Pagination** — acknowledged for the ledger in Suggested Future; the list will need it too once the table grows.

### Transaction form
- **"Save & New" button** — saves and returns to a blank form of the same `kind`, preserving customer/supplier if a "keep party" toggle is on. Essential for entering a run of bills in one sitting.
- **Drag-and-drop attachment zone** — currently file-picker only. A drop zone + paste-from-clipboard (image data) is cheap and matches how invoices arrive.
- **Ctrl+S to submit** — keyboard users (the primary user for this app) never need to hunt for the button.
- **Inline "Create new" in customer/supplier autocomplete** — when the typed string has zero matches, show a "+ Create '{query}'" row at the bottom of the dropdown that opens a quick-add modal and returns the new ID. Current flow forces the user out of the form.
- **Account dropdown shows up to 12 matches only (`routes.py` line ~375)** — make it virtual-scroll or paginated so power users can scroll the whole chart. 12 is fine when you know the name but breaks browsing.
- **Reference auto-suggest** — prefill `INV-####` / `BILL-####` / `CN-####` based on max existing reference for the kind (dovetails with the "Invoice numbering" item in the main list).

### Ledger
- **Consistency with Transactions list filters** — ledger has date presets but no kind filter; list has kind filter but no date presets. Both should expose both.
- **Group-by-transaction toggle** — one row per journal (collapsed) vs one row per line (current). Reduces noise when browsing a busy account.
- **Print-friendly view** — Session 7 touches print layouts for reports; the ledger benefits from the same treatment for auditor hand-off.
- **Remember last-used filter selections in `localStorage`** — re-opening the ledger should restore accounts/date range, not reset to empty.

### OCR / Scan Invoice
- **Drag-and-drop upload zone on `bulk_upload.html`** — currently a plain file-input.
- **Selected-file preview list before submit** — show names, sizes, and a remove-this-one (×) button per file. Right now you only get a count.
- **Progress indicator during extraction** — `/ocr/bulk` runs pdfplumber synchronously; on a batch of 10+ PDFs the user stares at a hung Upload button. Either show a spinner with per-file status, or move to polling + job-status endpoint.
- **Side-by-side invoice preview on `bulk_review.html`** — today the PDF opens in a modal. Splitting the page into preview-left / form-right removes a click per file and is the usual pattern for AP-automation tools.
- **Vendor field → Supplier record link** — currently free-text `fields.vendor`. Turn it into an autocomplete against `Supplier.name`; on approve, auto-populate `Transaction.supplier_id`. Avoids the AR/AP-profile data drifting from OCR-extracted vendor names.
- **"Approve all remaining" action on the queue when every pending item is a known vendor** — mirrors existing auto-approve path but user-initiated.
- **Remember "Save mapping" as default on** per-session — most users will always want to save.

### Bank Reconciliation
- **Auto-match suggestions** — exact-amount + same-day first, then ±3 days / exact-amount, surfaced as a "Suggested matches: N" banner with a one-click "Accept all suggested" button. Biggest productivity win in this feature.
- **Sortable / searchable columns in both unmatched tables** — dates, amount, description. Hard-coded order today.
- **Mark Complete guard** — currently just a confirm('Mark this reconciliation as complete?'). Warn explicitly if `totals.unmatched_count > 0` or if a closing-balance field (proposed below) differs from ledger.
- **Capture closing balance on Mark Complete** — prompt for the bank's end-of-period balance and record a diff vs the ledger. Makes the "complete" state meaningful rather than just a status flag.
- **CSV preview step after upload, before commit** — show parsed columns + first 10 rows + row count, let the user map columns if headers don't match. Reduces fear of feeding a wrongly-formatted CSV.
- **Description truncation** — `max-w-[140px]` hard-clips every bank line. Let the column flex; wrap on hover or show a full tooltip.

### Customers / Suppliers
- **Search + sort on the list page** — needed once the list grows past ~20 rows.
- **"New Invoice for this customer" / "New Bill for this supplier" CTA on detail page** — jumps to the kind-specific form with the party pre-filled.
- **Filter linked transactions by kind/date on the detail page** — the Suggested Future tabs item solves part of this; a simple filter bar is a smaller step.
- **AR/AP balance aging** — even a rough 0–30 / 31–60 / 60+ split on the customer/supplier detail card gives the number context.

### Chart of Accounts
- **Collapse/expand tree** — per-type and per Level-2 node. Currently the whole tree renders expanded; with 50+ leaves the page gets long.
- **Search/filter box** — same filter pattern already used in Transactions-list sidebar.
- **Balance column next to each posting account** — quick glance avoids bouncing to dashboard/ledger to check a number.

### Global polish
- **Loading states** — no spinner on any submit button. Adds feedback when OCR extraction or CSV import takes >1s.
- **Undo toast for destructive actions** — delete transaction / attachment / customer pops a 10s "Undone" window before committing. Current `confirm()` dialogs are easy to misclick.
- **Keyboard-shortcut help dialog** — `?` opens an overlay listing app-wide shortcuts. Pairs with the Ctrl+K palette and Save & New / Ctrl+S above.
- **Consistent date formatting** — lists use `dd MMM yyyy`, forms use ISO, flash messages are plain. Standardise on `dd MMM yyyy` for display, ISO only inside `<input type=date>`.

### Gaps / structural
- **Reports blueprint is empty** — `blueprints/reports/` contains only `__init__.py`; no routes or templates. Session 7 will fill this but worth noting.
- **No activity / audit log UI** — even before adding `updated_at`/`updated_by` to the model, a "Recent activity" feed on the dashboard (deletes, reconciliation completes, OCR approvals) is a confidence-builder for single-user accounting data.
- **No error page templates** — 404/500 fall back to Flask's default HTML. A branded error page with a link to dashboard is a small, cheap polish item.

---

## Verification Checklist — Session 6 changes

### Ledger sidebar
- [ ] Visit `/transactions/ledger` → empty state message shown (no accounts selected yet)
- [ ] Type in the sidebar search box → account list filters live
- [ ] Tick one account → page auto-submits, table shows that account's entries with Date | Account | Description | Reference | Debit | Credit columns
- [ ] Tick 3+ accounts → combined table ordered by date; account column clearly distinguishes rows
- [ ] "All" button → every account ticked; "None" → all cleared; both auto-submit
- [ ] Pick a date range preset (e.g. "This Mo") → form submits with the computed date range
- [ ] "Clear all" in header resets all filters
- [ ] Total debit / total credit footer matches the sum of the table columns

### Dashboard dropdown
- [ ] Click `+ New Transaction` → 3 options appear with sub-labels
- [ ] Click outside the menu → it closes
- [ ] Each option navigates to its respective form (URLs: `/transactions/invoices/new`, `/transactions/bills/new`, `/transactions/add`)

### Customer Invoice flow
- [ ] From dashboard dropdown → Customer Invoice → form shows **only** Customer field (Supplier hidden), Customer marked required with `*`
- [ ] Kind badge "Customer Invoice" visible in the page header
- [ ] Submit without selecting a customer → flash error "Customer is required."
- [ ] Submit with balanced Dr/Cr lines and a customer → success flash mentions "Customer Invoice", redirects to edit page
- [ ] On the edit page, Customer field shows selected customer, kind badge still visible, no Supplier field

### Supplier Bill flow
- [ ] Same as above but with Supplier required and Customer hidden; kind badge "Supplier Bill"

### Manual Journal
- [ ] From dropdown → Manual Journal → form shows **both** Customer and Supplier fields as optional (previous behaviour preserved)
- [ ] No kind badge shown (manual journal is the default "un-labeled" kind)

### Credit Note (standalone)
- [ ] Transactions list header shows `+ Credit Note` button → click → picker page with 2 cards (Customer / Supplier)
- [ ] Pick "Customer Credit Note" → form shows Customer field required, kind badge "Customer Credit Note"
- [ ] Pick "Supplier Credit Note" → form shows Supplier field required, kind badge "Supplier Credit Note"

### Credit Note (from invoice/bill)
- [ ] Open an existing Customer Invoice → "Create Credit Note" button visible (purple outline)
- [ ] Click it → new form pre-fills:
  - Date = today
  - Description = "Credit Note for {original description}"
  - Reference = "CN-{original ref}" if original had one
  - Customer = same customer as the invoice
  - Journal lines = **reversed** (debits swapped with credits, amounts preserved)
  - Hidden `related_transaction_id` points to the original
- [ ] Save → success, then open the saved credit note: header shows "↪ Related to Customer Invoice: {original description}" link back to the original
- [ ] Repeat for a Supplier Bill → credit note linked, Supplier pre-filled, lines reversed
- [ ] On a Manual Journal, no "Create Credit Note" button appears (correctly restricted)

### Regression checks
- [ ] Existing transactions (pre-migration) still open in the edit form — kind defaults to Manual Journal (no badge, both parties optional)
- [ ] OCR scan flow: upload an invoice, approve → resulting transaction has `kind = supplier_bill` (check via DB or by looking for the "Supplier Bill" badge on the edit page)
- [ ] CSV export from `/transactions/` still works
- [ ] Transaction list filter sidebar still filters correctly
