"""
Reconciliation: February 2026 Bank Statement vs POS Transactions
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pandas as pd
import numpy as np
from collections import defaultdict
from datetime import timedelta

BANK_FILE = r"C:\Users\Saran Likitkunawong\VScode\Medium\Financials\Reconciliations\Bankstatement inflows - february.csv"
POS_FILE  = r"C:\Users\Saran Likitkunawong\VScode\Medium\Financials\Reconciliations\FebPOS transactions.csv"

EXCLUDED_TYPES = {'entertainment', 'tasting', 'cash', 'staff'}
MAX_LAG_DAYS   = 5

# ==============================================================================
# 1. LOAD DATA
# ==============================================================================

# Bank statement
bank = pd.read_csv(BANK_FILE, thousands=',')
bank.columns = bank.columns.str.strip()
bank['Date'] = pd.to_datetime(bank['Date'], dayfirst=True)
bank['Deposit'] = pd.to_numeric(bank['Deposit'].astype(str).str.replace(',',''), errors='coerce').fillna(0)
bank = bank[bank['Deposit'] > 0].copy().reset_index(drop=True)
bank['is_line_pay'] = bank['Details'].str.contains('LINE PAY', case=False, na=False)
bank['matched'] = False
bank['matched_receipts'] = [[] for _ in range(len(bank))]

print(f"Bank inflow rows: {len(bank)}")

# POS transactions
pos = pd.read_csv(POS_FILE)
pos.columns = pos.columns.str.strip()
pos['Payment Date'] = pd.to_datetime(pos['Payment Date'], dayfirst=True, errors='coerce')
pos['Discounted Price'] = pd.to_numeric(pos['Discounted Price'].astype(str).str.replace(',',''), errors='coerce').fillna(0)

# Exclude irrelevant payment types
pos_filtered = pos[~pos['Payment Type'].str.strip().str.lower().isin(EXCLUDED_TYPES)].copy()
print(f"POS rows after excluding {EXCLUDED_TYPES}: {len(pos_filtered)} (of {len(pos)})")

# ==============================================================================
# 2. BUILD RECEIPT-LEVEL SUMMARY
# ==============================================================================

def receipt_summary(df):
    grp = df.groupby('Receipt Number')
    summary = grp.agg(
        date        = ('Payment Date', 'first'),
        payment_type= ('Payment Type', 'first'),
        total_discounted = ('Discounted Price', 'sum'),
    ).reset_index()
    # Flag whether all items are Food
    food_flags = df.groupby('Receipt Number')['Category'].apply(
        lambda cats: all(str(c).strip().lower() == 'food' for c in cats)
    ).rename('all_food')
    summary = summary.merge(food_flags, on='Receipt Number')
    # Apply 10% service charge if any non-food item
    summary['charge_amount'] = np.where(
        summary['all_food'],
        summary['total_discounted'],
        (summary['total_discounted'] * 1.10).round(2)
    )
    return summary

receipts = receipt_summary(pos_filtered)
print(f"Unique receipts (excl. excluded types): {len(receipts)}")

# QRCode in POS = LINE PAY grouped deposits in bank
is_line_pay = receipts['payment_type'].str.strip().str.lower().isin(['qrcode', 'qr code', 'qr'])
lp_receipts  = receipts[is_line_pay].copy()
ind_receipts = receipts[~is_line_pay].copy()

print(f"  LINE PAY receipts : {len(lp_receipts)}")
print(f"  Individual receipts: {len(ind_receipts)}")

# ==============================================================================
# 3. MATCHING
# ==============================================================================

match_log = []
matched_receipt_ids = set()

# -- 3a. Individual (non-LINE-PAY) receipts ------------------------------------
for _, rec in ind_receipts.iterrows():
    if pd.isna(rec['date']):
        continue
    pos_date   = rec['date'].date()
    target     = rec['charge_amount']
    receipt_id = rec['Receipt Number']

    for i, brow in bank.iterrows():
        if bank.at[i, 'matched']:
            continue
        if brow['is_line_pay']:
            continue
        lag = (brow['Date'].date() - pos_date).days
        if 0 <= lag <= MAX_LAG_DAYS and abs(brow['Deposit'] - target) < 1.0:
            bank.at[i, 'matched'] = True
            bank.at[i, 'matched_receipts'].append(receipt_id)
            matched_receipt_ids.add(receipt_id)
            match_log.append({
                'type': 'individual',
                'bank_date': brow['Date'].date(),
                'bank_amount': brow['Deposit'],
                'receipt': receipt_id,
                'pos_date': pos_date,
                'lag_days': lag,
                'payment_type': rec['payment_type'],
            })
            break

# -- 3b. LINE PAY grouped deposits ---------------------------------------------
lp_bank_rows = bank[(~bank['matched']) & (bank['is_line_pay'])].copy()

# Group LINE PAY receipts by date
lp_by_date = defaultdict(list)
for _, rec in lp_receipts.iterrows():
    if not pd.isna(rec['date']):
        lp_by_date[rec['date'].date()].append(rec)

for i, brow in lp_bank_rows.iterrows():
    if bank.at[i, 'matched']:
        continue
    bank_date = brow['Date'].date()
    target    = brow['Deposit']
    found     = False

    # Try rolling windows of consecutive days leading up to the bank date
    for window_days in range(1, MAX_LAG_DAYS + 1):
        for start_offset in range(MAX_LAG_DAYS):
            candidate_dates = [bank_date - timedelta(days=start_offset + d) for d in range(window_days)]
            candidates = []
            for cd in candidate_dates:
                for rec in lp_by_date.get(cd, []):
                    if rec['Receipt Number'] not in matched_receipt_ids:
                        candidates.append(rec)

            if not candidates:
                continue
            total = sum(r['charge_amount'] for r in candidates)
            if abs(total - target) < 2.0:
                bank.at[i, 'matched'] = True
                for rec in candidates:
                    bank.at[i, 'matched_receipts'].append(rec['Receipt Number'])
                    matched_receipt_ids.add(rec['Receipt Number'])
                match_log.append({
                    'type': 'LINE PAY group',
                    'bank_date': bank_date,
                    'bank_amount': target,
                    'receipt': [r['Receipt Number'] for r in candidates],
                    'pos_dates': sorted({r['date'].date() for r in candidates}),
                    'lag_days': start_offset,
                    'payment_type': 'LINE PAY',
                })
                found = True
                break
        if found:
            break

# ==============================================================================
# 4. RESULTS
# ==============================================================================

total_bank          = bank['Deposit'].sum()
matched_bank_amt    = bank.loc[bank['matched'], 'Deposit'].sum()
unmatched_bank_amt  = bank.loc[~bank['matched'], 'Deposit'].sum()

total_pos_rev       = receipts['charge_amount'].sum()
matched_pos_amt     = receipts.loc[receipts['Receipt Number'].isin(matched_receipt_ids), 'charge_amount'].sum()

print("\n" + "="*65)
print("RECONCILIATION SUMMARY — February 2026")
print("="*65)

print(f"""
BANK STATEMENT
  Total inflow entries  : {len(bank)}
  Total amount          : {total_bank:>10,.2f} THB
  Matched entries       : {bank['matched'].sum()}
  Matched amount        : {matched_bank_amt:>10,.2f} THB
  Unmatched entries     : {(~bank['matched']).sum()}
  Unmatched amount      : {unmatched_bank_amt:>10,.2f} THB

POS RECEIPTS  (excl. cash/staff/tasting/entertainment)
  Total receipts        : {len(receipts)}
  Total revenue         : {total_pos_rev:>10,.2f} THB
  Matched receipts      : {len(matched_receipt_ids)}
  Matched revenue       : {matched_pos_amt:>10,.2f} THB
  Unmatched receipts    : {len(receipts) - len(matched_receipt_ids)}
  Unmatched revenue     : {total_pos_rev - matched_pos_amt:>10,.2f} THB
""")

print("-"*65)
print("MATCHED TRANSACTIONS")
print("-"*65)
for m in match_log:
    if m['type'] == 'individual':
        print(f"  [{m['bank_date']}]  {m['bank_amount']:>8.2f} THB  <-{m['receipt']:6s} "
              f"({m['payment_type']}, lag {m['lag_days']}d)")
    else:
        count = len(m['receipt']) if isinstance(m['receipt'], list) else 1
        print(f"  [{m['bank_date']}]  {m['bank_amount']:>8.2f} THB  <-LINE PAY group "
              f"({count} receipts, dates {m['pos_dates']}, lag ~{m['lag_days']}d)")

print("\n" + "-"*65)
print("UNMATCHED BANK ENTRIES")
print("-"*65)
for _, b in bank[~bank['matched']].iterrows():
    print(f"  [{b['Date'].date()}]  {b['Deposit']:>8.2f} THB  | {b['Channel']}  | {str(b['Details'])[:55]}")

print("\n" + "-"*65)
print("UNMATCHED POS RECEIPTS")
print("-"*65)
unmatched_pos = receipts[~receipts['Receipt Number'].isin(matched_receipt_ids)]
for _, r in unmatched_pos.iterrows():
    print(f"  {r['Receipt Number']}  [{r['date'].date() if not pd.isna(r['date']) else 'N/A'}]  "
          f"{r['payment_type']:22s}  {r['charge_amount']:>8.2f} THB")

print("\n" + "-"*65)
print("PAYMENT TYPE BREAKDOWN (POS receipts)")
print("-"*65)
receipts['is_matched'] = receipts['Receipt Number'].isin(matched_receipt_ids)
pt_summary = receipts.groupby('payment_type').agg(
    receipts_count = ('Receipt Number', 'count'),
    total_revenue  = ('charge_amount', 'sum'),
    matched_count  = ('is_matched', 'sum'),
    matched_revenue= ('charge_amount', lambda x: x[receipts.loc[x.index, 'is_matched']].sum()),
).sort_values('total_revenue', ascending=False)

for pt, row in pt_summary.iterrows():
    pct = 100 * row['matched_count'] / row['receipts_count'] if row['receipts_count'] else 0
    print(f"  {pt:25s}  {int(row['receipts_count']):3d} receipts  "
          f"{row['total_revenue']:>9.2f} THB  "
          f"matched {int(row['matched_count'])}/{int(row['receipts_count'])} ({pct:.0f}%)")

print("\n" + "-"*65)
print("LAG TIME ANALYSIS (matched individual transactions)")
print("-"*65)
lag_counts = defaultdict(int)
for m in match_log:
    if m['type'] == 'individual':
        lag_counts[m['lag_days']] += 1
for lag in sorted(lag_counts):
    print(f"  {lag} day(s) lag: {lag_counts[lag]} transactions")

print("\n" + "-"*65)
print("SERVICE CHARGE BREAKDOWN")
print("-"*65)
sc_applied = receipts[~receipts['all_food']]
sc_not     = receipts[receipts['all_food']]
print(f"  Receipts with service charge (non-food items): {len(sc_applied)}")
print(f"  Receipts without service charge (food only)  : {len(sc_not)}")

print("\nDone. Done.")
