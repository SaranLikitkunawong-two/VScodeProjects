import uuid
from datetime import datetime, timezone
from app.extensions import db


class VendorMapping(db.Model):
    __tablename__ = "vendor_mappings"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    vendor_name = db.Column(db.String(255), unique=True, nullable=False)
    default_account_id = db.Column(db.String(36), db.ForeignKey("accounts.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    account = db.relationship("Account", back_populates="vendor_mappings")
