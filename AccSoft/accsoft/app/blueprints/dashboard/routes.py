from decimal import Decimal
from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy import func, case
from app.extensions import db
from app.models.account import Account
from app.models.transaction import Transaction, TransactionLine

dashboard_bp = Blueprint("dashboard", __name__, template_folder="../../templates/dashboard")

_TYPE_ORDER = ["asset", "liability", "equity", "income", "expense"]
_TYPE_LABELS = {
    "asset": "Assets",
    "liability": "Liabilities",
    "equity": "Equity",
    "income": "Income",
    "expense": "Expenses",
}
_DEBIT_NORMAL = {"asset", "expense"}


@dashboard_bp.route("/")
@login_required
def index():
    rows = db.session.execute(
        db.select(
            Account.id,
            Account.name,
            Account.code,
            Account.type,
            func.coalesce(
                func.sum(case((TransactionLine.type == "debit", TransactionLine.amount), else_=0)), 0
            ).label("total_debits"),
            func.coalesce(
                func.sum(case((TransactionLine.type == "credit", TransactionLine.amount), else_=0)), 0
            ).label("total_credits"),
        )
        .outerjoin(TransactionLine, TransactionLine.account_id == Account.id)
        .where(Account.is_active == True)
        .group_by(Account.id, Account.name, Account.code, Account.type)
        .order_by(Account.type, Account.code)
    ).all()

    groups: dict = {}
    for r in rows:
        debits = Decimal(str(r.total_debits))
        credits = Decimal(str(r.total_credits))
        bal = (debits - credits) if r.type in _DEBIT_NORMAL else (credits - debits)
        if r.type not in groups:
            groups[r.type] = {
                "label": _TYPE_LABELS.get(r.type, r.type.title()),
                "type": r.type,
                "accounts": [],
                "total": Decimal("0"),
            }
        groups[r.type]["accounts"].append({"name": r.name, "code": r.code, "balance": bal})
        groups[r.type]["total"] += bal

    ordered_balances = [groups[t] for t in _TYPE_ORDER if t in groups]

    recent_raw = db.session.execute(
        db.select(Transaction)
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
        .limit(10)
    ).scalars().all()

    recent_txns = [
        {
            "txn": t,
            "amount": sum(l.amount for l in t.lines if l.type == "debit"),
        }
        for t in recent_raw
    ]

    return render_template(
        "dashboard/index.html",
        ordered_balances=ordered_balances,
        recent_txns=recent_txns,
    )
