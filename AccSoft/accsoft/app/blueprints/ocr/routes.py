import os
import uuid as _uuid
from datetime import date as date_cls
from decimal import Decimal, InvalidOperation

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app.extensions import db
from app.models.account import Account
from app.models.attachment import Attachment
from app.models.ocr_result import OcrResult
from app.blueprints.transactions import service as txn_service
from . import pipeline, extractor, gl_suggester

ocr_bp = Blueprint(
    "ocr", __name__,
    url_prefix="/ocr",
    template_folder="../../templates/ocr",
)

_ALLOWED_EXT = {"pdf", "jpg", "jpeg", "png"}


@ocr_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "GET":
        return render_template("ocr/upload.html")

    f = request.files.get("invoice")
    if not f or not f.filename:
        flash("Please select a file to upload.", "danger")
        return render_template("ocr/upload.html")

    ext = f.filename.rsplit(".", 1)[-1].lower() if "." in f.filename else ""
    if ext not in _ALLOWED_EXT:
        flash("Only PDF, JPG, and PNG files are supported.", "danger")
        return render_template("ocr/upload.html")

    # Save file to uploads folder (no transaction yet)
    folder = os.path.join(current_app.root_path, "static", "uploads")
    os.makedirs(folder, exist_ok=True)
    stored_name = f"{_uuid.uuid4()}.{ext}"
    file_path = os.path.join(folder, stored_name)
    f.save(file_path)

    # Store a placeholder attachment (transaction_id null until confirmed)
    attachment = Attachment(
        transaction_id=_placeholder_txn_id(),
        filename=f.filename,
        storage_path=stored_name,
        mime_type="application/pdf" if ext == "pdf" else f"image/{ext}",
    )
    db.session.add(attachment)
    db.session.flush()

    # Run pipeline
    raw_text, confidence = pipeline.extract_text(file_path)
    fields = extractor.extract_fields(raw_text)
    suggestion = gl_suggester.suggest(fields.get("vendor", ""), fields.get("notes", ""))

    ocr_result = OcrResult(
        attachment_id=attachment.id,
        raw_text=raw_text,
        extracted_fields=fields,
        confidence=confidence,
    )
    db.session.add(ocr_result)
    db.session.commit()

    if not raw_text:
        flash(
            "No text could be extracted from this file. "
            "Please fill in the fields manually.",
            "warning",
        )

    return redirect(url_for("ocr.review", ocr_id=ocr_result.id,
                             suggestion_debit=suggestion["debit_account_id"] or "",
                             suggestion_credit=suggestion["credit_account_id"] or "",
                             vendor_known=int(suggestion["vendor_known"])))


@ocr_bp.route("/review/<ocr_id>", methods=["GET", "POST"])
@login_required
def review(ocr_id):
    ocr = db.session.get(OcrResult, ocr_id)
    if not ocr:
        flash("OCR result not found.", "danger")
        return redirect(url_for("ocr.upload"))

    accounts = txn_service.get_active_accounts()
    fields = ocr.extracted_fields or {}

    suggestion_debit = request.args.get("suggestion_debit", "")
    suggestion_credit = request.args.get("suggestion_credit", "")
    vendor_known = request.args.get("vendor_known", "0") == "1"

    return render_template(
        "ocr/review.html",
        ocr=ocr,
        fields=fields,
        accounts=accounts,
        suggestion_debit=suggestion_debit,
        suggestion_credit=suggestion_credit,
        vendor_known=vendor_known,
    )


@ocr_bp.route("/confirm/<ocr_id>", methods=["POST"])
@login_required
def confirm(ocr_id):
    ocr = db.session.get(OcrResult, ocr_id)
    if not ocr:
        flash("OCR result not found.", "danger")
        return redirect(url_for("ocr.upload"))

    accounts = txn_service.get_active_accounts()

    # Collect form fields
    vendor      = request.form.get("vendor", "").strip()
    invoice_no  = request.form.get("invoice_no", "").strip()
    invoice_date= request.form.get("invoice_date", "").strip()
    total_str   = request.form.get("total", "").strip()
    debit_id    = request.form.get("debit_account_id", "").strip()
    credit_id   = request.form.get("credit_account_id", "").strip()
    save_vendor = request.form.get("save_vendor_mapping") == "1"

    errors = []
    if not invoice_date:
        errors.append("Date is required.")
    else:
        try:
            txn_date = date_cls.fromisoformat(invoice_date)
        except ValueError:
            errors.append("Invalid date format (use YYYY-MM-DD).")
            txn_date = None

    if not total_str:
        errors.append("Total amount is required.")
        total = None
    else:
        try:
            total = Decimal(total_str)
            if total <= 0:
                errors.append("Total must be greater than zero.")
        except InvalidOperation:
            errors.append("Invalid total amount.")
            total = None

    if not debit_id:
        errors.append("Debit account is required.")
    if not credit_id:
        errors.append("Credit account is required.")
    if debit_id and credit_id and debit_id == credit_id:
        errors.append("Debit and credit accounts must be different.")

    if errors:
        for e in errors:
            flash(e, "danger")
        fields = {
            "vendor": vendor, "invoice_no": invoice_no,
            "invoice_date": invoice_date, "total": total_str,
        }
        return render_template(
            "ocr/review.html",
            ocr=ocr, fields=fields, accounts=accounts,
            suggestion_debit=debit_id, suggestion_credit=credit_id,
            vendor_known=False,
        )

    description = f"Invoice – {vendor}" if vendor else "Invoice"
    if invoice_no:
        description += f" #{invoice_no}"

    lines_data = [
        {"account_id": debit_id,  "type": "debit",  "amount": total},
        {"account_id": credit_id, "type": "credit", "amount": total},
    ]
    txn = txn_service.create_transaction(
        date=txn_date,
        description=description,
        reference=invoice_no,
        lines_data=lines_data,
    )

    # Reattach the uploaded file to the new transaction
    attachment = db.session.get(Attachment, ocr.attachment_id)
    if attachment:
        attachment.transaction_id = txn.id
        db.session.commit()

    if save_vendor and vendor and debit_id:
        gl_suggester.save_vendor_mapping(vendor, debit_id)
        flash(f"Vendor mapping saved for '{vendor}'.", "info")

    flash(f"Invoice posted as transaction '{description}'.", "success")
    return redirect(url_for("transactions.edit_transaction", txn_id=txn.id))


def _placeholder_txn_id() -> str:
    """Return the ID of a sentinel transaction used to satisfy the NOT NULL FK
    on attachments until the real transaction is created on confirm."""
    from app.models.transaction import Transaction
    sentinel = db.session.execute(
        db.select(Transaction).where(Transaction.description == "__ocr_placeholder__")
    ).scalar_one_or_none()
    if not sentinel:
        sentinel = Transaction(
            date=date_cls(2000, 1, 1),
            description="__ocr_placeholder__",
            reference="",
        )
        db.session.add(sentinel)
        db.session.flush()
    return sentinel.id
