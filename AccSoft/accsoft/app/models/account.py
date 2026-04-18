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

    # Hierarchy: 0 = leaf/posting, 1 = mid-level, 2 = top-level type
    hierarchy = db.Column(db.Integer, default=0, nullable=False)
    allows_posting = db.Column(db.Boolean, default=True, nullable=False)
    gl_description = db.Column(db.String(500), default="", nullable=True)

    # Denormalized ancestor path for fast querying without recursive joins.
    # level_0_account_id: FK to direct parent (a level-1 account); null for level-1 and level-2 accounts.
    # level_1_account_id: FK to level-2 grandparent for level-0, or level-2 parent for level-1; null for level-2 accounts.
    level_0_account_id = db.Column(
        db.String(36), db.ForeignKey("accounts.id"), nullable=True
    )
    level_1_account_id = db.Column(
        db.String(36), db.ForeignKey("accounts.id"), nullable=True
    )

    level_0_account = db.relationship(
        "Account",
        foreign_keys=[level_0_account_id],
        primaryjoin="Account.level_0_account_id == Account.id",
        remote_side="Account.id",
    )
    level_1_account = db.relationship(
        "Account",
        foreign_keys=[level_1_account_id],
        primaryjoin="Account.level_1_account_id == Account.id",
        remote_side="Account.id",
    )

    transaction_lines = db.relationship("TransactionLine", back_populates="account")
    vendor_mappings = db.relationship("VendorMapping", back_populates="account")
    keyword_mappings = db.relationship("KeywordMapping", back_populates="account")

    def __repr__(self):
        return f"<Account {self.code} {self.name}>"
