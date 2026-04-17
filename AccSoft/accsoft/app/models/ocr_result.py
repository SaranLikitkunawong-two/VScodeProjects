import uuid
from datetime import datetime, timezone
from app.extensions import db


class OcrResult(db.Model):
    __tablename__ = "ocr_results"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    attachment_id = db.Column(db.String(36), db.ForeignKey("attachments.id"), nullable=False)
    raw_text = db.Column(db.Text, default="")
    extracted_fields = db.Column(db.JSON, default=dict)
    confidence = db.Column(db.Float, nullable=True)
    processed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    attachment = db.relationship("Attachment", back_populates="ocr_result")
