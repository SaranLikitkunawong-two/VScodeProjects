from decimal import Decimal
from app.extensions import db
from app.models.account import Account
from app.models.transaction import Transaction, TransactionLine


def get_active_accounts():
    return db.session.execute(
        db.select(Account)
        .where(Account.is_active == True, Account.allows_posting == True)
        .order_by(Account.code)
    ).scalars().all()


def get_transactions(search=None, sort="date_desc", date_from=None, date_to=None, account_ids=None, kinds=None):
    q = db.select(Transaction)
    if search:
        q = q.where(
            db.or_(
                Transaction.description.ilike(f"%{search}%"),
                Transaction.reference.ilike(f"%{search}%"),
            )
        )
    if date_from:
        q = q.where(Transaction.date >= date_from)
    if date_to:
        q = q.where(Transaction.date <= date_to)
    if kinds:
        q = q.where(Transaction.kind.in_(kinds))
    if account_ids:
        q = q.where(
            Transaction.id.in_(
                db.select(TransactionLine.transaction_id).where(
                    TransactionLine.account_id.in_(account_ids)
                )
            )
        )
    if sort == "date_asc":
        q = q.order_by(Transaction.date.asc(), Transaction.created_at.asc())
    else:
        q = q.order_by(Transaction.date.desc(), Transaction.created_at.desc())
    return db.session.execute(q).scalars().all()


def validate_lines(lines_data: list) -> list[str]:
    errors = []
    if len(lines_data) < 2:
        errors.append("A transaction needs at least 2 lines.")
        return errors
    total_debits = Decimal("0")
    total_credits = Decimal("0")
    for i, line in enumerate(lines_data, start=1):
        if not line.get("account_id"):
            errors.append(f"Line {i}: account is required.")
        else:
            acct = db.session.get(Account, line["account_id"])
            if acct and not acct.allows_posting:
                errors.append(f"Line {i}: '{acct.name}' does not allow posting.")
        try:
            amt = Decimal(str(line["amount"]))
            if amt <= 0:
                errors.append(f"Line {i}: amount must be greater than zero.")
            if line["type"] == "debit":
                total_debits += amt
            else:
                total_credits += amt
        except Exception:
            errors.append(f"Line {i}: invalid amount.")
    if not errors and total_debits != total_credits:
        errors.append(
            f"Debits (${total_debits:,.2f}) must equal credits (${total_credits:,.2f})."
        )
    return errors


def create_transaction(date, description, reference, lines_data,
                       customer_id=None, supplier_id=None,
                       kind="manual_journal",
                       related_transaction_id=None) -> Transaction:
    txn = Transaction(
        date=date, description=description, reference=reference or "",
        customer_id=customer_id or None, supplier_id=supplier_id or None,
        kind=kind,
        related_transaction_id=related_transaction_id or None,
    )
    db.session.add(txn)
    for line in lines_data:
        db.session.add(TransactionLine(
            transaction=txn,
            account_id=line["account_id"],
            type=line["type"],
            amount=Decimal(str(line["amount"])),
        ))
    db.session.commit()
    return txn


def update_transaction(txn: Transaction, date, description, reference, lines_data,
                       customer_id=None, supplier_id=None) -> None:
    # kind is immutable after creation
    txn.date = date
    txn.description = description
    txn.reference = reference or ""
    txn.customer_id = customer_id or None
    txn.supplier_id = supplier_id or None
    for line in list(txn.lines):
        db.session.delete(line)
    db.session.flush()
    for line in lines_data:
        db.session.add(TransactionLine(
            transaction=txn,
            account_id=line["account_id"],
            type=line["type"],
            amount=Decimal(str(line["amount"])),
        ))
    db.session.commit()


def delete_transaction(txn: Transaction) -> None:
    db.session.delete(txn)
    db.session.commit()


def has_attachments(txn_id: str) -> bool:
    from app.models.attachment import Attachment
    count = db.session.execute(
        db.select(db.func.count(Attachment.id))
        .where(Attachment.transaction_id == txn_id)
    ).scalar()
    return (count or 0) > 0


def get_general_ledger(account_ids: list[str], date_from=None, date_to=None):
    """Return a flat, date-ordered list of (txn, line, account) entries across
    all selected accounts. Running balance is omitted when combining multiple
    accounts because it has no meaningful interpretation across heterogeneous
    account types."""
    if not account_ids:
        return []

    q = (
        db.select(TransactionLine, Transaction, Account)
        .join(Transaction, TransactionLine.transaction_id == Transaction.id)
        .join(Account, TransactionLine.account_id == Account.id)
        .where(TransactionLine.account_id.in_(account_ids))
    )
    if date_from:
        q = q.where(Transaction.date >= date_from)
    if date_to:
        q = q.where(Transaction.date <= date_to)
    q = q.order_by(
        Transaction.date.asc(),
        Transaction.created_at.asc(),
        Account.code.asc(),
    )

    rows = db.session.execute(q).all()
    return [(txn, line, acct) for line, txn, acct in rows]
