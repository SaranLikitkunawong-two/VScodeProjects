import os
import uuid as _uuid
from datetime import date as date_cls
from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.transaction import Transaction
from app.models.attachment import Attachment
from app.models.customer import Customer
from app.models.supplier import Supplier
from . import service

_ALLOWED_EXT = {"pdf", "jpg", "jpeg", "png"}


def _save_attachments(files, txn_id: str) -> int:
    folder = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(folder, exist_ok=True)
    saved = 0
    for f in files:
        if not f or not f.filename:
            continue
        ext = f.filename.rsplit(".", 1)[1].lower() if "." in f.filename else ""
        if ext not in _ALLOWED_EXT:
            continue
        stored = f"{_uuid.uuid4()}.{ext}"
        f.save(os.path.join(folder, stored))
        mime = "application/pdf" if ext == "pdf" else f"image/{ext}"
        db.session.add(Attachment(transaction_id=txn_id, filename=f.filename,
                                  storage_path=stored, mime_type=mime))
        saved += 1
    if saved:
        db.session.commit()
    return saved

transactions_bp = Blueprint(
    "transactions", __name__,
    url_prefix="/transactions",
    template_folder="../../templates/transactions",
)


@transactions_bp.route("/")
@login_required
def list_transactions():
    search = request.args.get("search", "").strip()
    sort = request.args.get("sort", "date_desc")
    txns = service.get_transactions(search=search or None, sort=sort)
    return render_template("transactions/list.html", transactions=txns, search=search, sort=sort)


@transactions_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    accounts = service.get_active_accounts()
    customers = _get_active_customers()
    suppliers = _get_active_suppliers()
    if request.method == "POST":
        lines_data, parse_errors = _parse_lines(request.form)
        errors = _validate_header(request.form) + parse_errors + service.validate_lines(lines_data)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "transactions/form.html", title="New Transaction",
                form_action=url_for("transactions.add_transaction"),
                accounts=accounts, transaction=None,
                prefill=request.form, lines=lines_data,
                customers=customers, suppliers=suppliers,
            )
        txn = service.create_transaction(
            date=date_cls.fromisoformat(request.form["date"]),
            description=request.form["description"].strip(),
            reference=request.form.get("reference", "").strip(),
            lines_data=lines_data,
            customer_id=request.form.get("customer_id", "").strip() or None,
            supplier_id=request.form.get("supplier_id", "").strip() or None,
        )
        _save_attachments(request.files.getlist("attachments"), txn.id)
        flash(f"Transaction '{txn.description}' saved.", "success")
        return redirect(url_for("transactions.edit_transaction", txn_id=txn.id))

    return render_template(
        "transactions/form.html", title="New Transaction",
        form_action=url_for("transactions.add_transaction"),
        accounts=accounts, transaction=None, prefill={}, lines=[],
        customers=customers, suppliers=suppliers,
    )


@transactions_bp.route("/<txn_id>/edit", methods=["GET", "POST"])
@login_required
def edit_transaction(txn_id):
    txn = db.session.get(Transaction, txn_id)
    if not txn:
        flash("Transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))
    accounts = service.get_active_accounts()
    customers = _get_active_customers()
    suppliers = _get_active_suppliers()

    if request.method == "POST":
        lines_data, parse_errors = _parse_lines(request.form)
        errors = _validate_header(request.form) + parse_errors + service.validate_lines(lines_data)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "transactions/form.html", title="Edit Transaction",
                form_action=url_for("transactions.edit_transaction", txn_id=txn_id),
                accounts=accounts, transaction=txn,
                prefill=request.form, lines=lines_data,
                customers=customers, suppliers=suppliers,
            )
        service.update_transaction(
            txn,
            date=date_cls.fromisoformat(request.form["date"]),
            description=request.form["description"].strip(),
            reference=request.form.get("reference", "").strip(),
            lines_data=lines_data,
            customer_id=request.form.get("customer_id", "").strip() or None,
            supplier_id=request.form.get("supplier_id", "").strip() or None,
        )
        flash("Transaction updated.", "success")
        return redirect(url_for("transactions.list_transactions"))

    existing_lines = [
        {"account_id": l.account_id, "type": l.type, "amount": str(l.amount)}
        for l in txn.lines
    ]
    return render_template(
        "transactions/form.html", title="Edit Transaction",
        form_action=url_for("transactions.edit_transaction", txn_id=txn_id),
        accounts=accounts, transaction=txn, prefill={}, lines=existing_lines,
        customers=customers, suppliers=suppliers,
    )


@transactions_bp.route("/<txn_id>/delete", methods=["POST"])
@login_required
def delete_transaction(txn_id):
    txn = db.session.get(Transaction, txn_id)
    if not txn:
        flash("Transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))
    if service.has_attachments(txn_id):
        flash(
            "Cannot delete — this transaction has attachments. Remove attachments first.",
            "danger",
        )
        return redirect(url_for("transactions.list_transactions"))
    service.delete_transaction(txn)
    flash("Transaction deleted.", "success")
    return redirect(url_for("transactions.list_transactions"))


@transactions_bp.route("/ledger")
@login_required
def ledger():
    account_id = request.args.get("account_id", "")
    date_from_str = request.args.get("date_from") or None
    date_to_str = request.args.get("date_to") or None

    date_from = date_to = None
    if date_from_str:
        try:
            date_from = date_cls.fromisoformat(date_from_str)
        except ValueError:
            pass
    if date_to_str:
        try:
            date_to = date_cls.fromisoformat(date_to_str)
        except ValueError:
            pass

    all_accounts = service.get_active_accounts()
    account, entries = (None, [])
    if account_id:
        account, entries = service.get_general_ledger(account_id, date_from, date_to)

    return render_template(
        "transactions/ledger.html",
        all_accounts=all_accounts,
        account=account,
        entries=entries,
        account_id=account_id,
        date_from=date_from,
        date_to=date_to,
    )


# ── helpers ───────────────────────────────────────────────────────────────────

def _parse_lines(form) -> tuple[list, list]:
    lines, errors = [], []
    i = 0
    while True:
        account_id = form.get(f"lines[{i}][account_id]")
        if account_id is None:
            break
        line_type = form.get(f"lines[{i}][type]", "debit")
        amount_str = form.get(f"lines[{i}][amount]", "0").strip()
        try:
            amount = float(amount_str)
        except ValueError:
            amount = 0.0
            errors.append(f"Line {i + 1}: invalid amount '{amount_str}'.")
        lines.append({"account_id": account_id, "type": line_type, "amount": amount})
        i += 1
    return lines, errors


def _get_active_customers():
    return db.session.execute(
        db.select(Customer).where(Customer.is_active == True).order_by(Customer.name)
    ).scalars().all()


def _get_active_suppliers():
    return db.session.execute(
        db.select(Supplier).where(Supplier.is_active == True).order_by(Supplier.name)
    ).scalars().all()


def _validate_header(form) -> list[str]:
    errors = []
    if not form.get("date", "").strip():
        errors.append("Date is required.")
    else:
        try:
            date_cls.fromisoformat(form["date"])
        except ValueError:
            errors.append("Invalid date format.")
    if not form.get("description", "").strip():
        errors.append("Description is required.")
    return errors
