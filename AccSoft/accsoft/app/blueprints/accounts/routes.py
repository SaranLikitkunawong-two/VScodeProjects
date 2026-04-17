from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from app.extensions import db
from app.models.account import Account, ACCOUNT_TYPES
from . import service
from .service import TYPE_ORDER, TYPE_LABELS, TYPE_COLORS

accounts_bp = Blueprint(
    "accounts", __name__,
    url_prefix="/accounts",
    template_folder="../../templates/accounts",
)


@accounts_bp.route("/")
@login_required
def list_accounts():
    grouped = service.get_accounts_grouped()
    return render_template(
        "list.html",
        grouped=grouped,
        type_order=TYPE_ORDER,
        type_labels=TYPE_LABELS,
        type_colors=TYPE_COLORS,
        next_codes=service.get_next_codes_all(),
        account_types=ACCOUNT_TYPES,
        type_locked_ids=service.get_accounts_with_transactions(),
    )


@accounts_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_account():
    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        acct_type   = request.form.get("type", "").strip()
        code        = request.form.get("code", "").strip()
        description = request.form.get("description", "").strip()

        errors = _validate_new(name, acct_type, code)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "form.html",
                title="Add Account",
                form_action=url_for("accounts.add_account"),
                account=None,
                account_types=ACCOUNT_TYPES,
                next_codes=service.get_next_codes_all(),
                type_locked=False,
                prefill=request.form,
            )

        acct = service.create_account(name, acct_type, code, description)
        flash(f"Account '{acct.name}' ({acct.code}) created.", "success")
        return redirect(url_for("accounts.list_accounts"))

    return render_template(
        "form.html",
        title="Add Account",
        form_action=url_for("accounts.add_account"),
        account=None,
        account_types=ACCOUNT_TYPES,
        next_codes=service.get_next_codes_all(),
        type_locked=False,
        prefill={},
    )


@accounts_bp.route("/<account_id>/edit", methods=["GET", "POST"])
@login_required
def edit_account(account_id):
    account = db.session.get(Account, account_id)
    if not account:
        flash("Account not found.", "danger")
        return redirect(url_for("accounts.list_accounts"))

    type_locked = service.has_transactions(account_id)

    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        code        = request.form.get("code", "").strip()
        description = request.form.get("description", "").strip()
        acct_type   = request.form.get("type", account.type).strip()

        errors = _validate_edit(name, code, acct_type, account_id, type_locked)
        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "form.html",
                title=f"Edit — {account.code} {account.name}",
                form_action=url_for("accounts.edit_account", account_id=account_id),
                account=account,
                account_types=ACCOUNT_TYPES,
                next_codes=service.get_next_codes_all(),
                type_locked=type_locked,
                prefill=request.form,
            )

        service.update_account(
            account, name, code, description,
            account_type=None if type_locked else acct_type,
        )
        flash(f"Account '{account.name}' updated.", "success")
        return redirect(url_for("accounts.list_accounts"))

    return render_template(
        "form.html",
        title=f"Edit — {account.code} {account.name}",
        form_action=url_for("accounts.edit_account", account_id=account_id),
        account=account,
        account_types=ACCOUNT_TYPES,
        next_codes=service.get_next_codes_all(),
        type_locked=type_locked,
        prefill={},
    )


@accounts_bp.route("/<account_id>/deactivate", methods=["POST"])
@login_required
def deactivate_account(account_id):
    account = db.session.get(Account, account_id)
    if not account:
        flash("Account not found.", "danger")
        return redirect(url_for("accounts.list_accounts"))
    service.toggle_active(account)
    state = "activated" if account.is_active else "deactivated"
    flash(f"Account '{account.name}' {state}.", "info")
    return redirect(url_for("accounts.list_accounts"))


@accounts_bp.route("/<account_id>/delete", methods=["POST"])
@login_required
def delete_account(account_id):
    account = db.session.get(Account, account_id)
    if not account:
        flash("Account not found.", "danger")
        return redirect(url_for("accounts.list_accounts"))
    if service.has_transactions(account_id):
        flash(
            f"Cannot delete '{account.name}' — it has linked transactions. "
            "Deactivate it instead.",
            "danger",
        )
        return redirect(url_for("accounts.list_accounts"))
    name = account.name
    service.delete_account(account)
    flash(f"Account '{name}' deleted.", "success")
    return redirect(url_for("accounts.list_accounts"))


# ── validation helpers ────────────────────────────────────────────────────────

def _validate_new(name: str, acct_type: str, code: str) -> list[str]:
    errors = []
    if not name:
        errors.append("Account name is required.")
    if acct_type not in ACCOUNT_TYPES:
        errors.append("Invalid account type.")
    if not code:
        errors.append("Account code is required.")
    elif db.session.execute(
        db.select(Account).where(Account.code == code)
    ).scalar_one_or_none():
        errors.append(f"Account code {code!r} is already in use.")
    return errors


def _validate_edit(name: str, code: str, acct_type: str,
                   account_id: str, type_locked: bool) -> list[str]:
    errors = []
    if not name:
        errors.append("Account name is required.")
    if not code:
        errors.append("Account code is required.")
    elif db.session.execute(
        db.select(Account).where(Account.code == code, Account.id != account_id)
    ).scalar_one_or_none():
        errors.append(f"Account code {code!r} is already in use.")
    if not type_locked and acct_type not in ACCOUNT_TYPES:
        errors.append("Invalid account type.")
    return errors
