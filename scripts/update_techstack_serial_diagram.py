import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# Build updated archContent-techstack HTML featuring Diagram 5 (Serial Execution Pipeline Flowchart) + Detailed Tool Sequence Cards
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

            <!-- DETAILED SERIAL EXECUTION TOOL BREAKDOWN CARDS -->
            <h4 style="color:var(--tx-0); font-size:16px; margin:24px 0 14px; font-weight:700;">⚙️ Tool-by-Tool Serial Execution Breakdown</h4>
            
            <div style="display:flex; flex-direction:column; gap:16px;">
              
              <!-- Step 1 Card -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                  <span style="font-size:22px;">🦉</span>
                  <div>
                    <div style="color:var(--amber); font-size:11px; font-weight:700;">SERIAL STEP 1</div>
                    <h5 style="color:var(--tx-0); margin:0; font-size:15px;">Protégé & OWL 2 Ontology Schema (Pre-Ingestion Rules)</h5>
                  </div>
                </div>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:8px 0 0;">
                  <strong>How it Takes Input:</strong> Ingests high-level domain concepts, entity definitions, and relationship logic designed by domain ontologists in Protégé.<br>
                  <strong>Serial Role:</strong> Establishes the authoritative schema blueprint <em>before</em> any data is processed. Defines entity classes (<code style="color:var(--mono);">Customer</code>, <code style="color:var(--mono);">Account</code>, <code style="color:var(--mono);">Compound</code>, <code style="color:var(--mono);">TargetProtein</code>) and object properties (<code style="color:var(--mono);">TRANSFERRED_FUNDS</code>, <code style="color:var(--mono);">BINDS_TO</code>) with strict domain/range constraints.<br>
                  <strong>Output Passed to Next Step:</strong> Validated semantic schema rules that govern how data is extracted, checked, and written to Neo4j without schema drift.
                </p>
              </div>

              <!-- Step 2 Card -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                  <span style="font-size:22px;">🤖</span>
                  <div>
                    <div style="color:#9B7CF6; font-size:11px; font-weight:700;">SERIAL STEP 2</div>
                    <h5 style="color:var(--tx-0); margin:0; font-size:15px;">ChromaDB Vector Store & Embeddings (Unstructured Vectorization)</h5>
                  </div>
                </div>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:8px 0 0;">
                  <strong>How it Takes Input:</strong> Receives raw unstructured text extracted from PDFs, Word docs, SAR narratives, and PubMed preprints via PyMuPDF/pdfplumber.<br>
                  <strong>Serial Role:</strong> Splits document text into overlapping passages (2,000 chars), generates 384-dimensional dense vector embeddings using <code style="color:var(--mono);">sentence-transformers/all-MiniLM-L6-v2</code>, and indexes passages into ChromaDB.<br>
                  <strong>Output Passed to Next Step:</strong> Vector-indexed text passages capable of fast cosine similarity search ($>0.82$) and text chunk identifiers bound to Neo4j nodes.
                </p>
              </div>

              <!-- Step 3 Card -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                  <span style="font-size:22px;">🔷</span>
                  <div>
                    <div style="color:#60A5FA; font-size:11px; font-weight:700;">SERIAL STEP 3</div>
                    <h5 style="color:var(--tx-0); margin:0; font-size:15px;">Neo4j Property Graph Database (Property Topology & Graph Storage)</h5>
                  </div>
                </div>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:8px 0 0;">
                  <strong>How it Takes Input:</strong> Takes structured SQL/CSV record rows, canonical mapping keys (<code style="color:var(--emerald);">Tax_ID</code>, <code style="color:var(--emerald);">IBAN</code>, <code style="color:var(--emerald);">UniProt_ID</code>, <code style="color:var(--emerald);">SMILES</code>), and extracted unstructured text chunk IDs.<br>
                  <strong>Serial Role:</strong> Executes parameterized Cypher <code style="color:var(--mono);">MERGE</code> commands to build a unified property graph in memory, enforcing Protégé schema rules. Uses <strong>Indexless Adjacency</strong> for $O(1)$ multi-hop traversals.<br>
                  <strong>Output Passed to Next Step:</strong> Fully connected in-memory property graph ready for real-time Cypher pattern recognition and path analysis.
                </p>
              </div>

              <!-- Step 4 Card -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                  <span style="font-size:22px;">⚡</span>
                  <div>
                    <div style="color:var(--amber); font-size:11px; font-weight:700;">SERIAL STEP 4</div>
                    <h5 style="color:var(--tx-0); margin:0; font-size:15px;">Cypher Query Engine (Graph Pattern Recognition)</h5>
                  </div>
                </div>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:8px 0 0;">
                  <strong>How it Takes Input:</strong> Receives live property graph memory state from Neo4j and pre-compiled structural graph pattern templates.<br>
                  <strong>Serial Role:</strong> Executes declarative graph motif queries to discover multi-hop layering rings <code style="color:var(--mono);">(acc)-[:TRANSFERRED*3..6]->(acc)</code>, shared device hubs, target-affinity paths (<code style="color:var(--mono);">IC50 &lt; 50nM</code>), and PageRank centrality.<br>
                  <strong>Output Passed to Next Step:</strong> Extracted sub-graph paths, identified risk flags, ringleader lists, and structural context passed to the RAG synthesis engine.
                </p>
              </div>

              <!-- Step 5 Card -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                  <span style="font-size:22px;">🚀</span>
                  <div>
                    <div style="color:var(--emerald); font-size:11px; font-weight:700;">SERIAL STEP 5</div>
                    <h5 style="color:var(--tx-0); margin:0; font-size:15px;">Hybrid Graph-RAG Engine (Dual Synthesis & Executive Deliverables)</h5>
                  </div>
                </div>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:8px 0 0;">
                  <strong>How it Takes Input:</strong> Ingests semantic text vector passages retrieved from ChromaDB + structural sub-graph path context retrieved from Neo4j Cypher.<br>
                  <strong>Serial Role:</strong> Fuses both vector and graph contexts into an LLM prompt (Groq Llama 3.1 70B / Ollama Mistral) to generate zero-hallucination decision briefs backed by node and document citations.<br>
                  <strong>Final Executive Output:</strong> Quantified money laundering exposure ($14.25M), suspect lists (`Acme Shell LLC`), 1-click regulatory SAR filing packages, and lead drug candidate validation recipes (`Gefitinib / LG-772` $IC_{50}=2.3\text{ nM}$).
                </p>
              </div>

            </div>

          </div>
        </div>
'''

# Replace archContent-techstack block in index.html
start_pos = txt.find('<div id="archContent-techstack"')
end_pos = txt.find('</div>\n\n      </div>')
if start_pos != -1:
    # Find closing tag of archContent-techstack
    next_div = txt.find('</div>\n\n      </div>', start_pos)
    if next_div != -1:
        txt = txt[:start_pos] + techstack_html + txt[next_div+6:]
        print("Successfully replaced archContent-techstack in index.html.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Updated index.html with Diagram 5 and Serial Component Execution Pipeline.")
