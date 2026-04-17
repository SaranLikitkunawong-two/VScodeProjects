import uuid
from datetime import datetime, timezone
from app.extensions import db

ACCOUNT_TYPES = ("asset", "liability", "equity", "income", "expense")


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.Enum(*ACCOUNT_TYPES, name="account_type"), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.Text, default="")
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    transaction_lines = db.relationship("TransactionLine", back_populates="account")
    vendor_mappings = db.relationship("VendorMapping", back_populates="account")
    keyword_mappings = db.relationship("KeywordMapping", back_populates="account")

    def __repr__(self):
        return f"<Account {self.code} {self.name}>"
