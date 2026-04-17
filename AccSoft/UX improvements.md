# AccSoft — UX Improvements

> UX items, polish tasks, and user-facing verifications that are not part of core feature delivery.
> Pick these up after a session's core functionality is verified.

---

## Accounts (Session 2)

### Done ✓
- Modal overlay for Add/Edit account — accounts list visible behind form
- Scroll position preserved after all actions (deactivate/reactivate, delete, edit/save)

### Pending
- [ ] Implement 3-level account hierarchy: Level 1 = type, Level 2 = parent account, Level 3 = subaccount. Only Level 3 allows transaction posting. Render as indented tree; Levels 1–2 show aggregated balances from descendants only.

### Verify
- [ ] Modal opens correctly for Add and Edit — confirm accounts list is visible behind modal
- [ ] Scroll position is restored after Deactivate/Activate, Delete, and Save actions
- [ ] Edit modal shows Type field as locked (disabled) for accounts that have transactions
- [ ] Type dropdown auto-suggests account code in Add mode

---

## Transactions & Ledger (Session 3)

### Done ✓
- CSV export button on transaction list (respects search filter)
- Account autocomplete on journal line rows (type-to-filter, click to select)
- Date field opens calendar picker on click anywhere in the input
- Journal lines split into separate Debit and Credit columns (replaces Type + Amount)
- Balance effect column (+/−) on each journal line, calculated from account normal balance side
- Balancing hint shows "$X.XX more needed on debits/credits" when unbalanced
- Ledger preset date range buttons: Today, Yesterday, Last 7 Days, This Month, Last Month

### Pending
- [ ] Transaction list: add a left-hand filter panel with date range slicer and account slicer (search + multi-select); filters list on apply
- [ ] Transaction entry: support selecting multiple GL account lines via checkboxes

---

## Dashboard (Session 4)

### Done ✓
- Dashboard balance display: DR/CR suffix and "deficit" indicator now respect normal balance sides (debit-normal accounts are never flagged as deficit when balance is positive)

---

## UX Suggestions Log

| Date | Item | Status |
|---|---|---|
| 2026-04-17 | Balancing hint under transaction totals | ✓ Done |
| 2026-04-17 | Dashboard DR/CR deficit indicator fix | ✓ Done |
