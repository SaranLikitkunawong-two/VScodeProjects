"""Suggest GL accounts from vendor name and description text."""
from app.models.vendor_mapping import VendorMapping
from app.models.keyword_mapping import KeywordMapping
from app.models.account import Account


def suggest(vendor: str, description: str = "") -> dict:
    """
    Returns:
        {
            "debit_account_id":  str | None,
            "credit_account_id": str | None,
            "source":            "vendor" | "keyword" | "none",
            "vendor_known":      bool,
        }
    """
    result = {
        "debit_account_id": None,
        "credit_account_id": None,
        "source": "none",
        "vendor_known": False,
    }

    # 1. Exact vendor name lookup
    if vendor:
        mapping = VendorMapping.query.filter(
            VendorMapping.vendor_name.ilike(vendor.strip())
        ).first()
        if mapping:
            result["debit_account_id"] = mapping.default_account_id
            result["source"] = "vendor"
            result["vendor_known"] = True
            result["credit_account_id"] = _default_ap_account_id()
            return result

    # 2. Keyword scan on description (highest priority keyword wins)
    search_text = f"{vendor} {description}".lower()
    mappings = (
        KeywordMapping.query
        .order_by(KeywordMapping.priority.desc())
        .all()
    )
    for km in mappings:
        if km.keyword.lower() in search_text:
            result["debit_account_id"] = km.account_id
            result["source"] = "keyword"
            result["credit_account_id"] = _default_ap_account_id()
            return result

    return result


def _default_ap_account_id() -> str | None:
    """Return the first active Accounts Payable account."""
    ap = (
        Account.query
        .filter(
            Account.is_active.is_(True),
            Account.name.ilike("%accounts payable%"),
        )
        .first()
    )
    return ap.id if ap else None


def save_vendor_mapping(vendor: str, account_id: str) -> None:
    """Upsert a vendor → GL account mapping."""
    from app.extensions import db
    mapping = VendorMapping.query.filter(
        VendorMapping.vendor_name.ilike(vendor.strip())
    ).first()
    if mapping:
        mapping.default_account_id = account_id
    else:
        mapping = VendorMapping(
            vendor_name=vendor.strip(),
            default_account_id=account_id,
        )
        db.session.add(mapping)
    db.session.commit()
