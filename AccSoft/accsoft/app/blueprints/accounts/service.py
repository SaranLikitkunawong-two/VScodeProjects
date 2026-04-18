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

    result = {}
    for t in TYPE_ORDER:
        type_accts = [a for a in accounts if a.type == t]
        level2 = [a for a in type_accts if a.hierarchy == 2]
        level1 = [a for a in type_accts if a.hierarchy == 1]
        level0 = [a for a in type_accts if a.hierarchy == 0]

        parented_l1_ids: set[str] = set()
        parented_l0_ids: set[str] = set()

        l2_nodes = []
        for l2 in level2:
            l1_children = [a for a in level1 if a.level_1_account_id == l2.id]
            l1_nodes = []
            for l1 in l1_children:
                parented_l1_ids.add(l1.id)
                l0_kids = [a for a in level0 if a.level_0_account_id == l1.id]
                parented_l0_ids.update(a.id for a in l0_kids)
                l1_nodes.append({"account": l1, "children": l0_kids})
            direct_l0 = [
                a for a in level0
                if a.level_0_account_id is None and a.level_1_account_id == l2.id
            ]
            parented_l0_ids.update(a.id for a in direct_l0)
            l2_nodes.append({"account": l2, "level1": l1_nodes, "direct_level0": direct_l0})

        orphan_l1 = []
        for l1 in level1:
            if l1.id not in parented_l1_ids:
                l0_kids = [a for a in level0 if a.level_0_account_id == l1.id]
                parented_l0_ids.update(a.id for a in l0_kids)
                orphan_l1.append({"account": l1, "children": l0_kids})

        orphan_l0 = [a for a in level0 if a.id not in parented_l0_ids]

        result[t] = {
            "level2":        l2_nodes,
            "orphan_level1": orphan_l1,
            "orphan_level0": orphan_l0,
            "count":         len(type_accts),
        }

    return result


def get_parent_accounts_for_js() -> dict:
    """JSON-serialisable dict for the sidebar parent dropdowns."""
    accounts = db.session.execute(
        db.select(Account)
        .where(Account.hierarchy.in_([1, 2]))
        .order_by(Account.code)
    ).scalars().all()
    result = {t: {"1": [], "2": []} for t in TYPE_ORDER}
    for a in accounts:
        if a.type in result:
            key = str(a.hierarchy)
            result[a.type][key].append({
                "id":                  a.id,
                "code":                a.code,
                "name":                a.name,
                "level_1_account_id":  a.level_1_account_id or "",
            })
    return result


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


def create_account(
    name: str,
    account_type: str,
    code: str,
    description: str,
    hierarchy: int = 0,
    allows_posting: bool = True,
    level_0_account_id: str | None = None,
    level_1_account_id: str | None = None,
    gl_description: str = "",
) -> Account:
    account = Account(
        name=name.strip(),
        type=account_type,
        code=code.strip(),
        description=description.strip(),
        hierarchy=hierarchy,
        allows_posting=allows_posting,
        level_0_account_id=level_0_account_id or None,
        level_1_account_id=level_1_account_id or None,
        gl_description=gl_description.strip(),
    )
    db.session.add(account)
    db.session.commit()
    return account


def update_account(
    account: Account,
    name: str,
    code: str,
    description: str,
    account_type: str | None = None,
    hierarchy: int | None = None,
    allows_posting: bool | None = None,
    level_0_account_id: str | None = None,
    level_1_account_id: str | None = None,
    gl_description: str | None = None,
) -> None:
    account.name = name.strip()
    account.code = code.strip()
    account.description = description.strip()
    if account_type and account_type in ACCOUNT_TYPES:
        account.type = account_type
    if hierarchy is not None:
        account.hierarchy = hierarchy
    if allows_posting is not None:
        account.allows_posting = allows_posting
    account.level_0_account_id = level_0_account_id or None
    account.level_1_account_id = level_1_account_id or None
    if gl_description is not None:
        account.gl_description = gl_description.strip()
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
