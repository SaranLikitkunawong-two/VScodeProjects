import uuid
from datetime import datetime, timezone
from app.extensions import db

RECON_STATUSES = ("open", "in_review", "complete", "reopened")


class BankStatement(db.Model):
    __tablename__ = "bank_statements"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = db.Column(db.String(36), db.ForeignKey("accounts.id"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    imported_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    statement_date = db.Column(db.Date, nullable=True)

    account = db.relationship("Account")
    lines = db.relationship(
        "BankStatementLine", back_populates="statement", cascade="all, delete-orphan"
    )


class BankStatementLine(db.Model):
    __tablename__ = "bank_statement_lines"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    bank_statement_id = db.Column(
        db.String(36), db.ForeignKey("bank_statements.id"), nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    reference = db.Column(db.String(200), nullable=True)
    balance = db.Column(db.Numeric(12, 2), nullable=True)
    external_id = db.Column(db.String(200), nullable=True)
    is_matched = db.Column(db.Boolean, default=False, nullable=False)

    statement = db.relationship("BankStatement", back_populates="lines")
    matches = db.relationship(
        "ReconciliationMatch", back_populates="bank_line", cascade="all, delete-orphan"
    )


class ReconciliationSession(db.Model):
    __tablename__ = "reconciliation_sessions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    account_id = db.Column(db.String(36), db.ForeignKey("accounts.id"), nullable=False)
    bank_statement_id = db.Column(
        db.String(36), db.ForeignKey("bank_statements.id"), nullable=False
    )
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    status = db.Column(
        db.Enum(*RECON_STATUSES, name="recon_status"), default="open", nullable=False
    )
    opening_balance = db.Column(db.Numeric(12, 2), nullable=False, default=0)
    closing_balance = db.Column(db.Numeric(12, 2), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)

    account = db.relationship("Account")
    bank_statement = db.relationship("BankStatement")
    matches = db.relationship(
        "ReconciliationMatch", back_populates="session", cascade="all, delete-orphan"
    )


class ReconciliationMatch(db.Model):
    __tablename__ = "reconciliation_matches"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(
        db.String(36), db.ForeignKey("reconciliation_sessions.id"), nullable=False
    )
    bank_statement_line_id = db.Column(
        db.String(36), db.ForeignKey("bank_statement_lines.id"), nullable=False
    )
    transaction_id = db.Column(
        db.String(36), db.ForeignKey("transactions.id"), nullable=False
    )
    matched_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    matched_by_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=True)

    session = db.relationship("ReconciliationSession", back_populates="matches")
    bank_line = db.relationship("BankStatementLine", back_populates="matches")
    transaction = db.relationship("Transaction")
    matched_by = db.relationship("User")
