# Flask Guide for AccSoft

## Purpose
This document defines how Flask should be used in AccSoft so the code stays clean, simple, and maintainable. It favors the built-in Flask patterns that support modularity and testing without introducing unnecessary architectural complexity.[cite:47][cite:56]

## Core philosophy
AccSoft should use Flask as a server-rendered web application framework, not as a thin shell around an overengineered architecture. Flask’s own patterns for application factories, blueprints, configuration handling, error handling, and logging are enough for a clean single-user accounting app when used consistently.[cite:13][cite:47][cite:54][cite:57]

The guiding rule is: use the minimum Flask structure that keeps the project organized. That means modular code, explicit configuration, and thin view functions, but not premature abstractions like service locators, plugin systems, or distributed components.[cite:13][cite:47]

## Use the application factory pattern
Flask recommends the application factory pattern for packaged applications because it allows multiple app instances, cleaner testing, and better extension setup. The factory pattern also helps avoid circular imports because extensions and blueprints are created independently, then bound inside `create_app()`.[cite:47][cite:48]

Recommended pattern:

```python
# app/__init__.py
from flask import Flask
from .config import config_by_name
from .extensions import db, migrate, login_manager

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from .blueprints.auth.routes import auth_bp
    from .blueprints.dashboard.routes import dashboard_bp
    from .blueprints.accounts.routes import accounts_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(accounts_bp, url_prefix="/accounts")

    register_error_handlers(app)
    return app
```

Rules:
- Do not create a global `app = Flask(__name__)` for the main project.[cite:47]
- Create extensions once in `extensions.py`, then initialize them inside the factory.[cite:47][cite:4]
- Keep `create_app()` readable; if setup grows, move parts into helper functions like `register_blueprints()` and `register_error_handlers()`.[cite:4][cite:47]

## Organize by blueprints
Flask blueprints are the right unit of modularity for this project. Flask documentation describes blueprints as the mechanism for application components and common patterns inside larger applications.[cite:56]

For AccSoft, organize by business feature, not by technical layer alone. Good blueprint boundaries are:
- `auth`
- `dashboard`
- `accounts`
- `transactions`
- `attachments`
- `ocr`
- `reconciliation`
- `reports` [cite:1][cite:56]

Rules:
- Each blueprint should own its routes, feature-level forms, and feature-specific service functions.[cite:16][cite:56]
- Use URL prefixes to keep routes clear and avoid conflicts.[cite:16][cite:56]
- Avoid a huge catch-all blueprint called `main` once the app grows beyond a few pages.[cite:16][cite:56]
- Shared models, extensions, and utilities should live outside blueprint folders.[cite:16]

## Keep routes thin
A Flask view function should mostly do four things: read request data, validate it, call business logic, and return a response. This keeps HTTP concerns in the route and domain rules elsewhere, which makes the app easier to test and reason about.[cite:13][cite:16]

Good route responsibilities:
- Parse query params and form fields.[cite:35]
- Handle authorization and user session checks.[cite:26]
- Choose template or redirect target.[cite:13]
- Flash user-facing success or error messages.[cite:13]

Bad route responsibilities:
- Complex accounting logic.
- Multi-step OCR parsing pipelines.
- Directly coordinating several unrelated database writes inline.
- Duplicating money/date normalization in multiple routes.

For AccSoft, anything involving balanced journal entries, GL suggestion logic, reconciliation rules, or OCR review state should move into service functions or dedicated modules.[cite:1]

## Prefer server-rendered HTML
Flask works very well with server-rendered templates, and that matches this project’s simplicity-first goals. Most screens in AccSoft are forms, tables, dashboards, ledgers, and review pages, so Jinja templates plus minimal JavaScript are simpler and more maintainable than a SPA frontend.[cite:1][cite:13]

Rules:
- Use Jinja templates for all primary screens.
- Use JavaScript only where it meaningfully improves UX, such as image preview, drag-and-drop upload, or inline OCR field correction.[cite:1]
- Prefer full-page form flows over dense modal workflows.
- Use `url_for()` for internal links and form actions rather than hardcoded paths.[cite:16]

## Configuration handling
Flask’s configuration system supports environment-driven configuration and loading variables from environment prefixes, which is the safest default for application secrets and deployment settings.[cite:38]

Recommended structure:
- `config.py` with `DevelopmentConfig`, `TestingConfig`, and `ProductionConfig` classes.
- `.env` for local secrets only, never committed.
- `.env.example` committed with placeholder values.
- App config selected by environment variable or explicit `create_app("production")` style startup.[cite:38][cite:47]

Store these in config, not in code:
- `SECRET_KEY`
- `SQLALCHEMY_DATABASE_URI`
- `UPLOAD_FOLDER`
- `MAX_CONTENT_LENGTH`
- session cookie settings
- OCR-related paths or toggles [cite:38]

## Error handling
Flask supports application-level and blueprint-aware error handling, and custom error handlers should be part of the standard setup. Flask’s error handling docs recommend returning different responses for different URL spaces when appropriate, such as HTML for web pages and JSON for APIs.[cite:54]

Recommended rules:
- Register app-level handlers for 404, 403, 405, and 500 errors.[cite:54]
- Return friendly HTML pages for user-facing sections.
- If you later add API endpoints, return JSON errors in that URL space.[cite:54]
- On unhandled write errors, ensure the SQLAlchemy session is rolled back before responding.[cite:4][cite:54]
- Never expose stack traces in production.[cite:54]

A clean pattern is:
- service raises a domain-specific exception
- route or error handler maps it to flash message or status code
- template shows clear user-facing explanation

## Logging
Flask documentation recommends configuring logging before creating the application object if possible, because accessing `app.logger` too early can attach a default handler.[cite:57]

Recommended logging rules:
- Configure Python logging centrally before app creation in production entrypoints.[cite:57]
- Log warnings and errors with enough context to debug request failures.
- Log OCR failures, upload rejections, and unexpected reconciliation mismatches.
- Do not log passwords, raw session cookies, or sensitive document contents.
- Start with file/console logging; only add external monitoring later if needed.[cite:57]

## Testing approach
The application factory pattern makes Flask apps easier to test because tests can create isolated app instances with test-specific configuration. Flask testing guidance and pytest-oriented best practice sources consistently recommend app factories, independent tests, and fixture-based setup.[cite:37][cite:47]

Recommended testing setup:
- Use `pytest`.
- Create an `app` fixture that calls `create_app("testing")`.[cite:37][cite:47]
- Use a separate test database or transaction-isolated test setup.
- Keep tests independent; each test should pass on its own without relying on execution order.[cite:37][cite:46]
- Prioritize edge cases: invalid amounts, missing fields, unbalanced entries, unauthorized access, bad file uploads.[cite:37][cite:46]

Test layers:
- Unit tests for utility functions and service logic.
- Integration tests for request -> route -> DB workflows.
- A few end-to-end tests for the highest-risk paths such as login, create transaction, upload receipt, and OCR confirm.[cite:37][cite:46]

## Form handling and request flow
Flask’s request/response model is simple, and AccSoft should lean into that simplicity. Use standard POST forms for writes, redirect after success, and render templates with errors when validation fails.[cite:25][cite:13]

Recommended pattern:
- GET shows form.
- POST validates input.
- On success: write once, flash success, redirect.
- On failure: re-render form with user input and clear error messages.

This POST-redirect-GET pattern reduces duplicate submissions and keeps browser behavior predictable in server-rendered apps.[cite:13]

## Use Flask-Login simply
Flask-Login is designed to handle user session management, login state, and route protection in Flask applications.[cite:26] For AccSoft’s current scope, use only the simple parts:
- user loader
- `login_user()`
- `logout_user()`
- `@login_required`
- session-based auth [cite:26]

Avoid overcomplicating auth with OAuth, refresh-token systems, or API token layers unless the product scope changes materially.[cite:1][cite:26]

## File upload handling in Flask
Flask’s file upload pattern and OWASP’s upload guidance strongly support a conservative implementation. Flask recommends `secure_filename()` and `MAX_CONTENT_LENGTH`, while OWASP advises strict allowlists, safe storage, and not trusting client input.[cite:18][cite:12]

Recommended Flask-specific rules:
- Use `request.files` only in the route layer, then pass validated file objects to an attachment service.[cite:18]
- Use `secure_filename()` only as a safety aid, not as the final storage naming strategy; generate your own unique server-side filenames.[cite:18][cite:12]
- Set `MAX_CONTENT_LENGTH` in Flask config.[cite:18]
- Reject files that do not match the allowlist before writing them to disk.[cite:12][cite:18]
- Serve protected uploads through authenticated routes, not directly from a public static directory.[cite:12]

## Avoid common Flask pitfalls
- Do not keep everything in one file once the project has multiple features; blueprints exist to avoid that trap.[cite:16][cite:56]
- Do not create circular imports by importing the app object everywhere; use the application factory and extension pattern instead.[cite:47][cite:48]
- Do not mix HTML views and JSON API behavior in the same route unless there is a strong reason.[cite:54]
- Do not put raw SQLAlchemy session handling in every route; centralize conventions and keep transaction boundaries predictable.[cite:4]
- Do not rely on debug mode behavior in production.[cite:38][cite:54]

## Suggested Flask file layout
```text
app/
├── __init__.py
├── config.py
├── extensions.py
├── models/
├── blueprints/
│   ├── auth/
│   ├── dashboard/
│   ├── accounts/
│   ├── transactions/
│   ├── attachments/
│   ├── ocr/
│   ├── reconciliation/
│   └── reports/
├── templates/
├── static/
└── utils/
```

This layout aligns with Flask’s packaged-application patterns and keeps the project modular without adding unnecessary ceremony.[cite:13][cite:47][cite:56]

## Recommended defaults for AccSoft
- Use Flask app factory from day one.[cite:47]
- Use one blueprint per feature area.[cite:56]
- Use Jinja templates and minimal JavaScript.[cite:1]
- Use class-based config and environment variables.[cite:38]
- Use Flask-Login for simple session auth.[cite:26]
- Use central error handlers and logging configuration.[cite:54][cite:57]
- Use pytest with fixtures and isolated app instances.[cite:37][cite:47]

## Final recommendation
For AccSoft, Flask should be used in the most boring professional way possible: application factory, feature-based blueprints, thin routes, server-rendered templates, explicit configuration, central error handling, conservative file uploads, and pytest-backed testing. That combination matches Flask’s own guidance and gives you clean code with minimal framework complexity.[cite:13][cite:47][cite:54][cite:56][cite:57]
