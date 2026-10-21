import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# Build updated archContent-techstack HTML featuring Diagram 5 + Data Table (Replacing paragraph cards)
techstack_html = '''        <!-- TAB 5: TECH STACK & SERIAL COMPONENT EXECUTION ARCHITECTURE -->
        <div id="archContent-techstack" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:12px;">
              <div>
                <span style="background:rgba(96,165,250,0.15); color:#60A5FA; font-size:11px; font-weight:700; padding:4px 10px; border-radius:6px; text-transform:uppercase;">Serial Component Execution Pipeline</span>
                <h3 style="color:var(--tx-0); font-size:20px; margin:8px 0 0; font-weight:700;">Diagram 5: Serial Role of Protégé, ChromaDB, Neo4j, Cypher & Hybrid Graph-RAG</h3>
              </div>
              <span style="font-size:32px;">⚙️</span>
            </div>

            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Comprehensive architectural flowchart showing the exact serial sequence of how raw structured tables and unstructured documents enter the platform, pass through Protégé OWL semantic rules, ChromaDB vector indexing, Neo4j property graph storage, Cypher pattern recognition, and Hybrid Graph-RAG to produce executive deliverables.
            </p>

            <!-- DIAGRAM 5 SERIAL EXECUTION FLOWCHART -->
            <div style="display:flex; justify-content:center; margin-bottom:24px;">
              <div class="arch-flowchart-container">
                
                <!-- Input Step -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">0. Multi-Source Input Data Streams</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Input Data<span class="arch-sub-note">(Core Banking SQL, Wires, KYC, Assays, PubChem)</span></div>
                    <div class="arch-sub-box">Unstructured Input Data<span class="arch-sub-note">(SAR Narratives, Loan PDFs, PubMed Papers, Protocols)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Tool 1: Protégé OWL 2 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">Step 1: Protégé & OWL 2 Ontology Schema <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Semantic Governance]</span></div>
                  <div class="arch-sub-box amber">Defines allowed entity classes (Customer, Account, Compound, Target), relationship types (OWNS, TRANSFERRED, BINDS_TO), domain/range constraints, and validation rules BEFORE data enters the graph.</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Tool 2: ChromaDB -->
                <div class="arch-stage-box" style="border-color:rgba(155,124,246,0.5);">
                  <div class="arch-stage-title" style="color:#9B7CF6;">Step 2: ChromaDB Vector Store & Embeddings <span style="float:right; color:#9B7CF6; font-size:11px; font-weight:600;">[Semantic Text Vectorization]</span></div>
                  <div class="arch-sub-box blue">Chunks unstructured document text, extracts 384-dimensional dense vectors (sentence-transformers), and indexes semantic passages for instant cosine similarity vector retrieval.</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Tool 3: Neo4j Graph DB -->
                <div class="arch-stage-box" style="border-color:rgba(96,165,250,0.5);">
                  <div class="arch-stage-title" style="color:#60A5FA;">Step 3: Neo4j Property Graph Database <span style="float:right; color:#60A5FA; font-size:11px; font-weight:600;">[Graph Topology & Storage]</span></div>
                  <div class="arch-sub-box blue">Executes Cypher MERGE scripts to build a unified property graph in memory. Connects structured records and document chunks with indexless adjacency for O(1) multi-hop traversals.</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Tool 4: Cypher Engine -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">Step 4: Cypher Query Pattern Recognition Engine <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Graph Motif & Rule Execution]</span></div>
                  <div class="arch-sub-box amber">Executes declarative graph motif queries matching 3-6 hop circular wire layering rings, shared device fraud hubs, nanomolar affinity paths (IC50<50nM), and PageRank entity centrality.</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Tool 5: Hybrid Graph-RAG & Leadership Output -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">Step 5: Hybrid Graph-RAG Engine & Executive Deliverables <span style="float:right; color:var(--emerald); font-size:11px; font-weight:600;">[Dual Synthesis & Output]</span></div>
                  <div class="arch-sub-box emerald">Fuses ChromaDB semantic vectors with Neo4j structural graph context to generate zero-hallucination executive deliverables ($14.25M AML exposure, 1-click SAR package, Gefitinib lead drug IC50=2.3nM).</div>
                </div>

              </div>
            </div>

            <!-- SERIAL ROLE BREAKDOWN TABLE (REPLACING PARAGRAPH DISPLAY CARDS) -->
            <h4 style="color:var(--tx-0); font-size:16px; margin:24px 0 14px; font-weight:700;">⚙️ Serial Role Breakdown: How Inputs Flow to Outputs</h4>
            
            <div style="overflow-x:auto; background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:4px;">
              <table style="width:100%; border-collapse:collapse; text-align:left; font-size:12.5px; color:var(--tx-1);">
                <thead>
                  <tr style="background:var(--surface); border-bottom:1.5px solid var(--line-strong); color:var(--tx-0);">
                    <th style="padding:12px 14px; font-weight:700; width:110px;">Serial Sequence</th>
                    <th style="padding:12px 14px; font-weight:700; width:170px;">System Component</th>
                    <th style="padding:12px 14px; font-weight:700;">How it Takes Input</th>
                    <th style="padding:12px 14px; font-weight:700;">Serial Technical Role</th>
                    <th style="padding:12px 14px; font-weight:700;">Output Passed to Next Stage</th>
                  </tr>
                </thead>
                <tbody>
                  <tr style="border-bottom:1px solid var(--line-soft);">
                    <td style="padding:12px 14px; font-weight:700; color:var(--amber);">Step 0</td>
                    <td style="padding:12px 14px; font-weight:700; color:var(--tx-0);">Multi-Source Inputs</td>
                    <td style="padding:12px 14px;">Ingests Core Banking SQL, SWIFT Wires, KYC, ChEMBL Assays, SAR Narratives, Loan PDFs, PubMed Papers.</td>
                    <td style="padding:12px 14px;">Receives structured tables and unstructured documents.</td>
                    <td style="padding:12px 14px;">Raw byte streams and tabular rows.</td>
                  </tr>
                  <tr style="border-bottom:1px solid var(--line-soft);">
                    <td style="padding:12px 14px; font-weight:700; color:var(--amber);">Step 1</td>
                    <td style="padding:12px 14px; font-weight:700; color:var(--tx-0);">Protégé &amp; OWL 2 Ontology</td>
                    <td style="padding:12px 14px;">Ingests domain concepts, class hierarchies, and relationship constraints designed in Protégé (<code style="color:var(--amber);">.owl</code> / <code style="color:var(--amber);">.ttl</code>).</td>
                    <td style="padding:12px 14px;">Establishes semantic rules <strong>before</strong> data is processed. Defines entity classes (<code style="color:var(--mono);">Customer</code>, <code style="color:var(--mono);">Compound</code>) and object properties (<code style="color:var(--mono);">OWNS</code>, <code style="color:var(--mono);">BINDS_TO</code>).</td>
                    <td style="padding:12px 14px;">Validated semantic schema rules governing graph writes.</td>
                  </tr>
                  <tr style="border-bottom:1px solid var(--line-soft);">
                    <td style="padding:12px 14px; font-weight:700; color:#9B7CF6;">Step 2</td>
                    <td style="padding:12px 14px; font-weight:700; color:var(--tx-0);">ChromaDB Vector Store</td>
                    <td style="padding:12px 14px;">Ingests raw unstructured text extracted from PDFs/Word docs via PyMuPDF/pdfplumber.</td>
                    <td style="padding:12px 14px;">Splits text into overlapping passages (2,000 chars), embeds vectors (<code style="color:var(--mono);">sentence-transformers/all-MiniLM-L6-v2</code>), and indexes passages for cosine search (&ge; 0.82).</td>
                    <td style="padding:12px 14px;">Vector-indexed text passages and chunk IDs bound to Neo4j nodes.</td>
                  </tr>
                  <tr style="border-bottom:1px solid var(--line-soft);">
                    <td style="padding:12px 14px; font-weight:700; color:#60A5FA;">Step 3</td>
                    <td style="padding:12px 14px; font-weight:700; color:var(--tx-0);">Neo4j Property Graph DB</td>
                    <td style="padding:12px 14px;">Ingests structured SQL/CSV rows, canonical mapping keys (<code style="color:var(--emerald);">Tax_ID</code>, <code style="color:var(--emerald);">IBAN</code>, <code style="color:var(--emerald);">UniProt_ID</code>, <code style="color:var(--emerald);">SMILES</code>), and chunk IDs.</td>
                    <td style="padding:12px 14px;">Executes Cypher <code style="color:var(--mono);">MERGE</code> scripts building a unified property graph in memory. Uses <strong>Indexless Adjacency</strong> for O(1) multi-hop traversals.</td>
                    <td style="padding:12px 14px;">Fully connected in-memory property graph.</td>
                  </tr>
                  <tr style="border-bottom:1px solid var(--line-soft);">
                    <td style="padding:12px 14px; font-weight:700; color:var(--amber);">Step 4</td>
                    <td style="padding:12px 14px; font-weight:700; color:var(--tx-0);">Cypher Query Engine</td>
                    <td style="padding:12px 14px;">Ingests live property graph memory state from Neo4j + structural graph pattern templates.</td>
                    <td style="padding:12px 14px;">Executes declarative graph motif queries to discover multi-hop layering rings <code style="color:var(--mono);">(acc)-[:TRANSFERRED*3..6]-&gt;(acc)</code>, shared device hubs, and PageRank centrality.</td>
                    <td style="padding:12px 14px;">Extracted sub-graph paths, ringleader lists, and structural risk context.</td>
                  </tr>
                  <tr>
                    <td style="padding:12px 14px; font-weight:700; color:var(--emerald);">Step 5</td>
                    <td style="padding:12px 14px; font-weight:700; color:var(--tx-0);">Hybrid Graph-RAG Engine</td>
                    <td style="padding:12px 14px;">Ingests vector semantic passages from ChromaDB + structural sub-graph path context from Neo4j Cypher.</td>
                    <td style="padding:12px 14px;">Fuses vector and graph context into an LLM prompt (Groq Llama 3.1 70B / Ollama Mistral) for zero-hallucination decision synthesis.</td>
                    <td style="padding:12px 14px; color:var(--emerald); font-weight:600;"><strong>Concrete Executive Deliverables:</strong> Quantified money laundering exposure (<strong>$14.25M</strong>), suspect accounts, 1-click SAR package, and lead drug validation recipe (<strong>Gefitinib / LG-772</strong>, IC50 = 2.3 nM).</td>
                  </tr>
                </tbody>
              </table>
            </div>

          </div>
        </div>
'''

# Replace archContent-techstack block in index.html
start_pos = txt.find('<div id="archContent-techstack"')
end_pos = txt.find('<!-- ============ STRUCTURED PIPELINE ============ -->')
if start_pos != -1 and end_pos != -1:
    txt = txt[:start_pos] + techstack_html + '\n\n      ' + txt[end_pos:]
    print("Successfully replaced archContent-techstack block in index.html with table.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Updated index.html with Serial Role Breakdown data table.")
