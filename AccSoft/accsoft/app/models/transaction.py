import uuid
from datetime import datetime, timezone
from app.extensions import db


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    customer_id = db.Column(db.String(36), db.ForeignKey("customers.id"), nullable=True)
    supplier_id = db.Column(db.String(36), db.ForeignKey("suppliers.id"), nullable=True)

    lines = db.relationship("TransactionLine", back_populates="transaction", cascade="all, delete-orphan")
    attachments = db.relationship("Attachment", back_populates="transaction", cascade="all, delete-orphan")
    customer = db.relationship("Customer", back_populates="transactions")
    supplier = db.relationship("Supplier", back_populates="transactions")

    def __repr__(self):
        return f"<Transaction {self.date} {self.description}>"


class TransactionLine(db.Model):
    __tablename__ = "transaction_lines"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    transaction_id = db.Column(db.String(36), db.ForeignKey("transactions.id"), nullable=False)
    account_id = db.Column(db.String(36), db.ForeignKey("accounts.id"), nullable=False)
    type = db.Column(db.Enum("debit", "credit", name="line_type"), nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)

    transaction = db.relationship("Transaction", back_populates="lines")
    account = db.relationship("Account", back_populates="transaction_lines")
