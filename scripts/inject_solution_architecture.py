import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# 1. Add Appendix Sidebar Group if not present
appendix_sidebar_html = '''
        <div class="nav-group nav-group-util" id="navGroupAppendix">
          <div class="side-label" style="color:var(--amber,#FF9F0A); font-weight:700; font-size:11px; letter-spacing:0.08em;">APPENDIX</div>
          <button type="button" class="nav-card" data-view="arch">
            <span class="nav-ico">🏛️</span>
            <span class="nav-text">
              <span class="nav-title">Solution Architecture</span>
              <span class="nav-sub">End-to-end KG design & 2 Use Cases</span>
            </span>
          </button>
        </div>'''

if 'id="navGroupAppendix"' not in txt:
    txt = txt.replace(
        '<div class="sidebar-foot"',
        appendix_sidebar_html + '\n        <div class="sidebar-foot"'
    )
    print("Added Appendix sidebar group.")

# 2. Build the rich Solution Architecture HTML for view-arch
view_arch_html = '''      <!-- ============ SOLUTION ARCHITECTURE & TECHNICAL BLUEPRINT ============ -->
      <div class="view" id="view-arch">
        <div class="page-head">
          <div class="eyebrow">APPENDIX · TECHNICAL BLUEPRINT & SOLUTION ARCHITECTURE</div>
          <div class="page-title">Knowledge Graph Solution Architecture</div>
          <div class="page-sub">End-to-end architectural specification, structured & unstructured data unification, entity resolution framework, Cypher pattern detection, and executive leadership outcomes for Financial AML/Fraud Risk & Healthcare Drug Discovery.</div>
        </div>

        <!-- Section Navigation Pills -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" onclick="showArchTab('pipeline')" id="archTab-pipeline" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:600;">📌 10-Step Pipeline Blueprint</button>
          <button type="button" onclick="showArchTab('fintech')" id="archTab-fintech" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">💳 Financial Services — AML & Fraud Risk</button>
          <button type="button" onclick="showArchTab('health')" id="archTab-health" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">🧬 Healthcare — Drug Discovery</button>
          <button type="button" onclick="showArchTab('techstack')" id="archTab-techstack" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">⚙️ Neo4j, Protégé OWL & Cypher</button>
        </div>

        <!-- TAB 1: 10-STEP PIPELINE BLUEPRINT -->
        <div id="archContent-pipeline" class="arch-tab-content">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:12px; font-weight:700;">🌐 10-Step End-to-End Knowledge Graph Architecture</h3>
            <p style="color:var(--tx-2); font-size:13.5px; line-height:1.6; margin-bottom:20px;">
              GRAPHEN transforms siloed structured tabular databases and unstructured textual document repositories into a unified, ontology-constrained Neo4j Knowledge Graph. The end-to-end pipeline operates in ten distinct stages:
            </p>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:16px;">
              
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 1</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Objective & Domain Setup</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Defines the business goal (e.g. AML fraud detection or target validation), imports domain ontology (OWL 2), and sets target entity/relationship schemas.</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 2</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Multi-Source Data Ingestion</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Ingests structured tables (CSV, SQL, ERP, Core Banking) and unstructured documents (PDFs, Word docs, preprints, SAR narratives).</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 3</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Structured Data Pipeline</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Validates data types, enforces foreign keys, normalizes columns against ontology classes, and builds relational join tuples.</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 4</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Unstructured Data Pipeline</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Text extraction via PyMuPDF/pdfplumber, sentence chunking, spaCy NER, LLM structured field extraction, and vector embedding in ChromaDB.</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 5</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Structured & Unstructured Joining</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Binds document chunks and unstructured entity mentions directly to structured record nodes via unified mapping keys (<code style="color:var(--emerald);">Account_ID</code>, <code style="color:var(--emerald);">Tax_ID</code>, <code style="color:var(--emerald);">UniProt_ID</code>, <code style="color:var(--emerald);">CAS_No</code>).</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 6</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Entity Resolution Engine</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Fuzzy name matching (Levenshtein, Jaro-Winkler), phonetic matching (Metaphone), vector similarity, and deterministic rules merge duplicate entities into master nodes.</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 7</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Graph Construction & Topology</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Executes Cypher <code style="color:var(--ok);">MERGE</code> commands in Neo4j to build nodes and directed edges, representing hidden relationships, transaction loops, and evidence chains.</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 8</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Cypher Pattern Detection</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Executes graph pattern matching for circular layering rings, shared device hubs, target affinity gaps, and high-risk clause exposure.</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 9</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Intelligence Synthesis & Graph-RAG</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Combines vector semantic search with Cypher sub-graph topology to generate zero-hallucination answers with node-level evidence citations.</p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:16px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.05em;">Step 10</div>
                <h4 style="color:var(--tx-0); margin:4px 0 8px; font-size:14px;">Executive Leadership Delivery</h4>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">Delivers interactive dashboards, executive risk scorecards, decision briefs, and automated compliance/SAR exports directly to leadership.</p>
              </div>

            </div>
          </div>
        </div>

        <!-- TAB 2: FINANCIAL SERVICES AML & FRAUD RISK -->
        <div id="archContent-fintech" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
              <div>
                <span style="background:rgba(255,159,10,0.15); color:var(--amber); font-size:11px; font-weight:700; padding:4px 10px; border-radius:6px; text-transform:uppercase;">Financial Services Industry Blueprint</span>
                <h3 style="color:var(--tx-0); font-size:20px; margin:8px 0 0; font-weight:700;">Anti-Money Laundering (AML) & Synthetic Fraud Risk Architecture</h3>
              </div>
              <span style="font-size:32px;">💳</span>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px;">
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--amber); margin-top:0; font-size:14px;">🎯 Purpose & Executive Objective</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  Uncover sophisticated multi-account circular wire transfers, shell company networks, shared device/IP fraud rings, and undisclosed Ultimate Beneficial Owners (UBOs) that traditional SQL rule engines miss due to single-table isolation.
                </p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--emerald); margin-top:0; font-size:14px;">🚀 Executive Leadership Deliverable</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  <strong>1. Interactive Financial Network Explorer:</strong> Live 360° graph view of high-risk account clusters.<br>
                  <strong>2. Automated SAR Generator:</strong> One-click regulatory Suspicious Activity Report with graph evidence traces.<br>
                  <strong>3. AML Risk Score Matrix:</strong> Quantified entity risk score based on PageRank & Cypher cycle counts.
                </p>
              </div>
            </div>

            <h4 style="color:var(--tx-0); font-size:15px; margin-bottom:12px; font-weight:700;">📊 Data Unification & Mapping Key Strategy</h4>
            <div style="background:var(--bg-1); border:1px solid var(--line-soft); border-radius:10px; padding:16px; margin-bottom:24px;">
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px; font-size:12px;">
                <div><strong style="color:var(--tx-0);">Structured Sources:</strong> Core Banking SQL, SWIFT Wire Transfers, Customer KYC DB, OFAC Sanctions List.</div>
                <div><strong style="color:var(--tx-0);">Unstructured Sources:</strong> Loan Application PDFs, SAR Narratives, Email Logs, Beneficial Ownership Contracts.</div>
                <div><strong style="color:var(--emerald);">Unified Mapping Keys:</strong> <code style="color:var(--emerald);">Tax_ID / SSN</code>, <code style="color:var(--emerald);">Account_IBAN</code>, <code style="color:var(--emerald);">LEI_Code</code>, <code style="color:var(--emerald);">Device_Fingerprint</code>.</div>
              </div>
            </div>

            <h4 style="color:var(--tx-0); font-size:15px; margin-bottom:12px; font-weight:700;">⚡ Cypher Pattern Detection Query Example</h4>
            <div style="background:#121824; border:1px solid var(--line-soft); border-radius:8px; padding:16px; font-family:var(--mono); font-size:12px; color:#60A5FA; overflow-x:auto;">
// Detecting Circular Wire Transfers (Layering Ring)
MATCH (c:Customer)-[:OWNS]->(acc1:Account)
MATCH path = (acc1)-[:TRANSFERRED_FUNDS*3..6]->(acc1)
WHERE ALL(r IN relationships(path) WHERE r.amount > 10000)
RETURN c.name AS Customer, nodes(path) AS CircularRing, length(path) AS HopLength
            </div>
          </div>
        </div>

        <!-- TAB 3: HEALTHCARE & LIFE SCIENCES DRUG DISCOVERY -->
        <div id="archContent-health" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
              <div>
                <span style="background:rgba(61,220,151,0.15); color:var(--emerald); font-size:11px; font-weight:700; padding:4px 10px; border-radius:6px; text-transform:uppercase;">Healthcare & Life Sciences Industry Blueprint</span>
                <h3 style="color:var(--tx-0); font-size:20px; margin:8px 0 0; font-weight:700;">Drug Discovery & Biomarker Intelligence Architecture</h3>
              </div>
              <span style="font-size:32px;">🧬</span>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px;">
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--amber); margin-top:0; font-size:14px;">🎯 Purpose & Executive Objective</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  Accelerate target identification and lead optimization by synthesizing bioassay IC50 data, UniProt target protein structures, PubChem chemical properties, scientific preprints, and clinical trial outcomes into a connected biological knowledge graph.
                </p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--emerald); margin-top:0; font-size:14px;">🚀 Executive Leadership Deliverable</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  <strong>1. High-Confidence Target-Lead Matrix:</strong> Prioritized list of drug compounds with verified affinity.<br>
                  <strong>2. Off-Target Toxicity Risk Heatmap:</strong> Graph traversal highlighting unexpected cross-binding.<br>
                  <strong>3. Mechanistic Insight Synthesis:</strong> Cross-document Graph-RAG synthesis linking target genes to disease pathways.
                </p>
              </div>
            </div>

            <h4 style="color:var(--tx-0); font-size:15px; margin-bottom:12px; font-weight:700;">📊 Data Unification & Mapping Key Strategy</h4>
            <div style="background:var(--bg-1); border:1px solid var(--line-soft); border-radius:10px; padding:16px; margin-bottom:24px;">
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px; font-size:12px;">
                <div><strong style="color:var(--tx-0);">Structured Sources:</strong> ChEMBL Assay IC50 DB, UniProtKB Target Proteins, PubChem SMILES DB, ClinicalTrials.gov NCT.</div>
                <div><strong style="color:var(--tx-0);">Unstructured Sources:</strong> PubMed Scientific Papers, bioRxiv Preprints, Patent PDF Documents, Trial Protocol PDFs.</div>
                <div><strong style="color:var(--emerald);">Unified Mapping Keys:</strong> <code style="color:var(--emerald);">UniProt_ID</code>, <code style="color:var(--emerald);">InChIKey / SMILES</code>, <code style="color:var(--emerald);">NCBI_Gene_ID</code>, <code style="color:var(--emerald);">NCT_ID</code>.</div>
              </div>
            </div>

            <h4 style="color:var(--tx-0); font-size:15px; margin-bottom:12px; font-weight:700;">⚡ Cypher Target-Compound Traversal Query Example</h4>
            <div style="background:#121824; border:1px solid var(--line-soft); border-radius:8px; padding:16px; font-family:var(--mono); font-size:12px; color:#34D399; overflow-x:auto;">
// Traversing Compound -> Target Protein -> Pathway -> Disease Indication
MATCH (c:Compound)-[r:BINDS_TO]->(tp:TargetProtein)-[:PART_OF_PATHWAY]->(pw:Pathway)-[:ASSOCIATED_WITH]->(d:Disease)
WHERE r.ic50_nm < 50 AND d.name = 'Non-Small Cell Lung Cancer'
RETURN c.name AS Compound, tp.gene_symbol AS Target, pw.name AS Pathway, r.ic50_nm AS BindingAffinity
ORDER BY r.ic50_nm ASC LIMIT 10
            </div>
          </div>
        </div>

        <!-- TAB 4: TECH STACK & CONTRIBUTION OF NEO4J, PROTEGE & CYPHER -->
        <div id="archContent-techstack" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:16px; font-weight:700;">⚙️ Technical Stack & Architectural Contributions</h3>
            
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:18px; margin-bottom:24px;">
              
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:20px;">🦉</span>
                  <h4 style="color:var(--tx-0); margin:0; font-size:15px;">Protégé & OWL 2 Ontology</h4>
                </div>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">
                  Acts as the authoritative semantic governance framework. Defines class hierarchies, object properties, domain/range rules, and cardinality constraints. Prevents schema drift and ensures zero invalid relationship writes.
                </p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:20px;">🔷</span>
                  <h4 style="color:var(--tx-0); margin:0; font-size:15px;">Neo4j Graph Database</h4>
                </div>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">
                  Native property graph engine providing indexless adjacency. Performs multi-hop traversals in constant time $O(1)$ per hop regardless of total database size, replacing expensive SQL 10-table JOINs.
                </p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:20px;">⚡</span>
                  <h4 style="color:var(--tx-0); margin:0; font-size:15px;">Cypher Query Language</h4>
                </div>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">
                  Declarative graph pattern matching language optimized for visual graph traversal. Executes multi-hop ring detections, shortest-path algorithms, and real-time risk flag writes efficiently.
                </p>
              </div>

              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
                  <span style="font-size:20px;">🤖</span>
                  <h4 style="color:var(--tx-0); margin:0; font-size:15px;">ChromaDB & Hybrid Graph-RAG</h4>
                </div>
                <p style="color:var(--tx-2); font-size:12px; line-height:1.5; margin:0;">
                  Combines dense vector embeddings (sentence-transformers) with explicit Neo4j graph paths. Returns grounded, zero-hallucination answers backed by precise document and node citations.
                </p>
              </div>

            </div>
          </div>
        </div>

      </div>
'''

# Replace view-arch in index.html
arch_view_pattern = r'<div class="view" id="view-arch">[\s\S]*?</div>\s*<!-- ============ STRUCTURED PIPELINE ============ -->'
if re.search(arch_view_pattern, txt):
    txt = re.sub(
        arch_view_pattern,
        view_arch_html + '\n\n      <!-- ============ STRUCTURED PIPELINE ============ -->',
        txt,
        count=1
    )
    print("Replaced view-arch in index.html.")
else:
    print("WARNING: view-arch pattern not matched directly! Trying fallback replacement...")
    # Alternative search for view-arch
    start_pos = txt.find('<div class="view" id="view-arch">')
    end_pos = txt.find('<!-- ============ STRUCTURED PIPELINE ============ -->')
    if start_pos != -1 and end_pos != -1:
        txt = txt[:start_pos] + view_arch_html + '\n\n      ' + txt[end_pos:]
        print("Fallback replaced view-arch.")

# 3. Add JS helper function showArchTab in index.html script block
show_arch_tab_js = '''
    window.showArchTab = function(tabName) {
      const tabs = ['pipeline', 'fintech', 'health', 'techstack'];
      tabs.forEach(t => {
        const btn = document.getElementById('archTab-' + t);
        const content = document.getElementById('archContent-' + t);
        if (btn) {
          if (t === tabName) {
            btn.className = 'btn btn-sm btn-primary';
          } else {
            btn.className = 'btn btn-sm btn-secondary';
          }
        }
        if (content) {
          content.style.display = (t === tabName) ? 'block' : 'none';
        }
      });
    };
'''

if 'window.showArchTab' not in txt:
    script_pos = txt.find('<script>')
    if script_pos != -1:
        txt = txt[:script_pos + 8] + show_arch_tab_js + txt[script_pos + 8:]
        print("Inserted showArchTab JS helper.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Successfully updated index.html with complete Solution Architecture section.")
