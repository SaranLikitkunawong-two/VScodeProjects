"""Parse raw OCR text into structured invoice fields."""
import re
from datetime import date, datetime
from decimal import Decimal, InvalidOperation


def extract_fields(raw_text: str) -> dict:
    """
    Parse raw text into a structured dict. All values are strings so the
    review form can show them as-is and let the user correct them.
    Returns keys: vendor, invoice_no, invoice_date, total, gst, subtotal, notes.
    """
    if not raw_text:
        return _empty_fields()

    return {
        "vendor":       _find_vendor(raw_text),
        "invoice_no":   _find_invoice_no(raw_text),
        "invoice_date": _find_date(raw_text),
        "subtotal":     _find_subtotal(raw_text),
        "gst":          _find_gst(raw_text),
        "total":        _find_total(raw_text),
        "notes":        "",
    }


def _empty_fields() -> dict:
    return {
        "vendor": "", "invoice_no": "", "invoice_date": "",
        "subtotal": "", "gst": "", "total": "", "notes": "",
    }


# ── vendor ────────────────────────────────────────────────────────────────────

_SKIP_WORDS = {
    "invoice", "tax invoice", "receipt", "statement", "bill", "pty", "ltd",
    "street", "road", "ave", "abn", "acn", "gst", "total", "subtotal",
    "date", "due", "amount", "paid", "page", "phone", "email", "www",
}

def _find_vendor(text: str) -> str:
    # First non-empty line that isn't a skip word is usually the vendor
    for line in text.splitlines():
        clean = line.strip()
        if not clean:
            continue
        if clean.lower() in _SKIP_WORDS:
            continue
        if re.match(r"^\d", clean):   # starts with digit → skip
            continue
        return clean[:120]
    return ""


# ── invoice number ────────────────────────────────────────────────────────────

_INV_NO_RE = re.compile(
    r"(?:invoice\s*(?:no|number|#)[:\s]*|inv[:\s]+|#\s*)([A-Z0-9\-/]+)",
    re.IGNORECASE,
)

def _find_invoice_no(text: str) -> str:
    m = _INV_NO_RE.search(text)
    return m.group(1).strip() if m else ""


# ── date ──────────────────────────────────────────────────────────────────────

_DATE_FORMATS = [
    "%d/%m/%Y", "%d-%m-%Y", "%d %B %Y", "%d %b %Y",
    "%B %d, %Y", "%b %d, %Y", "%Y-%m-%d",
]
_DATE_RE = re.compile(
    r"\b(\d{1,2}[/\-]\d{1,2}[/\-]\d{2,4}"
    r"|\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?"
    r"|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
    r"\s+\d{2,4}"
    r"|\d{4}-\d{2}-\d{2})\b",
    re.IGNORECASE,
)

def _find_date(text: str) -> str:
    for m in _DATE_RE.finditer(text):
        raw = m.group(1).strip()
        for fmt in _DATE_FORMATS:
            try:
                return datetime.strptime(raw, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue
    return ""


# ── amounts ───────────────────────────────────────────────────────────────────

def _find_amount(pattern: re.Pattern, text: str) -> str:
    m = pattern.search(text)
    if not m:
        return ""
    raw = m.group(1).replace(",", "").strip()
    try:
        return str(Decimal(raw.lstrip("$")))
    except InvalidOperation:
        return ""


_TOTAL_RE = re.compile(
    r"(?<!sub)(?<!net\s)(?:total(?:\s+(?:amount|due|payable))?|amount\s+due|balance\s+due)[:\s]*\$?\s*([\d,]+\.?\d*)",
    re.IGNORECASE,
)
_GST_RE = re.compile(
    r"(?:gst|tax)[:\s]*\$?\s*([\d,]+\.?\d*)",
    re.IGNORECASE,
)
_SUBTOTAL_RE = re.compile(
    r"(?:subtotal|sub\s*total|net\s*amount)[:\s]*\$?\s*([\d,]+\.?\d*)",
    re.IGNORECASE,
)


def _find_total(text: str) -> str:
    return _find_amount(_TOTAL_RE, text)


def _find_gst(text: str) -> str:
    return _find_amount(_GST_RE, text)


def _find_subtotal(text: str) -> str:
    return _find_amount(_SUBTOTAL_RE, text)
