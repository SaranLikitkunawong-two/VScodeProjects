from datetime import date as date_cls

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app.extensions import db
from app.models.reconciliation import ReconciliationMatch
from . import service

reconciliation_bp = Blueprint(
    "reconciliation",
    __name__,
    url_prefix="/reconciliation",
    template_folder="../../templates/reconciliation",
)


@reconciliation_bp.route("/")
@login_required
def list_sessions():
    sessions = service.get_all_sessions()
    return render_template("reconciliation/list.html", sessions=sessions)


@reconciliation_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_session():
    accounts = service.get_active_accounts()
    if request.method == "POST":
        account_id = request.form.get("account_id", "").strip()
        period_start_str = request.form.get("period_start", "").strip()
        period_end_str = request.form.get("period_end", "").strip()
        opening_balance_str = request.form.get("opening_balance", "0").strip()
        statement_date_str = request.form.get("statement_date", "").strip()
        notes = request.form.get("notes", "").strip() or None
        csv_file = request.files.get("csv_file")

        errors = []
        if not account_id:
            errors.append("Account is required.")
        if not period_start_str:
            errors.append("Period start is required.")
        if not period_end_str:
            errors.append("Period end is required.")
        if not csv_file or not csv_file.filename:
            errors.append("CSV file is required.")

        period_start = period_end = None
        if period_start_str:
            try:
                period_start = date_cls.fromisoformat(period_start_str)
            except ValueError:
                errors.append("Invalid period start date.")
        if period_end_str:
            try:
                period_end = date_cls.fromisoformat(period_end_str)
            except ValueError:
                errors.append("Invalid period end date.")
        if period_start and period_end and period_start > period_end:
            errors.append("Period start must be before period end.")

        opening_balance = 0.0
        try:
            opening_balance = float(opening_balance_str)
        except ValueError:
            errors.append("Invalid opening balance.")

        statement_date = None
        if statement_date_str:
            try:
                statement_date = date_cls.fromisoformat(statement_date_str)
            except ValueError:
                errors.append("Invalid statement date.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "reconciliation/new.html", accounts=accounts, prefill=request.form
            )

        statement, csv_errors = service.import_csv(csv_file, account_id, statement_date)
        if not statement:
            for e in csv_errors:
                flash(e, "danger")
            return render_template(
                "reconciliation/new.html", accounts=accounts, prefill=request.form
            )
        for e in csv_errors:
            flash(e, "warning")

        recon = service.create_session(
            account_id=account_id,
            bank_statement=statement,
            period_start=period_start,
            period_end=period_end,
            opening_balance=opening_balance,
            notes=notes,
        )
        flash(
            f"Session created — {len(statement.lines)} bank line(s) imported.", "success"
        )
        return redirect(url_for("reconciliation.detail", session_id=recon.id))

    return render_template(
        "reconciliation/new.html", accounts=accounts, prefill={}
    )


@reconciliation_bp.route("/<session_id>")
@login_required
def detail(session_id):
    recon = service.get_session(session_id)
    if not recon:
        flash("Session not found.", "danger")
        return redirect(url_for("reconciliation.list_sessions"))

    unmatched_lines = service.get_unmatched_bank_lines(recon)
    unmatched_txns = service.get_unmatched_transactions(recon)
    matched_lines = service.get_matched_bank_lines(recon)
    totals = service.get_session_totals(recon)

    txn_amounts = {}
    for txn in unmatched_txns:
        txn_amounts[txn.id] = service.get_txn_amount(txn, recon.account_id)
    for _, txns in matched_lines:
        for txn in txns:
            if txn.id not in txn_amounts:
                txn_amounts[txn.id] = service.get_txn_amount(txn, recon.account_id)

    return render_template(
        "reconciliation/detail.html",
        session=recon,
        unmatched_lines=unmatched_lines,
        unmatched_txns=unmatched_txns,
        matched_lines=matched_lines,
        txn_amounts=txn_amounts,
        totals=totals,
    )


@reconciliation_bp.route("/<session_id>/match", methods=["POST"])
@login_required
def match(session_id):
    recon = service.get_session(session_id)
    if not recon:
        flash("Session not found.", "danger")
        return redirect(url_for("reconciliation.list_sessions"))

    line_ids = request.form.getlist("line_ids")
    txn_ids = request.form.getlist("txn_ids")
    count, errors = service.create_match(recon, line_ids, txn_ids, current_user.id)
    if errors:
        for e in errors:
            flash(e, "danger")
    else:
        flash(f"{count} match link(s) created.", "success")
    return redirect(url_for("reconciliation.detail", session_id=session_id))


@reconciliation_bp.route("/<session_id>/unmatch", methods=["POST"])
@login_required
def unmatch(session_id):
    recon = service.get_session(session_id)
    if not recon:
        flash("Session not found.", "danger")
        return redirect(url_for("reconciliation.list_sessions"))

    line_id = request.form.get("line_id", "").strip()
    errors = service.remove_match(recon, line_id)
    if errors:
        for e in errors:
            flash(e, "danger")
    else:
        flash("Match removed.", "success")
    return redirect(url_for("reconciliation.detail", session_id=session_id))


@reconciliation_bp.route("/<session_id>/complete", methods=["POST"])
@login_required
def complete(session_id):
    recon = service.get_session(session_id)
    if not recon:
        flash("Session not found.", "danger")
        return redirect(url_for("reconciliation.list_sessions"))

    errors = service.complete_session(recon)
    if errors:
        for e in errors:
            flash(e, "danger")
    else:
        flash("Reconciliation marked as complete.", "success")
    return redirect(url_for("reconciliation.detail", session_id=session_id))


@reconciliation_bp.route("/<session_id>/reopen", methods=["POST"])
@login_required
def reopen(session_id):
    recon = service.get_session(session_id)
    if not recon:
        flash("Session not found.", "danger")
        return redirect(url_for("reconciliation.list_sessions"))

    errors = service.reopen_session(recon)
    if errors:
        for e in errors:
            flash(e, "danger")
    else:
        flash("Reconciliation session reopened.", "success")
    return redirect(url_for("reconciliation.detail", session_id=session_id))


@reconciliation_bp.route("/<session_id>/history")
@login_required
def history(session_id):
    recon = service.get_session(session_id)
    if not recon:
        flash("Session not found.", "danger")
        return redirect(url_for("reconciliation.list_sessions"))

    matches = db.session.execute(
        db.select(ReconciliationMatch)
        .where(ReconciliationMatch.session_id == session_id)
        .order_by(ReconciliationMatch.matched_at.desc())
    ).scalars().all()

    return render_template(
        "reconciliation/history.html", session=recon, matches=matches
    )
