"""
LeaseGuard — Streamlit Web Application

Run:
    streamlit run ui/app.py
"""
from __future__ import annotations
import os
import sys
import json
import tempfile

import pandas as pd
import streamlit as st

# Ensure project root is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from leaseguard.agents.lease_agent  import LeaseAgent
from leaseguard.agents.risk_agent   import RiskAgent
from leaseguard.graph.graph_queries import GraphQueries
from leaseguard.graph.neo4j_client  import Neo4jClient

# Individual pipeline stages — used by the guided, step-by-step ingest wizard
from leaseguard.ingestion.pdf_extractor    import PDFExtractor
from leaseguard.ingestion.entity_extractor import EntityExtractor
from leaseguard.ingestion.entity_resolver  import EntityResolver
from leaseguard.llm.extractor_llm          import LLMExtractor
from leaseguard.graph.graph_writer         import GraphWriter
from leaseguard.intelligence.vector_store  import VectorStore

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LeaseGuard",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Cached singletons ────────────────────────────────────────────────────────
@st.cache_resource(show_spinner="Connecting to knowledge graph …")
def get_agent()   -> LeaseAgent:    return LeaseAgent()
@st.cache_resource
def get_risk()    -> RiskAgent:     return RiskAgent()
@st.cache_resource
def get_queries() -> GraphQueries:  return GraphQueries()
@st.cache_resource
def get_neo4j()   -> Neo4jClient:   return Neo4jClient()

# Per-stage singletons for the guided wizard
@st.cache_resource
def get_pdf()     -> PDFExtractor:    return PDFExtractor()
@st.cache_resource(show_spinner="Loading spaCy NER model …")
def get_ner()     -> EntityExtractor: return EntityExtractor()
@st.cache_resource
def get_llm_ext() -> LLMExtractor:    return LLMExtractor()
@st.cache_resource
def get_writer()  -> GraphWriter:     return GraphWriter()
@st.cache_resource
def get_vector()  -> VectorStore:     return VectorStore()


# ════════════════════════════════════════════════════════════════════════════
# GUIDED STEP-BY-STEP INGEST WIZARD
# ════════════════════════════════════════════════════════════════════════════
# Each step runs one pipeline stage, shows its output for human review, and only
# passes that output forward as the next step's input once the user approves.

STEPS = [
    {"key": "pdf",     "title": "PDF Text Extraction",
     "sub": "pdfplumber → raw text + tables",
     "hint": "Input: the uploaded PDF bytes."},
    {"key": "ner",     "title": "Pattern + NER Extraction",
     "sub": "spaCy + regex → dates, $, sqft, org names",
     "hint": "Input: the raw text from Step 1."},
    {"key": "llm",     "title": "LLM Structured Extraction",
     "sub": "Groq Llama-3.1-70B → strict JSON schema",
     "hint": "Input: the raw text from Step 1."},
    {"key": "resolve", "title": "Entity Resolution",
     "sub": "Fuzzy match against existing graph nodes",
     "hint": "Input: the structured JSON from Step 3."},
    {"key": "graph",   "title": "Graph Write (Neo4j MERGE)",
     "sub": "Property → Lease → Tenant → Clause nodes",
     "hint": "Input: the (reviewed) structured JSON from Step 3."},
    {"key": "embed",   "title": "Vector Embedding",
     "sub": "sentence-transformers → ChromaDB chunks",
     "hint": "Input: the raw text (Step 1) + the lease_id (Step 5)."},
]

TRACKER_CSS = """
<style>
.lg-track {display:flex;flex-direction:column;gap:9px;margin:6px 0 4px;}
.lg-step {display:flex;align-items:flex-start;gap:14px;padding:11px 15px;border-radius:12px;
          border:1px solid #1e2a3d;background:#0f1726;}
.lg-step.lg-active {border-color:#4C8DFF;background:#12203a;box-shadow:0 0 0 1px #4C8DFF55;}
.lg-badge {flex:none;width:30px;height:30px;border-radius:50%;display:flex;align-items:center;
           justify-content:center;font-weight:700;font-size:14px;color:#fff;}
.lg-done   .lg-badge {background:#1f8f68;}
.lg-active .lg-badge {background:#4C8DFF;}
.lg-failed .lg-badge {background:#c0384a;}
.lg-pending .lg-badge {background:#2a3648;color:#8091a8;}
.lg-title {font-weight:700;color:#e8edf4;font-size:15px;line-height:1.35;}
.lg-sub {font-family:ui-monospace,SFMono-Regular,Menlo,monospace;color:#7f8da6;font-size:12.5px;}
.lg-pending .lg-title {color:#93a1b5;}
</style>
"""


def render_tracker(statuses: list[str]) -> None:
    rows = []
    for i, (step, status) in enumerate(zip(STEPS, statuses)):
        badge = "✓" if status == "done" else "✕" if status == "failed" else str(i + 1)
        rows.append(
            f'<div class="lg-step lg-{status}"><div class="lg-badge">{badge}</div>'
            f'<div><div class="lg-title">{step["title"]}</div>'
            f'<div class="lg-sub">{step["sub"]}</div></div></div>'
        )
    st.markdown(TRACKER_CSS + '<div class="lg-track">' + "".join(rows) + "</div>",
                unsafe_allow_html=True)


# ── Stage runners: each reads prior outputs from session_state, returns output ──

def _run_pdf() -> dict:
    return get_pdf().extract_from_bytes(
        st.session_state.wiz_file_bytes, st.session_state.wiz_file_name)

def _run_ner() -> dict:
    return get_ner().extract(st.session_state.wiz_out["pdf"]["full_text"])

def _run_llm() -> dict:
    return get_llm_ext().extract(st.session_state.wiz_out["pdf"]["full_text"])

def _run_resolve() -> dict:
    data = st.session_state.wiz_out["llm"]
    r = EntityResolver()
    return {
        "raw_address":       data.get("property_address"),
        "canonical_address": r.canonical_address(data.get("property_address")),
        "raw_tenant":        data.get("tenant_name"),
        "canonical_tenant":  r.canonical_tenant(data.get("tenant_name")),
    }

def _run_graph() -> dict:
    data     = st.session_state.wiz_out["llm"]          # may have been edited in Step 3
    lease_id = get_writer().write_lease(data, source_file=st.session_state.wiz_file_name)
    return {"lease_id": lease_id}

def _run_embed() -> dict:
    text     = st.session_state.wiz_out["pdf"]["full_text"]
    lease_id = st.session_state.wiz_out["graph"]["lease_id"]
    chunks   = get_pdf().chunk_text(text)
    added    = get_vector().add_chunks(chunks, lease_id, st.session_state.wiz_file_name)
    return {"chunk_count": len(chunks), "chunks_added": added}

STEP_FUNCS = {
    "pdf": _run_pdf, "ner": _run_ner, "llm": _run_llm,
    "resolve": _run_resolve, "graph": _run_graph, "embed": _run_embed,
}


def _render_output(key: str, out: dict):
    """Render a step's output. Returns an override dict {value, valid} for
    editable steps, else None (meaning: no override, always valid)."""
    if key == "pdf":
        c1, c2, c3 = st.columns(3)
        c1.metric("Pages",      out.get("page_count", 0))
        c2.metric("Characters", f"{out.get('char_count', 0):,}")
        c3.metric("Tables",     len(out.get("tables", [])))
        with st.expander("📄 Extracted raw text (first 3,000 chars)", expanded=True):
            st.text(out.get("full_text", "")[:3000] or "(no text extracted)")
        if out.get("tables"):
            with st.expander(f"📊 Extracted tables ({len(out['tables'])})"):
                for t in out["tables"][:5]:
                    try:    st.table(pd.DataFrame(t))
                    except Exception: st.write(t)
        return None

    if key == "ner":
        c = st.columns(4)
        c[0].metric("Dates",      len(out.get("dates", [])))
        c[1].metric("Rents PSF",  len(out.get("rents_psf", [])))
        c[2].metric("Sqft vals",  len(out.get("sqft_values", [])))
        c[3].metric("Org names",  len(out.get("candidate_tenants", [])))
        st.json(out, expanded=False)
        return None

    if key == "llm":
        st.caption("✏️ This JSON is what gets written to the graph — edit it if the LLM got anything wrong.")
        default = json.dumps(out, indent=2, default=str)
        txt = st.text_area("Structured lease JSON", value=default, height=340, key="wiz_llm_edit")
        try:
            parsed = json.loads(txt)
            st.caption("✅ Valid JSON — ready to continue.")
            return {"value": parsed, "valid": True}
        except Exception as e:
            st.warning(f"⚠️ Invalid JSON — fix before continuing: {e}")
            return {"value": None, "valid": False}

    if key == "resolve":
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Property address**")
            st.caption(f"Raw: {out.get('raw_address')}")
            st.success(out.get("canonical_address"))
        with c2:
            st.markdown("**Tenant**")
            st.caption(f"Raw: {out.get('raw_tenant')}")
            st.success(out.get("canonical_tenant"))
        return None

    if key == "graph":
        st.metric("Lease ID created", out.get("lease_id", "—"))
        st.caption("MERGED into Neo4j: Property → Lease → Tenant (+ Clause / Renewal / Termination).")
        return None

    if key == "embed":
        c1, c2 = st.columns(2)
        c1.metric("Chunks generated",         out.get("chunk_count", 0))
        c2.metric("Chunks embedded → Chroma", out.get("chunks_added", 0))
        return None

    st.json(out)
    return None


def _wiz_reset() -> None:
    for k in ("wiz_sig", "wiz_file_bytes", "wiz_file_name", "wiz_step",
              "wiz_out", "wiz_status", "wiz_err", "wiz_celebrated", "wiz_llm_edit"):
        st.session_state.pop(k, None)


def render_ingest_wizard() -> None:
    up = st.file_uploader(
        "Upload a single lease PDF to walk through the pipeline stage-by-stage",
        type=["pdf"], key="wiz_uploader",
    )
    if up is not None:
        sig = f"{up.name}:{up.size}"
        if st.session_state.get("wiz_sig") != sig:
            _wiz_reset()
            st.session_state.wiz_sig        = sig
            st.session_state.wiz_file_bytes = up.getvalue()
            st.session_state.wiz_file_name  = up.name
            st.session_state.wiz_step       = 0
            st.session_state.wiz_out        = {}
            st.session_state.wiz_status     = {}
            st.session_state.wiz_err        = {}

    if "wiz_file_bytes" not in st.session_state:
        st.info("⬆️ Upload a lease PDF to begin the guided, step-by-step ingestion.")
        return

    cur = st.session_state.wiz_step

    # Build tracker statuses
    statuses = []
    for i, s in enumerate(STEPS):
        k = s["key"]
        if st.session_state.wiz_status.get(k) == "done":
            statuses.append("done")
        elif i == cur and k in st.session_state.wiz_err:
            statuses.append("failed")
        elif i == cur:
            statuses.append("active")
        else:
            statuses.append("pending")
    render_tracker(statuses)

    # All steps complete
    if cur >= len(STEPS):
        if not st.session_state.get("wiz_celebrated"):
            st.balloons()
            st.session_state.wiz_celebrated = True
        st.success("🎉 Pipeline complete — this lease is now in the knowledge graph and vector store.")
        g = st.session_state.wiz_out.get("graph", {})
        e = st.session_state.wiz_out.get("embed", {})
        c1, c2, c3 = st.columns(3)
        c1.metric("Lease ID",         g.get("lease_id", "—"))
        c2.metric("Chunks embedded",  e.get("chunks_added", 0))
        c3.metric("Source file",      st.session_state.get("wiz_file_name", "—"))
        if st.button("➕ Ingest another document", type="primary"):
            _wiz_reset()
            st.rerun()
        return

    step = STEPS[cur]
    k    = step["key"]
    st.divider()
    st.subheader(f"Step {cur + 1} of {len(STEPS)} · {step['title']}")
    st.caption(step["hint"])

    # Failed → offer retry
    if k in st.session_state.wiz_err:
        st.error(st.session_state.wiz_err[k])
        if st.button("🔁 Retry this step", type="primary", key=f"retry_{k}"):
            st.session_state.wiz_err.pop(k, None)
            st.rerun()
        return

    # Not yet run → offer run
    if k not in st.session_state.wiz_out:
        if st.button(f"▶ Run: {step['title']}", type="primary", key=f"run_{k}"):
            try:
                with st.spinner(f"Running {step['title']} …"):
                    st.session_state.wiz_out[k] = STEP_FUNCS[k]()
            except Exception as ex:
                st.session_state.wiz_err[k] = f"{type(ex).__name__}: {ex}"
            st.rerun()
        return

    # Ran → show output + approve gate
    out = st.session_state.wiz_out[k]
    st.success("Step complete — review the output below, then approve to pass it to the next step.")
    override = _render_output(k, out)

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("✅ Approve & Continue", type="primary", key=f"ok_{k}"):
            if override is not None and not override["valid"]:
                st.error("Cannot continue — fix the JSON above first.")
            else:
                if override is not None:
                    st.session_state.wiz_out[k] = override["value"]
                st.session_state.wiz_status[k] = "done"
                st.session_state.wiz_step += 1
                st.rerun()
    with c2:
        if st.button("🔁 Re-run this step", key=f"rerun_{k}"):
            st.session_state.wiz_out.pop(k, None)
            if k == "llm":
                st.session_state.pop("wiz_llm_edit", None)
            st.rerun()


def render_batch_ingest() -> None:
    """Original one-shot behaviour: bulk upload or 25-lease demo."""
    uploaded = st.file_uploader(
        "Upload PDF lease(s)", type=["pdf"], accept_multiple_files=True, key="uploader",
    )
    col_a, col_b = st.columns([2, 1])
    with col_a:
        run_demo = st.button(
            "▶ Generate 25 synthetic test leases (demo)", type="secondary",
            help="Creates realistic fake lease PDFs, then ingests them into the graph.",
        )
    with col_b:
        run_btn = st.button("🚀 Process uploaded files", type="primary",
                            disabled=not (uploaded or run_demo))

    results = []
    if run_demo:
        with st.spinner("Generating synthetic leases …"):
            from leaseguard.ingestion.lease_generator import generate_batch
            metas = generate_batch(25)
        with st.spinner("Ingesting all 25 leases into graph …"):
            agent = get_agent()
            prog  = st.progress(0)
            for i, m in enumerate(metas):
                try:
                    r = agent.ingest_path(f"data/sample_leases/{m['filename']}")
                    results.append({"file": m["filename"], "lease_id": r["lease_id"],
                                    "tenant": m["tenant"], "status": "✅"})
                except Exception as ex:
                    results.append({"file": m["filename"], "lease_id": "—",
                                    "tenant": m["tenant"], "status": f"❌ {ex}"})
                prog.progress((i + 1) / len(metas))
        st.balloons()

    elif run_btn and uploaded:
        agent = get_agent()
        prog  = st.progress(0)
        for i, f in enumerate(uploaded):
            with st.spinner(f"Processing {f.name} …"):
                try:
                    r = agent.ingest_bytes(f.read(), f.name)
                    results.append({
                        "file": f.name, "lease_id": r["lease_id"],
                        "tenant":  r["data"].get("tenant_name", "Unknown"),
                        "address": r["data"].get("property_address", "Unknown"),
                        "status": "✅",
                    })
                except Exception as ex:
                    results.append({"file": f.name, "lease_id": "—",
                                    "tenant": "—", "address": "—",
                                    "status": f"❌ {ex}"})
            prog.progress((i + 1) / len(uploaded))

    if results:
        ok = len([r for r in results if "✅" in r["status"]])
        st.success(f"✅ Processed {ok} lease(s)")
        st.dataframe(pd.DataFrame(results), use_container_width=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏢 LeaseGuard")
    st.caption("Knowledge Graph Lease Intelligence")
    st.divider()

    # Neo4j health check
    try:
        neo4j_ok = get_neo4j().ping()
        if neo4j_ok:
            st.success("✅ Neo4j connected")
        else:
            st.error("❌ Neo4j not reachable\nStart Neo4j on localhost:7687")
    except Exception:
        st.error("❌ Neo4j not reachable")
        neo4j_ok = False

    # Portfolio stats
    if neo4j_ok:
        try:
            stats = get_queries().portfolio_summary()
            st.markdown("### Portfolio at a glance")
            col1, col2 = st.columns(2)
            col1.metric("Leases",     stats.get("lease_count",    0))
            col2.metric("Properties", stats.get("property_count", 0))
            col1.metric("Tenants",    stats.get("tenant_count",   0))
            col2.metric("Avg Rent PSF", f"${stats.get('avg_rent_psf', 0):.2f}")
            st.metric("Total Sqft", f"{int(stats.get('total_sqft', 0)):,}")
            st.caption(f"⚠️ {stats.get('high_risk_clauses', 0)} high-risk clauses")
        except Exception:
            st.info("Ingest leases to see portfolio stats.")

    st.divider()
    st.markdown("### 🔧 Free Stack")
    for chip in ["Neo4j Community", "ChromaDB", "spaCy NER",
                 "sentence-transformers", "Groq / Ollama"]:
        st.markdown(f"- `{chip}`")


# ── Main area: tabs ───────────────────────────────────────────────────────────
tab_ingest, tab_ask, tab_risk, tab_graph, tab_export = st.tabs([
    "📄 Ingest Leases",
    "💬 Ask AI",
    "⚠️ Risk Dashboard",
    "🔗 Knowledge Graph",
    "📊 Export",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — INGEST
# ════════════════════════════════════════════════════════════════════════════
with tab_ingest:
    st.header("Upload & Process Lease Documents")

    mode = st.radio(
        "Ingestion mode",
        ["🪄 Guided — step-by-step (review each stage)", "⚡ Auto — batch / demo"],
        horizontal=True, key="ingest_mode",
    )
    st.divider()

    if mode.startswith("🪄"):
        st.info(
            "Walk one lease through the pipeline one stage at a time. Each stage runs, shows "
            "its output for you to review, and only passes that output forward as the next "
            "stage's input when you click **Approve & Continue**."
        )
        render_ingest_wizard()
    else:
        st.info(
            "Upload one or more commercial lease PDFs (or generate a demo batch). The full "
            "pipeline runs automatically and populates the Neo4j knowledge graph."
        )
        render_batch_ingest()

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — ASK AI
# ════════════════════════════════════════════════════════════════════════════
with tab_ask:
    st.header("Ask About Your Lease Portfolio")
    st.info(
        "Every answer is grounded in the Neo4j knowledge graph — not in raw document text. "
        "The AI cites specific graph nodes for every claim."
    )

    # Example questions
    EXAMPLES = [
        "Which leases expire in the next 90 days?",
        "Which tenant has the highest concentration risk?",
        "Are there any high-risk termination clauses?",
        "What is the average rent PSF across the portfolio?",
        "Show me all NNN leases in Austin",
        "Give me a portfolio summary",
    ]
    example = st.selectbox("Example questions:", ["— custom question —"] + EXAMPLES)
    question = st.text_input(
        "Your question:",
        value="" if example.startswith("—") else example,
        placeholder="e.g. Which leases expire in the next 90 days?",
    )

    if st.button("🔍 Ask", type="primary") and question.strip():
        with st.spinner("Querying knowledge graph + generating answer …"):
            result = get_agent().ask(question)

        st.markdown("### 💡 Answer")
        st.markdown(result["answer"])

        col_g, col_d = st.columns(2)
        with col_g:
            with st.expander(f"📊 Graph context ({len(result['graph_context'])} rows)"):
                if result["graph_context"]:
                    st.dataframe(pd.DataFrame(result["graph_context"]), use_container_width=True)
                else:
                    st.write("No graph rows retrieved.")
        with col_d:
            with st.expander(f"📄 Document context ({len(result['doc_context'])} chunks)"):
                for chunk in result["doc_context"]:
                    st.caption(f"**{chunk.get('source', '')}** — score {chunk.get('score', 0):.3f}")
                    st.code(chunk["text"][:400], language="text")

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — RISK DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
with tab_risk:
    st.header("⚠️ Portfolio Risk Dashboard")
    st.caption("All data sourced live from Neo4j graph traversals.")

    refresh = st.button("🔄 Refresh dashboard")

    # Expiration risk
    st.subheader("🗓️ Lease Expiration Risk")
    days_sel = st.select_slider("Show leases expiring within:", [30, 60, 90, 180], value=90)
    try:
        exp_df = pd.DataFrame(get_queries().expiring_leases(days_sel))
        if not exp_df.empty:
            st.dataframe(exp_df, use_container_width=True)
            st.bar_chart(exp_df.set_index("tenant")["sqft"].astype(float))
        else:
            st.success(f"No leases expire in the next {days_sel} days.")
    except Exception as e:
        st.warning(f"Could not load expiration data: {e}")

    st.divider()

    # Concentration
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("👥 Tenant Concentration")
        try:
            conc_df = pd.DataFrame(get_queries().tenant_concentration())
            if not conc_df.empty:
                threshold = st.slider("Flag above (%)", 10, 50, 25)
                if "concentration_pct" in conc_df.columns:
                    conc_df["flag"] = conc_df["concentration_pct"].apply(
                        lambda x: "⚠️" if (x or 0) > threshold else ""
                    )
                st.dataframe(conc_df, use_container_width=True)
        except Exception as e:
            st.warning(f"Concentration data unavailable: {e}")

    with col2:
        st.subheader("🚨 High-Risk Clauses")
        try:
            clauses = get_queries().high_risk_clauses()
            for c in clauses[:8]:
                with st.expander(f"{c.get('lease_id')} — {c.get('property', '')[:35]}"):
                    st.caption(f"Tenant: {c.get('tenant')}")
                    st.write(c.get("clause_text", ""))
            if not clauses:
                st.success("No high-risk clauses detected.")
        except Exception as e:
            st.warning(f"Clause data unavailable: {e}")

    st.divider()

    # AI Risk report
    st.subheader("🤖 AI Portfolio Risk Report")
    if st.button("Generate AI risk report"):
        with st.spinner("Analysing portfolio risk via LLM …"):
            try:
                report = get_risk().full_risk_report()
                st.markdown(report)
            except Exception as e:
                st.error(f"Report generation failed: {e}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — KNOWLEDGE GRAPH
# ════════════════════════════════════════════════════════════════════════════
with tab_graph:
    st.header("🔗 Knowledge Graph Explorer")
    st.info(
        "Interactive visualisation of the Neo4j graph. "
        "Nodes are colour-coded: 🔵 Property · 🟢 Tenant · 🟣 Lease · 🔴 Clause."
    )

    node_limit = st.slider("Max nodes to display", 20, 150, 60)
    if st.button("🔄 Render graph"):
        try:
            from pyvis.network import Network  # type: ignore
            import streamlit.components.v1 as components

            graph_data = get_queries().graph_for_visualisation(limit=node_limit)
            net = Network(
                height="560px", width="100%",
                bgcolor="#0E1726", font_color="#FFFFFF",
            )
            net.set_options(
                '{"physics":{"enabled":true,'
                '"solver":"forceAtlas2Based",'
                '"forceAtlas2Based":{"gravitationalConstant":-50}}}'
            )

            NODE_COLORS = {
                "Property": "#4C8DFF",
                "Tenant":   "#27D199",
                "Lease":    "#9B7CF6",
                "Clause":   "#FB5A6A",
            }
            for node in graph_data["nodes"]:
                color = NODE_COLORS.get(node["type"], "#AAAAAA")
                net.add_node(
                    node["id"], label=node["label"], color=color,
                    title=f"{node['type']}: {node['id']}",
                )
            for edge in graph_data["edges"]:
                net.add_edge(
                    edge["from"], edge["to"],
                    label=edge.get("label", ""),
                    color="#334466",
                )

            # Save and render
            with tempfile.NamedTemporaryFile(
                suffix=".html", delete=False, mode="w", encoding="utf-8"
            ) as f:
                net.save_graph(f.name)
                html_path = f.name
            with open(html_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            os.unlink(html_path)
            components.html(html_content, height=580, scrolling=False)

        except ImportError:
            st.error("pyvis not installed. Run: pip install pyvis")
        except Exception as e:
            st.error(f"Graph render failed: {e}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — EXPORT
# ════════════════════════════════════════════════════════════════════════════
with tab_export:
    st.header("📊 Export Lease Data")

    try:
        leases = get_queries().all_leases()
        if leases:
            df = pd.DataFrame(leases)
            st.dataframe(df, use_container_width=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇️ Download CSV", csv,
                    "leaseguard_leases.csv", "text/csv",
                )
            with col2:
                js  = json.dumps(leases, default=str, indent=2).encode("utf-8")
                st.download_button(
                    "⬇️ Download JSON", js,
                    "leaseguard_leases.json", "application/json",
                )
            with col3:
                summary = get_queries().portfolio_summary()
                sm_json = json.dumps(summary, default=str, indent=2).encode("utf-8")
                st.download_button(
                    "⬇️ Portfolio Summary JSON", sm_json,
                    "portfolio_summary.json", "application/json",
                )
        else:
            st.info("No leases to export yet — ingest some documents first.")
    except Exception as e:
        st.error(f"Export unavailable: {e}")
