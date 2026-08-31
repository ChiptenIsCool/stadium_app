# Feature Spec: Display Stadium Entries from Persistent Storage

Date: 2026-08-31

## Why this feature exists

Detectives must be able to review stadium entry logs when investigating an
incident. Entry records are evidence. Evidence must survive server crashes and
restarts. This feature is the first step toward that: it moves entry data into
persistent SQLite storage and surfaces it in the dashboard.

The quote that drives us:

> "We got lucky this time. But what happens when we don't? We cannot afford to
> lose evidence every time a server hiccups." — Reyes

## Scope (in)

- Display stadium entries in the dashboard as a table.
- Read entries from a persistent SQLite database (`stadium.db`).
- Provide a Flask backend endpoint `GET /api/entries` that returns entries as JSON.
- Keep all SQL inside a dedicated data layer (`backend/data_layer.py`).
- Allow optional filtering by gate via a query parameter (`?gate=A`).
- Frontend loads and renders entries on page load and on refresh.

## Scope (out)

- Writing / adding new entries (a later feature).
- Backups, export, or recovery tooling (a later feature).
- Real-time gate feeds and alerts (later roadmap phases).
- Authentication and roles.

## Context / decisions

- **Persistence over in-memory**: The repo's feature-spec skill default leans
  toward in-memory data, but the mission explicitly requires that evidence
  survives server crashes. SQLite stores data on disk, so it survives restarts.
  This is the whole point of the feature, so the default is overridden here.
- **Architectural boundaries** (from SPECS/TECH.md) are non-negotiable:
  - Frontend renders and issues HTTP requests only — zero SQL knowledge.
  - Backend handles HTTP routing only — no `sqlite3` import, no raw SQL.
  - Data layer is the single place that touches the database.
- **Parameterized queries only**: user input (e.g. the gate filter) must go
  through `?` placeholders to prevent SQL injection.
- **Beginner-friendly**: keep the code simple and well-commented. The students
  are still learning basic Python, Flask, and JavaScript.

## Non-negotiables

- The data layer is the only module allowed to `import sqlite3` or write SQL.
- All user input is bound via parameterized placeholders, never string
  interpolation.
- Entries are rendered from `stadium.db`, not from a mocked in-memory list.
