# DEBUG: Resolved Issues

## PostgreSQL auth failure (`flask db upgrade`)
**Cause:** Wrong port (5432 instead of 5433) or mismatched password in `DATABASE_URL`.  
**Fix:** Use `postgresql://postgres:WatermarkD21@127.0.0.1:5433/accsoft_dev`. Reset password if needed via pgAdmin Query Tool: `ALTER USER postgres WITH PASSWORD 'newpassword';`

---

## Session 2 — Accounts nav link missing / 404 on `/accounts/`
**Cause:** Stale Flask process from a previous session still serving the old app on port 5000.  
**Fix:** Restart computer to kill zombie processes, then reactivate venv and run `flask run` fresh.
