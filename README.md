# 🏢 LeaseGuard — Knowledge Graph Lease Intelligence

> Ontology-driven, graph-grounded AI for commercial lease management.  
> **100% free & open-source stack.** No paid cloud database. No paid LLM required.

---

## What It Does

LeaseGuard ingests commercial lease PDFs, extracts every entity (property, tenant, clause, rent schedule, renewal option) using NLP + LLM, stores them as an ontology-aligned knowledge graph in **Neo4j**, and answers business questions through a **Graph-RAG pipeline** — where every answer is traced back to specific graph nodes rather than re-reading raw text.

**Five capabilities:**
1. **Ingest** — PDF → spaCy NER → LLM structured extraction → Neo4j graph
2. **Ask AI** — natural language Q&A, graph-grounded answers with citations
3. **Risk Dashboard** — lease expiration timeline, tenant concentration, high-risk clauses
4. **Graph Explorer** — interactive force-directed visualization of the Neo4j graph
5. **Export** — CSV / JSON export of all lease data

---

## Tech Stack (All Free)

| Layer | Technology | Cost |
|-------|-----------|------|
| Graph DB | Neo4j Community Edition 5.x | Free |
| Vector Store | ChromaDB (local file) | Free |
| LLM (cloud) | Groq API — Llama 3.1 70B | Free (14,400 req/day) |
| LLM (local) | Ollama — Mistral / Llama 3.2 | Free (unlimited) |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | Free |
| PDF parsing | pdfplumber + PyMuPDF | Free |
| NLP / NER | spaCy 3.7 + en_core_web_sm | Free |
| API | FastAPI + Uvicorn | Free |
| UI | Streamlit | Free |
| IDE | Cursor (free tier) / VS Code | Free |

---

## Quick Start (10 Steps)

```bash
# 1. Clone / unzip the project
cd leaseguard

# 2. Create Python virtual environment
python -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Download spaCy English model
python -m spacy download en_core_web_sm

# 5. Install Neo4j Community Edition
#    → https://neo4j.com/download-center/#community
#    Start Neo4j, open http://localhost:7474
#    Default login: neo4j / neo4j  →  change password to: leaseguard123

# 6. Install Ollama (local LLM) OR get a free Groq key
#    Ollama:  https://ollama.com  →  ollama pull mistral
#    Groq:    https://console.groq.com  →  free API key

# 7. Configure environment
cp .env.example .env
# Edit .env — set your LLM_PROVIDER and credentials

# 8. Set up Neo4j schema (run once)
python -m leaseguard.graph.setup_schema

# 9. Generate 25 synthetic test leases
python -m leaseguard.ingestion.lease_generator

# 10. Launch the UI
streamlit run ui/app.py
# Open http://localhost:8501
```

---

## Running the API (Optional)

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
# Swagger docs: http://localhost:8000/docs
```

**Endpoints:**
- `POST /api/ingest` — upload and process a lease PDF
- `GET  /api/leases` — list all leases in the graph
- `GET  /api/expiring?days=90` — leases expiring soon
- `GET  /api/concentration` — tenant concentration risk
- `GET  /api/clauses` — all high-risk clauses
- `POST /api/ask` — `{"question": "..."}` → graph-grounded answer
- `GET  /api/risk/{lease_id}` — AI risk summary for one lease

---

## Running Tests

```bash
# Unit tests (no Neo4j or LLM needed)
pytest tests/ -v

# Integration tests (requires running Neo4j)
SKIP_NEO4J_TESTS=false pytest tests/test_graph.py -v

# Coverage report
pytest --cov=leaseguard --cov-report=html
open htmlcov/index.html
```

---

## Project Structure

```
leaseguard/
├── leaseguard/
│   ├── ingestion/          # L1 — PDF extraction, NER, entity resolution
│   ├── llm/                # L2 — LLM client, prompts, structured extraction
│   ├── graph/              # L3 — Neo4j client, schema, writer, queries
│   ├── intelligence/       # L4 — embeddings, vector store, Graph-RAG
│   └── agents/             # L5 — orchestration agents
├── api/                    # FastAPI REST endpoints
├── ui/                     # Streamlit web application
├── tests/                  # pytest unit + integration tests
├── ontology/               # OWL 2 ontology (edit in Protégé)
├── data/sample_leases/     # Generated test PDFs go here
└── scripts/                # Utility scripts
```

---

## Architecture

```
PDF Upload
    ↓
L1  pdf_extractor  →  entity_extractor  →  entity_resolver
    ↓
L2  extractor_llm  →  llm_client  (Groq / Ollama / Gemini)
    ↓
L3  graph_writer   →  Neo4j Community  (Property→Lease→Tenant→Clause)
    ↓
L4  embedder  →  ChromaDB vector store
    graph_rag  =  Cypher query + vector search + LLM grounded answer
    ↓
L5  LeaseAgent  →  FastAPI REST  +  Streamlit UI
```

---

## License

MIT — free to use, modify, and extend.
