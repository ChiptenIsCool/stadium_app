# Validation: Display Stadium Entries from Persistent Storage

How we know this feature works and can be merged.

## Functional checks

1. **Entries render** — with the backend running, the dashboard shows rows from
   `stadium.db`, not a hard-coded mock list.
2. **API returns JSON** — `GET /api/entries` returns a JSON array of entry
   objects with the expected fields.
3. **Filtering works** — `GET /api/entries?gate=A` returns only Gate A entries;
   "All Gates" returns everything.
4. **Persistence across restarts** — stop the backend and restart it. The same
   entries are still there. This is the core mission requirement.

## Architectural boundary checks

1. **Zero SQL leak** — no raw SQL or `sqlite3` import anywhere except
   `backend/data_layer.py`.
2. **Parameterized queries** — no string interpolation in any SQL.
3. **Frontend is SQL-free** — the frontend only makes HTTP calls and renders.

## Success criteria (merge gate)

- [ ] Dashboard loads entries from `stadium.db`.
- [ ] Data survives a server restart without being lost.
- [ ] Gate filtering returns correct results.
- [ ] All SQL lives in the data layer and uses placeholders.
- [ ] The `backend/app.py` file contains no database code.

If any of these fail, the gap between implementation and spec must be
recorded, fixed, and the spec updated with the user's approval before merge.
