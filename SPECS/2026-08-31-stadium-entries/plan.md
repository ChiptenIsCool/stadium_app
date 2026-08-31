# Plan: Display Stadium Entries from Persistent Storage

Red/Green TDD in mind, though the current code already exists. This plan
documents the tasks to bring the feature fully in line with the spec and
verify it end to end.

## Task Group 1 — Verify data layer reads from SQLite
- [ ] Confirm `backend/data_layer.py` uses `sqlite3` and reads from `stadium.db`.
- [ ] Confirm `get_all_entries()` and `get_entries_by_gate(gate)` both use
      parameterized SQL and return plain dicts.
- [ ] Run a quick check: `python3 -c "import backend.data_layer as d; print(d.get_all_entries()[:2])"`
      (from the repo root).

## Task Group 2 — Verify backend route
- [ ] Confirm `backend/app.py` exposes `GET /api/entries`.
- [ ] Confirm the route delegates to the data layer and never imports `sqlite3`.
- [ ] Confirm `?gate=` filtering is wired and passed through as a parameter.

## Task Group 3 — Verify frontend renders entries
- [ ] Confirm `frontend/index.html` has a table body to render into.
- [ ] Confirm `frontend/app.js` fetches `/api/entries`, renders rows, updates
      the entry count, and toggles the connection badge.
- [ ] Confirm the gate filter and refresh button call `fetchEntries`.

## Task Group 4 — End-to-end smoke test
- [ ] Start the backend (`./run.sh`) and load the dashboard in the browser.
- [ ] Confirm entries from `stadium.db` render in the table.
- [ ] Confirm the connection badge shows "Backend Connected".
- [ ] Confirm gate filtering works (All Gates, A–D).
- [ ] Confirm data persists: stop the server, restart, entries still appear.

## Task Group 5 — Boundary / lint checks
- [ ] Grep that no SQL strings exist outside `backend/data_layer.py`.
- [ ] Confirm no `import sqlite3` outside the data layer.
- [ ] Confirm no lint/test failures if a runner is configured.
