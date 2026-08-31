// ─────────────────────────────────────────────────────────────────────────────
// frontend/app.js — Stadium Security Dashboard
//
// All data comes from the Flask backend via the /api/entries endpoint.
// The frontend NEVER talks to the database directly — it only makes HTTP
// requests and renders what the backend returns (architectural boundary in
// SPECS/TECH.md).
// ─────────────────────────────────────────────────────────────────────────────

// Same origin — the dashboard is served by Flask, so no full URL needed.
const API_BASE = '';


// ─── fetchEntries(gate) ──────────────────────────────────────────────────────
// Sends a GET request to the backend and hands the results to renderTable().
//
// Parameters:
//   gate — string, e.g. "A", "B", "C", "D", or "" for all gates
//
// What it does:
//   1. Builds the URL: /api/entries or /api/entries?gate=A
//   2. Fetches and parses the JSON response
//   3. Renders the entries and updates the count + connection badge
//   4. On error, marks the badge as "Backend Offline"
async function fetchEntries(gate = '') {
  try {
    const url = gate
      ? `${API_BASE}/api/entries?gate=${encodeURIComponent(gate)}`
      : `${API_BASE}/api/entries`;
    const res = await fetch(url);
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const entries = await res.json();
    renderTable(entries);

    document.getElementById('count-value').textContent = entries.length;

    const badge = document.getElementById('status-badge');
    badge.textContent = 'Backend Connected';
    badge.classList.add('connected');
  } catch (err) {
    console.error(err);
    const badge = document.getElementById('status-badge');
    badge.textContent = 'Backend Offline';
    badge.classList.remove('connected');
  }
}


// ─── renderTable(entries) ────────────────────────────────────────────────────
// Clears the table body and renders one <tr> per entry.
//
// Parameters:
//   entries — array of objects from the backend, each with
//             { id, person_id, name, gate, hour, bag }
function renderTable(entries) {
  const body = document.getElementById('entries-body');
  const emptyState = document.getElementById('empty-state');
  body.innerHTML = '';

  if (!entries || entries.length === 0) {
    emptyState.style.display = 'block';
    return;
  }

  emptyState.style.display = 'none';

  entries.forEach(entry => {
    const tr = document.createElement('tr');

    // #        Name                  Gate (badge)  Hour  Bag
    const cells = [entry.id, entry.name, entry.gate, entry.hour, entry.bag];

    cells.forEach((value, i) => {
      const td = document.createElement('td');
      if (i === 2) {
        // Gate column → wrap value in a colour badge
        const badge = document.createElement('span');
        badge.className = `gate-badge gate-${value}`;
        badge.textContent = value;
        td.appendChild(badge);
      } else {
        td.textContent = value;
      }
      tr.appendChild(td);
    });

    body.appendChild(tr);
  });
}


// ─── Event listeners ─────────────────────────────────────────────────────────
// 1. Gate filter dropdown → fetchEntries(selectedValue)
// 2. Refresh button       → fetchEntries(currentFilterValue)
// 3. On page load         → fetchEntries('') to show data immediately
document.addEventListener('DOMContentLoaded', () => {
  const filter = document.getElementById('gate-filter');
  const refresh = document.getElementById('refresh-btn');

  filter.addEventListener('change', () => fetchEntries(filter.value));
  refresh.addEventListener('click', () => fetchEntries(filter.value));

  fetchEntries('');
});
