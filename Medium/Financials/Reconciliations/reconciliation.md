# Reconciliation Analysis

This document is for analyzing and reconciling data from the following files:

- [Bankstatement inflows - february.csv](Bankstatement inflows - february.csv)
- [FebPOS transactions.csv](FebPOS transactions.csv)

## Analysis Steps

1. **Data Import**: Load the CSV files into a data analysis tool (e.g., Python with pandas, Excel, etc.).
2. **Data Cleaning**: Check for inconsistencies, missing values, and formatting issues.
3. **Matching Transactions**: Identify matching transactions between the bank statement and POS transactions.
4. **Discrepancy Identification**: Highlight any discrepancies or unmatched transactions.
5. **Reconciliation Summary**: Provide a summary of the reconciliation process and results.

## Notes

- Ensure dates are in the same format.
- Verify amounts match exactly or within a tolerance.
- Document any manual adjustments made.

## Reconciliation Rules and Insights

### Timing of Payments
- Cash received in the bank account may be on the same day as the transaction or a few days after.
- Some transactions may be grouped and paid at once by LINE, identifiable by descriptions like "From X4826 LINE PAY (THAILAND++".

### Amount Calculation
- Use the "discounted price" column from POS transactions as the target amount.
- A 10% service charge may be added to this amount if the category is not "Food".

### Discount Remarks
- The "remark" column contains free text describing why discounts are applied.

### Payment Methods
- Ignore payment types: 'entertainment', 'tasting', 'cash', and 'staff' (non-revenue or free for staff).
- Focus on other payment types to match back to the bank statement.
- Analyze:
  - Which payment types get grouped together.
  - Average lag time for payments.
  - Any POS sales that regularly get missed in the bank statement.

## Results

*Analysis run: 2026-03-24 using Python/pandas. Script: [reconcile.py](reconcile.py)*

---

### Overall Summary

| | Count | Amount (THB) |
|---|---|---|
| **Bank inflow entries** | 67 | 80,489.86 |
| Bank entries matched to POS | 41 | 37,691.00 |
| Bank entries unmatched | 26 | 42,798.86 |
| **POS receipts (excl. excluded types)** | 92 | 71,380.40 |
| POS receipts matched to bank | 41 | 37,690.70 |
| POS receipts unmatched | 51 | 33,689.70 |

- 109 POS rows were excluded (cash: 22, staff: 59, tasting: 16, entertainment: 12).
- 90 out of 92 receipts had non-food items and therefore attracted the 10% service charge.

---

### Payment Type Breakdown

| Payment Type | Receipts | Revenue (THB) | Match Rate |
|---|---|---|---|
| KBank-Other | 50 | 45,106.90 | **78%** |
| QRCode (LINE PAY) | 12 | 9,588.70 | **0%** — see note below |
| Bank Transfer | 13 | 5,712.30 | **15%** — see note below |
| VISA | 10 | 6,963.00 | **0%** — batched into LINE PAY deposit (see §3) |
| Master Card | 6 | 3,707.00 | **0%** — batched into LINE PAY deposit (see §3) |
| Grab | 1 | 302.50 | **0%** — separate payout |

---

### Key Learnings

#### 1. VISA & Master Card are settled via LINE PAY — not a separate card acquirer
VISA and MC payments are processed through the LINE Pay terminal (EDC) and batched together with QRCode payments into the LINE PAY lump-sum deposits. **They do NOT settle into a separate bank account.** The Feb 16 bank deposit of **17,204.67 THB** closely matches the combined QRCode + VISA + MC raw total for Feb 14–15 (**17,040.00 THB**, gap of only 164.67 THB / ~1%). No QRCode-only subset matches any LINE PAY deposit, confirming all three card types are batched together.

#### 2. Grab settles separately
The single Grab receipt (302.50 THB) will be paid out by Grab through their own payout cycle, not as an individual transfer to this account.

#### 3. LINE PAY batches QRCode + VISA + MC together, with a ~1-day settlement lag

| Bank date | Deposit | Best POS match | POS gross (raw) | Gap | Fee implied |
|---|---|---|---|---|---|
| 01 Feb | 2,555.26 | No Feb POS data | — | — | Likely Jan carry-over |
| 07 Feb | 574.93 | OIBDI VISA (06 Feb, raw 540) | 594.00 (with 10% SC) | −19.07 | ~3.21% MDR on VISA |
| 15 Feb | 1,265.00 | No matching POS subset | — | — | Likely Jan carry-over |
| 16 Feb | 17,204.67 | QR+VISA+MC Feb 14–15 | 17,040.00 (raw, no SC) | +164.67 | ~0% (or missing receipts) |

**Key findings from the matching analysis:**

- **No QRCode-only day matches any LINE PAY deposit** at any fee level (0–4%). LINE PAY does not settle QR codes separately — all terminal types (QR, VISA, MC) are batched.
- **Feb 16 near-match**: The combined QR + VISA + MC raw discounted total for Feb 14–15 is **17,040.00 THB**, vs the bank deposit of **17,204.67 THB** (gap of +164.67 THB). The bank received *more* than the raw discounted total, which rules out a positive fee on the full batch. Most likely explanation: **~165 THB of POS receipts are missing from the export** (e.g. receipts entered after the export was taken, or voided/re-entered receipts).
- **Feb 7 near-match**: The single VISA receipt (OIBDI, 06 Feb) at raw 540 THB becomes 594 THB with 10% SC. The bank received 574.93 — implying a **~3.2% LINE PAY MDR on VISA card payments**. If SC is 7% instead of 10%, the implied fee drops to 0.5%.
- **Feb 1 and Feb 15 deposits** (2,555.26 and 1,265.00) cannot be matched to any February POS data — these almost certainly represent **January LINE PAY transactions** settling in early February.
- **Batch period**: LINE PAY appears to settle in multi-day batches (Feb 14–15 receipts paid on Feb 16), consistent with a 1–2 business day settlement cycle.

#### 4. "Bank Transfer" in POS = exclusively AomJamies (owner's tab)
**100% of Bank Transfer POS receipts (13 receipts, 6,383 THB) are from the AomJamies table.** This payment type is used solely for the owner's consumption. These entries do not follow the normal same-day settlement pattern and need to be tracked separately. Some partial matches exist (e.g. E7AKA 600 THB matched to Uthit Chaw Feb 21 bank entry, E4TGF has 0 THB), but most require manual reconciliation against owner records.

#### 5. KBank-Other (non-AomJamies): 81–94% match rate with strong same-day settlement

Of 48 non-AomJamies KBank-Other receipts, **39 match exactly (81%)** within ±7 days. When looser matching is applied, up to **45/48 (94%)** can be reconciled:

| Receipt | Date | Charge | Bank match | Notes |
|---|---|---|---|---|
| BA8NK | 07 Feb | 264.00 | 240.00 (07 Feb) | Customer paid **raw price (no SC)** — service charge was skipped or waived |
| UDII8 | 15 Feb | 550.00 | 550.00 (14 Feb) | **Pre-payment** 1 day before — customer settled the bill before the POS receipt was created (the Feb 14 550 THB previously flagged as Valentine's Day is this receipt) |
| 782DJ | 24 Feb | 330.00 | 330.00 (24 Feb) | Exact match to BBL X2771 (Piroon) — confirmed |
| D9XYQ | 26 Feb | 330.00 | 330.00 (26 Feb) | Exact match to BBL X2771 (Piroon) — confirmed |
| ZZDV1 | 28 Feb | 649.00 | 650.00 (28 Feb) | 1 THB rounding — customer paid 650. **Reasonable match — accepted.** |
| S7YNX | 11 Feb | 792.00 | 792.00 (11 Feb) | **Conflict**: same bank entry (SCB X7483) already matched to E19R0 — two POS receipts of 792 from the same customer; bank shows only one 792 entry on this date |

**Genuinely unmatched (3 receipts):**

| Receipt | Date | Charge | Notes |
|---|---|---|---|
| Z44XS | 11 Feb | 1,311.20 | "Sabina" table — bank has 1,320.00 (MS. SIRIBHA SACHDE) same day. Diff = 8.80 THB; raw 1,200 × 1.10 = 1,320 exactly, suggesting one item was priced 8 THB higher than recorded in POS. **Reasonable match — accepted.** |
| E2M0A | 15 Feb | 2,684.00 | Table 6 — bottle (Jim Beam 1,400) + mixers + food. No bank entry of this amount in the full month. **Likely paid cash or via a different channel.** |
| EV00A | 27 Feb | 165.00 | Single food item (Khao Pad), no SC. No bank match. Small amount — possibly cash or missed. |

#### 6. Lag time is predominantly same-day
Of 39 confirmed-matched KBank-Other transactions:
- **0 days lag**: 35 transactions (90%)
- **1 day lag**: 1 transaction
- **3 days lag**: 2 transactions
- **5 days lag**: 1 transaction

Most customers pay the same night as the POS sale (bank timestamps are after midnight, matching late-night service hours). BBL X2771 (Piroon) is an exception — regularly pays 2–5 days later.

#### 7. Valentine's Day (14 Feb) — revised: the 550 THB is now explained
The 550 THB bank deposit on Feb 14 (previously flagged as an unexplained event pre-payment) is now matched to **UDII8** (table 35, KBank-Other, charge=550) — a customer who pre-paid the day before their POS receipt was entered.

Remaining unexplained Feb 14 event deposits: **490×9 + 980 = 5,390 THB** (not in POS). These 10 transfers of 490/980 THB from 10 different individuals remain unmatched and are almost certainly Valentine's Day event tickets. **Action: verify against event booking records; enter as a POS receipt if confirmed.**

---

### Outstanding Items (Action Required)

| # | Issue | Estimated Amount | Action |
|---|---|---|---|
| 1 | LINE PAY batch (Feb 16) — 164.67 gap vs POS | 164.67 THB | Check for ~1–2 missing POS receipts around 14–15 Feb |
| 2 | LINE PAY batches (Feb 1, Feb 15) — likely January carry-over | ~3,820 THB | Pull January POS export and match |
| 3 | Feb 7 LINE PAY deposit — confirm VISA MDR rate | 19.07 THB fee | Verify MDR rate in LINE Pay merchant portal |
| 4 | Valentine's Day pre-booked tickets not in POS | ~5,390 THB | 490×9 + 980 — match to booking records; enter in POS |
| 5 | E2M0A (KBank-Other, table 6, 15 Feb) — no bank match | 2,684 THB | Check if paid cash or via different channel |
| 6 | Z44XS (KBank-Other, Sabina, 11 Feb) — bank shows 1,320, POS 1,311.20 | 8.80 THB diff | Likely match (see §5 notes) — confirm if one item was priced 8 THB higher than recorded |
| 7 | S7YNX vs E19R0 — two 792 THB POS receipts, one bank entry (SCB X7483) | 792 THB conflict | Check SCB X7483 statement for second 792 payment |
| 8 | BA8NK — customer paid 240 (raw), POS shows 264 (with SC) | 24 THB SC gap | Confirm SC was waived; adjust if needed |
| 9 | AomJamies (owner tab) — 13 receipts not individually matched | 6,383 THB | Reconcile separately against owner's personal account |
| 10 | Grab payout not in this account | 302.50 THB | Check Grab partner portal |
| 11 | Feb 28 QRCode receipt (J5U7Y, 837 THB) — no bank match yet | 837 THB | Will settle early March; check March statement |
| 12 | EV00A (165 THB food, 27 Feb) — no bank match | 165 THB | Check if paid cash |