import uuid
from app.extensions import db


class KeywordMapping(db.Model):
    __tablename__ = "keyword_mappings"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    keyword = db.Column(db.String(100), unique=True, nullable=False)
    account_id = db.Column(db.String(36), db.ForeignKey("accounts.id"), nullable=False)
    priority = db.Column(db.Integer, default=0, nullable=False)

    account = db.relationship("Account", back_populates="keyword_mappings")
