import uuid
from datetime import datetime, timezone
from app.extensions import db


class Attachment(db.Model):
    __tablename__ = "attachments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = db.Column(db.String(36), db.ForeignKey("transactions.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    storage_path = db.Column(db.String(500), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    transaction = db.relationship("Transaction", back_populates="attachments")
    ocr_result = db.relationship("OcrResult", back_populates="attachment", uselist=False)
