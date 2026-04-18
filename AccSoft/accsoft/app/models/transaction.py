import uuid
from datetime import datetime, timezone
from app.extensions import db


TRANSACTION_KINDS = (
    "manual_journal",
    "customer_invoice",
    "supplier_bill",
    "customer_credit_note",
    "supplier_credit_note",
)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    kind = db.Column(
        db.Enum(*TRANSACTION_KINDS, name="transaction_kind"),
        nullable=False,
        default="manual_journal",
        server_default="manual_journal",
    )
    related_transaction_id = db.Column(
        db.String(36), db.ForeignKey("transactions.id"), nullable=True
    )

    customer_id = db.Column(db.String(36), db.ForeignKey("customers.id"), nullable=True)
    supplier_id = db.Column(db.String(36), db.ForeignKey("suppliers.id"), nullable=True)

    lines = db.relationship("TransactionLine", back_populates="transaction", cascade="all, delete-orphan")
    attachments = db.relationship("Attachment", back_populates="transaction", cascade="all, delete-orphan")
    customer = db.relationship("Customer", back_populates="transactions")
    supplier = db.relationship("Supplier", back_populates="transactions")

    related_transaction = db.relationship(
        "Transaction", remote_side=[id], foreign_keys=[related_transaction_id],
        backref="credit_notes",
    )

    def __repr__(self):
        return f"<Transaction {self.kind} {self.date} {self.description}>"

    @property
    def kind_label(self) -> str:
        return {
            "manual_journal": "Manual Journal",
            "customer_invoice": "Customer Invoice",
            "supplier_bill": "Supplier Bill",
            "customer_credit_note": "Customer Credit Note",
            "supplier_credit_note": "Supplier Credit Note",
        }.get(self.kind, self.kind)

    @property
    def is_credit_note(self) -> bool:
        return self.kind in ("customer_credit_note", "supplier_credit_note")

    @property
    def is_invoice_like(self) -> bool:
        return self.kind in ("customer_invoice", "supplier_bill")


class TransactionLine(db.Model):
    __tablename__ = "transaction_lines"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = db.Column(db.String(36), db.ForeignKey("transactions.id"), nullable=False)
    account_id = db.Column(db.String(36), db.ForeignKey("accounts.id"), nullable=False)
    type = db.Column(db.Enum("debit", "credit", name="line_type"), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)

    transaction = db.relationship("Transaction", back_populates="lines")
    account = db.relationship("Account", back_populates="transaction_lines")
