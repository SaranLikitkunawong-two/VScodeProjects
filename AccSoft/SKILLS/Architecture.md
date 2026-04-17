# AccSoft Architecture Guide

## Purpose

Single-user web-based accounting portal for a small service business. Priorities: clarity, correctness, and ease of change — not horizontal scalability. Scope covers login-protected bookkeeping, file attachments, OCR-assisted invoice capture, reconciliation, and reports.

---

## Architectural Principles

- **Modular monolith** — one Flask app, one PostgreSQL database, one codebase. Blueprints and the application factory give clean separation without deployment complexity.
- **Simple request flow** — `route → service → model → database`. Business rules stay in services, not templates or route handlers.
- **Explicit transaction boundaries** — SQLAlchemy session scope ≠ transaction scope. Never leave implicit transactions open.
- **Boring technology** — Flask, SQLAlchemy, PostgreSQL, server-rendered HTML, minimal JS. Complexity is added only when proven necessary.

---

## Project Structure

```
accsoft/
├── app/
│   ├── __init__.py            # create_app()
│   ├── config.py              # Dev/prod/test config classes
│   ├── extensions.py          # db, migrate, login_manager
│   ├── models/
│   │   ├── user.py
│   │   ├── account.py
│   │   ├── transaction.py
│   │   ├── attachment.py
│   │   ├── vendor_mapping.py
│   │   ├── keyword_mapping.py
│   │   └── ocr_result.py
│   ├── blueprints/
│   │   ├── auth/              routes.py, forms.py, service.py
│   │   ├── dashboard/         routes.py
│   │   ├── accounts/          routes.py, service.py
│   │   ├── transactions/      routes.py, service.py
│   │   ├── attachments/       routes.py, service.py
│   │   ├── ocr/               routes.py, service.py, extractor.py, gl_suggester.py
│   │   ├── reconciliation/    routes.py, service.py
│   │   └── reports/           routes.py, service.py
│   ├── templates/
│   ├── static/
│   ├── uploads/               # local dev only — outside web root in production
│   └── utils/
│       ├── money.py
│       ├── dates.py
│       └── validators.py
├── migrations/
├── tests/
├── requirements.txt
├── .env.example
└── run.py
```

---

## Layer Responsibilities

| Layer | Responsibility |
|---|---|
| Routes | Validate input, call a service, render or redirect. No business logic. |
| Services | Business rules: balanced journal entries, account deactivation, OCR posting, reconciliation. |
| Models | Persistence and simple invariants only. Multi-step workflows belong in services. |
| Templates | Render data. No accounting decisions. JS only where it clearly improves UX. |

---

## Flask Patterns

- Use the **application factory** (`create_app()`) so the app can be instantiated with different configs for dev, test, and production.
- Initialize extensions (`db`, `migrate`, `login_manager`) in `extensions.py` and bind them inside `create_app()`.
- One blueprint per feature area: auth, accounts, transactions, attachments, OCR, reconciliation, reports.
- Config is class-based and environment-driven — no secrets in code.

---

## Database

PostgreSQL fits well: the data is relational, transactional, and built around journals, account lines, mappings, and reports.

**Rules:**
- UUID primary keys across all tables.
- Store money as `NUMERIC(12,2)` — never float.
- Enforce balanced journal entries (debits = credits) in service logic before every commit.
- Add DB constraints where practical: non-negative amounts, required FKs, unique account codes, normalised vendor mapping uniqueness.
- One migration per schema change via Flask-Migrate/Alembic — no ad hoc SQL in production.

**Session/transaction scope:**
- One session per request, one explicit `commit()` per successful write workflow.
- Read-only pages must not hold open transactions — keep queries close to rendering.
- Write workflows (e.g. transaction + lines + attachment metadata) complete in a single transaction — all-or-nothing.

---

## Authentication

Flask-Login with email/password. Single-user for now — keep it simple.

- Hash passwords with Werkzeug; never store plaintext.
- Secret key from environment variables only.
- Production cookies: HTTPS-only, appropriate session lifetime (OWASP guidance).
- Every non-auth route protected by `@login_required` until a public page is intentionally added.

---

## File Attachments

Handles invoices, receipts, and photos (PDF, JPG, JPEG, PNG).

- Allowlist extensions and MIME types — reject everything else.
- Set `MAX_CONTENT_LENGTH` to cap upload size.
- Generate server-side filenames; store the original name as metadata only.
- Store files **outside the web root** in production; serve via authenticated app routes.
- Attachment metadata lives in PostgreSQL; file bytes on disk (S3-compatible storage later).

---

## OCR Pipeline

```
Upload file → persist attachment record
        │
        ▼
Digital PDF? ──Yes──▶ pdfplumber (text + tables)
        │                      │
        No                     ▼
        ▼              invoice2data (YAML templates → structured fields)
PaddleOCR (image → text)       │
        │                      ▼
        └─────────────▶ vendor / date / invoice no. / line items / totals
                                │
                                ▼
                       GL Suggestion Engine
                                │
                                ▼
                       User reviews & confirms
                                │
                                ▼
                       Transaction posted to ledger
```

**Library choices:**

| Input | Library | Why |
|---|---|---|
| Digital PDF | pdfplumber | Native text + table extraction; no OCR needed |
| Scanned PDF / image | PaddleOCR (PP-OCRv5) | ~94.5% CPU accuracy, fits 4 GB RAM, Apache 2.0 |
| Field extraction | invoice2data | Built-in invoice parsing via YAML templates |

**OCR is probabilistic; bookkeeping must be deterministic.** Always save the OCR result first, let the user review, then post in a separate explicit commit.

---

## GL Suggestion Engine

Two tiers, in order:

1. **Keyword/vendor rules** — check `vendor_mappings` and `keyword_mappings` tables. Free, instant. User corrections feed back into these tables (self-learning).
2. **Manual fallback** — if no match, flag for manual GL selection; save the result for future invoices from the same vendor.

Claude API (Phase 3, optional): if neither tier matches, send vendor + description to Claude with the chart of accounts and use the suggestion as a pre-fill.

---

## Frontend

Server-rendered HTML + Tailwind CSS + minimal JS. Most screens are forms, lists, ledgers, and review flows — not interactive SPA candidates.

- Full-page forms for transaction entry and OCR review.
- POST-redirect-GET after successful form submissions (prevents duplicate writes on refresh).
- Dashboard is read-only and derived from the database, not client-side state.

---

## Error Handling & Validation

Three layers:

| Layer | Examples |
|---|---|
| Request | Required fields, date format, file presence, allowed extension |
| Service | Balanced debits/credits, account active status, valid reconciliation state |
| Database | Unique account code, FK constraints, non-null columns, constrained enums |

---

## Testing Priorities

The application factory makes isolated test instances trivial. Focus on high-risk accounting rules:

- Balanced transaction succeeds; unbalanced is rejected.
- Account deactivation blocked/allowed by history rules.
- Login/logout and protected routes behave correctly.
- File uploads reject invalid types and oversized files.
- OCR review saves without posting; only posts after user confirmation.

---

## Deployment

Hetzner CX22 VPS — Nginx → Gunicorn → Flask, PostgreSQL, local file storage.

- Never run the Flask dev server in production.
- Secrets in environment variables only; never commit `.env`.
- Back up both PostgreSQL (`pg_dump`) and uploaded files — records are incomplete without attachments.
- Stay on the monolith until OCR or reporting proves to be a bottleneck.
