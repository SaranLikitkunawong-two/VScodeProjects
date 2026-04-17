from decimal import Decimal
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required
from app.extensions import db
from app.models.customer import Customer
from app.models.transaction import Transaction, TransactionLine
from app.models.account import Account

customers_bp = Blueprint(
    "customers", __name__,
    url_prefix="/customers",
    template_folder="../../templates/customers",
)


@customers_bp.route("/")
@login_required
def list_customers():
    show_inactive = request.args.get("show_inactive") == "1"
    q = db.select(Customer).order_by(Customer.name)
    if not show_inactive:
        q = q.where(Customer.is_active == True)
    customers = db.session.execute(q).scalars().all()
    return render_template("customers/list.html", customers=customers, show_inactive=show_inactive)


@customers_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_customer():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Customer name is required.", "danger")
            return render_template("customers/form.html", title="Add Customer",
                                   form_action=url_for("customers.add_customer"),
                                   customer=None, prefill=request.form)
        c = Customer(
            name=name,
            contact_person=request.form.get("contact_person", "").strip(),
            email=request.form.get("email", "").strip(),
            phone=request.form.get("phone", "").strip(),
            address=request.form.get("address", "").strip(),
            abn=request.form.get("abn", "").strip(),
            notes=request.form.get("notes", "").strip(),
        )
        db.session.add(c)
        db.session.commit()
        flash(f"Customer '{c.name}' added.", "success")
        return redirect(url_for("customers.list_customers"))
    return render_template("customers/form.html", title="Add Customer",
                           form_action=url_for("customers.add_customer"),
                           customer=None, prefill={})


@customers_bp.route("/<cust_id>/edit", methods=["GET", "POST"])
@login_required
def edit_customer(cust_id):
    c = db.session.get(Customer, cust_id)
    if not c:
        flash("Customer not found.", "danger")
        return redirect(url_for("customers.list_customers"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if not name:
            flash("Customer name is required.", "danger")
            return render_template("customers/form.html",
                                   title=f"Edit — {c.name}",
                                   form_action=url_for("customers.edit_customer", cust_id=cust_id),
                                   customer=c, prefill=request.form)
        c.name = name
        c.contact_person = request.form.get("contact_person", "").strip()
        c.email = request.form.get("email", "").strip()
        c.phone = request.form.get("phone", "").strip()
        c.address = request.form.get("address", "").strip()
        c.abn = request.form.get("abn", "").strip()
        c.notes = request.form.get("notes", "").strip()
        db.session.commit()
        flash(f"Customer '{c.name}' updated.", "success")
        return redirect(url_for("customers.list_customers"))
    return render_template("customers/form.html",
                           title=f"Edit — {c.name}",
                           form_action=url_for("customers.edit_customer", cust_id=cust_id),
                           customer=c, prefill={})


@customers_bp.route("/<cust_id>/toggle", methods=["POST"])
@login_required
def toggle_customer(cust_id):
    c = db.session.get(Customer, cust_id)
    if not c:
        flash("Customer not found.", "danger")
        return redirect(url_for("customers.list_customers"))
    c.is_active = not c.is_active
    db.session.commit()
    state = "activated" if c.is_active else "deactivated"
    flash(f"Customer '{c.name}' {state}.", "info")
    return redirect(url_for("customers.list_customers"))


@customers_bp.route("/<cust_id>")
@login_required
def detail(cust_id):
    c = db.session.get(Customer, cust_id)
    if not c:
        flash("Customer not found.", "danger")
        return redirect(url_for("customers.list_customers"))

    txns = db.session.execute(
        db.select(Transaction)
        .where(Transaction.customer_id == cust_id)
        .order_by(Transaction.date.desc(), Transaction.created_at.desc())
    ).scalars().all()

    ar_balance = _compute_ar_balance(txns)

    return render_template("customers/detail.html",
                           customer=c, transactions=txns, ar_balance=ar_balance)


@customers_bp.route("/search")
@login_required
def search():
    q = request.args.get("q", "").strip()
    results = db.session.execute(
        db.select(Customer)
        .where(Customer.is_active == True)
        .where(Customer.name.ilike(f"%{q}%"))
        .order_by(Customer.name)
        .limit(10)
    ).scalars().all()
    return jsonify([{"id": c.id, "name": c.name} for c in results])


def _compute_ar_balance(transactions) -> Decimal:
    """Net AR balance: debit AR lines - credit AR lines across all linked transactions."""
    balance = Decimal("0")
    for txn in transactions:
        for line in txn.lines:
            acct = db.session.get(Account, line.account_id)
            if acct and acct.type == "asset" and acct.code.startswith("11"):
                if line.type == "debit":
                    balance += line.amount
                else:
                    balance -= line.amount
    return balance
