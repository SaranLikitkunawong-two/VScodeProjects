import csv
import io
import os
import uuid as _uuid
from datetime import date as date_cls
from flask import Blueprint, Response, current_app, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.transaction import Transaction, TRANSACTION_KINDS
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
    date_from_str = request.args.get("date_from", "").strip()
    date_to_str = request.args.get("date_to", "").strip()
    account_ids = request.args.getlist("accounts")
    selected_kinds = [k for k in request.args.getlist("kinds") if k in TRANSACTION_KINDS]

    date_from = date_to = None
    if date_from_str:
        try:
            date_from = date_cls.fromisoformat(date_from_str)
        except ValueError:
            date_from_str = ""
    if date_to_str:
        try:
            date_to = date_cls.fromisoformat(date_to_str)
        except ValueError:
            date_to_str = ""

    all_accounts = service.get_active_accounts()
    txns = service.get_transactions(
        search=search or None, sort=sort,
        date_from=date_from, date_to=date_to,
        account_ids=account_ids or None,
        kinds=selected_kinds or None,
    )
    return render_template(
        "transactions/list.html",
        transactions=txns, search=search, sort=sort,
        all_accounts=all_accounts,
        date_from=date_from_str, date_to=date_to_str,
        selected_accounts=account_ids,
        all_kinds=TRANSACTION_KINDS,
        selected_kinds=selected_kinds,
    )


_KIND_TITLES = {
    "manual_journal": "New Manual Journal",
    "customer_invoice": "New Customer Invoice",
    "supplier_bill": "New Supplier Bill",
    "customer_credit_note": "New Customer Credit Note",
    "supplier_credit_note": "New Supplier Credit Note",
}


def _render_new_form(kind: str, prefill=None, lines=None,
                     related_transaction_id: str | None = None):
    accounts = service.get_active_accounts()
    customers = _get_active_customers()
    suppliers = _get_active_suppliers()
    return render_template(
        "transactions/form.html",
        title=_KIND_TITLES.get(kind, "New Transaction"),
        form_action=request.path,
        accounts=accounts, transaction=None,
        prefill=prefill or {}, lines=lines or [],
        customers=customers, suppliers=suppliers,
        kind=kind,
        related_transaction_id=related_transaction_id,
    )


def _handle_create(kind: str, success_redirect=None,
                   related_transaction_id: str | None = None):
    """Shared POST handler for new-transaction routes. On GET, callers render
    the form themselves. On POST, we validate, create, then redirect."""
    lines_data, parse_errors = _parse_lines(request.form)
    errors = _validate_header(request.form) + parse_errors + service.validate_lines(lines_data)

    if kind == "customer_invoice" or kind == "customer_credit_note":
        if not request.form.get("customer_id", "").strip():
            errors.append("Customer is required.")
    if kind == "supplier_bill" or kind == "supplier_credit_note":
        if not request.form.get("supplier_id", "").strip():
            errors.append("Supplier is required.")

    if errors:
        for e in errors:
            flash(e, "danger")
        return _render_new_form(
            kind,
            prefill=request.form,
            lines=lines_data,
            related_transaction_id=related_transaction_id,
        )

    txn = service.create_transaction(
        date=date_cls.fromisoformat(request.form["date"]),
        description=request.form["description"].strip(),
        reference=request.form.get("reference", "").strip(),
        lines_data=lines_data,
        customer_id=request.form.get("customer_id", "").strip() or None,
        supplier_id=request.form.get("supplier_id", "").strip() or None,
        kind=kind,
        related_transaction_id=related_transaction_id,
    )
    _save_attachments(request.files.getlist("attachments"), txn.id)
    flash(f"{txn.kind_label} '{txn.description}' saved.", "success")
    return redirect(success_redirect or url_for("transactions.edit_transaction", txn_id=txn.id))


@transactions_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_transaction():
    if request.method == "POST":
        return _handle_create("manual_journal")
    return _render_new_form("manual_journal")


@transactions_bp.route("/invoices/new", methods=["GET", "POST"])
@login_required
def new_customer_invoice():
    if request.method == "POST":
        return _handle_create("customer_invoice")
    return _render_new_form("customer_invoice")


@transactions_bp.route("/bills/new", methods=["GET", "POST"])
@login_required
def new_supplier_bill():
    if request.method == "POST":
        return _handle_create("supplier_bill")
    return _render_new_form("supplier_bill")


_CREDIT_NOTE_KIND = {
    "customer": "customer_credit_note",
    "supplier": "supplier_credit_note",
}


@transactions_bp.route("/credit-notes/new", methods=["GET", "POST"])
@login_required
def new_credit_note():
    cn_type = request.args.get("type", "").strip()
    if cn_type not in _CREDIT_NOTE_KIND:
        # Show picker screen
        return render_template("transactions/credit_note_picker.html")

    kind = _CREDIT_NOTE_KIND[cn_type]
    if request.method == "POST":
        return _handle_create(kind)
    return _render_new_form(kind)


@transactions_bp.route("/<txn_id>/credit-note", methods=["GET", "POST"])
@login_required
def new_credit_note_from(txn_id):
    original = db.session.get(Transaction, txn_id)
    if not original:
        flash("Original transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))
    if original.kind == "customer_invoice":
        kind = "customer_credit_note"
    elif original.kind == "supplier_bill":
        kind = "supplier_credit_note"
    else:
        flash("Credit notes can only be created from customer invoices or supplier bills.", "danger")
        return redirect(url_for("transactions.edit_transaction", txn_id=txn_id))

    if request.method == "POST":
        return _handle_create(kind, related_transaction_id=original.id)

    # Pre-populate lines as a reversal of the original
    reversed_lines = [
        {
            "account_id": l.account_id,
            "type": "credit" if l.type == "debit" else "debit",
            "amount": str(l.amount),
        }
        for l in original.lines
    ]
    prefill = {
        "date": date_cls.today().isoformat(),
        "description": f"Credit Note for {original.description}",
        "reference": f"CN-{original.reference}" if original.reference else "",
        "customer_id": original.customer_id or "",
        "supplier_id": original.supplier_id or "",
    }
    return _render_new_form(
        kind,
        prefill=prefill,
        lines=reversed_lines,
        related_transaction_id=original.id,
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
        if txn.kind in ("customer_invoice", "customer_credit_note"):
            if not request.form.get("customer_id", "").strip():
                errors.append("Customer is required.")
        if txn.kind in ("supplier_bill", "supplier_credit_note"):
            if not request.form.get("supplier_id", "").strip():
                errors.append("Supplier is required.")
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "transactions/form.html", title=f"Edit {txn.kind_label}",
                form_action=url_for("transactions.edit_transaction", txn_id=txn_id),
                accounts=accounts, transaction=txn,
                prefill=request.form, lines=lines_data,
                customers=customers, suppliers=suppliers,
                kind=txn.kind,
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
        flash(f"{txn.kind_label} updated.", "success")
        return redirect(url_for("transactions.list_transactions"))

    existing_lines = [
        {"account_id": l.account_id, "type": l.type, "amount": str(l.amount)}
        for l in txn.lines
    ]
    return render_template(
        "transactions/form.html", title=f"Edit {txn.kind_label}",
        form_action=url_for("transactions.edit_transaction", txn_id=txn_id),
        accounts=accounts, transaction=txn, prefill={}, lines=existing_lines,
        customers=customers, suppliers=suppliers,
        kind=txn.kind,
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


@transactions_bp.route("/export.csv")
@login_required
def export_csv():
    search = request.args.get("search", "").strip()
    date_from_str = request.args.get("date_from", "").strip()
    date_to_str = request.args.get("date_to", "").strip()
    account_ids = request.args.getlist("accounts")
    selected_kinds = [k for k in request.args.getlist("kinds") if k in TRANSACTION_KINDS]

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

    txns = service.get_transactions(
        search=search or None, sort="date_asc",
        date_from=date_from, date_to=date_to,
        account_ids=account_ids or None,
        kinds=selected_kinds or None,
    )

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(["Date", "Description", "Reference", "Account Code", "Account Name", "Type", "Amount"])
    for txn in txns:
        for line in txn.lines:
            writer.writerow([
                txn.date.isoformat(),
                txn.description,
                txn.reference or "",
                line.account.code,
                line.account.name,
                line.type.capitalize(),
                f"{line.amount:.2f}",
            ])

    return Response(
        buf.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=transactions.csv"},
    )


@transactions_bp.route("/ledger")
@login_required
def ledger():
    account_ids = request.args.getlist("accounts")
    date_from_str = request.args.get("date_from", "").strip()
    date_to_str = request.args.get("date_to", "").strip()

    date_from = date_to = None
    if date_from_str:
        try:
            date_from = date_cls.fromisoformat(date_from_str)
        except ValueError:
            date_from_str = ""
    if date_to_str:
        try:
            date_to = date_cls.fromisoformat(date_to_str)
        except ValueError:
            date_to_str = ""

    all_accounts = service.get_active_accounts()
    entries = service.get_general_ledger(account_ids, date_from, date_to) if account_ids else []

    return render_template(
        "transactions/ledger.html",
        all_accounts=all_accounts,
        entries=entries,
        selected_accounts=account_ids,
        date_from=date_from_str,
        date_to=date_to_str,
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
