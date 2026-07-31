# LeaseGuard — React + Material UI Frontend

A React single-page app built with [Material UI (MUI) v6](https://mui.com) that mirrors
the Streamlit UI, talking to the existing FastAPI backend (`api/main.py`).

This is the **second theme/frontend** — the original is the Streamlit app (`ui/app.py`);
this one is the Material UI rebuild. It additionally ships a built-in **light/dark theme
toggle** (top-right of the app bar).

## Prerequisites

1. **Backend running** on port 8000:
   ```powershell
   # from c:\CBRE_Ontology
   uvicorn api.main:app --reload --port 8000
   ```
   (Needs Neo4j on `localhost:7687`, same as the Streamlit app.)

2. **Node.js** (v18+; tested on v24).

## Run (development)

```powershell
cd frontend
npm install      # first time only
npm run dev
```

Open **http://localhost:5173**. Vite proxies `/api/*` → `http://localhost:8000`, so no
CORS setup is needed.

## Build (production)

```powershell
npm run build     # outputs to frontend/dist
npm run preview   # serve the built bundle locally
```

## What maps to what

| Streamlit tab          | React component            | Backend endpoint(s)                            |
|------------------------|----------------------------|------------------------------------------------|
| Sidebar stats + health | `components/Sidebar.jsx`   | `GET /api/health`, `GET /api/summary`          |
| 📄 Ingest Leases       | `tabs/IngestTab.jsx`       | `POST /api/ingest`                             |
| 💬 Ask AI              | `tabs/AskTab.jsx`          | `POST /api/ask`                               |
| ⚠️ Risk Dashboard      | `tabs/RiskTab.jsx`         | `/api/expiring`, `/api/concentration`, `/api/clauses`, `/api/risk/portfolio/report` |
| 🔗 Knowledge Graph     | `tabs/GraphTab.jsx`        | `GET /api/graph`                              |
| 📊 Export              | `tabs/ExportTab.jsx`       | `GET /api/leases`, `GET /api/summary`         |

## Stack

React 18 · Vite 6 · MUI 6 · MUI X DataGrid · Recharts · react-force-graph-2d · axios
