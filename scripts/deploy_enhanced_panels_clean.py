# -*- coding: utf-8 -*-
"""
Clean, self-contained deployment script that enhances all 12 Data Snapshot Panels with:
- Required Tools & Tech Stack Strip (Neo4j, Protégé, ChromaDB, Cypher, etc.)
- Formatted Input Data Snapshot Table (HTML table)
- Formatted Output Data Snapshot Table (HTML table)
- Raw Data Payload & Query Code (JSON/Cypher/SQL <pre>)
- Visual Graph Representation (SVG diagram)
- Mechanics explanation footer
"""

import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load original panels from inject_snapshots_into_cards.py
with open('scripts/inject_snapshots_into_cards.py', 'r', encoding='utf-8') as f:
    orig_code = f.read()

lines = orig_code.splitlines()
code_aml = "\n".join(lines[26:576])
code_med = "\n".join(lines[629:995])

scope = {}
exec(code_aml, scope)
exec(code_med, scope)

def extract_svg(panel_html):
    m = re.search(r'(<svg[\s\S]*?</svg>)', panel_html)
    return m.group(1) if m else ''

def extract_pre(panel_html):
    m = re.search(r'(<pre[\s\S]*?</pre>)', panel_html)
    return m.group(1) if m else ''

def extract_footer(panel_html):
    m = re.search(r'<div class="snapshot-mechanics-footer[^"]*">([\s\S]*?)</div>', panel_html)
    return m.group(1).strip() if m else ''

def build_panel(panel_id, title_text, format_badge, tech_pills, in_tbl, out_tbl, raw_pre, raw_title, svg_code, footer_text, is_med=False):
    theme_cls = " med" if is_med else ""
    pill_html = "".join([f'<div class="snapshot-tech-pill{theme_cls}"><span>{icon}</span><strong>{name}:</strong> {role}</div>' for icon, name, role in tech_pills])

    return f'''<div id="{panel_id}" class="snapshot-panel" style="display:none;">
                    <div class="snapshot-head">
                      <div class="snapshot-head-title{theme_cls}"><span>📊</span> {title_text}</div>
                      <span class="snapshot-format-badge{theme_cls}">{format_badge}</span>
                    </div>

                    <!-- 1. REQUIRED TOOLS & TECH STACK STRIP -->
                    <div class="snapshot-tech-bar">
                      <div class="snapshot-tech-bar-title">🛠️ REQUIRED TOOLS & TECH STACK TO SUPPORT THIS STEP:</div>
                      <div class="snapshot-tech-pills">
                        {pill_html}
                      </div>
                    </div>

                    <!-- 2. DATA SNAPSHOT TABLES (INPUT VS OUTPUT) -->
                    <div class="snapshot-tables-container">
                      <!-- INPUT TABLE -->
                      <div class="snapshot-table-box">
                        <div class="snapshot-table-title{theme_cls}"><span>📥</span> INPUT DATA SNAPSHOT (Raw Feeds & Sources)</div>
                        <div class="snapshot-table-wrapper">
                          {in_tbl}
                        </div>
                      </div>

                      <!-- OUTPUT TABLE -->
                      <div class="snapshot-table-box">
                        <div class="snapshot-table-title{theme_cls}"><span>📤</span> OUTPUT DATA SNAPSHOT (Transformed & Mapped Results)</div>
                        <div class="snapshot-table-wrapper">
                          {out_tbl}
                        </div>
                      </div>
                    </div>

                    <!-- 3. RAW PAYLOAD & VISUAL GRAPH REPRESENTATION -->
                    <div class="snapshot-grid">
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>📄</span> {raw_title}</div>
                        {raw_pre}
                      </div>
                      <div class="snapshot-col-box">
                        <div class="snapshot-col-title"><span>🕸️</span> Visual Graph Representation (How it Works)</div>
                        <div class="snapshot-graph-vis">
                          {svg_code}
                        </div>
                      </div>
                    </div>

                    <!-- 4. MECHANICS FOOTER -->
                    <div class="snapshot-mechanics-footer{theme_cls}">
                      {footer_text}
                    </div>
                  </div>'''

# CSS Enhancements
enhanced_css = '''
    /* ================= ENHANCED TABLE SNAPSHOTS & TECH STACKS ================= */
    .snapshot-tech-bar {
      background: #080E1C;
      border: 1px solid #1E2D4A;
      border-radius: 8px;
      padding: 12px 14px;
      margin-bottom: 16px;
    }
    .snapshot-tech-bar-title {
      font-size: 11px;
      font-weight: 800;
      color: #94A3B8;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .snapshot-tech-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .snapshot-tech-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #0D172B;
      border: 1px solid #243556;
      border-radius: 6px;
      padding: 5px 11px;
      font-size: 11px;
      color: #E2E8F0;
      line-height: 1.4;
    }
    .snapshot-tech-pill strong {
      color: #00F0FF;
    }
    .snapshot-tech-pill.med strong {
      color: #3DDC97;
    }
    .snapshot-tables-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 16px;
    }
    @media (max-width: 1024px) {
      .snapshot-tables-container {
        grid-template-columns: 1fr;
      }
    }
    .snapshot-table-box {
      background: #090E1A;
      border: 1px solid #1E293B;
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
    }
    .snapshot-table-title {
      font-size: 11.5px;
      font-weight: 800;
      color: #00F0FF;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .snapshot-table-title.med {
      color: #3DDC97;
    }
    .snapshot-table-wrapper {
      overflow-x: auto;
      max-height: 280px;
      border-radius: 6px;
      border: 1px solid #1A253A;
    }
    .snapshot-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      font-family: var(--mono, monospace);
      text-align: left;
    }
    .snapshot-table th {
      background: #0E1726;
      color: #00F0FF;
      padding: 7px 10px;
      font-weight: 700;
      border-bottom: 1px solid #23314E;
      position: sticky;
      top: 0;
      z-index: 2;
      font-size: 10px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .snapshot-table.med th {
      color: #3DDC97;
    }
    .snapshot-table td {
      padding: 7px 10px;
      border-bottom: 1px solid #141E33;
      color: #CBD5E1;
      vertical-align: middle;
      line-height: 1.4;
    }
    .snapshot-table tr:nth-child(even) td {
      background: rgba(255, 255, 255, 0.015);
    }
    .snapshot-table tr:hover td {
      background: rgba(0, 240, 255, 0.05);
    }
    .snapshot-table.med tr:hover td {
      background: rgba(61, 220, 151, 0.05);
    }
    .table-tag {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 9.5px;
      font-weight: 700;
      white-space: nowrap;
    }
    .tag-cyan { background: rgba(0, 240, 255, 0.15); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.3); }
    .tag-green { background: rgba(61, 220, 151, 0.15); color: #3DDC97; border: 1px solid rgba(61, 220, 151, 0.3); }
    .tag-amber { background: rgba(255, 159, 10, 0.15); color: #FF9F0A; border: 1px solid rgba(255, 159, 10, 0.3); }
    .tag-rose { background: rgba(255, 69, 58, 0.15); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.3); }
    .tag-purple { background: rgba(191, 90, 242, 0.15); color: #BF5AF2; border: 1px solid rgba(191, 90, 242, 0.3); }
'''

# AML Panels Data
aml_data = [
    # AML Step 1
    (1, "STEP 1 DATA SNAPSHOT: Unstructured Ingress & Entity Bridge", "FORMAT: JSON Payload & NLP Co-Occurrence Graph",
     [
         ("🔍", "spaCy & GLiNER", "Domain NER extracting Person, Organization, Shell Corp, Jurisdiction from PDFs & emails"),
         ("🔮", "ChromaDB Vector Store", "Dense 384-d semantic embedding index; links texts by cosine similarity (>0.84)"),
         ("🏛️", "Protégé & OWL 2", "Financial Industry Business Ontology (FIBO) classifying legal entity types"),
         ("⚡", "FastCoref / LLM Coref", "Cross-document coreference resolution reconciling alias names ('the borrower' == 'Apex')")
     ],
     '''<table class="snapshot-table">
  <thead><tr><th>Document ID</th><th>Doc Type</th><th>Raw Text Narrative Snippet</th><th>Extracted NLP Entities</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-cyan">SAR-2026-09.pdf</span></td><td>FinCEN 111</td><td>"Customer Vladimir S. directed wire of $485k to Apex Global Logistics FZE ref INV-8819."</td><td><span class="table-tag tag-amber">Vladimir S. (PERSON)</span>, <span class="table-tag tag-purple">Apex Global (ORG)</span></td></tr>
    <tr><td><span class="table-tag tag-cyan">LoanApp-482.pdf</span></td><td>Commercial Loan</td><td>"Apex Global Logistics FZE listed Vladimir S. as 100% beneficial owner (UBO)."</td><td><span class="table-tag tag-purple">Apex Global (BORROWER)</span>, <span class="table-tag tag-amber">Vladimir S. (UBO)</span></td></tr>
    <tr><td><span class="table-tag tag-cyan">Email-Thread-14</span></td><td>Compliance Memo</td><td>"URGENT: Subpoena ref FINCEN-CASE-4412 received regarding shell accounts in Dubai."</td><td><span class="table-tag tag-rose">FINCEN-CASE-4412 (REF)</span>, <span class="table-tag tag-cyan">Dubai (LOC)</span></td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table">
  <thead><tr><th>Source Doc</th><th>Mapping Layer</th><th>Target Document / Entity Bridge</th><th>Constructed Graph Relationship</th></tr></thead>
  <tbody>
    <tr><td>SAR-2026-09.pdf</td><td>Named Entity Co-Occurrence</td><td>LoanApp-482.pdf (Shared: Vladimir S.)</td><td><span class="table-tag tag-cyan">[:CO_OCCURS_WITH {confidence: 0.98}]</span></td></tr>
    <tr><td>SAR-2026-09.pdf</td><td>ChromaDB Vector Similarity</td><td>LoanApp-482.pdf (Layering Typology Match)</td><td><span class="table-tag tag-green">[:SEMANTIC_SIMILAR {cosine: 0.892}]</span></td></tr>
    <tr><td>Email-Thread-14</td><td>Explicit Citation Parsing</td><td>SAR-2026-09.pdf (Tag: FINCEN-CASE-4412)</td><td><span class="table-tag tag-amber">[:CITES_CASE {ref: 'FINCEN-CASE-4412'}]</span></td></tr>
    <tr><td>LoanApp-482.pdf</td><td>Cross-Doc Coreference</td><td>Email-Thread-14 ('the shell company' -> Apex)</td><td><span class="table-tag tag-purple">[:COREFERENCE_RESOLVED {prob: 0.95}]</span></td></tr>
  </tbody>
</table>''',
     "RAW DOCUMENT DATA & EXTRACTED NLP ENTITIES"),

    # AML Step 2
    (2, "STEP 2 DATA SNAPSHOT: Core Banking SQL & SWIFT Transactions", "FORMAT: Relational SQL Tables & SWIFT MT103 Feeds",
     [
         ("🗄️", "PostgreSQL / Oracle DB", "Core banking OLTP tables: accounts, corporate customers, balance ledgers"),
         ("📨", "SWIFT MT103 / ISO 20022", "Parses structured financial wire telegrams (Field 50K Ordering, Field 59 Beneficiary)"),
         ("🏛️", "Protégé & OWL 2 Ontology", "Standardizes disparate bank relational schemas into unified FIBO properties"),
         ("⚙️", "dbt / Apache Spark", "Cleanses, normalizes currency exchange rates to USD, and deduplicates customer Tax IDs")
     ],
     '''<table class="snapshot-table">
  <thead><tr><th>Table Source</th><th>Primary Key</th><th>Attributes / Columns</th><th>Sample Row Values</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-cyan">core_banking.accounts</span></td><td>ACC-001</td><td>cust_id, iban, currency, balance</td><td>CUST-901, GB29NWBK60161331926819, GBP, £412,000</td></tr>
    <tr><td><span class="table-tag tag-cyan">core_banking.customers</span></td><td>CUST-901</td><td>name, tax_id, risk_rating, kyc_status</td><td>Vladimir S., GB-77218-A, HIGH_RISK, VERIFIED</td></tr>
    <tr><td><span class="table-tag tag-green">swift_ledger.mt103</span></td><td>WIRE-109</td><td>sender_iban, receiver_iban, amount, ts</td><td>GB29NWBK.., AE44EBIL60161331920000, $485,000, 2026-10-12</td></tr>
    <tr><td><span class="table-tag tag-green">swift_ledger.mt103</span></td><td>WIRE-114</td><td>sender_iban, receiver_iban, amount, ts</td><td>AE44EBIL.., CH93SBIN00001122334455, $475,000, 2026-10-13</td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table">
  <thead><tr><th>Composite Join Key</th><th>Left Table (Source)</th><th>Right Table (Target)</th><th>Mapped Relational Transaction Flow</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-amber">cust_id: CUST-901</span></td><td>core_banking.customers</td><td>core_banking.accounts</td><td>Vladimir S. holds Account GB29NWBK (Balance: $520,000)</td></tr>
    <tr><td><span class="table-tag tag-amber">iban: GB29NWBK..</span></td><td>core_banking.accounts</td><td>swift_ledger.mt103</td><td>Account initiated Outward SWIFT Wire W109 ($485,000.00 USD)</td></tr>
    <tr><td><span class="table-tag tag-amber">iban: AE44EBIL..</span></td><td>swift_ledger.mt103</td><td>core_banking.companies</td><td>Wire W109 credited to Apex Global Logistics FZE (Dubai)</td></tr>
    <tr><td><span class="table-tag tag-amber">iban: CH93SBIN..</span></td><td>swift_ledger.mt103</td><td>swiss_canton.accounts</td><td>Second-hop wire W114 transferred $475k to Meridian FZE (Geneva)</td></tr>
  </tbody>
</table>''',
     "CORE BANKING SQL & SWIFT MT103 FEEDS"),

    # AML Step 3
    (3, "STEP 3 DATA SNAPSHOT: Unstructured-to-Structured Mapping Key Resolution", "FORMAT: Key Normalization Script & Cypher Transaction",
     [
         ("🔑", "Deterministic / Fuzzy Normalizer", "Reconciles unstructured textual entity strings to canonical relational DB keys"),
         ("🏛️", "Protégé & OWL 2", "Validates semantic typing: maps strings to fibo-fnd:LegalEntity and fibo-sec:BeneficialOwner"),
         ("🌐", "Neo4j Property Graph DB", "Executes MERGE statements creating typed edges connecting documents directly to SQL nodes"),
         ("⚡", "Cypher Ingestion Pipeline", "Declarative transactional commits binding unstructured citations with zero SQL table lock")
     ],
     '''<table class="snapshot-table">
  <thead><tr><th>Extracted Text Entity (Unstructured)</th><th>Source Document</th><th>Target SQL Table</th><th>Resolved DB Composite Key</th><th>Match Score</th></tr></thead>
  <tbody>
    <tr><td>"Vladimir S."</td><td>SAR-2026-09.pdf</td><td>core_banking.customers</td><td><span class="table-tag tag-amber">tax_id: GB-77218-A</span></td><td><span class="table-tag tag-green">1.00 (Exact)</span></td></tr>
    <tr><td>"Apex Global Logistics"</td><td>LoanApp-482.pdf</td><td>core_banking.companies</td><td><span class="table-tag tag-purple">reg_lei: 5493001KJTIIG</span></td><td><span class="table-tag tag-green">0.97 (Fuzzy)</span></td></tr>
    <tr><td>"INV-8819 ($485k wire)"</td><td>Compliance Memo</td><td>swift_ledger.mt103</td><td><span class="table-tag tag-cyan">wire_ref: W109</span></td><td><span class="table-tag tag-green">1.00 (Exact)</span></td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table">
  <thead><tr><th>Unstructured Source Node</th><th>Generated Graph Edge</th><th>Structured Target Node</th><th>Binding Cypher Action</th></tr></thead>
  <tbody>
    <tr><td>(Doc:SAR {id:'SAR-2026-09'})</td><td><span class="table-tag tag-rose">[:ALLEGES_CRIME_AGAINST]</span></td><td>(p:Person {name:'Vladimir S.', tax_id:'GB-77218-A'})</td><td>MERGE (Doc)-[:ALLEGES]->(p)</td></tr>
    <tr><td>(p:Person {name:'Vladimir S.'})</td><td><span class="table-tag tag-amber">[:BENEFICIAL_OWNER_OF {share: 100}]</span></td><td>(c:Company {lei:'5493001KJTIIG'})</td><td>MERGE (p)-[:BENEFICIAL_OWNER_OF]->(c)</td></tr>
    <tr><td>(c:Company {name:'Apex Global'})</td><td><span class="table-tag tag-cyan">[:HOLDS_ACCOUNT]</span></td><td>(a:Account {iban:'AE44EBIL..'})</td><td>MERGE (c)-[:HOLDS_ACCOUNT]->(a)</td></tr>
    <tr><td>(Doc:LoanApp {id:'Loan-482'})</td><td><span class="table-tag tag-purple">[:DISCLOSES_COLLATERAL]</span></td><td>(w:WireTransfer {id:'W109', amt:485000})</td><td>MERGE (Doc)-[:DISCLOSES]->(w)</td></tr>
  </tbody>
</table>''',
     "KEY EXTRACTION & CYPHER BINDING SCRIPT"),

    # AML Step 4
    (4, "STEP 4 DATA SNAPSHOT: Multi-Modal Property Graph Data Structure", "FORMAT: Labeled Property Graph (LPG) Node & Edge Schema",
     [
         ("🌐", "Neo4j Enterprise Graph DB", "Stores multi-modal property graph: heterogeneous vertices, directed relationships, and rich key-value maps"),
         ("🏛️", "Protégé & OWL 2 Reasoner", "HermiT/Pellet semantic reasoner verifies ontology consistency, detects illegal circular inheritance"),
         ("🔮", "ChromaDB Vector Store", "Vector collection linked to Neo4j Node IDs; enables hybrid semantic-topological RAG"),
         ("⚡", "APOC Procedures", "High-throughput graph batch algorithms, schema indexing, and sub-graph JSON projections")
     ],
     '''<table class="snapshot-table">
  <thead><tr><th>Integrated Modality</th><th>Data Format</th><th>Source System</th><th>Ingested Volume</th><th>Ontology Class (OWL 2)</th></tr></thead>
  <tbody>
    <tr><td>Unstructured Narratives</td><td>PDF & Email Text</td><td>ChromaDB / Document Store</td><td>1,420 Documents</td><td><span class="table-tag tag-cyan">fibo:ComplianceReport</span></td></tr>
    <tr><td>Structured Accounts</td><td>Relational SQL Rows</td><td>Oracle Core Banking</td><td>85,000 Accounts</td><td><span class="table-tag tag-green">fibo:BankDepositAccount</span></td></tr>
    <tr><td>SWIFT Wire Feeds</td><td>Flat MT103 / ISO</td><td>SWIFT Transaction Gateway</td><td>412,000 Wires</td><td><span class="table-tag tag-amber">fibo:PaymentExecution</span></td></tr>
    <tr><td>PEP & Sanctions Lists</td><td>XML / JSON Feeds</td><td>OFAC / World-Check Watchlist</td><td>12,500 Profiles</td><td><span class="table-tag tag-rose">fibo:SanctionedSubject</span></td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table">
  <thead><tr><th>Subject Node (Label & ID)</th><th>Relationship Edge</th><th>Object Node (Label & ID)</th><th>Integrated Modality Bridge</th></tr></thead>
  <tbody>
    <tr><td>(p:Person {name:'Vladimir S.'})</td><td><span class="table-tag tag-amber">[:CONTROLS {share_pct: 100}]</span></td><td>(c:Company {name:'Apex Global'})</td><td>Hybrid: Unstructured UBO + SQL Company</td></tr>
    <tr><td>(c:Company {name:'Apex Global'})</td><td><span class="table-tag tag-cyan">[:HOLDS_ACCOUNT]</span></td><td>(a:Account {iban:'AE44EBIL..'})</td><td>Structured: Core Banking Foreign Key</td></tr>
    <tr><td>(a:Account {iban:'GB29NWBK..'})</td><td><span class="table-tag tag-rose">[:TRANSFERRED {amt:485000, ts:'2026-10-12'}]</span></td><td>(a:Account {iban:'AE44EBIL..'})</td><td>Structured: SWIFT MT103 Wire Edge</td></tr>
    <tr><td>(doc:SAR {id:'SAR-2026-09'})</td><td><span class="table-tag tag-green">[:VECTOR_SIMILAR {cosine: 0.892}]</span></td><td>(doc:LoanApp {id:'LoanApp-482'})</td><td>Unstructured: ChromaDB Vector Cosine Sim</td></tr>
  </tbody>
</table>''',
     "UNIFIED MULTI-MODAL GRAPH DATA SERIALIZATION"),

    # AML Step 5
    (5, "STEP 5 DATA SNAPSHOT: Pattern Recognition & Circular Ring Detection", "FORMAT: Executed Cypher Query & Detected Ring Data",
     [
         ("⚡", "Neo4j Cypher Query Engine", "Executes recursive multi-hop graph pattern matching ([:TRANSFERRED*3..6]) in <12ms"),
         ("🧠", "Neo4j Graph Data Science (GDS)", "Executes Louvain Community Detection, Weakly Connected Components (WCC), and PageRank"),
         ("⏱️", "Temporal-Amount Path Filter", "Restricts cycle evaluation: hops must occur within 72 hours with <12% amount decay"),
         ("🛡️", "Graph Pattern Recognition", "Automates discovery of circular layering rings, smurfing aggregators, and shadow directors")
     ],
     '''<table class="snapshot-table">
  <thead><tr><th>Candidate Path Sequence</th><th>Accounts Traversed</th><th>Hop Amounts (USD)</th><th>Duration</th><th>Evaluated Typology Rule</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-rose">Path #1 (Cycle)</span></td><td>Acc A -> Acc B -> Acc C -> Acc A</td><td>$485k -> $475k -> $460k -> $455k</td><td>38.4 Hours</td><td>Circular Layering Ring (3-6 Hops)</td></tr>
    <tr><td><span class="table-tag tag-amber">Path #2 (Fan-In)</span></td><td>5 Smurf Accounts -> Shell Hub</td><td>$9,500, $9,800, $9,200, $9,700</td><td>18.2 Hours</td><td>Smurfing / Structuring (<$10k limit)</td></tr>
    <tr><td><span class="table-tag tag-green">Path #3 (Normal)</span></td><td>Client Acc -> Vendor Acc</td><td>$12,000</td><td>120 Hours</td><td>Standard Commercial Wire (No Alert)</td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table">
  <thead><tr><th>Detected Anomaly Typology</th><th>Ringleader / Origin</th><th>Laundered Sum</th><th>Traversal Topology</th><th>Risk Score</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-rose">CIRCULAR_LAYERING_RING</span></td><td>Vladimir S. (GB29NWBK..)</td><td><strong>$485,000.00 USD</strong></td><td>4-Hop Cross-Border Closed Loop</td><td><span class="table-tag tag-rose">98.4 / 100 (CRITICAL)</span></td></tr>
    <tr><td><span class="table-tag tag-amber">STRUCTURING_FAN_IN</span></td><td>Apex Aggregator (AE44EBIL..)</td><td><strong>$76,400.00 USD</strong></td><td>8 Sub-$10k Wires within 24h</td><td><span class="table-tag tag-amber">94.1 / 100 (HIGH)</span></td></tr>
    <tr><td><span class="table-tag tag-purple">HIGH_PAGERANK_CONTROLLER</span></td><td>Vladimir S. (CUST-901)</td><td>N/A (Centrality: 0.87)</td><td>Hub connecting 14 Shell Companies</td><td><span class="table-tag tag-rose">99.2 / 100 (CRITICAL)</span></td></tr>
  </tbody>
</table>''',
     "EXECUTED CYPHER PATTERN & QUERY OUTPUT"),

    # AML Step 6
    (6, "STEP 6 DATA SNAPSHOT: Leadership Deliverables & Asset Seizure Package", "FORMAT: FinCEN SAR XML & Forensic Asset Summary",
     [
         ("🤖", "Hybrid Graph-RAG Engine", "Synthesizes multi-hop Neo4j Cypher subgraphs and ChromaDB text evidence into C-suite narrative"),
         ("📑", "FinCEN SAR XML Generator", "Compiles regulatory BSA E-Filing Form 111 with 100% cited graph provenance"),
         ("🔒", "Asset Forensics Ledger", "Calculates exact frozen asset amounts and generates court-admissible SWIFT cryptographic audit trail"),
         ("📊", "Leadership KPI Dashboard", "Translates raw graph topologies into board-level risk exposure and balance-sheet impact metrics")
     ],
     '''<table class="snapshot-table">
  <thead><tr><th>Investigation Target</th><th>Total Laundered Volume</th><th>Identified Jurisdictions</th><th>Shell Entities Involved</th><th>Primary Perpetrators</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-rose">Apex Global Syndicate</span></td><td><strong>$3,840,000.00 USD</strong></td><td>UK, UAE (Dubai), Switzerland, BVI</td><td>Apex Global, Meridian FZE, Velo Maritime</td><td>Vladimir S. (UBO), Elena R. (Nominee)</td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table">
  <thead><tr><th>Leadership Deliverable</th><th>Target Audience</th><th>Concrete Actionable Deliverable</th><th>Regulatory / Legal Defensibility</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-cyan">Board Risk Summary</span></td><td>Board of Directors / CEO</td><td>"$3.84M Syndicate Laundering Intercepted; $12M Exposure Averted"</td><td>100% Graph Proof, Zero False Positives</td></tr>
    <tr><td><span class="table-tag tag-amber">FinCEN Form 111 (SAR)</span></td><td>CCO / FinCEN / FCA</td><td>Full pre-populated XML filing with narrative, UBO tax IDs & account paths</td><td>Fully Audited, Cypher Path Attached</td></tr>
    <tr><td><span class="table-tag tag-green">Asset Seizure Ledger</span></td><td>CRO / Law Enforcement</td><td>"$3,840,000 in Accounts AE44EBIL & CH93SBIN flagged for immediate freeze"</td><td>Court-admissible SWIFT hash trail</td></tr>
  </tbody>
</table>''',
     "PRE-POPULATED FINCEN SAR XML & ASSET LEDGER")
]

# Med Panels Data
med_data = [
    # Med Step 1
    (1, "STEP 1 DATA SNAPSHOT: Biomedical Unstructured Ingress & BioBERT Entities", "FORMAT: BioBERT Literature Entities & Ontological Triples",
     [
         ("🔬", "PubMed Central & bioRxiv APIs", "Bulk literature ingestion: 1.4M biomedical research papers and oncology trial pre-prints"),
         ("🧬", "BioBERT & SciSpacy", "Domain NER (en_ner_bc5cdr_md) extracting Genes, Mutations, Diseases, Cell Lines, Residues"),
         ("🔮", "ChromaDB Biomedical Vector Index", "Dense 768-d BioLinkBERT embeddings for semantic target-mechanism search"),
         ("🏛️", "Protégé & Gene Ontology (GO)", "Normalizes medical synonymy to OBO Foundry standard ontology IDs (GO, MeSH, DOID)")
     ],
     '''<table class="snapshot-table med">
  <thead><tr><th>PMID / Source</th><th>Doc Type</th><th>Abstract Text Snippet</th><th>Extracted BioBERT Entities</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-green">PMID:3829104</span></td><td>Journal Paper</td><td>"The C797S mutation in EGFR confers profound resistance to osimertinib in NSCLC."</td><td><span class="table-tag tag-green">EGFR (GENE)</span>, <span class="table-tag tag-amber">C797S (MUTATION)</span>, <span class="table-tag tag-cyan">Osimertinib (DRUG)</span></td></tr>
    <tr><td><span class="table-tag tag-green">NCT-0492</span></td><td>Trial Protocol</td><td>"Evaluating allosteric kinase inhibitors targeting osimertinib-refractory lung adenocarcinoma."</td><td><span class="table-tag tag-green">EGFR-mutant (TARGET)</span>, <span class="table-tag tag-purple">NSCLC (DISEASE)</span></td></tr>
    <tr><td><span class="table-tag tag-green">BioRxiv-2026.04</span></td><td>Structure Study</td><td>"Cryo-EM reveals structural alteration at Met793 and Ser797 active pocket preventing covalent bond."</td><td><span class="table-tag tag-cyan">Met793 (RESIDUE)</span>, <span class="table-tag tag-amber">Ser797 (RESIDUE)</span></td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table med">
  <thead><tr><th>Source Literature</th><th>Biomedical Mapping Layer</th><th>Linked Document / Concept Bridge</th><th>Constructed Ontological Relationship</th></tr></thead>
  <tbody>
    <tr><td>PMID:3829104</td><td>BioBERT Co-Occurrence</td><td>Clinical Trial NCT-0492 (Shared Target: EGFR C797S)</td><td><span class="table-tag tag-green">[:DRIVES_RESISTANCE_TO {drug: 'Osimertinib'}]</span></td></tr>
    <tr><td>PMID:3829104</td><td>ChromaDB Vector Sim</td><td>BioRxiv-2026.04 (Structural Active Pocket)</td><td><span class="table-tag tag-cyan">[:MECHANISTICALLY_ALIGNED {cosine: 0.914}]</span></td></tr>
    <tr><td>NCT-0492 Trial</td><td>Gene Ontology Normalization</td><td>Gene Ontology GO:0004714 (Kinase Activity)</td><td><span class="table-tag tag-purple">[:HAS_FUNCTION {go_id: 'GO:0004714'}]</span></td></tr>
  </tbody>
</table>''',
     "PUBMED ABSTRACT DATA & BIOBERT EXTRACTED ENTITIES"),

    # Med Step 2
    (2, "STEP 2 DATA SNAPSHOT: ChEMBL Bioassays & RCSB PDB Active Sites", "FORMAT: Structured ChEMBL Ki/IC50 & mmCIF 3D Atomic Coords",
     [
         ("💎", "RCSB Protein Data Bank (PDB)", "mmCIF 3D atomic coordinates of kinase active binding pockets at <2.0 Å resolution"),
         ("💊", "ChEMBL & PubChem", "Curated bioactivity assays: IC50, Ki, Kd values, and SMILES chemical structure representations"),
         ("🧬", "UniProtKB & NCBI Gene", "Canonical protein sequence reference aligning mutant amino acid positions (Position 797)"),
         ("🏛️", "Protégé & OWL 2 (BFO / BioTop)", "Formal foundational ontology modeling chemical-biological interaction classes")
     ],
     '''<table class="snapshot-table med">
  <thead><tr><th>Database</th><th>Record ID</th><th>Target / Protein</th><th>Measurement / Metric</th><th>Sample Data Content</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-green">RCSB PDB</span></td><td>PDB: 7LUD</td><td>EGFR (C797S Mutated)</td><td>Resolution: 1.82 Å</td><td>Atomic 3D Coords: Met793 hinge, Lys745 salt bridge</td></tr>
    <tr><td><span class="table-tag tag-cyan">ChEMBL</span></td><td>CHEMBL480112</td><td>EGFR C797S Kinase</td><td>IC50: 1.8 nM</td><td>Bioassay: Aminopyrimidine lead inhibition</td></tr>
    <tr><td><span class="table-tag tag-cyan">ChEMBL</span></td><td>CHEMBL2034</td><td>EGFR C797S Kinase</td><td>IC50: >2,000 nM</td><td>Osimertinib benchmark (Activity Lost)</td></tr>
    <tr><td><span class="table-tag tag-purple">UniProtKB</span></td><td>P00533</td><td>Human EGFR</td><td>Sequence: 1,210 AA</td><td>Wild-type Cys797 -> Mutated Ser797 coordinate</td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table med">
  <thead><tr><th>Target Protein Key</th><th>Foreign Key Relational Join</th><th>Mapped Life Sciences Record</th><th>Biological Measurement</th><th>OWL 2 Property</th></tr></thead>
  <tbody>
    <tr><td>UniProt: P00533 (EGFR)</td><td>pdb_id -> 7LUD</td><td>PDB 7LUD (Resolution: 1.82 Å)</td><td>Active Pocket: Met793, Lys745</td><td><span class="table-tag tag-green">owl:Class :KinaseDomain</span></td></tr>
    <tr><td>CHEMBL480112</td><td>target_id -> P00533</td><td>EGFR C797S Mutated Bioassay</td><td>IC50: 1.8 nM (High Potency)</td><td><span class="table-tag tag-cyan">owl:ObjectProperty :inhibitsActivity</span></td></tr>
    <tr><td>CHEMBL2034</td><td>compound -> Osimertinib</td><td>Wild-Type vs C797S Comparison</td><td>IC50: 0.4 nM (WT) vs >2,000 nM (Mutant)</td><td><span class="table-tag tag-rose">owl:ObjectProperty :lacksBinding</span></td></tr>
  </tbody>
</table>''',
     "CHEMBL BIOASSAY & PDB ACTIVE POCKET DATA"),

    # Med Step 3
    (3, "STEP 3 DATA SNAPSHOT: Biomedical Mapping Key Resolution & Cypher Binding", "FORMAT: UniProt/InChIKey Resolution & Cypher Graph Ingest",
     [
         ("🔑", "UniProt & InChIKey Resolver", "Standardizes research text mentions to immutable biological accessions and chemical keys"),
         ("🏛️", "Protégé & Gene Ontology", "Maps synonymous medical terminology to standardized GO, MeSH, and ChEMBL entity classes"),
         ("🌐", "Neo4j Cypher Ingest Engine", "Binds unstructured literature citations directly to 3D atomic active pocket nodes"),
         ("⚡", "SMILES Structure Normalizer", "RDKit canonicalization ensuring identical stereochemistry for small molecule ligands")
     ],
     '''<table class="snapshot-table med">
  <thead><tr><th>Unstructured Text Mention</th><th>Source Literature</th><th>Target Life Science DB</th><th>Resolved Deterministic Key</th><th>Validation</th></tr></thead>
  <tbody>
    <tr><td>"EGFR exon 19 del / C797S"</td><td>PMID:3829104</td><td>UniProtKB</td><td><span class="table-tag tag-green">UniProt: P00533 (Position: 797)</span></td><td><span class="table-tag tag-green">100% Sequence Valid</span></td></tr>
    <tr><td>"Osimertinib / Tagrisso"</td><td>Trial NCT-0492</td><td>ChEMBL / PubChem</td><td><span class="table-tag tag-cyan">InChIKey: UCGDIPOCXAYWHS..</span></td><td><span class="table-tag tag-green">100% Chemical Valid</span></td></tr>
    <tr><td>"Hinge pocket Met793"</td><td>BioRxiv Structure Study</td><td>RCSB PDB</td><td><span class="table-tag tag-purple">PDB: 7LUD (Chain A, Pocket 1)</span></td><td><span class="table-tag tag-green">100% 3D Atomic Valid</span></td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table med">
  <thead><tr><th>Source Literature Node</th><th>Constructed Biological Relationship</th><th>Target Life Science Node</th><th>Graph Ingestion Action</th></tr></thead>
  <tbody>
    <tr><td>(Paper:PMID_3829104)</td><td><span class="table-tag tag-green">[:REPORTS_TARGET_MUTATION]</span></td><td>(p:Protein {uniprot:'P00533', mutant:'C797S'})</td><td>MERGE (Paper)-[:REPORTS]->(p)</td></tr>
    <tr><td>(p:Protein {uniprot:'P00533'})</td><td><span class="table-tag tag-cyan">[:HAS_3D_CRYSTAL_STRUCTURE]</span></td><td>(pdb:PDBStructure {id:'7LUD', res:1.82})</td><td>MERGE (p)-[:HAS_3D]->(pdb)</td></tr>
    <tr><td>(pdb:PDBStructure {id:'7LUD'})</td><td><span class="table-tag tag-purple">[:CONTAINS_BINDING_POCKET]</span></td><td>(pocket:Pocket {hinge:'Met793', salt:'Lys745'})</td><td>MERGE (pdb)-[:CONTAINS]->(pocket)</td></tr>
    <tr><td>(Drug:Candidate_904)</td><td><span class="table-tag tag-amber">[:COMPLEMENTS_ACTIVE_POCKET]</span></td><td>(pocket:Pocket {hinge:'Met793'})</td><td>MERGE (Drug)-[:BINDS_POCKET]->(pocket)</td></tr>
  </tbody>
</table>''',
     "BIO-KEY EXTRACTION & CYPHER BINDING SCRIPT"),

    # Med Step 4
    (4, "STEP 4 DATA SNAPSHOT: Unified Biomedical Knowledge Graph Structure", "FORMAT: Biomedical Labeled Property Graph (LPG) Schema",
     [
         ("🌐", "Neo4j Biomedical Graph DB", "Multi-scale property graph uniting literature, genomics, 3D structures, and clinical trials"),
         ("🏛️", "Protégé & OWL 2 Reasoner", "Guarantees formal biological taxonomies; prevents inconsistent enzymatic inhibition classes"),
         ("🔮", "ChromaDB Bio-Vector Store", "Stores 768-d BioLinkBERT embeddings for natural language hypothesis generation"),
         ("🧬", "Neo4j APOC & GDS Library", "Executes graph traversals across protein-protein networks and ligand chemical graphs")
     ],
     '''<table class="snapshot-table med">
  <thead><tr><th>Biological Modality</th><th>Data Format</th><th>Source Database</th><th>Ingested Entity Volume</th><th>Ontology Class (OWL 2)</th></tr></thead>
  <tbody>
    <tr><td>Clinical Abstracts</td><td>BioNLP Text / XML</td><td>PubMed Central / BioRxiv</td><td>450,000 Articles</td><td><span class="table-tag tag-green">bfo:ScientificPublication</span></td></tr>
    <tr><td>3D Protein Pockets</td><td>mmCIF Atomic Files</td><td>RCSB Protein Data Bank</td><td>2,800 Crystal Structures</td><td><span class="table-tag tag-cyan">bfo:ProteinConformation</span></td></tr>
    <tr><td>Chemical Bioassays</td><td>Bioactivity Rows</td><td>ChEMBL 33 Database</td><td>1,200,000 Bioassays</td><td><span class="table-tag tag-amber">bfo:BioAssayMeasurement</span></td></tr>
    <tr><td>Patient Trial Data</td><td>Tabular Cohort Data</td><td>ClinicalTrials.gov</td><td>8,500 Trial Cohorts</td><td><span class="table-tag tag-purple">bfo:ClinicalObservation</span></td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table med">
  <thead><tr><th>Subject (Biomedical Entity)</th><th>Biological Relationship Edge</th><th>Object (Target / Molecule)</th><th>Multi-Modal Integration</th></tr></thead>
  <tbody>
    <tr><td>(Protein:EGFR_C797S)</td><td><span class="table-tag tag-green">[:ASSOCIATED_WITH_DISEASE]</span></td><td>(Disease:Osimertinib_Resistant_NSCLC)</td><td>Unstructured: PubMed BioNLP Ingest</td></tr>
    <tr><td>(Protein:EGFR_C797S)</td><td><span class="table-tag tag-cyan">[:EXHIBITS_STRUCTURAL_CONFORMATION]</span></td><td>(PDB:7LUD {res: 1.82, chain:'A'})</td><td>Structured: RCSB PDB Coordinates</td></tr>
    <tr><td>(Candidate:FEU_EGFR_904)</td><td><span class="table-tag tag-green">[:POTENTLY_INHIBITS {ic50: 1.8, unit:'nM'}]</span></td><td>(Protein:EGFR_C797S)</td><td>Structured: ChEMBL Bioactivity Join</td></tr>
    <tr><td>(Candidate:FEU_EGFR_904)</td><td><span class="table-tag tag-purple">[:SPATIALLY_COMPATIBLE_WITH]</span></td><td>(Pocket:Met793_Lys745 {hbonds: 2})</td><td>Multi-Modal: 3D Coordinate Mapping</td></tr>
  </tbody>
</table>''',
     "UNIFIED BIOMEDICAL GRAPH JSON SERIALIZATION"),

    # Med Step 5
    (5, "STEP 5 DATA SNAPSHOT: Kinase Selectivity Pattern Recognition & Link Prediction", "FORMAT: Executed Cypher Selectivity Query & Hit Data",
     [
         ("⚡", "Neo4j Cypher Graph Engine", "Performs subgraph isomorphism querying kinase binding pockets across 500+ kinome targets"),
         ("🧪", "RDKit Cheminformatics", "Computes molecular weight (MW: 513.57), LogP, tPSA, and Lipinski Rule of 5 drug-likeness"),
         ("🧠", "PyTorch Geometric (PyG)", "Graph Neural Network (GNN) link prediction predicting ligand-protein binding affinity"),
         ("🛡️", "Off-Target Safety Screener", "Traverses hERG cardiac channel and wild-type EGFR bioassays ensuring zero toxicity")
     ],
     '''<table class="snapshot-table med">
  <thead><tr><th>Compound ID</th><th>Molecular Scaffold / Warhead</th><th>Target Kinase Affinity</th><th>Off-Target (hERG / WT)</th><th>Structural Fit</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-green">FEU-EGFR-904</span></td><td>Aminopyrimidine + Cyclobutane</td><td><strong>IC50: 1.8 nM (C797S)</strong></td><td>IC50: >10,000 nM (180x WT)</td><td>Optimal (Lys745 Salt Bridge)</td></tr>
    <tr><td><span class="table-tag tag-amber">Analog-B2</span></td><td>Pyrimidine + Straight Acrylamide</td><td>IC50: 82.0 nM (C797S)</td><td>IC50: 340 nM (Poor Selectivity)</td><td>Steric Clash with Ser797</td></tr>
    <tr><td><span class="table-tag tag-rose">Osimertinib</span></td><td>Standard Covalent Inhibitor</td><td>IC50: >2,000 nM (Inactive)</td><td>IC50: 0.4 nM (Wild-Type)</td><td>Ineffective (Lost Cys797)</td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table med">
  <thead><tr><th>Lead Candidate</th><th>Predicted Binding Mechanism</th><th>Selectivity Ratio</th><th>Oral Bioavailability</th><th>Pattern Recognition Status</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-green">FEU-EGFR-904</span></td><td>Non-Covalent Lys745 Salt Bridge Trap</td><td><strong>>180x Selective vs WT</strong></td><td>78% Oral (Low CYP3A4 Clearance)</td><td><span class="table-tag tag-green">TOP LEAD CANDIDATE</span></td></tr>
    <tr><td><span class="table-tag tag-cyan">FEU-EGFR-907</span></td><td>Dual Hinge-Binding Allosteric Pocket</td><td>45x Selective vs WT</td><td>52% Oral Bioavailability</td><td><span class="table-tag tag-cyan">BACKUP OPTIMIZATION</span></td></tr>
  </tbody>
</table>''',
     "EXECUTED KINASE SELECTIVITY QUERY & RESULTS"),

    # Med Step 6
    (6, "STEP 6 DATA SNAPSHOT: CSO Drug Dossier & Chemical Synthesis Recipe", "FORMAT: Preclinical Discovery Dossier & SMILES Recipe",
     [
         ("🤖", "Hybrid Graph-RAG Engine", "Synthesizes multi-hop PDB crystal coordinates and ChEMBL assays into discovery dossiers"),
         ("⚗️", "RDKit & ChemDraw Synthesis Engine", "Generates validated 4-step organic synthesis routes with precursor CAS numbers & yields"),
         ("📑", "FDA IND Regulatory Module", "Auto-formats Preclinical Investigational New Drug (IND) briefing documents for CDER"),
         ("📈", "Pharma Commercial Analytics", "Forecasts market opportunity ($2.8B global NSCLC) and hit-to-lead timeline compression")
     ],
     '''<table class="snapshot-table med">
  <thead><tr><th>Target Disease / Mutation</th><th>Novel Lead Candidate</th><th>Chemical Formula & MW</th><th>Potency & Selectivity</th><th>Commercial Opportunity</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-green">Osimertinib-Resistant NSCLC</span></td><td><span class="table-tag tag-green">FEU-EGFR-904</span></td><td>C28H28FN7O2 (MW: 513.57)</td><td>IC50: 1.8 nM (>180x WT)</td><td><strong>$2.8B USD Addressable Market</strong></td></tr>
  </tbody>
</table>''',
     '''<table class="snapshot-table med">
  <thead><tr><th>Leadership Deliverable</th><th>Target Leadership Audience</th><th>Concrete Actionable Deliverable</th><th>Business & Clinical Impact</th></tr></thead>
  <tbody>
    <tr><td><span class="table-tag tag-green">Novel Lead Dossier</span></td><td>Chief Scientific Officer (CSO)</td><td>FEU-EGFR-904 composition-of-matter IP & patentable crystal binding pose</td><td>First-in-Class Asset with Strong Patentability</td></tr>
    <tr><td><span class="table-tag tag-cyan">4-Step Synthesis Recipe</span></td><td>VP of Medicinal Chemistry</td><td>Step-by-step reaction conditions: Aminopyrimidine core + fluorophenyl tail (68% yield)</td><td>Wet-lab synthesis ready in 14 days</td></tr>
    <tr><td><span class="table-tag tag-purple">Preclinical Target Dossier</span></td><td>Board of Directors / Head of R&D</td><td>Hit-to-lead timeline compressed from 18 months down to <strong>6 weeks</strong></td><td>Preclinical Phase I Candidate Ready</td></tr>
  </tbody>
</table>''',
     "NOVEL DRUG SYNTHESIS RECIPE & REGULATORY DOSSIER")
]

# Read current index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add CSS if not present
if '.snapshot-tech-bar' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>\n' + enhanced_css + '\n</style>\n' + html[head_pos:]
        print("Injected Enhanced CSS into <head>.")

# Now replace panels in reverse order:
# We find exact slices for all 12 panels
panel_slices = []

for step_num, title, fmt, tech, in_t, out_t, raw_title in aml_data:
    pid = f"snapshot-aml-{step_num}"
    pos = html.find(f'id="{pid}"')
    if pos == -1:
        print(f"ERROR: could not find {pid}")
        continue
    p_start = html.rfind('<div', 0, pos)
    pos_foot = html.find('snapshot-mechanics-footer', pos)
    pos_foot_end = html.find('</div>', pos_foot)
    p_end = html.find('</div>', pos_foot_end + 6) + 6
    
    orig_panel = scope[f'panel_aml_{step_num}']
    svg_code = extract_svg(orig_panel)
    pre_code = extract_pre(orig_panel)
    footer_text = extract_footer(orig_panel)
    
    new_html = build_panel(pid, title, fmt, tech, in_t, out_t, pre_code, raw_title, svg_code, footer_text, is_med=False)
    panel_slices.append((p_start, p_end, pid, new_html))

for step_num, title, fmt, tech, in_t, out_t, raw_title in med_data:
    pid = f"snapshot-med-{step_num}"
    pos = html.find(f'id="{pid}"')
    if pos == -1:
        print(f"ERROR: could not find {pid}")
        continue
    p_start = html.rfind('<div', 0, pos)
    pos_foot = html.find('snapshot-mechanics-footer', pos)
    pos_foot_end = html.find('</div>', pos_foot)
    p_end = html.find('</div>', pos_foot_end + 6) + 6
    
    orig_panel = scope[f'panel_med_{step_num}']
    svg_code = extract_svg(orig_panel)
    pre_code = extract_pre(orig_panel)
    footer_text = extract_footer(orig_panel)
    
    new_html = build_panel(pid, title, fmt, tech, in_t, out_t, pre_code, raw_title, svg_code, footer_text, is_med=True)
    panel_slices.append((p_start, p_end, pid, new_html))

print(f"Total panel slices found: {len(panel_slices)}")

# Sort in reverse order of p_start
panel_slices.sort(key=lambda x: x[0], reverse=True)

for p_start, p_end, pid, new_html in panel_slices:
    html = html[:p_start] + new_html + html[p_end:]
    print(f"Updated {pid} at range [{p_start}:{p_end}]")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully enhanced with all 12 Table Snapshots, Tech Stacks, and Visual Graphs!")
