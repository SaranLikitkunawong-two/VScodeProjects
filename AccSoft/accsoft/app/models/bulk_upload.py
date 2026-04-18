import uuid
from datetime import datetime, timezone
from app.extensions import db


class BulkUploadJob(db.Model):
    __tablename__ = "bulk_upload_jobs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(20), nullable=False, default="processing")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    items = db.relationship(
        "BulkUploadItem",
        back_populates="job",
        order_by="BulkUploadItem.position",
    )


class BulkUploadItem(db.Model):
    __tablename__ = "bulk_upload_items"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = db.Column(db.String(36), db.ForeignKey("bulk_upload_jobs.id"), nullable=False)
    attachment_id = db.Column(db.String(36), db.ForeignKey("attachments.id"), nullable=True)
    ocr_result_id = db.Column(db.String(36), db.ForeignKey("ocr_results.id"), nullable=True)
    transaction_id = db.Column(db.String(36), db.ForeignKey("transactions.id"), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending")
    original_filename = db.Column(db.String(255), nullable=False, default="")
    position = db.Column(db.Integer, nullable=False, default=0)

    job = db.relationship("BulkUploadJob", back_populates="items")
    attachment = db.relationship("Attachment")
    ocr_result = db.relationship("OcrResult")
    transaction = db.relationship("Transaction")
