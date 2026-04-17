import uuid
from datetime import datetime, timezone
from app.extensions import db


class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    contact_person = db.Column(db.String(200), default="")
    email = db.Column(db.String(200), default="")
    phone = db.Column(db.String(50), default="")
    address = db.Column(db.Text, default="")
    abn = db.Column(db.String(20), default="")
    notes = db.Column(db.Text, default="")
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    transactions = db.relationship("Transaction", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier {self.name}>"
