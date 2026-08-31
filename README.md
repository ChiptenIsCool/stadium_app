# Stadium Security Dashboard

A web dashboard that helps detectives review stadium entry logs — built so
that entry evidence **survives server crashes**.

> "We got lucky this time. But what happens when we don't? We cannot afford to
> lose evidence every time a server hiccups." — Reyes

## What it does

- Displays stadium entry records in a table (name, gate, hour, bag).
- Lets you filter entries by gate (A–D).
- Keeps all data in a persistent SQLite database (`stadium.db`), so records
  are not lost when the server restarts.
- Keeps the layers clean: the frontend never touches SQL, and the backend
  never writes queries — all database work lives in one file.

## Project structure

```
SPECS/                    Project constitution and feature specs
  TECH.md                 Architecture & technical boundaries
  ROADMAP.md             Planned milestones
  2026-08-31-…/          Feature spec: display entries from storage
backend/
  app.py                 Flask routes (HTTP only — no SQL)
  data_layer.py          All SQLite queries live here
frontend/
  index.html             Dashboard page
  app.js                 Fetches and renders entries
stadium.db               SQLite database (seeded with championship-game data)
seed.sql                 Re-seeds stadium.db from scratch
run.sh                   Starts the backend on port 5000
```

## Getting started

### 1. Install requirements

```bash
pip install flask
```

### 2. (Re)seed the database

The `stadium.db` file ships with data. To reset it to the seeded
championship-game records:

```bash
sqlite3 stadium.db < seed.sql
```

### 3. Run the server

```bash
./run.sh
```

The server starts on port **5000**. Open the Codio preview for port 5000
(or `http://localhost:5000` locally) to see the dashboard.

### 4. Use the dashboard

- The table loads automatically on page open.
- Use the **gate filter** dropdown and **Refresh** button to filter entries.
- The status badge shows whether the backend is connected.

## Architecture rules (see SPECS/TECH.md)

1. **Frontend** — renders the UI and makes HTTP requests only. Zero SQL.
2. **Backend** — handles HTTP routing only. No `sqlite3` import, no SQL.
3. **Data layer** — the single place that talks to the database.
4. **Database** — on-disk SQLite (`stadium.db`), persistent across restarts.

All user input is passed through parameterized placeholders in the data layer
to prevent SQL injection.

## Tests

Run the data layer check to confirm it reads from SQLite and returns rows:

```bash
python3 -c "import sys; sys.path.insert(0,'backend'); import data_layer; print(len(data_layer.get_all_entries()), 'entries')"
```

## Where to look next

- **Constitution:** `SPECS/TECH.md`, `SPECS/ROADMAP.md`
- **Current feature spec:** `SPECS/2026-08-31-stadium-entries/`
