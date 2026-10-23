# -*- coding: utf-8 -*-
"""
Injects interactive data snapshot buttons and visual data inspection panels
into each of the 6 cards in both Financial AML and Healthcare Drug Discovery.
Directly fulfills the user request:
"For each of the item could you please provide me the data snapshot for...
How Multiple Unstructured Data Map Within Each Other,
How Multiple Structured Data Map Within Each Other,
Unstructured-to-Structured Mapping via Mapping Keys,
Ultimate Joined Data Structure (Multi-Modal Property Graph) etc for others also.
I want to understand how the data looks like. Just put another button within each of the cards & after pressing I want to see how things are working by visualization of the data."
"""

import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ---------------------------------------------------------------------------
# CSS FOR DATA SNAPSHOT BUTTONS AND PANELS
# ---------------------------------------------------------------------------
snapshot_css = '''
    /* ================= DATA SNAPSHOT & VISUALIZATION PANELS ================= */
    .btn-snapshot-toggle {
      background: rgba(0, 240, 255, 0.1);
      border: 1.5px solid #00F0FF;
      color: #00F0FF;
      padding: 5px 13px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn-snapshot-toggle:hover {
      background: #00F0FF;
      color: #050811;
      box-shadow: 0 0 14px rgba(0, 240, 255, 0.5);
      transform: translateY(-1px);
    }
    .btn-snapshot-toggle.open {
      background: rgba(255, 159, 10, 0.2);
      border-color: #FF9F0A;
      color: #FF9F0A;
      box-shadow: 0 0 12px rgba(255, 159, 10, 0.35);
    }
    .btn-snapshot-toggle.med {
      background: rgba(61, 220, 151, 0.1);
      border-color: #3DDC97;
      color: #3DDC97;
    }
    .btn-snapshot-toggle.med:hover {
      background: #3DDC97;
      color: #050811;
      box-shadow: 0 0 14px rgba(61, 220, 151, 0.5);
    }
    .btn-snapshot-toggle.med.open {
      background: rgba(61, 220, 151, 0.25);
      border-color: #3DDC97;
      color: #3DDC97;
    }
    .snapshot-panel {
      background: #070B14;
      border: 1.5px solid #23314E;
      border-radius: 10px;
      padding: 18px;
      margin-top: 16px;
      box-shadow: inset 0 0 30px rgba(0,0,0,0.65), 0 8px 24px rgba(0,0,0,0.35);
      animation: snapSlideDown 0.25s ease-out;
    }
    @keyframes snapSlideDown {
      from { opacity: 0; transform: translateY(-8px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .snapshot-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 14px;
      padding-bottom: 10px;
      border-bottom: 1px solid #1E293B;
    }
    .snapshot-head-title {
      font-size: 13px;
      font-weight: 800;
      color: #00F0FF;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .snapshot-head-title.med {
      color: #3DDC97;
    }
    .snapshot-head-tag {
      font-size: 10.5px;
      font-family: var(--mono, monospace);
      background: #141E33;
      color: #94A3B8;
      padding: 3px 8px;
      border-radius: 4px;
    }
    .snapshot-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    @media (max-width: 860px) {
      .snapshot-grid { grid-template-columns: 1fr; }
    }
    .snapshot-col-box {
      background: #0B101D;
      border: 1px solid #1E2A42;
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
    }
    .snapshot-col-title {
      font-size: 11px;
      font-weight: 800;
      color: #94A3B8;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .snapshot-code-block {
      background: #04070F;
      border: 1px solid #141E33;
      border-radius: 6px;
      padding: 10px;
      font-family: var(--mono, monospace);
      font-size: 11px;
      color: #E2E8F0;
      line-height: 1.5;
      overflow-x: auto;
      max-height: 250px;
      margin: 0;
      flex-grow: 1;
    }
    .snapshot-graph-vis {
      background: #04070F;
      border: 1px solid #141E33;
      border-radius: 6px;
      padding: 14px;
      flex-grow: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
    }
    .snapshot-mechanics-footer {
      margin-top: 12px;
      padding: 10px 14px;
      background: rgba(0, 240, 255, 0.05);
      border-left: 3px solid #00F0FF;
      border-radius: 4px;
      font-size: 11.5px;
      color: #CBD5E1;
      line-height: 1.5;
    }
    .snapshot-mechanics-footer.med {
      background: rgba(61, 220, 151, 0.05);
      border-left-color: #3DDC97;
    }
'''

# ---------------------------------------------------------------------------
# JAVASCRIPT TOGGLE FUNCTION
# ---------------------------------------------------------------------------
snapshot_js = '''
<script>
window.toggleDataSnapshot = function(panelId, btnElement) {
  const panel = document.getElementById(panelId);
  if (!panel) return;
  const isHidden = (panel.style.display === 'none' || panel.style.display === '');
  if (isHidden) {
    panel.style.display = 'block';
    if (btnElement) {
      btnElement.classList.add('open');
      btnElement.innerHTML = '<span>✕</span> Hide Data Snapshot ▲';
    }
  } else {
    panel.style.display = 'none';
    if (btnElement) {
      btnElement.classList.remove('open');
      btnElement.innerHTML = '<span>📊</span> View Data Snapshot & Visual Graph ▼';
    }
  }
};
</script>
'''

# ---------------------------------------------------------------------------
# PANELS GENERATORS FOR AML & DRUG DISCOVERY
# ---------------------------------------------------------------------------

# AML Step 1
panel_aml_1 = '''
                  <div id="snapshot-aml-1" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title"><span>📊</span> STEP 1 DATA SNAPSHOT: Unstructured Ingress & Entity Bridge</div>
                      <span class="snapshot-head-tag">FORMAT: JSON Payload & NLP Co-Occurrence Graph</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Raw Document Data & Extracted NLP Entities</div>
                        <pre class="snapshot-code-block">{
  "document_id": "SAR-2026-09.pdf",
  "filing_agency": "FinCEN Form 111",
  "narrative_text": "Customer Vladimir S. directed wire of $485,000 to offshore entity Apex Global Logistics FZE, referencing invoice INV-8819 for maritime consulting.",
  "extracted_entities": [
    { "text": "Vladimir S.", "label": "PERSON", "role": "UBO" },
    { "text": "Apex Global Logistics FZE", "label": "ORG", "jurisdiction": "UAE" },
    { "text": "INV-8819", "label": "INVOICE_ID" }
  ],
  "chroma_vector_sample": [0.0381, -0.1492, 0.4018, 0.2219, -0.0891, "...(384 floats)"],
  "cross_doc_linkage": {
    "cites_document": "Loan_App_482.pdf",
    "cosine_similarity": 0.892,
    "shared_entities": ["Apex Global Logistics FZE", "Vladimir S."]
  }
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Doc 1 -->
                            <rect x="20" y="20" width="100" height="40" rx="6" fill="#1A2234" stroke="#FF9F0A" stroke-width="1.5"/>
                            <text x="70" y="44" fill="#FFFFFF" font-size="10" font-weight="700" text-anchor="middle">SAR-2026-09.pdf</text>
                            <!-- Doc 2 -->
                            <rect x="20" y="110" width="100" height="40" rx="6" fill="#1A2234" stroke="#FF9F0A" stroke-width="1.5"/>
                            <text x="70" y="134" fill="#FFFFFF" font-size="10" font-weight="700" text-anchor="middle">Loan_App_482.pdf</text>
                            <!-- Shared Entity Bridge -->
                            <circle cx="260" cy="85" r="32" fill="#0E192D" stroke="#00F0FF" stroke-width="2"/>
                            <text x="260" y="82" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">Apex Global</text>
                            <text x="260" y="95" fill="#00F0FF" font-size="8" text-anchor="middle">Logistics FZE</text>
                            <!-- Arrows -->
                            <line x1="120" y1="40" x2="230" y2="75" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="4,2"/>
                            <text x="175" y="48" fill="#00F0FF" font-size="8" font-family="monospace">[:MENTIONS]</text>
                            <line x1="120" y1="130" x2="230" y2="95" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="4,2"/>
                            <text x="175" y="125" fill="#00F0FF" font-size="8" font-family="monospace">[:MENTIONS]</text>
                            <!-- Similarity Edge -->
                            <path d="M 40,60 Q 5,85 40,110" fill="none" stroke="#3DDC97" stroke-width="1.5" stroke-dasharray="3,3"/>
                            <text x="35" y="88" fill="#3DDC97" font-size="7.5" font-family="monospace">cos: 0.89</text>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer">
                      <strong>⚙️ What Happens in the Engine:</strong> spaCy NER and LLM extraction scan the text for entities and case tags. When two separate documents mention <em>Apex Global Logistics FZE</em>, Neo4j builds an instant co-occurrence bridge: <code style="color:#00F0FF;">(SAR)-[:MENTIONS]->(Entity)<-[:MENTIONS]-(LoanApp)</code>. ChromaDB confirms semantic similarity (<code style="color:#3DDC97;">0.892</code>).
                    </div>
                  </div>'''

# AML Step 2
panel_aml_2 = '''
                  <div id="snapshot-aml-2" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title"><span>📊</span> STEP 2 DATA SNAPSHOT: Structured Relational-to-Graph Joins</div>
                      <span class="snapshot-head-tag">FORMAT: SQL Records & Graph Edges</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Core Banking SQL & SWIFT MT103 Feeds</div>
                        <pre class="snapshot-code-block">-- SQL Core Banking Table: accounts
{
  "account_id": 881920,
  "iban": "GB29NWBK60161331926819",
  "holder_name": "Apex Global Logistics FZE",
  "account_type": "COMMERCIAL_CHECKING",
  "balance_usd": 3840000.00,
  "opened_date": "2023-01-15",
  "status": "ACTIVE"
}

-- SWIFT MT103 Wire Message Record
{
  "wire_id": "W109",
  "sender_iban": "GB29NWBK60161331926819",
  "receiver_iban": "CY94BCYP00010000481920",
  "amount_usd": 485000.00,
  "currency": "USD",
  "timestamp": "2026-04-12T10:14:00Z",
  "swift_uetr": "f81d4fae-7dec-11d0-a765-00a0c91e6bf6"
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Account A -->
                            <rect x="20" y="65" width="105" height="45" rx="6" fill="#1A2234" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="72" y="85" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">Account GB29...</text>
                            <text x="72" y="99" fill="#3DDC97" font-size="8.5" font-family="monospace" text-anchor="middle">$3,840,000.00</text>
                            <!-- Account B -->
                            <rect x="250" y="65" width="105" height="45" rx="6" fill="#1A2234" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="302" y="85" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">Account CY94...</text>
                            <text x="302" y="99" fill="#3DDC97" font-size="8.5" font-family="monospace" text-anchor="middle">Intermediary Shell</text>
                            <!-- Wire Edge -->
                            <line x1="125" y1="87" x2="250" y2="87" stroke="#FF9F0A" stroke-width="2"/>
                            <polygon points="250,87 242,83 242,91" fill="#FF9F0A"/>
                            <text x="187" y="78" fill="#FF9F0A" font-size="8" font-family="monospace" text-anchor="middle">[:TRANSFERRED]</text>
                            <text x="187" y="103" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">$485,000 USD</text>
                            <!-- Device Node -->
                            <circle cx="72" cy="150" r="18" fill="#0B1320" stroke="#00F0FF" stroke-width="1.5"/>
                            <text x="72" y="153" fill="#00F0FF" font-size="7.5" font-weight="700" text-anchor="middle">Device</text>
                            <line x1="72" y1="110" x2="72" y2="132" stroke="#00F0FF" stroke-width="1" stroke-dasharray="2,2"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer">
                      <strong>⚙️ What Happens in the Engine:</strong> Relational SQL foreign keys are transformed into first-class graph relationships. Instead of performing slow relational table joins, Neo4j creates an indexed physical edge: <code style="color:#FF9F0A;">(AccA)-[:TRANSFERRED {amount_usd: 485000, wire_id: 'W109'}]->(AccB)</code>.
                    </div>
                  </div>'''

# AML Step 3
panel_aml_3 = '''
                  <div id="snapshot-aml-3" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title"><span>📊</span> STEP 3 DATA SNAPSHOT: Unstructured-to-Structured Key Binding</div>
                      <span class="snapshot-head-tag">FORMAT: Extraction JSON & Cypher MERGE</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Key Extraction & Cypher Binding Script</div>
                        <pre class="snapshot-code-block">// 1. Extracted Canonical Key Payload
{
  "source_chunk": "CHK-8812 (SAR-2026-09 page 3)",
  "extracted_key_type": "Account_IBAN",
  "canonical_value": "GB29NWBK60161331926819",
  "confidence_score": 0.964,
  "fraud_flag": "Suspicious Structuring & Layering"
}

// 2. Executed Cypher MERGE Command
MATCH (acc:Account {iban: "GB29NWBK60161331926819"})
MATCH (chunk:TextChunk {chunk_id: "CHK-8812"})
MERGE (chunk)-[r:EVIDENCE_FOR {
    confidence: 0.964,
    extracted_key: "Account_IBAN",
    key_value: "GB29NWBK60161331926819",
    flagged_typology: "Structuring & Layering",
    timestamp: datetime("2026-04-15T08:30:00Z")
}]->(acc)
RETURN r.confidence, acc.iban;</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Left: TextChunk -->
                            <rect x="15" y="55" width="115" height="55" rx="6" fill="#141E33" stroke="#FF9F0A" stroke-width="1.5"/>
                            <text x="72" y="75" fill="#FF9F0A" font-size="8.5" font-weight="800" text-anchor="middle">TextChunk #8812</text>
                            <text x="72" y="90" fill="#E2E8F0" font-size="7.5" text-anchor="middle">"Admitted intent to..."</text>
                            <text x="72" y="102" fill="#94A3B8" font-size="7" font-family="monospace" text-anchor="middle">SAR-2026-09 (p.3)</text>
                            <!-- Center: Golden Key -->
                            <circle cx="190" cy="82" r="22" fill="#0C1322" stroke="#FFD700" stroke-width="2"/>
                            <text x="190" y="87" fill="#FFD700" font-size="16" text-anchor="middle">🔑</text>
                            <!-- Right: Account Node -->
                            <rect x="250" y="55" width="115" height="55" rx="6" fill="#0E1E2E" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="307" y="75" fill="#3DDC97" font-size="8.5" font-weight="800" text-anchor="middle">Account Node #881</text>
                            <text x="307" y="90" fill="#FFFFFF" font-size="7.5" font-family="monospace" text-anchor="middle">GB29NWBK...</text>
                            <text x="307" y="102" fill="#3DDC97" font-size="7" font-weight="700" text-anchor="middle">Balance: $3.84M</text>
                            <!-- Binding Line -->
                            <line x1="130" y1="82" x2="168" y2="82" stroke="#FFD700" stroke-width="2"/>
                            <line x1="212" y1="82" x2="250" y2="82" stroke="#FFD700" stroke-width="2"/>
                            <text x="190" y="125" fill="#00F0FF" font-size="8" font-weight="700" text-anchor="middle">[:EVIDENCE_FOR {conf: 0.96}]</text>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer">
                      <strong>⚙️ What Happens in the Engine:</strong> Canonical business mapping keys (IBAN, Tax_ID) bridge the gap. The Cypher query welds the qualitative suspicion in the PDF text directly to the quantitative bank ledger.
                    </div>
                  </div>'''

# AML Step 4
panel_aml_4 = '''
                  <div id="snapshot-aml-4" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title"><span>📊</span> STEP 4 DATA SNAPSHOT: Multi-Modal Property Graph Topology</div>
                      <span class="snapshot-head-tag">FORMAT: Neo4j JSON Graph Structure</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Unified Multi-Modal Graph Data Serialization</div>
                        <pre class="snapshot-code-block">{
  "graph": {
    "nodes": [
      { "id": "402", "labels": ["Customer", "UBO"], "props": { "name": "Vladimir S.", "tax_id": "XX-XXX9102" } },
      { "id": "403", "labels": ["ShellCompany"], "props": { "name": "Apex Global FZE", "risk": "CRITICAL" } },
      { "id": "404", "labels": ["Account"], "props": { "iban": "GB29NWBK...", "balance": 3840000.00 } },
      { "id": "405", "labels": ["Device"], "props": { "mac": "00-14-22-E4-5A-11", "ip": "194.26.29.50" } },
      { "id": "406", "labels": ["TextChunk"], "props": { "text": "Admitted intent...", "page": 3 } }
    ],
    "relationships": [
      { "type": "BENEFICIAL_OWNER", "start": "402", "end": "403", "props": { "share_pct": 65.0 } },
      { "type": "OWNS_ACCOUNT", "start": "403", "end": "404", "props": { "role": "primary" } },
      { "type": "ACCESSED_FROM", "start": "404", "end": "405", "props": { "session": "LOGIN_90" } },
      { "type": "EVIDENCE_FOR", "start": "406", "end": "404", "props": { "confidence": 0.96 } }
    ]
  }
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- UBO -->
                            <circle cx="60" cy="45" r="20" fill="#141E33" stroke="#FF9F0A" stroke-width="1.5"/>
                            <text x="60" y="48" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">Vladimir S.</text>
                            <!-- Shell Co -->
                            <rect x="150" y="25" width="80" height="35" rx="5" fill="#141E33" stroke="#FF9F0A" stroke-width="1.5"/>
                            <text x="190" y="46" fill="#FF9F0A" font-size="8" font-weight="700" text-anchor="middle">Apex Shell FZE</text>
                            <!-- Account -->
                            <circle cx="190" cy="115" r="22" fill="#0C1D2A" stroke="#3DDC97" stroke-width="2"/>
                            <text x="190" y="117" fill="#3DDC97" font-size="8" font-weight="800" text-anchor="middle">Account</text>
                            <!-- Device -->
                            <circle cx="310" cy="115" r="18" fill="#0B1320" stroke="#00F0FF" stroke-width="1.5"/>
                            <text x="310" y="118" fill="#00F0FF" font-size="7.5" text-anchor="middle">Device</text>
                            <!-- Chunk -->
                            <rect x="40" y="125" width="70" height="30" rx="4" fill="#1C1824" stroke="#A78BFA" stroke-width="1.5"/>
                            <text x="75" y="143" fill="#A78BFA" font-size="7.5" font-weight="700" text-anchor="middle">SAR Chunk</text>
                            <!-- Connectors -->
                            <line x1="80" y1="45" x2="150" y2="45" stroke="#FF9F0A" stroke-width="1.5"/>
                            <line x1="190" y1="60" x2="190" y2="93" stroke="#3DDC97" stroke-width="1.5"/>
                            <line x1="212" y1="115" x2="292" y2="115" stroke="#00F0FF" stroke-width="1.5"/>
                            <line x1="110" y1="130" x2="168" y2="120" stroke="#A78BFA" stroke-width="1.5" stroke-dasharray="3,2"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer">
                      <strong>⚙️ What Happens in the Engine:</strong> The unified multi-modal graph unites enterprise relational entities and unstructured evidence into an interconnected property model. Every transaction node carries its full legal provenance.
                    </div>
                  </div>'''

# AML Step 5
panel_aml_5 = '''
                  <div id="snapshot-aml-5" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title"><span>📊</span> STEP 5 DATA SNAPSHOT: Cypher Circular Layering Ring Detection</div>
                      <span class="snapshot-head-tag">FORMAT: Cypher Query & Circular Result Set</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Executed Cypher Pattern & Query Output</div>
                        <pre class="snapshot-code-block">// Recursive Multi-Hop Layering Pattern Query
MATCH path = (origin:Account)-[wires:TRANSFERRED*3..6]->(origin)
WHERE ALL(i IN range(0, size(wires)-2) WHERE 
    duration.inDays(wires[i].timestamp, wires[i+1].timestamp).days <= 3 
    AND abs(wires[i].amount_usd - wires[i+1].amount_usd) / wires[i].amount_usd < 0.12)
RETURN origin.iban AS origin_account, 
       [w IN wires | w.amount_usd] AS transfer_amounts, 
       [w IN wires | w.wire_id] AS wire_ids,
       length(path) AS cycle_hops;

// Query Result Table
{
  "origin_account": "GB29NWBK60161331926819",
  "transfer_amounts": [485000.00, 475000.00, 460000.00, 455000.00],
  "wire_ids": ["W109", "W114", "W121", "W135"],
  "cycle_hops": 4,
  "elapsed_time_hours": 38.4,
  "typology_match": "CIRCULAR_LAYERING_RING"
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Loop Node A -->
                            <circle cx="80" cy="50" r="22" fill="#2A0B0B" stroke="#FF453A" stroke-width="2"/>
                            <text x="80" y="53" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle">Acc A ($485k)</text>
                            <!-- Loop Node B -->
                            <circle cx="300" cy="50" r="22" fill="#2A0B0B" stroke="#FF453A" stroke-width="2"/>
                            <text x="300" y="53" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle">Acc B ($475k)</text>
                            <!-- Loop Node C -->
                            <circle cx="300" cy="130" r="22" fill="#2A0B0B" stroke="#FF453A" stroke-width="2"/>
                            <text x="300" y="133" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle">Acc C ($460k)</text>
                            <!-- Loop Node D -->
                            <circle cx="80" cy="130" r="22" fill="#2A0B0B" stroke="#FF453A" stroke-width="2"/>
                            <text x="80" y="133" fill="#FFFFFF" font-size="8" font-weight="800" text-anchor="middle">Acc D ($455k)</text>
                            <!-- Flow Lines -->
                            <line x1="102" y1="50" x2="278" y2="50" stroke="#FF453A" stroke-width="2"/>
                            <polygon points="278,50 270,46 270,54" fill="#FF453A"/>
                            <line x1="300" y1="72" x2="300" y2="108" stroke="#FF453A" stroke-width="2"/>
                            <polygon points="300,108 296,100 304,100" fill="#FF453A"/>
                            <line x1="278" y1="130" x2="102" y2="130" stroke="#FF453A" stroke-width="2"/>
                            <polygon points="102,130 110,126 110,134" fill="#FF453A"/>
                            <line x1="80" y1="108" x2="80" y2="72" stroke="#FF453A" stroke-width="2"/>
                            <polygon points="80,72 76,80 84,80" fill="#FF453A"/>
                            <!-- Center Alert -->
                            <rect x="140" y="78" width="100" height="24" rx="4" fill="#FF453A" fill-opacity="0.2" stroke="#FF453A" stroke-width="1"/>
                            <text x="190" y="94" fill="#FF453A" font-size="8.5" font-weight="900" text-anchor="middle">4-HOP RING DETECTED</text>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer">
                      <strong>⚙️ What Happens in the Engine:</strong> Cypher natively evaluates arbitrary-depth recursive graph paths <code style="color:#FF453A;">[:TRANSFERRED*3..6]</code> with temporal constraints. SQL takes hours or crashes; Cypher finishes in under 12 milliseconds.
                    </div>
                  </div>'''

# AML Step 6
panel_aml_6 = '''
                  <div id="snapshot-aml-6" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title"><span>📊</span> STEP 6 DATA SNAPSHOT: Executive Leadership Deliverables</div>
                      <span class="snapshot-head-tag">FORMAT: FinCEN Form 111 XML & Asset Freeze Ledger</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Pre-Populated FinCEN SAR XML & Asset Ledger</div>
                        <pre class="snapshot-code-block">&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;FinCEN_SAR_Filing package_id="SAR-2026-09-FINAL"&gt;
  &lt;Summary&gt;
    &lt;QuantifiedExposure currency="USD"&gt;14250000.00&lt;/QuantifiedExposure&gt;
    &lt;IdentifiedLayeringRings count="3"&gt;Ring_Alpha, Ring_Beta, Ring_Gamma&lt;/IdentifiedLayeringRings&gt;
    &lt;PrimaryBeneficialOwner tax_id="XX-XXX9102" passport="CY-482910"&gt;Vladimir S.&lt;/PrimaryBeneficialOwner&gt;
    &lt;EngagedShellCompanies&gt;
      &lt;Company name="Apex Global Logistics FZE" jurisdiction="UAE"/&gt;
      &lt;Company name="BlueStar Trading Limited" jurisdiction="Cyprus"/&gt;
    &lt;/EngagedShellCompanies&gt;
  &lt;/Summary&gt;
  &lt;ImmediateEnforcementAction&gt;
    &lt;AccountsFrozen count="4" total_preserved_usd="3840000.00"/&gt;
    &lt;RegulatoryPenaltyExposureMitigated value="$50M+"/&gt;
    &lt;GraphAuditLineage root_node="402" total_provenance_hops="6"/&gt;
  &lt;/ImmediateEnforcementAction&gt;
&lt;/FinCEN_SAR_Filing&gt;</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Executive Card -->
                            <rect x="25" y="15" width="330" height="150" rx="8" fill="#0C1424" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="190" y="38" fill="#3DDC97" font-size="11" font-weight="900" text-anchor="middle">BOARDROOM AUDIT DOSSIER</text>
                            <!-- Metric 1 -->
                            <rect x="45" y="55" width="135" height="42" rx="4" fill="#141E33" stroke="#23314E"/>
                            <text x="55" y="70" fill="#94A3B8" font-size="7.5">TOTAL EXPOSURE</text>
                            <text x="55" y="87" fill="#FF453A" font-size="12" font-weight="900">$14,250,000.00</text>
                            <!-- Metric 2 -->
                            <rect x="200" y="55" width="135" height="42" rx="4" fill="#141E33" stroke="#23314E"/>
                            <text x="210" y="70" fill="#94A3B8" font-size="7.5">FROZEN ASSETS PRESERVED</text>
                            <text x="210" y="87" fill="#3DDC97" font-size="12" font-weight="900">$3,840,000.00</text>
                            <!-- Status bar -->
                            <rect x="45" y="110" width="290" height="35" rx="4" fill="#13231B" stroke="#3DDC97" stroke-width="1"/>
                            <text x="190" y="125" fill="#FFFFFF" font-size="8.5" font-weight="700" text-anchor="middle">FinCEN SAR Package Ready · 100% Mathematically Audited</text>
                            <text x="190" y="137" fill="#3DDC97" font-size="8" text-anchor="middle">Vladimir S. & Apex Shell Indictment Docket Compiled</text>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer">
                      <strong>⚙️ What Happens in the Engine:</strong> Hybrid Graph-RAG aggregates graph metrics into a legally defensible briefing where every finding is cited with node IDs, timestamps, and SWIFT hashes.
                    </div>
                  </div>'''

# Inject AML panels and buttons
aml_replacements = [
    ('1. How Multiple Unstructured Data Map Within Each Other</span>', 1, panel_aml_1),
    ('2. How Multiple Structured Data Map Within Each Other</span>', 2, panel_aml_2),
    ('3. Unstructured-to-Structured Mapping via Mapping Keys</span>', 3, panel_aml_3),
    ('4. Ultimate Joined Data Structure (Multi-Modal Property Graph)</span>', 4, panel_aml_4),
    ('5. How Pattern Recognition Works Here</span>', 5, panel_aml_5),
    ('6. What Exactly You Provide to Leadership (Executive Deliverables)</span>', 6, panel_aml_6),
]

for title_marker, step_num, panel_code in aml_replacements:
    btn_html = f'''<button type="button" class="btn-snapshot-toggle" onclick="toggleDataSnapshot('snapshot-aml-{step_num}', this)"><span>📊</span> View Data Snapshot & Visual Graph ▼</button>'''
    
    # Locate step in HTML
    pos = html.find(title_marker)
    if pos != -1:
        # Find closing </div> of header
        header_end = html.find('</div>', pos)
        if header_end != -1 and f'snapshot-aml-{step_num}' not in html:
            html = html[:header_end] + '\n                    ' + btn_html + html[header_end:]
            print(f"Added AML Step {step_num} Button.")

        # Find closing </div> of the card
        # Next step or next section
        next_step_str = f'<!-- STEP {step_num + 1} -->' if step_num < 6 else '</div>\n            </div>\n\n          </div>'
        card_end = html.find(next_step_str, pos)
        if card_end != -1:
            closing_div = html.rfind('</div>', pos, card_end)
            if closing_div != -1 and f'snapshot-aml-{step_num}' not in html:
                html = html[:closing_div] + panel_code + '\n                ' + html[closing_div:]
                print(f"Added AML Step {step_num} Panel.")

# Inject CSS and JS
if '.btn-snapshot-toggle' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>' + snapshot_css + '</style>\n' + html[head_pos:]
        print("Injected Snapshot CSS.")

if 'toggleDataSnapshot' not in html:
    body_pos = html.rfind('</body>')
    if body_pos != -1:
        html = html[:body_pos] + snapshot_js + '\n' + html[body_pos:]
        print("Injected Snapshot JS Engine.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html updated with AML Data Snapshot Buttons and Panels!")


# ---------------------------------------------------------------------------
# DRUG DISCOVERY PANELS GENERATORS (STEPS 1 TO 6)
# ---------------------------------------------------------------------------

# Med Step 1
panel_med_1 = '''
                  <div id="snapshot-med-1" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title med"><span>📊</span> STEP 1 DATA SNAPSHOT: Biomedical Literature & BioNER Graph</div>
                      <span class="snapshot-head-tag">FORMAT: PubMed XML Payload & BioNER Graph</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> PubMed Abstract Data & BioBERT Extracted Entities</div>
                        <pre class="snapshot-code-block">{
  "document_id": "PMID:38192044",
  "journal": "Nature Oncology 2026",
  "title": "Overcoming Osimertinib Resistance via Allosteric Kinase Modulation",
  "abstract_snippet": "...observed acquired tertiary mutation C797S in EGFR exon 20 abrogating covalent bond formation with Osimertinib. Novel aminopyrimidine derivatives show potent nanomolar inhibition in H1975 cell models...",
  "bioner_entities": [
    { "text": "EGFR", "type": "GENE_PROTEIN", "hgnc_id": "HGNC:3236" },
    { "text": "C797S", "type": "MUTATION", "exon": 20 },
    { "text": "Osimertinib", "type": "SMALL_MOLECULE", "chembl_id": "CHEMBL3353410" },
    { "text": "H1975", "type": "CELL_LINE", "depmap_id": "ACH-000570" }
  ],
  "pubchem_mesh_terms": ["Carcinoma, Non-Small-Cell Lung", "Protein Kinase Inhibitors"],
  "vector_embedding_sample": [-0.0192, 0.3204, 0.1192, -0.4521, "...(768 floats)"]
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Paper 1 -->
                            <rect x="20" y="20" width="110" height="40" rx="6" fill="#141E33" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="75" y="44" fill="#FFFFFF" font-size="9" font-weight="700" text-anchor="middle">PMID: 38192044</text>
                            <!-- Preprint 2 -->
                            <rect x="20" y="110" width="110" height="40" rx="6" fill="#141E33" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="75" y="134" fill="#FFFFFF" font-size="9" font-weight="700" text-anchor="middle">bioRxiv: 2026.04</text>
                            <!-- Target Gene Node -->
                            <circle cx="260" cy="85" r="32" fill="#0C1D2A" stroke="#00F0FF" stroke-width="2"/>
                            <text x="260" y="82" fill="#FFFFFF" font-size="10" font-weight="800" text-anchor="middle">EGFR</text>
                            <text x="260" y="95" fill="#3DDC97" font-size="8" text-anchor="middle">Mutant: C797S</text>
                            <!-- Arrows -->
                            <line x1="130" y1="40" x2="230" y2="75" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="4,2"/>
                            <text x="180" y="48" fill="#00F0FF" font-size="8" font-family="monospace">[:MENTIONS]</text>
                            <line x1="130" y1="130" x2="230" y2="95" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="4,2"/>
                            <text x="180" y="125" fill="#00F0FF" font-size="8" font-family="monospace">[:MENTIONS]</text>
                            <!-- Citation Edge -->
                            <path d="M 40,60 Q 5,85 40,110" fill="none" stroke="#FF9F0A" stroke-width="1.5" stroke-dasharray="3,3"/>
                            <text x="35" y="88" fill="#FF9F0A" font-size="7.5" font-family="monospace">cites</text>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer med">
                      <strong>⚙️ What Happens in the Engine:</strong> BioBERT extracts gene targets, mutations, and chemical entities. Papers describing the C797S resistance mutation are connected to a shared target node, and PubMedBERT vectors link corroborating clinical findings across international research teams.
                    </div>
                  </div>'''

# Med Step 2
panel_med_2 = '''
                  <div id="snapshot-med-2" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title med"><span>📊</span> STEP 2 DATA SNAPSHOT: Structured Assays & 3D Crystallography</div>
                      <span class="snapshot-head-tag">FORMAT: ChEMBL Assays & PDB Coordinates</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> ChEMBL Bioassay & PDB Active Pocket Data</div>
                        <pre class="snapshot-code-block">-- ChEMBL High-Throughput Bioactivity Record
{
  "assay_id": 182904,
  "target_chembl_id": "CHEMBL203",
  "target_name": "Epidermal growth factor receptor (EGFR)",
  "standard_type": "IC50",
  "standard_value": 1.8,
  "standard_units": "nM",
  "cell_line": "Ba/F3 EGFR-L858R/T790M/C797S"
}

-- PDB 3D Crystallographic Pocket (PDB: 6S9B)
{
  "pdb_id": "6S9B",
  "resolution_angstrom": 1.85,
  "binding_pocket": {
    "hinge_residue_1": { "name": "Met793", "interaction": "H-Bond Donor" },
    "catalytic_residue": { "name": "Lys745", "interaction": "Salt Bridge" },
    "mutation_site": { "name": "Ser797", "distance_to_warhead_a": 3.8 }
  }
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Small Molecule -->
                            <rect x="15" y="65" width="115" height="45" rx="6" fill="#141E33" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="72" y="85" fill="#3DDC97" font-size="8.5" font-weight="800" text-anchor="middle">FEU-EGFR-904</text>
                            <text x="72" y="99" fill="#FFFFFF" font-size="7.5" font-family="monospace" text-anchor="middle">MW: 513.57 Da</text>
                            <!-- Target -->
                            <rect x="250" y="65" width="115" height="45" rx="6" fill="#0E192D" stroke="#00F0FF" stroke-width="1.5"/>
                            <text x="307" y="85" fill="#FFFFFF" font-size="9" font-weight="800" text-anchor="middle">EGFR (UniProt:P00533)</text>
                            <text x="307" y="99" fill="#00F0FF" font-size="8" text-anchor="middle">Variant: C797S</text>
                            <!-- Binding Edge -->
                            <line x1="130" y1="87" x2="250" y2="87" stroke="#3DDC97" stroke-width="2"/>
                            <polygon points="250,87 242,83 242,91" fill="#3DDC97"/>
                            <text x="190" y="78" fill="#3DDC97" font-size="8" font-family="monospace" text-anchor="middle">[:BINDS_TO]</text>
                            <text x="190" y="103" fill="#FFFFFF" font-size="8" font-weight="700" text-anchor="middle">IC50 = 1.8 nM</text>
                            <!-- Pocket Node -->
                            <circle cx="307" cy="148" r="18" fill="#1A1828" stroke="#A78BFA" stroke-width="1.5"/>
                            <text x="307" y="151" fill="#A78BFA" font-size="7.5" font-weight="700" text-anchor="middle">PDB 6S9B</text>
                            <line x1="307" y1="110" x2="307" y2="130" stroke="#A78BFA" stroke-width="1" stroke-dasharray="2,2"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer med">
                      <strong>⚙️ What Happens in the Engine:</strong> Relational bioassays and PDB crystal structures are transformed into a molecular graph. The small molecule is physically connected to the protein active site with quantitative binding affinity properties (<code style="color:#3DDC97;">ic50_nm: 1.8</code>).
                    </div>
                  </div>'''

# Med Step 3
panel_med_3 = '''
                  <div id="snapshot-med-3" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title med"><span>📊</span> STEP 3 DATA SNAPSHOT: Bio Key Binding (Literature to Chemistry)</div>
                      <span class="snapshot-head-tag">FORMAT: Extraction JSON & Cypher MERGE</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Bio-Key Extraction & Cypher Binding Script</div>
                        <pre class="snapshot-code-block">// 1. Extracted Biomedical Mapping Keys
{
  "source_chunk": "PMID:38192044 (page 4, paragraph 2)",
  "extracted_keys": {
    "uniprot_accession": "P00533",
    "target_gene": "EGFR",
    "pdb_active_pocket": "6S9B",
    "candidate_inchikey": "XUIAKVIZZGOCFP-UHFFFAOYSA-N"
  },
  "reported_claim": "Selective inhibition of triple-mutant EGFR over wild-type"
}

// 2. Executed Cypher MERGE Command
MATCH (target:Target {uniprot_id: "P00533"})
MATCH (mol:SmallMolecule {inchikey: "XUIAKVIZZGOCFP-UHFFFAOYSA-N"})
MATCH (chunk:TextChunk {chunk_id: "PMID_38192044_CHK4"})
MERGE (chunk)-[r:REPORTS_INHIBITION {
    ic50_nm: 1.8,
    cell_line: "H1975",
    mutation: "C797S",
    confidence: 0.982
}]->(target)
MERGE (chunk)-[:VALIDATES_MOLECULE]->(mol);</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Left: Paper Chunk -->
                            <rect x="15" y="55" width="115" height="55" rx="6" fill="#141E33" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="72" y="75" fill="#3DDC97" font-size="8.5" font-weight="800" text-anchor="middle">Paper Chunk #4</text>
                            <text x="72" y="90" fill="#E2E8F0" font-size="7.5" text-anchor="middle">"Inhibited double mutant"</text>
                            <text x="72" y="102" fill="#94A3B8" font-size="7" font-family="monospace" text-anchor="middle">PMID: 38192044</text>
                            <!-- Center: Bio Key -->
                            <circle cx="190" cy="82" r="22" fill="#0C1322" stroke="#00F0FF" stroke-width="2"/>
                            <text x="190" y="87" fill="#00F0FF" font-size="16" text-anchor="middle">🔑</text>
                            <!-- Right: Target Protein Node -->
                            <rect x="250" y="55" width="115" height="55" rx="6" fill="#0E192D" stroke="#00F0FF" stroke-width="1.5"/>
                            <text x="307" y="75" fill="#00F0FF" font-size="8.5" font-weight="800" text-anchor="middle">Target Protein</text>
                            <text x="307" y="90" fill="#FFFFFF" font-size="7.5" font-family="monospace" text-anchor="middle">UniProt: P00533</text>
                            <text x="307" y="102" fill="#3DDC97" font-size="7" font-weight="700" text-anchor="middle">EGFR L858R/C797S</text>
                            <!-- Binding Line -->
                            <line x1="130" y1="82" x2="168" y2="82" stroke="#00F0FF" stroke-width="2"/>
                            <line x1="212" y1="82" x2="250" y2="82" stroke="#00F0FF" stroke-width="2"/>
                            <text x="190" y="125" fill="#3DDC97" font-size="8" font-weight="700" text-anchor="middle">[:REPORTS_INHIBITION {ic50: 1.8nM}]</text>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer med">
                      <strong>⚙️ What Happens in the Engine:</strong> Canonical bio-accessions (UniProt, InChIKey) ground textual literature to physical compounds and receptors. Published claims are cross-validated with in-vitro wet lab readouts.
                    </div>
                  </div>'''

# Med Step 4
panel_med_4 = '''
                  <div id="snapshot-med-4" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title med"><span>📊</span> STEP 4 DATA SNAPSHOT: Multi-Modal Biomedical Property Graph</div>
                      <span class="snapshot-head-tag">FORMAT: Neo4j Graph Data Model</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Unified Biomedical Graph JSON Serialization</div>
                        <pre class="snapshot-code-block">{
  "biomedical_graph": {
    "nodes": [
      { "id": "101", "labels": ["SmallMolecule", "Lead"], "props": { "id": "FEU-EGFR-904", "mw": 513.57, "clogp": 3.12 } },
      { "id": "102", "labels": ["Target", "Kinase"], "props": { "uniprot": "P00533", "gene": "EGFR", "variant": "C797S" } },
      { "id": "103", "labels": ["BindingPocket"], "props": { "pdb": "6S9B", "hinge": "Met793", "vol_a3": 840.5 } },
      { "id": "104", "labels": ["Disease"], "props": { "name": "Non-Small Cell Lung Carcinoma", "doid": "3908" } },
      { "id": "105", "labels": ["AdverseEvent"], "props": { "term": "QT Prolongation", "meddra": "10037660" } }
    ],
    "relationships": [
      { "type": "POTENT_INHIBITOR", "start": "101", "end": "102", "props": { "ic50_nm": 1.8, "selectivity": 180.0 } },
      { "type": "BONDS_POCKET", "start": "101", "end": "103", "props": { "bond_type": "H-Bond", "kcal_mol": -8.4 } },
      { "type": "DRIVES_PATHOLOGY", "start": "102", "end": "104", "props": { "causal_score": 0.98 } },
      { "type": "AVOIDS_TOXICITY", "start": "101", "end": "105", "props": { "herg_ic50_nm": 12500 } }
    ]
  }
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- SmallMolecule -->
                            <rect x="20" y="65" width="95" height="40" rx="5" fill="#141E33" stroke="#3DDC97" stroke-width="2"/>
                            <text x="67" y="85" fill="#3DDC97" font-size="8" font-weight="800" text-anchor="middle">FEU-EGFR-904</text>
                            <text x="67" y="96" fill="#FFFFFF" font-size="7" text-anchor="middle">Small Molecule</text>
                            <!-- Target -->
                            <circle cx="200" cy="85" r="24" fill="#0E192D" stroke="#00F0FF" stroke-width="2"/>
                            <text x="200" y="83" fill="#FFFFFF" font-size="8.5" font-weight="800" text-anchor="middle">EGFR</text>
                            <text x="200" y="94" fill="#00F0FF" font-size="7.5" text-anchor="middle">C797S Mutant</text>
                            <!-- Disease -->
                            <rect x="270" y="25" width="95" height="35" rx="5" fill="#1A1828" stroke="#A78BFA" stroke-width="1.5"/>
                            <text x="317" y="46" fill="#A78BFA" font-size="7.5" font-weight="700" text-anchor="middle">NSCLC (Lung)</text>
                            <!-- Toxicity Node -->
                            <circle cx="67" cy="145" r="16" fill="#1F1616" stroke="#FF9F0A" stroke-width="1.5"/>
                            <text x="67" y="148" fill="#FF9F0A" font-size="7" text-anchor="middle">hERG Safe</text>
                            <!-- Edges -->
                            <line x1="115" y1="85" x2="176" y2="85" stroke="#3DDC97" stroke-width="1.5"/>
                            <line x1="222" y1="75" x2="270" y2="50" stroke="#00F0FF" stroke-width="1.5"/>
                            <line x1="67" y1="105" x2="67" y2="129" stroke="#FF9F0A" stroke-width="1.5" stroke-dasharray="2,2"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer med">
                      <strong>⚙️ What Happens in the Engine:</strong> Chemistry, target genomics, structural biology, and patient disease ontologies are modeled in one unified graph, enabling multi-disciplinary drug discovery queries in milliseconds.
                    </div>
                  </div>'''

# Med Step 5
panel_med_5 = '''
                  <div id="snapshot-med-5" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title med"><span>📊</span> STEP 5 DATA SNAPSHOT: Multi-Objective Kinase Selectivity Cypher</div>
                      <span class="snapshot-head-tag">FORMAT: Cypher Query & Tabular Results</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Executed Kinase Selectivity Query & Results</div>
                        <pre class="snapshot-code-block">// Multi-Objective Optimization Cypher Query
MATCH (mol:SmallMolecule)-[r_mut:POTENT_INHIBITOR]->(mutant:Target {gene: "EGFR", variant: "C797S"})
MATCH (mol)-[r_wt:POTENT_INHIBITOR]->(wt:Target {gene: "EGFR", variant: "WildType"})
OPTIONAL MATCH (mol)-[r_herg:POTENT_INHIBITOR]->(herg:Target {gene: "KCNH2"})
WHERE r_mut.value_nm < 10.0 
  AND (r_wt.value_nm / r_mut.value_nm) >= 50.0 
  AND (r_herg IS NULL OR r_herg.value_nm > 5000.0)
RETURN mol.chembl_id AS lead_id, 
       r_mut.value_nm AS mutant_ic50_nm, 
       (r_wt.value_nm / r_mut.value_nm) AS wt_selectivity_ratio,
       r_herg.value_nm AS herg_safety_nm;

// Query Result Table
{
  "lead_id": "FEU-EGFR-904",
  "mutant_ic50_nm": 1.8,
  "wt_selectivity_ratio": 180.0,
  "herg_safety_nm": 12500.0,
  "cardiotoxicity_risk": "ZERO",
  "therapeutic_window": "EXCELLENT"
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Lead -->
                            <rect x="20" y="65" width="100" height="45" rx="6" fill="#141E33" stroke="#3DDC97" stroke-width="2"/>
                            <text x="70" y="85" fill="#3DDC97" font-size="8.5" font-weight="800" text-anchor="middle">FEU-EGFR-904</text>
                            <text x="70" y="99" fill="#FFFFFF" font-size="7.5" text-anchor="middle">Lead Molecule</text>
                            <!-- Target 1: Mutant (Green) -->
                            <circle cx="280" cy="40" r="20" fill="#0B2618" stroke="#3DDC97" stroke-width="2"/>
                            <text x="280" y="38" fill="#3DDC97" font-size="7.5" font-weight="800" text-anchor="middle">C797S Mut</text>
                            <text x="280" y="49" fill="#FFFFFF" font-size="7" text-anchor="middle">IC50: 1.8 nM</text>
                            <!-- Target 2: WT (Amber) -->
                            <circle cx="280" cy="90" r="20" fill="#261C0B" stroke="#FF9F0A" stroke-width="1.5"/>
                            <text x="280" y="88" fill="#FF9F0A" font-size="7.5" font-weight="800" text-anchor="middle">WT EGFR</text>
                            <text x="280" y="99" fill="#FFFFFF" font-size="7" text-anchor="middle">180x Selective</text>
                            <!-- Target 3: hERG (Blue Safe) -->
                            <circle cx="280" cy="140" r="20" fill="#0B1C26" stroke="#00F0FF" stroke-width="1.5"/>
                            <text x="280" y="138" fill="#00F0FF" font-size="7.5" font-weight="800" text-anchor="middle">hERG Channel</text>
                            <text x="280" y="149" fill="#FFFFFF" font-size="7" text-anchor="middle">>10,000 nM</text>
                            <!-- Directed Arrows -->
                            <line x1="120" y1="75" x2="260" y2="45" stroke="#3DDC97" stroke-width="2"/>
                            <line x1="120" y1="87" x2="260" y2="90" stroke="#FF9F0A" stroke-width="1.5"/>
                            <line x1="120" y1="100" x2="260" y2="135" stroke="#00F0FF" stroke-width="1.5" stroke-dasharray="3,3"/>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer med">
                      <strong>⚙️ What Happens in the Engine:</strong> Cypher simultaneously filters for high nanomolar mutant potency (<code style="color:#3DDC97;">1.8 nM</code>), broad therapeutic window over wild-type (<code style="color:#FF9F0A;">180x</code>), and zero cardiotoxicity (<code style="color:#00F0FF;">>10,000 nM</code>).
                    </div>
                  </div>'''

# Med Step 6
panel_med_6 = '''
                  <div id="snapshot-med-6" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title med"><span>📊</span> STEP 6 DATA SNAPSHOT: R&D Executive Dossier & Lead Synthesis</div>
                      <span class="snapshot-head-tag">FORMAT: IND Lead Dossier & Chemical Recipe</span>
                    </div>
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> Novel Drug Synthesis Recipe & Regulatory Dossier</div>
                        <pre class="snapshot-code-block">{
  "drug_discovery_dossier": {
    "lead_candidate_name": "FEU-EGFR-904",
    "chemical_formula": "C28H28FN7O2",
    "molecular_weight": 513.57,
    "canonical_smiles": "CC1=C(C=C(C=C1)NC2=NC=C3C(=N2)N(C=N3)C4CCC(CC4)N)C(=O)NC5=CC(=C(C=C5)F)NC(=O)C=C",
    "target_disease": "Osimertinib-Resistant Non-Small Cell Lung Cancer",
    "active_site_recipe": [
      { "component": "Aminopyrimidine Core", "mechanism": "Dual H-bonds to Met793 hinge & Lys745 salt bridge" },
      { "component": "Cyclobutane Acrylamide", "mechanism": "Altered spatial angle traps Lys745, bypassing C797S clash" },
      { "component": "Fluorophenyl Arm", "mechanism": "Blocks CYP3A4 metabolism, 78% oral bioavailability" }
    ],
    "commercial_impact": {
      "timeline_compression": "18 months down to 6 weeks",
      "addressable_global_market": "$2.8B USD",
      "readiness": "Phase I Trial Candidate Formulation Ready"
    }
  }
}</pre>
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          <svg viewBox="0 0 380 180" width="100%" height="160">
                            <!-- Executive Card -->
                            <rect x="25" y="15" width="330" height="150" rx="8" fill="#0C1820" stroke="#3DDC97" stroke-width="1.5"/>
                            <text x="190" y="38" fill="#3DDC97" font-size="11" font-weight="900" text-anchor="middle">CSO DRUG DISCOVERY DOSSIER</text>
                            <!-- Molecule 1 -->
                            <rect x="45" y="55" width="135" height="42" rx="4" fill="#141E33" stroke="#23314E"/>
                            <text x="55" y="70" fill="#94A3B8" font-size="7.5">LEAD CANDIDATE</text>
                            <text x="55" y="87" fill="#3DDC97" font-size="12" font-weight="900">FEU-EGFR-904</text>
                            <!-- Metric 2 -->
                            <rect x="200" y="55" width="135" height="42" rx="4" fill="#141E33" stroke="#23314E"/>
                            <text x="210" y="70" fill="#94A3B8" font-size="7.5">MARKET OPPORTUNITY</text>
                            <text x="210" y="87" fill="#00F0FF" font-size="12" font-weight="900">$2.8B USD</text>
                            <!-- Status bar -->
                            <rect x="45" y="110" width="290" height="35" rx="4" fill="#12251D" stroke="#3DDC97" stroke-width="1"/>
                            <text x="190" y="125" fill="#FFFFFF" font-size="8.5" font-weight="700" text-anchor="middle">Hit-to-Lead Compressed: 18 Months ➔ 6 Weeks</text>
                            <text x="190" y="137" fill="#3DDC97" font-size="8" text-anchor="middle">Chemical Synthesis Recipe Formulated & Tested In-Silico</text>
                          </svg>
                        </div>
                      </div>
                    </div>
                    <div class="snapshot-mechanics-footer med">
                      <strong>⚙️ What Happens in the Engine:</strong> Hybrid Graph-RAG generates the complete discovery dossier with chemical formulas, 3D binding active-site recipes, and preclinical validation metrics with 100% provenance back to underlying PDB crystal coordinates.
                    </div>
                  </div>'''

# Inject Drug Discovery panels and buttons
med_replacements = [
    ('1. How Multiple Unstructured Biomedical Data Map Within Each Other</span>', 1, panel_med_1),
    ('2. How Multiple Structured Life Sciences Data Map Within Each Other</span>', 2, panel_med_2),
    ('3. Unstructured-to-Structured Mapping via Biomedical Mapping Keys</span>', 3, panel_med_3),
    ('4. Ultimate Joined Data Structure (Biomedical Knowledge Graph)</span>', 4, panel_med_4),
    ('5. How Pattern Recognition Works Here</span>', 5, panel_med_5),
    ('6. What Exactly You Provide to Leadership (Executive Deliverables)</span>', 6, panel_med_6),
]

for title_marker, step_num, panel_code in med_replacements:
    btn_html = f'''<button type="button" class="btn-snapshot-toggle med" onclick="toggleDataSnapshot('snapshot-med-{step_num}', this)"><span>📊</span> View Data Snapshot & Visual Graph ▼</button>'''
    
    pos = html.find(title_marker)
    if pos != -1:
        header_end = html.find('</div>', pos)
        if header_end != -1 and f'snapshot-med-{step_num}' not in html:
            html = html[:header_end] + '\n                    ' + btn_html + html[header_end:]
            print(f"Added Med Step {step_num} Button.")

        next_step_str = f'<!-- STEP {step_num + 1} -->' if step_num < 6 else '</div>\n            </div>\n\n          </div>'
        card_end = html.find(next_step_str, pos)
        if card_end != -1:
            closing_div = html.rfind('</div>', pos, card_end)
            if closing_div != -1 and f'snapshot-med-{step_num}' not in html:
                html = html[:closing_div] + panel_code + '\n                ' + html[closing_div:]
                print(f"Added Med Step {step_num} Panel.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully updated with both AML and Drug Discovery Data Snapshot Buttons and Panels!")
