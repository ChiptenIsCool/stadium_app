# ─────────────────────────────────────────────────────────────────────────────
# backend/data_layer.py — Database access layer
#
# ARCHITECTURAL BOUNDARY RULE (from SPECS/TECH.md):
#   This is the ONLY file in the project that may import sqlite3 or write SQL.
#   backend/app.py calls these functions. It never touches the database.
#
#   Every query that uses user input MUST use a parameterised placeholder (?).
#   Never build SQL with string formatting like f"...={gate}". That opens the
#   door to SQL injection attacks.
# ─────────────────────────────────────────────────────────────────────────────
import sqlite3
import os

# Path to the database file — one level up from this backend/ folder.
DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'stadium.db'
)


# ─── get_db_connection() ──────────────────────────────────────────────────────
# Opens and returns a connection to stadium.db.
#
# conn.row_factory = sqlite3.Row lets each returned row behave like a
# dictionary, so you can access columns by name (row['name']) instead of by
# index (row[2]).
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ─── get_all_entries() ────────────────────────────────────────────────────────
# Retrieves every entry from stadium_entries, joined with the person's name,
# newest (latest hour) first.
#
# Returns: a list of plain Python dicts, one per entry row. Each dict has
#   { id, person_id, name, gate, hour, bag }
#
# The JOIN pulls the matching person's name from the people table so the
# dashboard can show who entered rather than a bare ID.
def get_all_entries():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT
            e.id,
            e.person_id,
            p.name,
            e.gate,
            e.hour,
            e.bag
        FROM stadium_entries e
        JOIN people p ON p.id = e.person_id
        ORDER BY e.hour DESC, e.id DESC
        '''
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


# ─── get_entries_by_gate(gate) ────────────────────────────────────────────────
# Retrieves only the entries where the gate matches the given value.
#
# Parameters:
#   gate — string, e.g. "A", "B", "C", or "D"
#
# SECURITY: the gate value is passed as a query parameter (the ? placeholder),
# NOT interpolated into the SQL string.
def get_entries_by_gate(gate):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT
            e.id,
            e.person_id,
            p.name,
            e.gate,
            e.hour,
            e.bag
        FROM stadium_entries e
        JOIN people p ON p.id = e.person_id
        WHERE e.gate = ?
        ORDER BY e.hour DESC, e.id DESC
        ''',
        (gate,)
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
