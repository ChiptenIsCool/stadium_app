# ─────────────────────────────────────────────────────────────────────────────
# backend/app.py — Flask API server
#
# ARCHITECTURAL BOUNDARY RULE (from SPECS/TECH.md):
#   This file handles HTTP routing ONLY.
#   It must NEVER import sqlite3 or write SQL queries directly.
#   All database access goes through data_layer.py.
# ─────────────────────────────────────────────────────────────────────────────
import os

from flask import Flask, jsonify, request, send_from_directory

import data_layer

app = Flask(__name__)
FRONTEND_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'frontend'
)


@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)


# ─── GET /api/entries ─────────────────────────────────────────────────────────
# Returns stadium entry records as JSON.
#
# Optional query parameter:
#   ?gate=A — filters results to a single gate (A, B, C, or D)
#
# NOTE: this route contains ZERO SQL. It delegates all database work to
# data_layer. The gate value is handed to the data layer, which binds it as a
# parameter — never into a raw SQL string.
@app.route('/api/entries', methods=['GET'])
def get_entries():
    try:
        gate = request.args.get('gate')
        if gate:
            entries = data_layer.get_entries_by_gate(gate)
        else:
            entries = data_layer.get_all_entries()
        return jsonify(entries)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ─── GET /api/health ─────────────────────────────────────────────────────────
# Simple health check so the frontend can confirm the backend is running.
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


# ─────────────────────────────────────────────────────────────────────────────
# Server entry point
#
# host="0.0.0.0" — required for Codio's preview panel to reach the server.
# port=5000 — matches how run.sh starts the app.
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("Stadium Security Backend starting…")
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
