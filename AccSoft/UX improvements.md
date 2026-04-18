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
- **Transaction form**: "Auto balance" button next to "+ Add line" — appears when exactly one line is empty and debits ≠ credits; fills the empty line's debit or credit with the diff
- **Transaction list**: Kind badge column (compact, colour-coded — Journal/Invoice/Bill/Credit Note)
- **Transaction list**: Kind filter in sidebar (multi-select with All/None, auto-submit, respected by CSV export)

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
| 2026-04-18 | Transaction form: Auto-balance button (fills sole empty line with diff) | ✓ Done |
| 2026-04-18 | Transactions list: Kind badge column + kind filter in sidebar | ✓ Done |

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

### Data integrity
- **DB check constraints**: a `customer_invoice`/`customer_credit_note` must have `customer_id` set; `supplier_bill`/`supplier_credit_note` must have `supplier_id` set (currently enforced at form layer only)
- **Audit trail**: `updated_at` / `updated_by` on Transaction so edits to posted transactions are traceable
- **Prevent editing kind** after creation (currently relies on UI not exposing a widget)

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
