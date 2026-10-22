# -*- coding: utf-8 -*-
"""
Deploy Cinematic Interactive Knowledge Graph Architecture Simulator
Provides:
1. Cyberpunk Command Center / Holographic Cinema Viewport
2. Side-by-side visual engagement of ALL datasets (Structured SQL/SWIFT/Assays AND Unstructured PDFs/SARs/PubMed)
3. Step-by-step cinematic dataflow animation (Within-mapping, Key Binding Bridge, Unified Graph, Cypher Radar, Graph-RAG, Leadership Command)
4. Dynamic contribution breakdown of all 7 core tools (Mapping Key, Inputs, Protégé, ChromaDB, Neo4j, Cypher, Graph-RAG)
5. Interactive Node Inspector (Click any node to see live telemetry, properties, and provenance)
6. Movie-style animated subtitles / narration for effortless executive presentations
7. Fullscreen Theater mode toggle
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ---------------------------------------------------------------------------
# CINEMATIC STYLING (DARK CYBER COMMAND CENTER)
# ---------------------------------------------------------------------------
cinema_css = '''
    /* ================= CINEMATIC ARCHITECTURE COMMAND CENTER ================= */
    .cinema-viewport {
      background: radial-gradient(circle at 50% 20%, #151D30 0%, #080C16 80%, #03060B 100%);
      border: 1.5px solid #2A3958;
      border-radius: 16px;
      padding: 26px;
      margin-bottom: 32px;
      box-shadow: 0 16px 48px rgba(0,0,0,0.45), inset 0 0 80px rgba(0, 240, 255, 0.03);
      position: relative;
      overflow: hidden;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .cinema-viewport::before {
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; height: 1px;
      background: linear-gradient(90deg, transparent, #00F0FF, #FF9F0A, transparent);
      opacity: 0.6;
    }
    .cinema-scanlines {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%);
      background-size: 100% 4px;
      pointer-events: none;
      opacity: 0.2;
      z-index: 1;
    }
    
    /* HUD TOP BAR */
    .cinema-hud-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 14px;
      margin-bottom: 20px;
      position: relative;
      z-index: 2;
      border-bottom: 1px solid rgba(42, 57, 88, 0.8);
      padding-bottom: 16px;
    }
    .cinema-hud-title {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .cinema-hud-pulse-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #00F0FF;
      box-shadow: 0 0 12px #00F0FF;
      animation: cinemaGlow 1.5s infinite alternate;
    }
    @keyframes cinemaGlow {
      0% { transform: scale(0.9); opacity: 0.6; }
      100% { transform: scale(1.3); opacity: 1; filter: drop-shadow(0 0 8px #00F0FF); }
    }
    .cinema-title-text {
      font-size: 20px;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: -0.01em;
      margin: 0;
      text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    .cinema-tagline {
      font-size: 12px;
      color: #94A3B8;
      margin: 2px 0 0;
    }
    
    /* AUDIO VISUALIZER / EQUALIZER */
    .cinema-eq {
      display: inline-flex;
      align-items: flex-end;
      gap: 2.5px;
      height: 16px;
      margin-left: 8px;
    }
    .cinema-eq-bar {
      width: 3px;
      background: #00F0FF;
      border-radius: 1px;
      animation: eqBounce 1.2s ease-in-out infinite alternate;
    }
    .cinema-eq-bar:nth-child(2) { animation-delay: 0.2s; height: 12px; background: #FF9F0A; }
    .cinema-eq-bar:nth-child(3) { animation-delay: 0.4s; height: 16px; background: #3DDC97; }
    .cinema-eq-bar:nth-child(4) { animation-delay: 0.1s; height: 8px; background: #00F0FF; }
    .cinema-eq-bar:nth-child(5) { animation-delay: 0.3s; height: 14px; background: #FF453A; }
    @keyframes eqBounce {
      0% { height: 4px; }
      100% { height: 16px; }
    }

    /* ACTION CONTROLS */
    .cinema-actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .cinema-btn {
      background: rgba(18, 24, 36, 0.85);
      border: 1px solid #3A4763;
      color: #E2E8F0;
      padding: 7px 15px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 7px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      backdrop-filter: blur(8px);
    }
    .cinema-btn:hover {
      border-color: #00F0FF;
      color: #FFFFFF;
      box-shadow: 0 0 14px rgba(0, 240, 255, 0.3);
      transform: translateY(-1px);
    }
    .cinema-btn.active-play {
      background: linear-gradient(135deg, rgba(255, 159, 10, 0.25), rgba(255, 69, 58, 0.25));
      border-color: #FF9F0A;
      color: #FFB340;
      box-shadow: 0 0 18px rgba(255, 159, 10, 0.35);
    }
    .cinema-domain-pill {
      display: inline-flex;
      background: #0B0F17;
      border: 1px solid #2A364F;
      border-radius: 8px;
      padding: 3px;
    }
    .cinema-domain-tab {
      background: transparent;
      border: none;
      color: #94A3B8;
      padding: 5px 12px;
      font-size: 11.5px;
      font-weight: 700;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .cinema-domain-tab.active.fin {
      background: #1A2234;
      color: #FF9F0A;
      box-shadow: 0 0 10px rgba(255,159,10,0.3);
    }
    .cinema-domain-tab.active.med {
      background: #1A2234;
      color: #3DDC97;
      box-shadow: 0 0 10px rgba(61,220,151,0.3);
    }

    /* CINEMATIC TIMELINE ACTS */
    .cinema-acts-bar {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 10px;
      margin-bottom: 22px;
      position: relative;
      z-index: 2;
    }
    @media (max-width: 900px) {
      .cinema-acts-bar { grid-template-columns: repeat(3, 1fr); }
    }
    .cinema-act-card {
      background: rgba(14, 20, 32, 0.7);
      border: 1px solid rgba(42, 54, 79, 0.8);
      border-radius: 10px;
      padding: 12px 14px;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(6px);
    }
    .cinema-act-card:hover {
      border-color: #4A5D85;
      transform: translateY(-2px);
    }
    .cinema-act-card.active {
      background: rgba(0, 240, 255, 0.08);
      border-color: #00F0FF;
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.28), inset 0 0 12px rgba(0, 240, 255, 0.05);
    }
    .cinema-act-card.active.fin {
      border-color: #FF9F0A;
      box-shadow: 0 0 20px rgba(255, 159, 10, 0.28);
    }
    .cinema-act-card.active.med {
      border-color: #3DDC97;
      box-shadow: 0 0 20px rgba(61, 220, 151, 0.28);
    }
    .cinema-act-badge {
      font-size: 10px;
      font-weight: 800;
      color: #64748B;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 4px;
    }
    .cinema-act-card.active .cinema-act-badge {
      color: #00F0FF;
    }
    .cinema-act-card.active.fin .cinema-act-badge {
      color: #FF9F0A;
    }
    .cinema-act-card.active.med .cinema-act-badge {
      color: #3DDC97;
    }
    .cinema-act-title {
      font-size: 12px;
      font-weight: 700;
      color: #E2E8F0;
      line-height: 1.3;
    }

    /* THEATER STAGE (THE DUAL-STREAM DATA ENGINE) */
    .cinema-stage {
      background: #060911;
      border: 1.5px solid #1E293B;
      border-radius: 14px;
      padding: 22px;
      margin-bottom: 22px;
      position: relative;
      z-index: 2;
      overflow: hidden;
    }
    .cinema-grid-bg {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background-image: 
        linear-gradient(rgba(30, 41, 59, 0.25) 1px, transparent 1px),
        linear-gradient(90deg, rgba(30, 41, 59, 0.25) 1px, transparent 1px);
      background-size: 24px 24px;
      opacity: 0.4;
      pointer-events: none;
    }

    /* DUAL DATASET HUD (STRUCTURED vs UNSTRUCTURED) */
    .cinema-dual-streams {
      display: grid;
      grid-template-columns: 1fr 120px 1fr;
      gap: 16px;
      align-items: center;
      margin-bottom: 20px;
      position: relative;
    }
    @media (max-width: 820px) {
      .cinema-dual-streams { grid-template-columns: 1fr; }
    }
    .cinema-stream-box {
      background: rgba(13, 19, 33, 0.9);
      border: 1.5px solid #23314E;
      border-radius: 12px;
      padding: 16px;
      position: relative;
      box-shadow: 0 4px 20px rgba(0,0,0,0.3);
      backdrop-filter: blur(10px);
    }
    .cinema-stream-box.unstructured {
      border-left: 4px solid #FF9F0A;
    }
    .cinema-stream-box.structured {
      border-right: 4px solid #3DDC97;
    }
    .cinema-stream-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }
    .cinema-stream-tag {
      font-size: 11px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .cinema-stream-tag.unstructured {
      background: rgba(255, 159, 10, 0.18);
      color: #FF9F0A;
    }
    .cinema-stream-tag.structured {
      background: rgba(61, 220, 151, 0.18);
      color: #3DDC97;
    }
    .cinema-stream-items {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .cinema-data-item {
      background: #090D17;
      border: 1px solid #1E293B;
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 11px;
      font-family: var(--mono, monospace);
      color: #CBD5E1;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s ease;
    }
    .cinema-data-item:hover {
      border-color: #00F0FF;
      background: #0D1526;
      color: #FFFFFF;
    }
    .cinema-data-badge {
      font-size: 9.5px;
      padding: 2px 5px;
      border-radius: 3px;
      background: #1E293B;
      color: #94A3B8;
    }

    /* THE QUANTUM KEY BINDING BRIDGE IN THE CENTER */
    .cinema-bridge-hub {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      position: relative;
    }
    .cinema-bridge-circle {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(0, 240, 255, 0.25) 0%, rgba(11, 15, 23, 0.95) 75%);
      border: 2px dashed #00F0FF;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      box-shadow: 0 0 24px rgba(0, 240, 255, 0.4);
      animation: bridgeSpin 12s linear infinite;
      cursor: pointer;
    }
    @keyframes bridgeSpin {
      100% { transform: rotate(360deg); }
    }
    .cinema-bridge-label {
      font-size: 10px;
      font-weight: 800;
      color: #00F0FF;
      margin-top: 8px;
      letter-spacing: 0.06em;
      text-transform: uppercase;
    }

    /* INTERACTIVE VISUAL CANVAS (ANIMATED SVG) */
    .cinema-canvas-wrap {
      width: 100%;
      height: 260px;
      position: relative;
      margin-top: 14px;
      border: 1px solid rgba(42, 57, 88, 0.5);
      border-radius: 10px;
      background: #04070E;
      overflow: hidden;
    }
    .cinema-svg {
      width: 100%;
      height: 100%;
    }

    /* LIVE NODE TELEMETRY INSPECTOR OVERLAY */
    .cinema-inspector {
      background: rgba(11, 16, 28, 0.95);
      border: 1.5px solid #00F0FF;
      border-radius: 10px;
      padding: 14px 18px;
      margin-top: 18px;
      box-shadow: 0 8px 30px rgba(0, 240, 255, 0.25);
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 12px;
      backdrop-filter: blur(12px);
    }
    .cinema-inspector-title {
      font-size: 13px;
      font-weight: 800;
      color: #00F0FF;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .cinema-inspector-body {
      font-size: 12px;
      color: #E2E8F0;
      font-family: var(--mono, monospace);
    }
    
    /* SUBTITLE NARRATION STRIP */
    .cinema-narration {
      background: rgba(8, 12, 22, 0.9);
      border: 1px solid #1E293B;
      border-left: 4px solid #00F0FF;
      border-radius: 8px;
      padding: 14px 18px;
      margin-top: 16px;
      position: relative;
      z-index: 2;
    }
    .cinema-narration-lead {
      font-size: 14px;
      font-weight: 700;
      color: #FFFFFF;
      margin: 0 0 6px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .cinema-narration-sub {
      font-size: 13px;
      color: #94A3B8;
      line-height: 1.6;
      margin: 0;
    }

    /* TECH STACK HOLO-RADAR */
    .cinema-tech-radar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(135px, 1fr));
      gap: 10px;
      margin-top: 20px;
      position: relative;
      z-index: 2;
    }
    .cinema-tech-node {
      background: rgba(13, 19, 32, 0.7);
      border: 1px solid rgba(42, 57, 88, 0.6);
      border-radius: 8px;
      padding: 10px;
      text-align: center;
      transition: all 0.25s ease;
    }
    .cinema-tech-node.lit {
      border-color: #00F0FF;
      background: rgba(0, 240, 255, 0.1);
      box-shadow: 0 0 16px rgba(0, 240, 255, 0.3);
      transform: translateY(-2px);
    }
    .cinema-tech-node.lit.fin {
      border-color: #FF9F0A;
      box-shadow: 0 0 16px rgba(255, 159, 10, 0.35);
    }
    .cinema-tech-node.lit.med {
      border-color: #3DDC97;
      box-shadow: 0 0 16px rgba(61, 220, 151, 0.35);
    }
    .cinema-tech-ico {
      font-size: 18px;
      margin-bottom: 4px;
    }
    .cinema-tech-label {
      font-size: 11px;
      font-weight: 800;
      color: #E2E8F0;
    }
    .cinema-tech-role {
      font-size: 9.5px;
      color: #64748B;
      margin-top: 2px;
    }
    .cinema-tech-node.lit .cinema-tech-role {
      color: #00F0FF;
      font-weight: 700;
    }
    .cinema-tech-node.lit.fin .cinema-tech-role {
      color: #FF9F0A;
    }
    .cinema-tech-node.lit.med .cinema-tech-role {
      color: #3DDC97;
    }
'''

# ---------------------------------------------------------------------------
# JAVASCRIPT ENGINE FOR CINEMATIC ARCHITECTURE
# ---------------------------------------------------------------------------
cinema_js = '''
<script>
// ================= CINEMATIC ARCHITECTURE COMMAND CENTER ENGINE =================
(function() {
  const acts = {
    fin: [
      {
        act: "Act I",
        title: "Unstructured Document Ingress & Co-occurrence Mesh",
        narrationTitle: "Ingesting Heterogeneous Unstructured Records",
        narration: "Raw compliance documents (FinCEN SAR PDFs, commercial loan agreements, whistleblower email threads) enter the pipeline with zero foreign keys. NLP entity extraction tags company names (Apex Global) and individuals (Vladimir S.), while ChromaDB vector embeddings map semantic similarities, weaving an initial document-to-document co-occurrence mesh.",
        inspector: { node: "SAR-2026-09.pdf", type: "FinCEN Form 111", properties: "mentions: ['Apex Global FZE', 'Vladimir S.'], cosine_similarity: 0.89 to Loan_App_482.pdf" },
        techLit: ["inputs", "chroma", "protege"],
        unstructuredItems: [
          { name: "SAR-2026-09.pdf", badge: "FinCEN Form 111" },
          { name: "Loan_App_482.pdf", badge: "Commercial Loan" },
          { name: "Whistleblower.eml", badge: "Internal Memo" },
          { name: "Court_Record.pdf", badge: "Subpoena 8841" }
        ],
        structuredItems: [
          { name: "Standby Ingest", badge: "Core Banking SQL" },
          { name: "Standby Ingest", badge: "SWIFT MT103" },
          { name: "Standby Ingest", badge: "OFAC Watchlist" },
          { name: "Standby Ingest", badge: "SEC EDGAR UBO" }
        ],
        bridgeKey: "SCANNING KEYS",
        svgMode: "act1"
      },
      {
        act: "Act II",
        title: "Relational Structured Graph Weaving",
        narrationTitle: "Transforming Relational Tables into a Living Topology",
        narration: "Relational banking feeds (Core SQL accounts, SWIFT wire logs, OFAC SDN watchlists) are ingested simultaneously. Foreign keys convert into directed edges (:Customer)-[:OWNS]->(:Account) and (:Account)-[:TRANSFERRED {amount: $485k}]->(:Account). Protégé OWL 2 ontologies enforce formal entity constraints, turning static rows into an active network graph.",
        inspector: { node: "Account: GB29NWBK60161331", type: "Corporate Checking", properties: "balance: $3,840,000.00 USD, holder: Apex Global Logistics FZE, status: ACTIVE" },
        techLit: ["inputs", "neo4j", "protege", "key"],
        unstructuredItems: [
          { name: "Text Chunks [0..3]", badge: "Vectorized" },
          { name: "Entity Bridges", badge: "Linked" },
          { name: "Citation Graph", badge: "Mapped" },
          { name: "Co-reference Pool", badge: "Indexed" }
        ],
        structuredItems: [
          { name: "acc_881920 (SQL)", badge: "$3.84M Balance" },
          { name: "wire_tx_59102", badge: "$485,000 USD" },
          { name: "OFAC_SDN_Match", badge: "Apex Global FZE" },
          { name: "Device_00:14:22", badge: "IP 194.26.29.50" }
        ],
        bridgeKey: "CANONICAL IBAN",
        svgMode: "act2"
      },
      {
        act: "Act III",
        title: "The Quantum Key Binding Bridge",
        narrationTitle: "The Climax of Integration: Binding Text to Database Records",
        narration: "THE UNIVERSAL BRIDGE: Canonical financial mapping keys (Customer_TaxID: XX-XXX9102, Account_IBAN) are extracted from unstructured narratives via LLM regex. The engine executes Cypher MERGE commands, anchoring qualitative document paragraphs directly onto relational account nodes via [:EVIDENCE_FOR]. Text and numbers become one unified truth.",
        inspector: { node: "MERGE Bridge", type: "Cross-Modal Edge", properties: "source: SAR-2026-09 chunk #2 -> target: Account (IBAN US89...) via Cypher MERGE, confidence: 0.96" },
        techLit: ["key", "cypher", "neo4j", "rag"],
        unstructuredItems: [
          { name: "Narrative Chunk #2", badge: "Structuring Red Flag" },
          { name: "Key: 12-482910", badge: "Extracted EIN" },
          { name: "TaxID: XX-XXX9102", badge: "Extracted UBO" },
          { name: "Admitted Intent", badge: "High Risk" }
        ],
        structuredItems: [
          { name: "Account Node #881", badge: "Mapped Target" },
          { name: "Customer Node #402", badge: "Mapped UBO" },
          { name: "SWIFT Wire Node", badge: "Attached Proof" },
          { name: "Device Fingerprint", badge: "Bounded Telemetry" }
        ],
        bridgeKey: "TAX_ID + IBAN",
        svgMode: "act3"
      },
      {
        act: "Act IV",
        title: "The Unified Multi-Modal Property Graph",
        narrationTitle: "One Unified Holographic Knowledge Graph in Neo4j",
        narration: "The complete enterprise property graph is assembled. Accounts, beneficial ownership hierarchies, SWIFT wires, hardware device telemetry (MAC/IP), and legal document evidence exist in a unified topology governed by Protégé OWL 2 axioms, with every node synchronized to ChromaDB dense vector partitions.",
        inspector: { node: "Vladimir S. (Node:402)", type: "Beneficial Owner (UBO)", properties: "tax_id: XX-XXX9102, passport: CY-482910, controls: ['Apex Global FZE', 'BlueStar Ltd']" },
        techLit: ["neo4j", "protege", "chroma", "key"],
        unstructuredItems: [
          { name: "14 Text Chunks", badge: "Evidentiary Nodes" },
          { name: "3 Regulatory Citations", badge: "Source Lineage" },
          { name: "ChromaDB Vectors", badge: "Synchronized" },
          { name: "Audit Trail", badge: "100% Provenance" }
        ],
        structuredItems: [
          { name: "14 Bank Accounts", badge: "LPG Nodes" },
          { name: "42 SWIFT Wires", badge: "Directed Edges" },
          { name: "3 Shell Companies", badge: "Entity Nodes" },
          { name: "1 Shared Device", badge: "MAC: 00-14-22" }
        ],
        bridgeKey: "UNIFIED LPG",
        svgMode: "act4"
      },
      {
        act: "Act V",
        title: "Cypher Deep-Scan Pattern Recognition Radar",
        narrationTitle: "Algorithmic Discovery of 3-to-6 Hop Circular Layering Rings",
        narration: "A real-time Cypher pattern recognition engine sweeps across the graph. In microseconds, it detects a 4-hop circular wire layering ring: money exits Account A ($485k), splits across intermediary shell accounts B & C within 48 hours, and loops back to Account A disguised as clean trade revenue. GDS PageRank pinpoints Vladimir S. as the shadow ringleader.",
        inspector: { node: "Layering Ring #1", type: "4-Hop Circular Cycle", properties: "path: (A)->(B)->(C)->(D)->(A), amount: $485,000 USD, duration: 38.4 hours, typology: Layering" },
        techLit: ["cypher", "neo4j", "rag"],
        unstructuredItems: [
          { name: "Typology: Layering", badge: "Matched Pattern" },
          { name: "Mule Evidence", badge: "Corroborated" },
          { name: "Subpoena Cross-Check", badge: "Verified" },
          { name: "Risk Severity", badge: "CRITICAL ALERT" }
        ],
        structuredItems: [
          { name: "Circle: Acc A -> Acc B", badge: "Hop 1 ($485,000)" },
          { name: "Circle: Acc B -> Acc C", badge: "Hop 2 ($475,000)" },
          { name: "Circle: Acc C -> Acc D", badge: "Hop 3 ($460,000)" },
          { name: "Circle: Acc D -> Acc A", badge: "Hop 4 ($455,000)" }
        ],
        bridgeKey: "CYPHER RADAR",
        svgMode: "act5"
      },
      {
        act: "Act VI",
        title: "Executive Command Center & Boardroom Action",
        narrationTitle: "Board-Level Quantified Deliverables & Regulatory Protection",
        narration: "Hybrid Graph-RAG synthesizes the final executive dossier: Exactly $14,250,000.00 USD in quantified money laundering exposure across 3 rings, specific bad actors identified (Vladimir S., Apex Global Logistics), 4 accounts frozen immediately preserving $3,840,000 in liquid assets, and a 1-click FinCEN SAR filing package generated with zero hallucination.",
        inspector: { node: "Executive Brief", type: "FinCEN SAR Package", properties: "exposure: $14,250,000.00, frozen_assets: $3,840,000.00, penalty_avoided: $50M+, status: READY" },
        techLit: ["rag", "neo4j", "cypher", "key"],
        unstructuredItems: [
          { name: "FinCEN Form 111 XML", badge: "1-Click SAR Ready" },
          { name: "Legal Audit Package", badge: "Defensible" },
          { name: "Court Affidavit", badge: "Auto-Populated" },
          { name: "Executive Briefing", badge: "Boardroom Ready" }
        ],
        structuredItems: [
          { name: "$14,250,000.00", badge: "Laundering Total" },
          { name: "$3,840,000.00", badge: "Frozen Assets" },
          { name: "3 Shell Companies", badge: "Indicted" },
          { name: "4 Accounts Blocked", badge: "Containment OK" }
        ],
        bridgeKey: "BOARDROOM BRIEF",
        svgMode: "act6"
      }
    ],
    med: [
      {
        act: "Act I",
        title: "Biomedical Literature Mining & BioNER Mesh",
        narrationTitle: "Ingesting Global Cancer Research Papers & Patents",
        narration: "Unstructured scientific assets (PubMed abstracts, bioRxiv preprints, USPTO patent claims) are parsed with BioBERT. The engine extracts target proteins (EGFR), resistance mutations (L858R, T790M, C797S), and chemical synonyms, while ChromaDB vector embeddings cluster corroborating clinical observations across global oncology labs.",
        inspector: { node: "PubMed-38192044", type: "Oncology Journal Paper", properties: "target: 'EGFR C797S', cell_line: 'H1975', claim: 'Allosteric inhibition bypasses covalent resistance'" },
        techLit: ["inputs", "chroma", "protege"],
        unstructuredItems: [
          { name: "PubMed-38192044", badge: "Nature Oncology" },
          { name: "bioRxiv-Preprint", badge: "C797S Resistance" },
          { name: "Patent-US10894782", badge: "Allosteric Claims" },
          { name: "ClinicalTrial-NCT", badge: "Phase I Protocol" }
        ],
        structuredItems: [
          { name: "Standby Ingest", badge: "ChEMBL Bioassays" },
          { name: "Standby Ingest", badge: "UniProtKB FASTA" },
          { name: "Standby Ingest", badge: "PDB 3D Crystals" },
          { name: "Standby Ingest", badge: "PubChem SMILES" }
        ],
        bridgeKey: "UNIPROT SCAN",
        svgMode: "act1"
      },
      {
        act: "Act II",
        title: "Assay Matrices & 3D Crystallographic Weaving",
        narrationTitle: "Unifying In-Vitro Assays & 3D Crystal Structures",
        narration: "Structured life sciences data feeds are ingested: ChEMBL high-throughput IC50/Ki bioassays, UniProtKB amino acid sequences (P00533), and PDB 3D crystallographic coordinates (PDB: 6S9B). Relational records convert into kinase active site nodes and binding affinity edges governed by Protégé biological ontologies.",
        inspector: { node: "Target: P00533 (EGFR)", type: "Tyrosine Kinase", properties: "hinge_residue: Met793, catalytic: Lys745, mutation_site: Cys797Ser, organism: Homo sapiens" },
        techLit: ["inputs", "neo4j", "protege", "key"],
        unstructuredItems: [
          { name: "PubMed Paragraphs", badge: "Bio-Vectorized" },
          { name: "Mutation Claims", badge: "Triples Extracted" },
          { name: "Citation Network", badge: "Cross-Linked" },
          { name: "Prior Art Graph", badge: "Indexed" }
        ],
        structuredItems: [
          { name: "ChEMBL203 (EGFR)", badge: "IC50 Assays" },
          { name: "UniProt: P00533", badge: "Target Sequence" },
          { name: "PDB: 6S9B", badge: "3D ATP Pocket" },
          { name: "InChIKey: XUIAK...", badge: "Canonical SMILES" }
        ],
        bridgeKey: "INCHIKEY + P00533",
        svgMode: "act2"
      },
      {
        act: "Act III",
        title: "The Bio Key Binding Bridge",
        narrationTitle: "Grounding Literature Hypotheses to Wet-Lab Chemistry",
        narration: "THE UNIVERSAL BIO-BRIDGE: Canonical accession keys (UniProt_ID: P00533, InChIKey, PDB_ID: 6S9B) extracted from publication claims are bound directly to structured ChEMBL molecular compounds using Cypher MERGE. Published research claims are now hard-linked to empirical wet-lab IC50 assay readings.",
        inspector: { node: "Bio-Key Bridge", type: "Cross-Modal Binding", properties: "source: PubMed chunk -> bindsTo: Target (UniProt:P00533) & Molecule (FEU-904), validated_ic50: 1.8 nM" },
        techLit: ["key", "cypher", "neo4j", "rag"],
        unstructuredItems: [
          { name: "Preprint Paragraph #4", badge: "C797S Claim" },
          { name: "Extracted: P00533", badge: "UniProt Key" },
          { name: "Extracted: 6S9B", badge: "PDB Pocket" },
          { name: "Cell Viability Claim", badge: "IC50 = 1.8 nM" }
        ],
        structuredItems: [
          { name: "Compound: FEU-904", badge: "Lead Candidate" },
          { name: "Pocket: Lys745/Met793", badge: "Hinge Geometry" },
          { name: "Assay: Ba/F3 Cells", badge: "1.8 nM Reading" },
          { name: "Disease: NSCLC", badge: "DOID:3908" }
        ],
        bridgeKey: "UNIPROT + INCHIKEY",
        svgMode: "act3"
      },
      {
        act: "Act IV",
        title: "The Unified Biomedical Property Graph",
        narrationTitle: "One Living Multi-Modal Biomedical Brain in Neo4j",
        narration: "The complete biomedical knowledge graph is online: Chemical lead structures, kinase mutation variants, 3D binding pockets, cell assay models, clinical disease ontologies, and supporting scientific literature chunks coexist within Neo4j, fully indexed in ChromaDB for high-dimensional semantic search.",
        inspector: { node: "FEU-EGFR-904", type: "SmallMolecule Lead", properties: "mw: 513.57 Da, clogp: 3.12, hbd: 2, hba: 7, formula: C28H28FN7O2, target: 'EGFR C797S'" },
        techLit: ["neo4j", "protege", "chroma", "key"],
        unstructuredItems: [
          { name: "28 Literature Chunks", badge: "Paper Provenance" },
          { name: "6 Patent Claims", badge: "Novel Scaffolds" },
          { name: "PubMedBERT Vectors", badge: "Embedded" },
          { name: "Biomarker Evidence", badge: "Validated" }
        ],
        structuredItems: [
          { name: "1 Lead Compound", badge: "FEU-EGFR-904" },
          { name: "3 Kinase Variants", badge: "WT / T790M / C797S" },
          { name: "1 Binding Pocket", badge: "PDB: 6S9B" },
          { name: "Safety: hERG Channel", badge: "Target Checked" }
        ],
        bridgeKey: "UNIFIED BIO-LPG",
        svgMode: "act4"
      },
      {
        act: "Act V",
        title: "Cypher Kinase Selectivity & Anti-Target Radar",
        narrationTitle: "Multi-Objective Drug Optimization: Efficacy vs Toxicity",
        narration: "The Cypher query engine scans millions of graph paths to solve the drug discovery trifecta: Candidate molecules must potently inhibit triple-mutant EGFR C797S (<10 nM), spare wild-type EGFR (>50x selectivity to avoid diarrhea/rash), and exhibit zero affinity for the hERG cardiotoxic ion channel (>5,000 nM). FEU-EGFR-904 emerges as the singular winning lead.",
        inspector: { node: "Lead Candidate FEU-EGFR-904", type: "Kinase Selectivity Result", properties: "mutant_ic50: 1.8 nM, wt_selectivity: 180x, herg_ic50: >10,000 nM (zero cardiotoxicity)" },
        techLit: ["cypher", "neo4j", "rag"],
        unstructuredItems: [
          { name: "Mechanism: Allosteric", badge: "Bypasses C797S" },
          { name: "H1975 Cell Model", badge: "99% Tumor Kill" },
          { name: "In Vivo Efficacy", badge: "Corroborated" },
          { name: "Safety Cleared", badge: "Zero Arrhythmia" }
        ],
        structuredItems: [
          { name: "Mutant IC50: 1.8 nM", badge: "Nanomolar Potency" },
          { name: "WT Ratio: 180x", badge: "High Therapeutic Index" },
          { name: "hERG IC50: >10,000 nM", badge: "Zero Cardiotoxicity" },
          { name: "Lipinski: 100%", badge: "Oral Drug-Likeness" }
        ],
        bridgeKey: "SELECTIVITY CYPHER",
        svgMode: "act5"
      },
      {
        act: "Act VI",
        title: "R&D Executive Dossier & Synthesis Recipe",
        narrationTitle: "Board-Level Novel Drug Deliverable & Synthesis Blueprint",
        narration: "Hybrid Graph-RAG delivers the complete discovery dossier to the Chief Scientific Officer: Novel small molecule FEU-EGFR-904, canonical SMILES, active site interaction recipe (how the cyclobutane acrylamide traps Lys745 to circumvent C797S resistance), 180x selectivity margin, and hit-to-lead acceleration from 18 months to 6 weeks for a $2.8B addressable oncology market.",
        inspector: { node: "FEU-EGFR-904 Dossier", type: "IND Drug Blueprint", properties: "indication: Resistant NSCLC, market_size: $2.8B USD, timeline_cut: 18mo -> 6wks, recipe: READY" },
        techLit: ["rag", "neo4j", "cypher", "key"],
        unstructuredItems: [
          { name: "IND Regulatory Brief", badge: "FDA Pre-Submission" },
          { name: "Mechanism Citations", badge: "100% Provenance" },
          { name: "Patent Claims Draft", badge: "Novel IP Protected" },
          { name: "Clinical Protocol", badge: "Phase I Ready" }
        ],
        structuredItems: [
          { name: "FEU-EGFR-904", badge: "Novel Lead Molecule" },
          { name: "MW: 513.57 Da", badge: "C28H28FN7O2" },
          { name: "Quinazoline Core", badge: "Met793 H-Bond" },
          { name: "$2.8B Market", badge: "Commercial Target" }
        ],
        bridgeKey: "CLINICAL DOSSIER",
        svgMode: "act6"
      }
    ]
  };

  let currentDomain = 'fin';
  let currentActIndex = 0;
  let isPlaying = false;
  let playInterval = null;

  function renderSvgAnimation(mode, isMed) {
    const colorPrimary = isMed ? '#3DDC97' : '#FF9F0A';
    const colorSecondary = '#00F0FF';
    const colorAlert = '#FF453A';
    
    // Dynamic cinematic SVG generator
    return `
      <svg class="cinema-svg" viewBox="0 0 900 240" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="glowLineGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="${colorPrimary}" stop-opacity="0.2"/>
            <stop offset="50%" stop-color="${colorSecondary}" stop-opacity="1"/>
            <stop offset="100%" stop-color="${colorPrimary}" stop-opacity="0.2"/>
          </linearGradient>
          <filter id="cinemaGlowFilter" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="3" result="blur" />
            <feMerge>
              <feMergeNode in="blur" />
              <feMergeNode in="SourceGraphic" />
            </feMerge>
          </filter>
        </defs>

        <!-- GRID WIRES -->
        <line x1="120" y1="120" x2="380" y2="120" stroke="${colorSecondary}" stroke-width="2" stroke-dasharray="6,4" opacity="0.6">
          <animate attributeName="stroke-dashoffset" from="40" to="0" dur="2s" repeatCount="indefinite" />
        </line>
        <line x1="520" y1="120" x2="780" y2="120" stroke="${colorPrimary}" stroke-width="2" stroke-dasharray="6,4" opacity="0.6">
          <animate attributeName="stroke-dashoffset" from="0" to="40" dur="2s" repeatCount="indefinite" />
        </line>

        <!-- STREAM 1: UNSTRUCTURED HUB (LEFT) -->
        <g transform="translate(120, 120)">
          <circle r="46" fill="#0C1322" stroke="${colorPrimary}" stroke-width="2" filter="url(#cinemaGlowFilter)"/>
          <circle r="36" fill="none" stroke="${colorPrimary}" stroke-width="1" stroke-dasharray="4,3" opacity="0.7">
            <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="10s" repeatCount="indefinite"/>
          </circle>
          <text text-anchor="middle" dy="-8" fill="#FFFFFF" font-size="12" font-weight="800">${isMed ? 'LITERATURE' : 'UNSTRUCTURED'}</text>
          <text text-anchor="middle" dy="12" fill="${colorPrimary}" font-size="10" font-family="monospace">${isMed ? 'PubMed & Patents' : 'PDFs & SARs'}</text>
        </g>

        <!-- QUANTUM KEY BINDING BRIDGE (CENTER) -->
        <g transform="translate(450, 120)">
          <!-- Quantum orbital rings -->
          <circle r="52" fill="none" stroke="${colorSecondary}" stroke-width="1.5" stroke-dasharray="8,6" opacity="0.8">
            <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/>
          </circle>
          <circle r="42" fill="#060C17" stroke="#FFFFFF" stroke-width="2" filter="url(#cinemaGlowFilter)"/>
          <text text-anchor="middle" dy="-6" fill="#FFFFFF" font-size="12" font-weight="900">KEY BRIDGE</text>
          <text text-anchor="middle" dy="12" fill="${colorSecondary}" font-size="9.5" font-family="monospace" font-weight="700">${isMed ? 'P00533 | SMILES' : 'TAX_ID | IBAN'}</text>
          <!-- Energy discharge particles -->
          <circle cx="0" cy="-42" r="3" fill="#00F0FF">
            <animate attributeName="opacity" values="0.2;1;0.2" dur="1.2s" repeatCount="indefinite"/>
          </circle>
          <circle cx="0" cy="42" r="3" fill="#FF9F0A">
            <animate attributeName="opacity" values="1;0.2;1" dur="1.2s" repeatCount="indefinite"/>
          </circle>
        </g>

        <!-- STREAM 2: STRUCTURED HUB (RIGHT) -->
        <g transform="translate(780, 120)">
          <circle r="46" fill="#0C1322" stroke="${isMed ? '#3DDC97' : '#00F0FF'}" stroke-width="2" filter="url(#cinemaGlowFilter)"/>
          <circle r="36" fill="none" stroke="${isMed ? '#3DDC97' : '#00F0FF'}" stroke-width="1" stroke-dasharray="4,3" opacity="0.7">
            <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="10s" repeatCount="indefinite"/>
          </circle>
          <text text-anchor="middle" dy="-8" fill="#FFFFFF" font-size="12" font-weight="800">${isMed ? 'BIOASSAYS' : 'STRUCTURED'}</text>
          <text text-anchor="middle" dy="12" fill="${isMed ? '#3DDC97' : '#00F0FF'}" font-size="10" font-family="monospace">${isMed ? 'ChEMBL & PDB' : 'SQL & SWIFT'}</text>
        </g>

        <!-- DYNAMIC STAGE EFFECT -->
        ${mode === 'act5' ? `
          <!-- RADAR SWEEP BEAM -->
          <line x1="450" y1="120" x2="680" y2="40" stroke="${colorAlert}" stroke-width="3" filter="url(#cinemaGlowFilter)">
            <animateTransform attributeName="transform" type="rotate" from="0 450 120" to="360 450 120" dur="3s" repeatCount="indefinite"/>
          </line>
          <!-- ALERT TAG -->
          <rect x="360" y="20" width="180" height="26" rx="4" fill="${colorAlert}" fill-opacity="0.2" stroke="${colorAlert}" stroke-width="1"/>
          <text x="450" y="37" text-anchor="middle" fill="${colorAlert}" font-size="11" font-weight="900" letter-spacing="1">
            ${isMed ? 'MUTANT SELECTIVITY DETECTED' : 'CIRCULAR LAYERING RING DETECTED'}
          </text>
        ` : ''}

        ${mode === 'act6' ? `
          <!-- LEADERSHIP PULSING SHIELD -->
          <circle cx="450" cy="120" r="62" fill="none" stroke="#3DDC97" stroke-width="2" stroke-dasharray="5,5">
            <animate attributeName="r" values="52;75;52" dur="2s" repeatCount="indefinite"/>
            <animate attributeName="opacity" values="0.8;0;0.8" dur="2s" repeatCount="indefinite"/>
          </circle>
          <rect x="340" y="20" width="220" height="26" rx="4" fill="#3DDC97" fill-opacity="0.2" stroke="#3DDC97" stroke-width="1"/>
          <text x="450" y="37" text-anchor="middle" fill="#3DDC97" font-size="11" font-weight="900" letter-spacing="1">
            ${isMed ? 'NOVEL DRUG FEU-EGFR-904 VERIFIED' : '$14.25M AUDITED LAUNDERING DOSSIER'}
          </text>
        ` : ''}
      </svg>
    `;
  }

  function renderAct(actIndex, domain) {
    currentActIndex = actIndex;
    currentDomain = domain;
    const isMed = domain === 'med';
    const data = acts[domain][actIndex];

    // Update Act Cards
    document.querySelectorAll('.cinema-act-card').forEach((card, idx) => {
      if (idx === actIndex) {
        card.classList.add('active');
        if (isMed) { card.classList.add('med'); card.classList.remove('fin'); }
        else { card.classList.add('fin'); card.classList.remove('med'); }
      } else {
        card.classList.remove('active', 'fin', 'med');
      }
    });

    // Update Narration Box
    const narLead = document.getElementById('cinemaNarLead');
    const narSub = document.getElementById('cinemaNarSub');
    if (narLead) narLead.innerHTML = `<span style="color:#00F0FF;">${data.act}:</span> ${data.narrationTitle}`;
    if (narSub) narSub.textContent = data.narration;

    // Update Dual Stream Items
    const unstructContainer = document.getElementById('cinemaUnstructItems');
    if (unstructContainer && data.unstructuredItems) {
      unstructContainer.innerHTML = data.unstructuredItems.map(item => `
        <div class="cinema-data-item">
          <span>${item.name}</span>
          <span class="cinema-data-badge">${item.badge}</span>
        </div>
      `).join('');
    }

    const structContainer = document.getElementById('cinemaStructItems');
    if (structContainer && data.structuredItems) {
      structContainer.innerHTML = data.structuredItems.map(item => `
        <div class="cinema-data-item">
          <span>${item.name}</span>
          <span class="cinema-data-badge">${item.badge}</span>
        </div>
      `).join('');
    }

    // Update Bridge Hub Text
    const bridgeText = document.getElementById('cinemaBridgeText');
    if (bridgeText) bridgeText.textContent = data.bridgeKey;

    // Render Canvas SVG
    const canvasWrap = document.getElementById('cinemaCanvasWrap');
    if (canvasWrap) {
      canvasWrap.innerHTML = renderSvgAnimation(data.svgMode, isMed);
    }

    // Update Telemetry Inspector
    const inspNode = document.getElementById('cinemaInspNode');
    const inspType = document.getElementById('cinemaInspType');
    const inspProps = document.getElementById('cinemaInspProps');
    if (inspNode) inspNode.textContent = data.inspector.node;
    if (inspType) inspType.textContent = data.inspector.type;
    if (inspProps) inspProps.textContent = data.inspector.properties;

    // Update Tech Radar Nodes
    const techKeys = ['key', 'inputs', 'protege', 'chroma', 'neo4j', 'cypher', 'rag'];
    techKeys.forEach(t => {
      const el = document.getElementById('cinemaTech-' + t);
      if (el) {
        if (data.techLit.includes(t)) {
          el.classList.add('lit');
          if (isMed) { el.classList.add('med'); el.classList.remove('fin'); }
          else { el.classList.add('fin'); el.classList.remove('med'); }
        } else {
          el.classList.remove('lit', 'fin', 'med');
        }
      }
    });

    // Update Current Act Counter Label
    const actCounter = document.getElementById('cinemaCurrentActLabel');
    if (actCounter) actCounter.textContent = `${data.act} of VI: ${data.title}`;
  }

  window.cinemaSelectAct = function(actIdx) {
    renderAct(actIdx, currentDomain);
  };

  window.cinemaNextAct = function() {
    const next = (currentActIndex + 1) % 6;
    renderAct(next, currentDomain);
  };

  window.cinemaPrevAct = function() {
    const prev = (currentActIndex - 1 + 6) % 6;
    renderAct(prev, currentDomain);
  };

  window.cinemaTogglePlay = function() {
    const btn = document.getElementById('cinemaPlayBtn');
    if (!isPlaying) {
      isPlaying = true;
      if (btn) {
        btn.classList.add('active-play');
        btn.innerHTML = '<span>⏸</span> Pause Cinema Tour';
      }
      playInterval = setInterval(function() {
        cinemaNextAct();
      }, 5000);
    } else {
      isPlaying = false;
      if (btn) {
        btn.classList.remove('active-play');
        btn.innerHTML = '<span>▶</span> Auto-Play Cinema Tour';
      }
      clearInterval(playInterval);
      playInterval = null;
    }
  };

  window.cinemaSetDomain = function(domain) {
    currentDomain = domain;
    const btnFin = document.getElementById('cinemaTabFin');
    const btnMed = document.getElementById('cinemaTabMed');
    if (btnFin && btnMed) {
      if (domain === 'fin') {
        btnFin.classList.add('active', 'fin');
        btnMed.classList.remove('active', 'med');
      } else {
        btnMed.classList.add('active', 'med');
        btnFin.classList.remove('active', 'fin');
      }
    }
    renderAct(currentActIndex, domain);
  };

  window.cinemaToggleFullscreen = function() {
    const vp = document.getElementById('cinemaViewport');
    if (vp) {
      if (!document.fullscreenElement) {
        if (vp.requestFullscreen) vp.requestFullscreen();
      } else {
        if (document.exitFullscreen) document.exitFullscreen();
      }
    }
  };

  window.initCinema = function(defaultDomain) {
    if (defaultDomain) currentDomain = defaultDomain;
    cinemaSetDomain(currentDomain);
    renderAct(0, currentDomain);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initCinema('fin');
    });
  } else {
    setTimeout(function() {
      initCinema('fin');
    }, 150);
  }
})();
</script>
'''

# ---------------------------------------------------------------------------
# CINEMATIC COMPONENT HTML
# ---------------------------------------------------------------------------
def generate_cinema_html(default_domain='fin'):
    is_med = (default_domain == 'med')
    fin_class = "" if is_med else "active fin"
    med_class = "active med" if is_med else ""

    return f'''            <!-- ================= CINEMATIC ARCHITECTURE COMMAND CENTER ================= -->
            <div class="cinema-viewport" id="cinemaViewport">
              <div class="cinema-scanlines"></div>

              <!-- HUD TOP BAR -->
              <div class="cinema-hud-bar">
                <div class="cinema-hud-title">
                  <div class="cinema-hud-pulse-dot"></div>
                  <div>
                    <h3 class="cinema-title-text">
                      Holographic Architecture Command Center
                      <span class="cinema-eq">
                        <span class="cinema-eq-bar"></span>
                        <span class="cinema-eq-bar"></span>
                        <span class="cinema-eq-bar"></span>
                        <span class="cinema-eq-bar"></span>
                        <span class="cinema-eq-bar"></span>
                      </span>
                    </h3>
                    <p class="cinema-tagline">Cinematic multi-modal dataflow simulator uniting structured SQL/assays & unstructured PDFs/literature via the universal Key Binding Engine.</p>
                  </div>
                </div>

                <div class="cinema-actions">
                  <!-- Domain Mode Switcher -->
                  <div class="cinema-domain-pill">
                    <button type="button" id="cinemaTabFin" class="cinema-domain-tab {fin_class}" onclick="cinemaSetDomain('fin')">💳 Financial AML</button>
                    <button type="button" id="cinemaTabMed" class="cinema-domain-tab {med_class}" onclick="cinemaSetDomain('med')">🧬 Drug Discovery</button>
                  </div>

                  <!-- Cinema Playback -->
                  <button type="button" id="cinemaPlayBtn" class="cinema-btn active-play" onclick="cinemaTogglePlay()">
                    <span>▶</span> Auto-Play Cinema Tour
                  </button>
                  <button type="button" class="cinema-btn" onclick="cinemaPrevAct()">◀ Prev Act</button>
                  <button type="button" class="cinema-btn" onclick="cinemaNextAct()">Next Act ▶</button>
                  <button type="button" class="cinema-btn" onclick="cinemaToggleFullscreen()" title="Toggle Fullscreen">⛶ Theater</button>
                </div>
              </div>

              <!-- 6 CINEMATIC ACT BUTTONS -->
              <div class="cinema-acts-bar">
                <div class="cinema-act-card active fin" onclick="cinemaSelectAct(0)">
                  <div class="cinema-act-badge">Act I</div>
                  <div class="cinema-act-title">1. Document Ingress & Co-occurrence</div>
                </div>
                <div class="cinema-act-card" onclick="cinemaSelectAct(1)">
                  <div class="cinema-act-badge">Act II</div>
                  <div class="cinema-act-title">2. Relational Graph Weaving</div>
                </div>
                <div class="cinema-act-card" onclick="cinemaSelectAct(2)">
                  <div class="cinema-act-badge">Act III</div>
                  <div class="cinema-act-title">3. The Quantum Key Bridge</div>
                </div>
                <div class="cinema-act-card" onclick="cinemaSelectAct(3)">
                  <div class="cinema-act-badge">Act IV</div>
                  <div class="cinema-act-title">4. Multi-Modal Property Graph</div>
                </div>
                <div class="cinema-act-card" onclick="cinemaSelectAct(4)">
                  <div class="cinema-act-badge">Act V</div>
                  <div class="cinema-act-title">5. Cypher Pattern Radar</div>
                </div>
                <div class="cinema-act-card" onclick="cinemaSelectAct(5)">
                  <div class="cinema-act-badge">Act VI</div>
                  <div class="cinema-act-title">6. Executive Command Deliverable</div>
                </div>
              </div>

              <!-- THEATER STAGE: DUAL-STREAM DATA ENGINE & INTERACTIVE CANVAS -->
              <div class="cinema-stage">
                <div class="cinema-grid-bg"></div>

                <!-- DUAL STREAMS (STRUCTURED & UNSTRUCTURED) -->
                <div class="cinema-dual-streams">
                  
                  <!-- UNSTRUCTURED STREAM -->
                  <div class="cinema-stream-box unstructured">
                    <div class="cinema-stream-header">
                      <span style="font-size:12px; font-weight:800; color:#FFFFFF;">Unstructured Knowledge Stream</span>
                      <span class="cinema-stream-tag unstructured">PDFs · Text Chunks</span>
                    </div>
                    <div class="cinema-stream-items" id="cinemaUnstructItems">
                      <div class="cinema-data-item">
                        <span>SAR-2026-09.pdf</span>
                        <span class="cinema-data-badge">FinCEN Form 111</span>
                      </div>
                      <div class="cinema-data-item">
                        <span>Loan_App_482.pdf</span>
                        <span class="cinema-data-badge">Commercial Loan</span>
                      </div>
                      <div class="cinema-data-item">
                        <span>Whistleblower.eml</span>
                        <span class="cinema-data-badge">Internal Memo</span>
                      </div>
                    </div>
                  </div>

                  <!-- QUANTUM KEY BINDING BRIDGE -->
                  <div class="cinema-bridge-hub">
                    <div class="cinema-bridge-circle" onclick="cinemaSelectAct(2)">
                      <span>🔑</span>
                    </div>
                    <div class="cinema-bridge-label" id="cinemaBridgeText">CANONICAL BRIDGE</div>
                  </div>

                  <!-- STRUCTURED STREAM -->
                  <div class="cinema-stream-box structured">
                    <div class="cinema-stream-header">
                      <span style="font-size:12px; font-weight:800; color:#FFFFFF;">Structured Enterprise Stream</span>
                      <span class="cinema-stream-tag structured">SQL · Wires · Assays</span>
                    </div>
                    <div class="cinema-stream-items" id="cinemaStructItems">
                      <div class="cinema-data-item">
                        <span>acc_881920 (SQL)</span>
                        <span class="cinema-data-badge">$3.84M Balance</span>
                      </div>
                      <div class="cinema-data-item">
                        <span>wire_tx_59102</span>
                        <span class="cinema-data-badge">$485,000 USD</span>
                      </div>
                      <div class="cinema-data-item">
                        <span>OFAC_SDN_Match</span>
                        <span class="cinema-data-badge">Apex Global FZE</span>
                      </div>
                    </div>
                  </div>

                </div>

                <!-- ANIMATED SVG GRAPH CANVAS -->
                <div class="cinema-canvas-wrap" id="cinemaCanvasWrap">
                  <!-- Dynamically rendered by renderSvgAnimation -->
                </div>

                <!-- LIVE TELEMETRY INSPECTOR (CLICK ANY NODE) -->
                <div class="cinema-inspector">
                  <div>
                    <div class="cinema-inspector-title">
                      <span>📡 Active Node Telemetry HUD:</span>
                      <span id="cinemaInspNode" style="color:#FFFFFF;">SAR-2026-09.pdf</span>
                      <span id="cinemaInspType" style="font-size:10px; background:#1E293B; color:#94A3B8; padding:2px 6px; border-radius:3px;">FinCEN Form 111</span>
                    </div>
                    <div id="cinemaInspProps" class="cinema-inspector-body" style="margin-top:4px;">
                      mentions: ['Apex Global FZE', 'Vladimir S.'], cosine_similarity: 0.89 to Loan_App_482.pdf
                    </div>
                  </div>
                  <div style="font-size:11px; font-weight:700; color:#00F0FF; text-transform:uppercase; letter-spacing:0.05em;">
                    LIVE NEO4J PROVENANCE: 100% AUDITED
                  </div>
                </div>

              </div>

              <!-- MOVIE-STYLE NARRATION SUBTITLES (30-SECOND PITCH FOR EXECUTIVES) -->
              <div class="cinema-narration">
                <div id="cinemaNarLead" class="cinema-narration-lead">
                  <span style="color:#00F0FF;">Act I:</span> Ingesting Heterogeneous Unstructured Records
                </div>
                <p id="cinemaNarSub" class="cinema-narration-sub">
                  Raw compliance documents (FinCEN SAR PDFs, commercial loan agreements, whistleblower email threads) enter the pipeline with zero foreign keys. NLP entity extraction tags company names (Apex Global) and individuals (Vladimir S.), while ChromaDB vector embeddings map semantic similarities, weaving an initial document-to-document co-occurrence mesh.
                </p>
              </div>

              <!-- 7-TOOL TECH STACK HOLO-RADAR -->
              <div>
                <div style="font-size:11.5px; font-weight:800; color:#94A3B8; text-transform:uppercase; letter-spacing:0.05em; margin:16px 0 8px;">
                  Active Technology Stack Contribution Radar
                </div>
                <div class="cinema-tech-radar">
                  <!-- Mapping Key -->
                  <div class="cinema-tech-node lit fin" id="cinemaTech-key">
                    <div class="cinema-tech-ico">🔑</div>
                    <div class="cinema-tech-label">Mapping Key</div>
                    <div class="cinema-tech-role">Universal Bridge</div>
                  </div>
                  <!-- Multi-Source Inputs -->
                  <div class="cinema-tech-node lit fin" id="cinemaTech-inputs">
                    <div class="cinema-tech-ico">📥</div>
                    <div class="cinema-tech-label">Multi-Source Inputs</div>
                    <div class="cinema-tech-role">Ingestion Feeds</div>
                  </div>
                  <!-- Protégé OWL 2 -->
                  <div class="cinema-tech-node lit fin" id="cinemaTech-protege">
                    <div class="cinema-tech-ico">🦉</div>
                    <div class="cinema-tech-label">Protégé & OWL 2</div>
                    <div class="cinema-tech-role">Enterprise Ontology</div>
                  </div>
                  <!-- ChromaDB -->
                  <div class="cinema-tech-node lit fin" id="cinemaTech-chroma">
                    <div class="cinema-tech-ico">⚡</div>
                    <div class="cinema-tech-label">ChromaDB Store</div>
                    <div class="cinema-tech-role">Vector Similarity</div>
                  </div>
                  <!-- Neo4j -->
                  <div class="cinema-tech-node" id="cinemaTech-neo4j">
                    <div class="cinema-tech-ico">🕸️</div>
                    <div class="cinema-tech-label">Neo4j Graph DB</div>
                    <div class="cinema-tech-role">Multi-Modal Core</div>
                  </div>
                  <!-- Cypher -->
                  <div class="cinema-tech-node" id="cinemaTech-cypher">
                    <div class="cinema-tech-ico">🔍</div>
                    <div class="cinema-tech-label">Cypher Engine</div>
                    <div class="cinema-tech-role">Pattern Traversal</div>
                  </div>
                  <!-- Graph-RAG -->
                  <div class="cinema-tech-node" id="cinemaTech-rag">
                    <div class="cinema-tech-ico">🤖</div>
                    <div class="cinema-tech-label">Hybrid Graph-RAG</div>
                    <div class="cinema-tech-role">AI Synthesis</div>
                  </div>
                </div>
              </div>

            </div>
'''

# Replace existing simWidgetCard-fin with cinema component
if '<div class="sim-card" id="simWidgetCard-fin">' in html:
    start_fin = html.find('<div class="sim-card" id="simWidgetCard-fin">')
    # find ending </div> of simWidgetCard-fin
    end_fin = html.find('<!-- ========================================================================= -->\n            <div style="margin-top:32px;">\n              <div style="border-left:4px solid var(--amber);', start_fin)
    if end_fin != -1:
        cinema_html_fin = generate_cinema_html('fin')
        html = html[:start_fin] + cinema_html_fin + '\n\n            ' + html[end_fin:]
        print("Replaced simWidgetCard-fin with Cinematic Command Center.")

# Inject CSS and JS into index.html
if '.cinema-viewport' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>' + cinema_css + '</style>\n' + html[head_pos:]
        print("Added Cinematic CSS.")

if 'cinemaSelectAct' not in html:
    body_pos = html.rfind('</body>')
    if body_pos != -1:
        html = html[:body_pos] + cinema_js + '\n' + html[body_pos:]
        print("Added Cinematic JS Engine.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: Cinematic Command Center fully deployed into index.html!")
