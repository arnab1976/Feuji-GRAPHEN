"""Centralised configuration — reads from .env or environment variables."""
from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(override=False)

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT_DIR  = Path(__file__).parent.parent
DATA_DIR  = ROOT_DIR / "data"
LEASE_DIR = DATA_DIR / "sample_leases"

# ── Neo4j ─────────────────────────────────────────────────────────────────────
NEO4J_URI      = os.getenv("NEO4J_URI",      "bolt://localhost:7687")
NEO4J_USER     = os.getenv("NEO4J_USER",     "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "leaseguard123")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE", "neo4j")

# ── LLM ───────────────────────────────────────────────────────────────────────
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL   = os.getenv("GROQ_MODEL",   "llama-3.1-70b-versatile")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL",    "mistral")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL",   "gemini-1.5-flash")

OPENAI_API_KEY  = os.getenv("OPENAI_API_KEY",  "")
OPENAI_MODEL    = os.getenv("OPENAI_MODEL", os.getenv("LLM_MODEL", "gpt-4o"))
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")  # optional (Azure / proxy)

LLM_TEMPERATURE  = float(os.getenv("LLM_TEMPERATURE", "0.0"))
LLM_MAX_TOKENS   = int(os.getenv("LLM_MAX_TOKENS",    "2048"))
LLM_MAX_RETRIES  = int(os.getenv("LLM_MAX_RETRIES",   "3"))

# ── ChromaDB ─────────────────────────────────────────────────────────────────
CHROMA_DB_PATH   = os.getenv("CHROMA_DB_PATH",   str(DATA_DIR / "chroma_db"))
CHROMA_COLLECTION = os.getenv("CHROMA_COLLECTION", "lease_chunks")

# ── Embedding ─────────────────────────────────────────────────────────────────
EMBEDDING_MODEL     = "all-MiniLM-L6-v2"
EMBEDDING_DIMENSION = 384

# ── Text chunking ─────────────────────────────────────────────────────────────
CHUNK_SIZE    = int(os.getenv("CHUNK_SIZE",    "2000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# ── Extraction ────────────────────────────────────────────────────────────────
LLM_EXTRACT_CHARS    = int(os.getenv("LLM_EXTRACT_CHARS",    "6000"))
ENTITY_MATCH_THRESHOLD = float(os.getenv("ENTITY_MATCH_THRESHOLD", "0.85"))

# ── App ───────────────────────────────────────────────────────────────────────
LOG_LEVEL  = os.getenv("LOG_LEVEL", "INFO")
APP_ENV    = os.getenv("APP_ENV",   "development")
API_HOST   = os.getenv("API_HOST",  "0.0.0.0")
API_PORT   = int(os.getenv("API_PORT", "8000"))
API_RELOAD = os.getenv("API_RELOAD", "true").lower() == "true"
