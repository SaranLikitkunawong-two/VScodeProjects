"""
Run once after `flask db upgrade` to create the first user and seed starter accounts.
Usage: python seed.py
"""
import os
from dotenv import load_dotenv

load_dotenv()

from app import create_app
from app.extensions import db
from app.models import User, Account

STARTER_ACCOUNTS = [
    ("1000", "Bank Account",        "asset"),
    ("1100", "Accounts Receivable", "asset"),
    ("2000", "Accounts Payable",    "liability"),
    ("2100", "GST / Tax Payable",   "liability"),
    ("3000", "Owner's Equity",      "equity"),
    ("3100", "Retained Earnings",   "equity"),
    ("4000", "Service Revenue",     "income"),
    ("5000", "General Expenses",    "expense"),
    ("5100", "Office Expenses",     "expense"),
    ("5200", "Professional Fees",   "expense"),
    ("5300", "Travel & Transport",  "expense"),
]


def seed():
    app = create_app()
    with app.app_context():
        email = os.environ["SEED_EMAIL"]
        password = os.environ["SEED_PASSWORD"]

        if not db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none():
            user = User(email=email)
            user.set_password(password)
            db.session.add(user)
            print(f"Created user: {email}")
        else:
            print(f"User already exists: {email}")

        for code, name, acct_type in STARTER_ACCOUNTS:
            if not db.session.execute(db.select(Account).where(Account.code == code)).scalar_one_or_none():
                db.session.add(Account(code=code, name=name, type=acct_type))
                print(f"  Added account {code} {name}")
            else:
                print(f"  Account {code} already exists")

        db.session.commit()
        print("Seed complete.")


if __name__ == "__main__":
    seed()
