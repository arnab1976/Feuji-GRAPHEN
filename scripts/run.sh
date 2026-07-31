#!/usr/bin/env bash
# LeaseGuard convenience runner — choose what to start
set -e

COMMAND=${1:-ui}

case "$COMMAND" in
  setup)
    echo "⚙️  Setting up Neo4j schema …"
    python -m leaseguard.graph.setup_schema
    ;;
  demo)
    echo "🏗  Generating 25 synthetic lease PDFs …"
    python -m leaseguard.ingestion.lease_generator --count 25
    ;;
  ui)
    echo "🌐  Starting Streamlit UI on http://localhost:8501 …"
    streamlit run ui/app.py
    ;;
  api)
    echo "🚀  Starting FastAPI on http://localhost:8000 …"
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
    ;;
  test)
    echo "🧪  Running tests …"
    pytest tests/ -v --tb=short
    ;;
  test-all)
    echo "🧪  Running ALL tests (including Neo4j integration) …"
    SKIP_NEO4J_TESTS=false pytest tests/ -v --tb=short
    ;;
  *)
    echo "Usage: ./scripts/run.sh [setup|demo|ui|api|test|test-all]"
    exit 1
    ;;
esac
