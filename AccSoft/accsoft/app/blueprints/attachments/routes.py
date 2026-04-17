import os
import uuid
from flask import current_app, redirect, url_for, flash, request, send_from_directory, abort
from flask_login import login_required
from app.extensions import db
from app.models.attachment import Attachment
from app.models.transaction import Transaction
from . import attachments_bp


_ALLOWED = {"pdf", "jpg", "jpeg", "png"}


def _upload_dir():
    return os.path.join(current_app.root_path, "static", "uploads")


def _ext(filename):
    return filename.rsplit(".", 1)[1].lower() if "." in filename else ""


@attachments_bp.route("/upload/<txn_id>", methods=["POST"])
@login_required
def upload(txn_id):
    txn = db.session.get(Transaction, txn_id)
    if not txn:
        flash("Transaction not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))

    folder = _upload_dir()
    os.makedirs(folder, exist_ok=True)

    uploaded = 0
    for f in request.files.getlist("attachments"):
        if not f or not f.filename:
            continue
        ext = _ext(f.filename)
        if ext not in _ALLOWED:
            flash(f"'{f.filename}' skipped — only JPG, PNG, PDF allowed.", "warning")
            continue
        stored_name = f"{uuid.uuid4()}.{ext}"
        f.save(os.path.join(folder, stored_name))
        mime = "application/pdf" if ext == "pdf" else f"image/{ext}"
        db.session.add(Attachment(
            transaction_id=txn_id,
            filename=f.filename,
            storage_path=stored_name,
            mime_type=mime,
        ))
        uploaded += 1

    if uploaded:
        db.session.commit()
        flash(f"{uploaded} file(s) uploaded.", "success")

    return redirect(url_for("transactions.edit_transaction", txn_id=txn_id))


@attachments_bp.route("/<att_id>/delete", methods=["POST"])
@login_required
def delete(att_id):
    att = db.session.get(Attachment, att_id)
    if not att:
        flash("Attachment not found.", "danger")
        return redirect(url_for("transactions.list_transactions"))
    txn_id = att.transaction_id
    path = os.path.join(_upload_dir(), att.storage_path)
    if os.path.exists(path):
        os.remove(path)
    db.session.delete(att)
    db.session.commit()
    flash("Attachment deleted.", "success")
    return redirect(url_for("transactions.edit_transaction", txn_id=txn_id))


@attachments_bp.route("/view/<att_id>")
@login_required
def view(att_id):
    att = db.session.get(Attachment, att_id)
    if not att:
        abort(404)
    return send_from_directory(
        _upload_dir(), att.storage_path,
        as_attachment=False,
        download_name=att.filename,
    )
