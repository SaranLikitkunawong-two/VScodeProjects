from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app.extensions import db
from app.models.supplier import Supplier
from app.models.transaction import Transaction, TransactionLine
from app.models.account import Account

suppliers_bp = Blueprint(
    "suppliers", __name__,
    url_prefix="/suppliers",
    template_folder="../../templates/suppliers",
)


@suppliers_bp.route("/")
@login_required
def list_suppliers():
    show_inactive = request.args.get("show_inactive") == "1"
    q = db.select(Supplier).order_by(Supplier.name)
    if not show_inactive:
        q = q.where(Supplier.is_active == True)
    suppliers = db.session.execute(q).scalars().all()
    return render_template("suppliers/list.html", suppliers=suppliers, show_inactive=show_inactive)


@suppliers_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_supplier():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Supplier name is required.", "danger")
            return render_template("suppliers/form.html", title="Add Supplier",
                                   form_action=url_for("suppliers.add_supplier"),
                                   supplier=None, prefill=request.form)
        s = Supplier(
            name=name,
            contact_person=request.form.get("contact_person", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            address=request.form.get("address", "").strip(),
            abn=request.form.get("abn", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(s)
        db.session.commit()
        flash(f"Supplier '{s.name}' added.", "success")
        return redirect(url_for("suppliers.list_suppliers"))
    return render_template("suppliers/form.html", title="Add Supplier",
                           form_action=url_for("suppliers.add_supplier"),
                           supplier=None, prefill={})


@suppliers_bp.route("/<supp_id>/edit", methods=["GET", "POST"])
@login_required
def edit_supplier(supp_id):
    s = db.session.get(Supplier, supp_id)
    if not s:
        flash("Supplier not found.", "danger")
        return redirect(url_for("suppliers.list_suppliers"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Supplier name is required.", "danger")
            return render_template("suppliers/form.html",
                                   title=f"Edit — {s.name}",
                                   form_action=url_for("suppliers.edit_supplier", supp_id=supp_id),
                                   supplier=s, prefill=request.form)
        s.name = name
        s.contact_person = request.form.get("contact_person", "").strip()
        s.email = request.form.get("email", "").strip()
        s.phone = request.form.get("phone", "").strip()
        s.address = request.form.get("address", "").strip()
        s.abn = request.form.get("abn", "").strip()
        s.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash(f"Supplier '{s.name}' updated.", "success")
        return redirect(url_for("suppliers.list_suppliers"))
    return render_template("suppliers/form.html",
                           title=f"Edit — {s.name}",
                           form_action=url_for("suppliers.edit_supplier", supp_id=supp_id),
                           supplier=s, prefill={})


@suppliers_bp.route("/<supp_id>/toggle", methods=["POST"])
@login_required
def toggle_supplier(supp_id):
    s = db.session.get(Supplier, supp_id)
    if not s:
        flash("Supplier not found.", "danger")
        return redirect(url_for("suppliers.list_suppliers"))
    s.is_active = not s.is_active
    db.session.commit()
    state = "activated" if s.is_active else "deactivated"
    flash(f"Supplier '{s.name}' {state}.", "info")
    return redirect(url_for("suppliers.list_suppliers"))


@suppliers_bp.route("/<supp_id>")
@login_required
def detail(supp_id):
    s = db.session.get(Supplier, supp_id)
    if not s:
        flash("Supplier not found.", "danger")
        return redirect(url_for("suppliers.list_suppliers"))

    txns = db.session.execute(
        db.select(Transaction)
        .where(Transaction.supplier_id == supp_id)
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
    ).scalars().all()

    ap_balance = _compute_ap_balance(txns)

    return render_template("suppliers/detail.html",
                           supplier=s, transactions=txns, ap_balance=ap_balance)


@suppliers_bp.route("/search")
@login_required
def search():
    q = request.args.get("q", "").strip()
    results = db.session.execute(
        db.select(Supplier)
        .where(Supplier.is_active == True)
        .where(Supplier.name.ilike(f"%{q}%"))
        .order_by(Supplier.name)
        .limit(10)
    ).scalars().all()
    return jsonify([{"id": s.id, "name": s.name} for s in results])


def _compute_ap_balance(transactions) -> Decimal:
    """Net AP balance: credit AP lines - debit AP lines across all linked transactions."""
    balance = Decimal("0")
    for txn in transactions:
        for line in txn.lines:
            acct = db.session.get(Account, line.account_id)
            if acct and acct.type == "liability" and acct.code.startswith("20"):
                if line.type == "credit":
                    balance += line.amount
                else:
                    balance -= line.amount
    return balance
