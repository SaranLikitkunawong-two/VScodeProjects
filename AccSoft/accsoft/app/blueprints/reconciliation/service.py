import csv
import io
from datetime import datetime, timezone
from decimal import Decimal

from app.extensions import db
from app.models.reconciliation import (
    BankStatement,
    BankStatementLine,
    ReconciliationSession,
    ReconciliationMatch,
)
from app.models.transaction import Transaction, TransactionLine


# ── sessions ──────────────────────────────────────────────────────────────────

def get_all_sessions():
    return db.session.execute(
        db.select(ReconciliationSession).order_by(ReconciliationSession.created_at.desc())
    ).scalars().all()


def get_session(session_id: str):
    return db.session.get(ReconciliationSession, session_id)


def get_active_accounts():
    from app.models.account import Account
    return db.session.execute(
        db.select(Account).where(Account.is_active == True).order_by(Account.code)
    ).scalars().all()


def create_session(account_id, bank_statement, period_start, period_end,
                   opening_balance, notes=None) -> ReconciliationSession:
    recon = ReconciliationSession(
        account_id=account_id,
        bank_statement_id=bank_statement.id,
        period_start=period_start,
        period_end=period_end,
        opening_balance=Decimal(str(opening_balance)),
        notes=notes,
    )
    db.session.add(recon)
    db.session.commit()
    return recon


def complete_session(session: ReconciliationSession) -> list[str]:
    if session.status == "complete":
        return ["Session is already complete."]
    session.status = "complete"
    session.completed_at = datetime.now(timezone.utc)
    db.session.commit()
    return []


def reopen_session(session: ReconciliationSession) -> list[str]:
    if session.status not in ("complete", "reopened"):
        return ["Session is not complete — nothing to reopen."]
    session.status = "reopened"
    session.completed_at = None
    db.session.commit()
    return []


# ── csv import ────────────────────────────────────────────────────────────────

def import_csv(file, account_id: str, statement_date=None):
    """Parse an uploaded CSV and create BankStatement + lines.

    Returns (BankStatement, errors). If a fatal error occurs, returns (None, errors).
    Non-fatal row errors are returned alongside a valid statement.
    """
    try:
        content = file.read().decode("utf-8-sig")
    except Exception:
        return None, ["Could not read file — ensure it is a UTF-8 encoded CSV."]

    reader = csv.DictReader(io.StringIO(content))
    if not reader.fieldnames:
        return None, ["CSV appears to be empty."]

    fieldnames_lower = {f.strip().lower(): f for f in reader.fieldnames}
    missing = {"date", "description", "amount"} - set(fieldnames_lower.keys())
    if missing:
        return None, [f"CSV is missing required columns: {', '.join(sorted(missing))}."]

    statement = BankStatement(
        account_id=account_id,
        filename=getattr(file, "filename", "upload.csv"),
        statement_date=statement_date,
    )
    db.session.add(statement)
    db.session.flush()

    ref_col = fieldnames_lower.get("reference")
    bal_col = fieldnames_lower.get("balance")
    ext_col = fieldnames_lower.get("external_id")
    existing_ext_ids: set[str] = set()
    errors: list[str] = []
    rows_added = 0

    for i, row in enumerate(reader, start=2):
        date_raw = row.get(fieldnames_lower["date"], "").strip()
        parsed_date = _parse_date(date_raw)
        if parsed_date is None:
            errors.append(f"Row {i}: invalid date '{date_raw}'.")
            continue

        desc = row.get(fieldnames_lower["description"], "").strip()
        if not desc:
            errors.append(f"Row {i}: description is empty.")
            continue

        amt_raw = row.get(fieldnames_lower["amount"], "").strip().replace(",", "")
        try:
            amount = Decimal(amt_raw)
        except Exception:
            errors.append(f"Row {i}: invalid amount '{amt_raw}'.")
            continue

        reference = row.get(ref_col, "").strip() or None if ref_col else None
        balance = None
        if bal_col:
            bal_raw = row.get(bal_col, "").strip().replace(",", "")
            if bal_raw:
                try:
                    balance = Decimal(bal_raw)
                except Exception:
                    pass
        external_id = row.get(ext_col, "").strip() or None if ext_col else None

        if external_id:
            if external_id in existing_ext_ids:
                continue
            existing_ext_ids.add(external_id)

        db.session.add(BankStatementLine(
            bank_statement_id=statement.id,
            date=parsed_date,
            description=desc,
            amount=amount,
            reference=reference,
            balance=balance,
            external_id=external_id,
        ))
        rows_added += 1

    if rows_added == 0:
        db.session.rollback()
        if not errors:
            errors.append("No valid rows found in CSV.")
        return None, errors

    db.session.commit()
    return statement, errors


def _parse_date(date_str: str):
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    return None


# ── reconciliation data ───────────────────────────────────────────────────────

def get_unmatched_bank_lines(session: ReconciliationSession) -> list:
    return db.session.execute(
        db.select(BankStatementLine)
        .where(
            BankStatementLine.bank_statement_id == session.bank_statement_id,
            BankStatementLine.is_matched == False,
        )
        .order_by(BankStatementLine.date)
    ).scalars().all()


def get_unmatched_transactions(session: ReconciliationSession) -> list:
    matched_ids = db.select(ReconciliationMatch.transaction_id).where(
        ReconciliationMatch.session_id == session.id
    )
    return db.session.execute(
        db.select(Transaction)
        .where(
            Transaction.date >= session.period_start,
            Transaction.date <= session.period_end,
            Transaction.id.in_(
                db.select(TransactionLine.transaction_id).where(
                    TransactionLine.account_id == session.account_id
                )
            ),
            Transaction.id.notin_(matched_ids),
        )
        .order_by(Transaction.date)
    ).scalars().all()


def get_matched_bank_lines(session: ReconciliationSession) -> list[tuple]:
    """Return [(BankStatementLine, [Transaction, ...]), ...] for this session."""
    lines = db.session.execute(
        db.select(BankStatementLine)
        .where(
            BankStatementLine.bank_statement_id == session.bank_statement_id,
            BankStatementLine.is_matched == True,
        )
        .order_by(BankStatementLine.date)
    ).scalars().all()

    result = []
    for line in lines:
        session_matches = db.session.execute(
            db.select(ReconciliationMatch)
            .where(
                ReconciliationMatch.bank_statement_line_id == line.id,
                ReconciliationMatch.session_id == session.id,
            )
        ).scalars().all()
        result.append((line, [m.transaction for m in session_matches]))
    return result


def get_txn_amount(txn: Transaction, account_id: str) -> Decimal:
    """Net movement in account_id for this transaction (debit = positive)."""
    net = Decimal("0")
    for line in txn.lines:
        if line.account_id == account_id:
            net += line.amount if line.type == "debit" else -line.amount
    return net


def get_session_totals(session: ReconciliationSession) -> dict:
    lines = session.bank_statement.lines
    matched = [l for l in lines if l.is_matched]
    unmatched = [l for l in lines if not l.is_matched]
    return {
        "total_count": len(lines),
        "matched_count": len(matched),
        "unmatched_count": len(unmatched),
        "total_bank": sum((l.amount for l in lines), Decimal("0")),
        "matched_bank": sum((l.amount for l in matched), Decimal("0")),
        "unmatched_bank": sum((l.amount for l in unmatched), Decimal("0")),
    }


# ── match / unmatch ───────────────────────────────────────────────────────────

def create_match(session: ReconciliationSession, line_ids: list, txn_ids: list,
                 user_id: str) -> tuple[int, list[str]]:
    if session.status == "complete":
        return 0, ["Session is locked — reopen it before making changes."]
    if not line_ids:
        return 0, ["Select at least one bank line."]
    if not txn_ids:
        return 0, ["Select at least one transaction."]

    valid_lines = db.session.execute(
        db.select(BankStatementLine).where(
            BankStatementLine.id.in_(line_ids),
            BankStatementLine.bank_statement_id == session.bank_statement_id,
        )
    ).scalars().all()
    if len(valid_lines) != len(line_ids):
        return 0, ["One or more bank lines are invalid."]

    valid_txns = db.session.execute(
        db.select(Transaction).where(Transaction.id.in_(txn_ids))
    ).scalars().all()
    if len(valid_txns) != len(txn_ids):
        return 0, ["One or more transactions are invalid."]

    count = 0
    for line in valid_lines:
        for txn in valid_txns:
            existing = db.session.execute(
                db.select(ReconciliationMatch).where(
                    ReconciliationMatch.session_id == session.id,
                    ReconciliationMatch.bank_statement_line_id == line.id,
                    ReconciliationMatch.transaction_id == txn.id,
                )
            ).scalar_one_or_none()
            if not existing:
                db.session.add(ReconciliationMatch(
                    session_id=session.id,
                    bank_statement_line_id=line.id,
                    transaction_id=txn.id,
                    matched_by_id=user_id,
                ))
                count += 1
        line.is_matched = True

    db.session.commit()
    return count, []


def remove_match(session: ReconciliationSession, line_id: str) -> list[str]:
    if session.status == "complete":
        return ["Session is locked — reopen it before making changes."]
    line = db.session.get(BankStatementLine, line_id)
    if not line or line.bank_statement_id != session.bank_statement_id:
        return ["Bank line not found."]
    db.session.execute(
        db.delete(ReconciliationMatch).where(
            ReconciliationMatch.bank_statement_line_id == line_id,
            ReconciliationMatch.session_id == session.id,
        )
    )
    line.is_matched = False
    db.session.commit()
    return []
