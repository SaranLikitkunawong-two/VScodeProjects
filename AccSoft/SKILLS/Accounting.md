# Accounting Guide for AccSoft (Australia)

## Purpose
This document sets out the accounting rules and principles AccSoft will follow so that the software behaves like a competent Australian small-business bookkeeper: reliable double-entry records, clean GST/BAS data, and reports that align with how Australian accountants and the ATO expect small business books to look.[file:1][web:65][web:71]

AccSoft is not a full tax engine and is not a substitute for professional advice. Where there is doubt, the user should confirm treatment with their accountant or the ATO.

## Core accounting model

### Double-entry fundamentals
AccSoft uses standard double-entry bookkeeping: every transaction affects at least two accounts, and total debits must always equal total credits. This preserves the accounting equation Assets = Liabilities + Equity at all times.[web:60][web:61][web:70]

Rules:
- Every saved transaction must have at least two lines.
- Sum of debit amounts must equal sum of credit amounts for each transaction.
- Asset and expense accounts normally carry **debit** balances and increase with debits, decrease with credits.[web:61][web:63]
- Liability, equity and income accounts normally carry **credit** balances and increase with credits, decrease with debits.[web:61][web:63][web:67]

### Account types and code ranges
AccSoft’s chart of accounts uses fixed code ranges so that reports and UI can reliably group accounts.[file:1]

- **1000–1999 Assets** – bank, accounts receivable, equipment, etc.[file:1]
- **2000–2999 Liabilities** – accounts payable, GST payable, credit cards, loans.[file:1][web:65]
- **3000–3999 Equity** – owner’s equity, retained earnings.[file:1]
- **4000–4999 Income** – service revenue and other income.[file:1]
- **5000–5999 Expenses** – operating and overhead expenses.[file:1]

Starter accounts include at minimum:[file:1]
- **1000 Bank Account** (asset)
- **1100 Accounts Receivable** (asset)
- **2000 Accounts Payable** (liability)
- **2100 GST Tax Payable** (liability) – net GST position for BAS.[file:1][web:65][web:68]
- **3000 Owner’s Equity** (equity)
- **3100 Retained Earnings** (equity)
- **4000 Service Revenue** (income)
- **5000+ various expense categories** such as General Expenses, Office Expenses, Professional Fees, Travel/Transport.[file:1][web:65]

Rules for accounts:
- Account **type** is fixed once transactions exist. Name, description and code can change but type cannot, to preserve reporting logic.[file:1]
- Accounts can be **deactivated** (hidden from new entries) but not deleted once they have history. Deletion is only allowed if an account has never been used.[file:1]
- Deactivating an account must not affect past reports; it only hides the account from selection going forward.[file:1]

## Australian GST and BAS context

### GST basics
For Australian small businesses, GST is generally 10% on most taxable sales and many business purchases, and BAS reporting is required once GST-registered.[web:71][web:71]

Key points for AccSoft:
- Every income and expense account should be associated with a default **GST treatment** (e.g. GST, GST-free, Input-taxed, No GST) so that GST coding is consistent.[web:65][web:68]
- Transactions coded to the wrong account can apply the wrong GST treatment, which flows directly into BAS totals, so consistent account use matters.[web:65][web:71]
- GST is tracked via a **GST payable** liability account that represents GST collected on sales minus GST credits on purchases.[web:65][web:68]

### Cash vs accrual basis (GST)
Australian businesses with turnover under a threshold (currently $10m aggregated turnover) can generally choose to account for GST on either a **cash** or **accrual (non-cash)** basis.[web:66][web:69][web:72]

AccSoft rules:
- The business chooses a basis (cash or accrual) during setup and this becomes a key configuration value.
- On **cash basis**, GST on sales is recognised when payments are received, and GST credits on expenses when they are paid.[web:66][web:69][web:72]
- On **accrual basis**, GST on sales and purchases is recognised when invoices are issued/received, regardless of actual payment.[web:66][web:69][web:72]
- Reports and BAS export must respect this setting when calculating GST collected and GST credits.

Implementation guidance:
- The general ledger stores transactions as they occur (usually invoice date).
- For cash-basis GST reporting, AccSoft should derive GST portions based on payment allocations (e.g. bank transactions matched to invoices) rather than invoice date alone.[web:66][web:69]
- For accrual-basis GST reporting, AccSoft can use invoice-based GST amounts.

### BAS reporting alignment
The ATO’s Simpler BAS guidelines classify common transactions into GST codes that flow into specific BAS labels such as G1 (Total sales), 1A (GST on sales), and 1B (GST on purchases).[web:71]

AccSoft principles:
- Each GST code in the system should map to BAS labels, not just to a percentage rate. For example, standard-taxable sales (GST) contribute to G1 and 1A, while GST on purchases contributes to G11 and 1B.[web:71]
- Only summary-level BAS mapping is needed in the app (e.g. total GST on sales, total GST credits on purchases) so that users can easily transfer figures to their actual BAS form.[web:71]
- Detailed tax law edge cases (for example, mixed GST and GST-free supplies on a single invoice) can be handled by separate line items with different GST codes, not by complex rules.

## Transaction types and common patterns
AccSoft’s core screens (manual transactions, invoice posting, bank reconciliation, and OCR-assisted postings) should behave like a basic Australian small-business ledger. The following patterns should guide default behaviors.[file:1][web:60][web:61][web:63]

### Sales to customers
- **Invoice raised** (accrual basis):
  - Debit **Accounts Receivable**.
  - Credit **Service Revenue**.
  - Credit **GST Tax Payable** for the GST component.
- **Payment received**:
  - Debit **Bank Account**.
  - Credit **Accounts Receivable**.

On cash-basis GST, GST is only counted when the payment transaction occurs; on accrual, GST is recognised at the invoice date.[web:66][web:69]

### Expenses and supplier bills
- **Supplier bill** (accrual basis):
  - Debit appropriate **Expense** account (e.g. Office Expenses).
  - Debit **GST Tax Payable** (GST credit reduces the net amount owed to ATO).
  - Credit **Accounts Payable**.
- **Bill payment**:
  - Debit **Accounts Payable**.
  - Credit **Bank Account**.

On cash-basis GST, GST credits are only recognised when the payment is recorded.[web:66][web:69][web:72]

### Simple cash expenses
For out-of-pocket or direct card expenses:
- Debit expense account.
- Debit GST (if applicable).
- Credit bank/credit card.

### Owner drawings and contributions
- **Owner contribution** (injecting cash):
  - Debit **Bank Account**.
  - Credit **Owner’s Equity**.
- **Owner drawings** (taking cash, not wages):
  - Debit **Owner’s Drawings/Equity** (or a separate drawings account under equity).
  - Credit **Bank Account**.

No GST should normally apply to owner drawings.

## Chart of accounts conventions
AccSoft’s chart of accounts should be simple but aligned with typical Australian small-business practice, where clean mapping to GST/BAS and year-end accounts is critical.[file:1][web:65][web:68]

Principles:
- Keep the number of active accounts modest. Many Australian bookkeeping templates suggest on the order of 10–20 revenue and 30–50 expense categories for micro/small businesses.[web:65][web:74]
- Every account should have:
  - Code (within its range).
  - Name.
  - Type (asset, liability, equity, income, expense).
  - Default GST treatment.
  - Short description of what belongs in the account.[file:1][web:65]
- Avoid generic “Miscellaneous” accounts; they create GST mistakes and messy reports.[web:65][web:68]

Operational rules in AccSoft:[file:1]
- Group accounts visually by type in the UI so users can see assets, liabilities, equity, income, and expenses separately.
- Auto-suggest the next available code within the correct range when creating new accounts.
- Prevent in-year deletion or renumbering that breaks comparability; encourage deactivation instead.[web:65]
- Allow new accounts to be created at any time, but suggest doing major restructuring at year-end only.

## General ledger and reporting

### General ledger
The general ledger is the master listing of all transactions by account. AccSoft must always be able to produce a complete ledger filtered by account and date range.[file:1][web:60][web:61]

Requirements:
- For any account, show beginning balance, all debits and credits in the period, and ending balance.
- Allow drill-down from summary reports (e.g. P&L or account balance summary) into the underlying ledger lines.
- Show linked attachments and invoice references when available.

### Profit & loss (P&L)
The P&L should reflect:
- Income accounts (4000–4999) as revenue.
- Expense accounts (5000–5999) as operating expenses.

For Australian small businesses, P&L is often used together with a tax accountant’s adjustments, so AccSoft’s P&L should be straightforward, without complex allocation rules. GST amounts can be excluded from revenue and expense totals where possible (i.e. report figures net of GST) if it simplifies understanding, but the app should be explicit about whether figures are GST-inclusive or exclusive.[web:65][web:71]

### Balance sheet
The balance sheet should present assets, liabilities and equity as at a selected date:
- **Assets:** bank accounts, receivables, and other assets.
- **Liabilities:** payables, GST payable, credit cards, loans.
- **Equity:** owner’s equity, retained earnings.

GST payable should clearly show as a liability, representing the net amount owed to or from the ATO at that date.[web:65][web:68]

### Tax and GST reports
AccSoft should provide a **GST summary report** aligned to BAS needs:
- Total taxable sales and GST on those sales.
- Total GST credits on purchases.
- Net GST payable or refundable.

These values should be derivable from underlying transactions and GST codes, and the report should explain how they relate to BAS labels such as G1, 1A and 1B.[web:71]

## Bank reconciliation rules
Bank reconciliation in a small Australian business is critical for confidence in BAS and year-end figures. AccSoft’s reconciliation feature should focus on matching actual bank statement lines to ledger transactions.[file:1][web:65]

Principles:
- Every bank statement line should either be matched to an existing ledger transaction or used to create one.
- The reconciliation screen must show statement balance, ledger balance, and any difference.
- For cash-basis GST, reconciled payments drive GST timing, so reconciliation status should be visible in GST reports.[web:66][web:69]

Workflow guidance:
- Import or enter bank transactions.
- Suggest matches based on date, amount and description.
- Allow manual matching and creation of new income/expense entries directly from the reconciliation screen.
- Lock reconciled periods so that changes after reconciliation are either blocked or clearly flagged.

## OCR and GL suggestion boundaries
AccSoft’s OCR and GL suggestion features are decision aids only. Accounting decisions remain with the user.[file:1]

Rules:
- OCR can propose vendor, date, invoice number, GST amounts and account coding, but final posting must always be confirmed by the user.[file:1]
- When users correct account suggestions, AccSoft may remember that mapping for future suggestions, but should not auto-post without review.[file:1]
- The system should clearly show when a transaction came from OCR and when values were modified manually.

## Data integrity and auditability

### Immutable history
- Posted transactions should not be silently altered once reconciled or reported. If changes are needed, use adjustments or clearly logged edits.
- Store timestamps and user IDs for creation and changes.

### Attachments and record-keeping
The ATO generally expects business records, including invoices and receipts, to be kept for at least five years, including supporting documents.[web:65][web:71]

AccSoft implications:
- Attachments should be linked to transactions and easy to retrieve.
- Deleting an attachment should be discouraged; if supported, log deletions.

## Scope limits and disclaimers
AccSoft is designed for **simple Australian small-service-business bookkeeping**, not for complex entities or full tax-return preparation.[file:1][web:65]

Out-of-scope areas include:
- Fringe Benefits Tax, payroll, and superannuation calculations.
- Complex asset depreciation schedules (beyond simple expense accounts).
- Detailed income tax calculations.

The software should periodically remind users that BAS and year-end tax positions should be reviewed by a registered tax or BAS agent.
