from app.extensions import db
from app.models.account import Account, ACCOUNT_TYPES
from app.models.transaction import TransactionLine

TYPE_RANGES = {
    "asset":     (1000, 1999),
    "liability": (2000, 2999),
    "equity":    (3000, 3999),
    "income":    (4000, 4999),
    "expense":   (5000, 5999),
}

TYPE_ORDER = ["asset", "liability", "equity", "income", "expense"]

TYPE_LABELS = {
    "asset":     "Assets",
    "liability": "Liabilities",
    "equity":    "Equity",
    "income":    "Income",
    "expense":   "Expenses",
}

TYPE_COLORS = {
    "asset":     "blue",
    "liability": "red",
    "equity":    "purple",
    "income":    "green",
    "expense":   "amber",
}


def get_accounts_grouped() -> dict:
    accounts = db.session.execute(
        db.select(Account).order_by(Account.code)
    ).scalars().all()
    grouped = {t: [] for t in TYPE_ORDER}
    for account in accounts:
        if account.type in grouped:
            grouped[account.type].append(account)
    return grouped


def get_next_code(account_type: str) -> str:
    low, high = TYPE_RANGES[account_type]
    rows = db.session.execute(
        db.select(Account.code).where(Account.type == account_type)
    ).scalars().all()
    int_codes = []
    for code in rows:
        try:
            n = int(code)
            if low <= n <= high:
                int_codes.append(n)
        except ValueError:
            pass
    if not int_codes:
        return str(low)
    return str(min(max(int_codes) + 10, high))


def get_next_codes_all() -> dict:
    return {t: get_next_code(t) for t in ACCOUNT_TYPES}


def has_transactions(account_id: str) -> bool:
    count = db.session.execute(
        db.select(db.func.count(TransactionLine.id))
        .where(TransactionLine.account_id == account_id)
    ).scalar()
    return (count or 0) > 0


def create_account(name: str, account_type: str, code: str, description: str) -> Account:
    account = Account(
        name=name.strip(),
        type=account_type,
        code=code.strip(),
        description=description.strip(),
    )
    db.session.add(account)
    db.session.commit()
    return account


def update_account(account: Account, name: str, code: str, description: str,
                   account_type: str | None = None) -> None:
    account.name = name.strip()
    account.code = code.strip()
    account.description = description.strip()
    if account_type and account_type in ACCOUNT_TYPES:
        account.type = account_type
    db.session.commit()


def toggle_active(account: Account) -> None:
    account.is_active = not account.is_active
    db.session.commit()


def get_accounts_with_transactions() -> set:
    rows = db.session.execute(
        db.select(TransactionLine.account_id).distinct()
    ).scalars().all()
    return set(rows)


def delete_account(account: Account) -> None:
    db.session.delete(account)
    db.session.commit()
