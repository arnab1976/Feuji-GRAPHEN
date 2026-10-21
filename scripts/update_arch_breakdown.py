import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# Build updated view-arch HTML with full 5-point technical breakdown and 3 customized diagrams
view_arch_html = '''      <!-- ============ SOLUTION ARCHITECTURE & TECHNICAL BLUEPRINT ============ -->
      <div class="view" id="view-arch">
        <div class="page-head">
          <div class="eyebrow">APPENDIX · TECHNICAL BLUEPRINT & SOLUTION ARCHITECTURE</div>
          <div class="page-title">Knowledge Graph Solution Architecture</div>
          <div class="page-sub">Comprehensive architectural specification, unstructured-to-unstructured mapping, structured key binding, ultimate graph data structure, pattern recognition mechanics, and concrete executive outputs for AML/Fraud & Drug Discovery.</div>
        </div>

        <!-- Section Navigation Pills -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" onclick="showArchTab('pipeline')" id="archTab-pipeline" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:600;">📌 10-Step Master Pipeline Diagram</button>
          <button type="button" onclick="showArchTab('fintech')" id="archTab-fintech" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">💳 Financial Services — AML Diagram & Outputs</button>
          <button type="button" onclick="showArchTab('health')" id="archTab-health" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">🧬 Healthcare — Drug Discovery Diagram & Outputs</button>
          <button type="button" onclick="showArchTab('breakdown')" id="archTab-breakdown" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">🔍 5-Step Deep-Dive Technical Mechanics</button>
          <button type="button" onclick="showArchTab('techstack')" id="archTab-techstack" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">⚙️ Neo4j, Protégé OWL & Cypher Roles</button>
        </div>

        <!-- TAB 1: 10-STEP PIPELINE BLUEPRINT & MASTER DIAGRAM -->
        <div id="archContent-pipeline" class="arch-tab-content">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:8px; font-weight:700;">🌐 Diagram 1: Overall 10-Step Knowledge Graph Architecture</h3>
            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Master architectural flow detailing multi-source ingestion, dual structured/unstructured processing pipelines, mapping key unification, Neo4j property graph storage, Cypher pattern detection, and concrete executive outputs.
            </p>

            <!-- DIAGRAM 1 FLOWCHART -->
            <div style="display:flex; justify-content:center;">
              <div class="arch-flowchart-container">
                
                <!-- Stage 1 -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">1. Multi-Source Data Ingestion</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured CSV / SQL Feeds<span class="arch-sub-note">(Transactions, Assays, KYC)</span></div>
                    <div class="arch-sub-box">Unstructured PDF / Word Docs<span class="arch-sub-note">(SAR Narratives, Protocols, Papers)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 2 -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">2. Ingestion Pipelines</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Pipeline<span class="arch-sub-note">Schema Validation & Foreign Keys</span></div>
                    <div class="arch-sub-box">Unstructured Pipeline<span class="arch-sub-note">PyMuPDF, Chunking, spaCy NER & Embeddings</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 3 -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">3. Unification & Entity Resolution</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box amber">Inter-Unstructured Mapping & Composite Keys<span class="arch-sub-note">(Co-occurrence, Citation Matching, Vector Distance & Canonical Keys)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box">Entity Resolution Engine<span class="arch-sub-note">Fuzzy Name, Phonetic, Vector & Deterministic Rules</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 4 -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">4. Neo4j & Cypher Detection Layer</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Protégé OWL 2 Ontology Schema</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box blue">Neo4j Unified Property Graph Storage<span class="arch-sub-note">(Nodes: Customer/Compound, Edges: OWNS/BINDS_TO, Provenance: Document)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box amber">Cypher Pattern Recognition Engine<span class="arch-sub-note">(Topology Motif Matching, N-Hop Cycle Traversal, PageRank Centrality)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 5 -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">5. Hybrid Graph-RAG & Executive Leadership Output</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Concrete Executive Leadership Deliverables<span class="arch-sub-note">(Quantified Dollar Laundering Exposure, Identified Suspects, Lead Drug & Affinity Recipe)</span></div>
                  </div>
                </div>

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
                <h3 style="color:var(--tx-0); font-size:20px; margin:8px 0 0; font-weight:700;">Diagram 2: Anti-Money Laundering (AML) & Fraud Architecture</h3>
              </div>
              <span style="font-size:32px;">💳</span>
            </div>

            <!-- DIAGRAM 2 FLOWCHART (FINANCIAL CUSTOMIZED) -->
            <div style="display:flex; justify-content:center;">
              <div class="arch-flowchart-container">
                
                <!-- Stage 1 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">1. Multi-Source Financial Data Ingestion</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Banking Feeds<span class="arch-sub-note">(Core Banking SQL, SWIFT Wires, KYC, OFAC Sanctions)</span></div>
                    <div class="arch-sub-box">Unstructured Compliance Docs<span class="arch-sub-note">(Loan Application PDFs, SAR Narratives, Emails)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 2 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">2. Financial Ingestion Pipelines</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Banking Pipeline<span class="arch-sub-note">Banking Schema Validation & Foreign Keys</span></div>
                    <div class="arch-sub-box">Unstructured Financial Pipeline<span class="arch-sub-note">PyMuPDF, Chunking, Financial NER & ChromaDB Vectors</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 3 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">3. Financial Unification & Entity Resolution</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box amber">Inter-Unstructured Mapping & Binding Keys<span class="arch-sub-note">(SAR Cross-Narrative Citation, Customer_TaxID, Account_IBAN, LEI_Code, Device_ID)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box">Financial Entity Resolution Engine<span class="arch-sub-note">Fuzzy Name, SSN Match, Device Hash & Metaphone</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 4 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">4. Neo4j & AML Cypher Detection Layer</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Financial Services OWL 2 Ontology Schema</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box blue">Neo4j AML Property Graph Storage<span class="arch-sub-note">(Customer)-[:OWNS]->(Account)-[:TRANSFERRED]->(Account), (Chunk)-[:MENTIONS]->(Customer)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box amber">Cypher AML Pattern Detection Engine<span class="arch-sub-note">(3-6 Hop Circular Wire Layering Rings, Shared Device Fraud Hubs)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 5 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">5. AML Graph-RAG & Leadership Output</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Financial Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Concrete Executive Leadership AML Deliverables<span class="arch-sub-note">($14.2M Laundering Exposure, Identified Suspects & Shell Co, 1-Click SAR Filing Package)</span></div>
                  </div>
                </div>

              </div>
            </div>

            <!-- PRECISE FINANCIAL EXECUTIVE DELIVERABLE BOX -->
            <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:20px; margin-top:20px;">
              <h4 style="color:var(--amber); margin-top:0; font-size:15px; font-weight:700;">🎯 Concrete Executive Leadership Output — Financial AML & Fraud</h4>
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:16px; margin-top:12px;">
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px;">
                  <div style="color:var(--amber); font-size:11px; font-weight:700;">QUANTIFIED MONEY LAUNDERING EXPOSURE</div>
                  <div style="font-size:22px; font-weight:700; color:var(--rose); margin:4px 0;">$14,250,000.00</div>
                  <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Identified across 3 active circular wire layering rings spanning 14 accounts and 4 jurisdictions.</p>
                </div>
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px;">
                  <div style="color:var(--amber); font-size:11px; font-weight:700;">ENGAGED BAD ACTORS & SHELL COS</div>
                  <div style="font-size:13px; font-weight:700; color:var(--tx-0); margin:4px 0;">Acme Shell LLC · John Doe · IP 192.168.1.50</div>
                  <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Connected via shared device fingerprint (MAC: 00-14-22) and common beneficial ownership agreements.</p>
                </div>
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px;">
                  <div style="color:var(--amber); font-size:11px; font-weight:700;">REGULATORY DELIVERABLE</div>
                  <div style="font-size:13px; font-weight:700; color:var(--emerald); margin:4px 0;">Automated 1-Click SAR Filing Package</div>
                  <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Pre-populated FinCEN Suspicious Activity Report complete with full graph evidence audit trail.</p>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- TAB 3: HEALTHCARE & LIFE SCIENCES DRUG DISCOVERY -->
        <div id="archContent-health" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            
            <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:16px;">
              <div>
                <span style="background:rgba(61,220,151,0.15); color:var(--emerald); font-size:11px; font-weight:700; padding:4px 10px; border-radius:6px; text-transform:uppercase;">Healthcare & Life Sciences Industry Blueprint</span>
                <h3 style="color:var(--tx-0); font-size:20px; margin:8px 0 0; font-weight:700;">Diagram 3: Drug Discovery & Biomarker Intelligence Architecture</h3>
              </div>
              <span style="font-size:32px;">🧬</span>
            </div>

            <!-- DIAGRAM 3 FLOWCHART (HEALTHCARE CUSTOMIZED) -->
            <div style="display:flex; justify-content:center;">
              <div class="arch-flowchart-container">
                
                <!-- Stage 1 -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">1. Multi-Source Bio Data Ingestion</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Life Sciences Feeds<span class="arch-sub-note">(ChEMBL Bioassays, UniProtKB, PubChem, ClinicalTrials)</span></div>
                    <div class="arch-sub-box">Unstructured Scientific Literature<span class="arch-sub-note">(PubMed Papers, bioRxiv Preprints, Patent PDFs, Protocols)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 2 -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">2. Life Sciences Ingestion Pipelines</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Bioassay Pipeline<span class="arch-sub-note">Bioassay Schema Validation & Foreign Keys</span></div>
                    <div class="arch-sub-box">Unstructured Scientific Pipeline<span class="arch-sub-note">PyMuPDF, Chunking, BioNER & ChromaDB Embeddings</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 3 -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">3. Bio Unification & Entity Resolution</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box emerald">Inter-Unstructured Mapping & Binding Keys<span class="arch-sub-note">(PubMed Citation Matching, UniProt_ID, InChIKey/SMILES, NCT_ID)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box">Bio Entity Resolution Engine<span class="arch-sub-note">Chemical Synonym Resolution, IUPAC & Gene Normalization</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 4 -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">4. Neo4j & Bio Cypher Detection Layer</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Life Sciences OWL 2 Ontology Schema</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box blue">Neo4j Bio Property Graph Storage<span class="arch-sub-note">(Compound)-[:BINDS_TO]->(TargetProtein)-[:PATHWAY]->(Disease)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Cypher Drug Discovery Pattern Engine<span class="arch-sub-note">(Nanomolar Affinity Paths IC50<50nM, Off-Target Toxicity Scans)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 5 -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">5. Bio Graph-RAG & Leadership Output</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Bio Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Concrete Executive Leadership Bio Deliverables<span class="arch-sub-note">(Lead Candidate Gefitinib/LG-772, IC50=2.3nM, Active Site Interaction Recipe)</span></div>
                  </div>
                </div>

              </div>
            </div>

            <!-- PRECISE BIOMEDICAL EXECUTIVE DELIVERABLE BOX -->
            <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:20px; margin-top:20px;">
              <h4 style="color:var(--emerald); margin-top:0; font-size:15px; font-weight:700;">🎯 Concrete Executive Leadership Output — Drug Discovery & Biomarkers</h4>
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:16px; margin-top:12px;">
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px;">
                  <div style="color:var(--emerald); font-size:11px; font-weight:700;">DISCOVERED LEAD DRUG CANDIDATE</div>
                  <div style="font-size:18px; font-weight:700; color:var(--emerald); margin:4px 0;">Gefitinib / LG-772</div>
                  <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Validated targeting <strong>EGFR L858R Mutation</strong> for Non-Small Cell Lung Cancer with nanomolar binding affinity <strong>IC50 = 2.3 nM</strong>.</p>
                </div>
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px;">
                  <div style="color:var(--emerald); font-size:11px; font-weight:700;">CHEMICAL INGREDIENT & RECIPE SYNTHESIS</div>
                  <div style="font-size:13px; font-weight:700; color:var(--tx-0); margin:4px 0;">Quinazoline Core + 3-Chloro-4-Fluoroaniline</div>
                  <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Interacts with ATP binding pocket hinge region (Lys745 / Met793) to inhibit ErbB signaling cascade.</p>
                </div>
                <div style="background:var(--surface); border:1px solid var(--line); border-radius:8px; padding:14px;">
                  <div style="color:var(--emerald); font-size:11px; font-weight:700;">OFF-TARGET TOXICITY WARNING</div>
                  <div style="font-size:13px; font-weight:700; color:var(--amber); margin:4px 0;">Low Risk · HER2 Cross-Binding Flag</div>
                  <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Graph traversal revealed minor affinity to HER2 (IC50 = 120 nM), manageable in Phase I trial protocol.</p>
                </div>
              </div>
            </div>

          </div>
        </div>

        <!-- TAB 4: 5-STEP TECHNICAL MECHANICS DEEP-DIVE -->
        <div id="archContent-breakdown" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:16px; font-weight:700;">🔍 5-Step Deep-Dive Technical Mechanics</h3>
            
            <div style="display:flex; flex-direction:column; gap:20px;">
              
              <!-- Breakdown 1 -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--amber); margin-top:0; font-size:15px;">1. How Multiple Unstructured Documents Map to Each Other</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  Unstructured documents (PDFs, Word docs, SAR narratives, scientific preprints) are linked using four complementary mechanics:<br>
                  • <strong>Co-Occurrence Entity Linking:</strong> When two documents mention the same entity (e.g., <code style="color:var(--emerald);">Customer_TaxID</code> or <code style="color:var(--emerald);">UniProt_ID</code>), a shared entity node acts as the bridge: <code style="color:var(--mono);">(Doc1)-[:MENTIONS]->(Entity)<-[:MENTIONS]-(Doc2)</code>.<br>
                  • <strong>Cross-Document Citation & Reference Extraction:</strong> Regex and LLM extraction parse explicit citations (e.g. PubMed <code style="color:var(--mono);">PMID:3829102</code> or Clinical Trial <code style="color:var(--mono);">NCT00003180</code>), creating explicit <code style="color:var(--mono);">(Doc1)-[:CITES]->(Doc2)</code> relationships.<br>
                  • <strong>Dense Vector Embedding Distance:</strong> Text chunks are embedded into 384-dimensional vectors via ChromaDB. Chunks with cosine similarity $>0.82$ generate implicit semantic links <code style="color:var(--mono);">(Chunk1)-[:SIMILAR_TOPIC]->(Chunk2)</code>.<br>
                  • <strong>Cross-Document Coreference Resolution:</strong> An LLM resolves ambiguous references (e.g., <em>"the suspect company"</em> in SAR 1 vs <em>"Acme Corp"</em> in Loan PDF 2) to the same canonical entity.
                </p>
              </div>

              <!-- Breakdown 2 -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--emerald); margin-top:0; font-size:15px;">2. How Unstructured Data Binds with Structured Data via Mapping Keys</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  Once unstructured documents are mapped together, they are anchored to structured SQL/CSV tables using <strong>Canonical Business Mapping Keys</strong>:<br>
                  • <strong>Extraction & Validation:</strong> During unstructured ingestion, spaCy NER and LLM JSON extraction extract canonical business keys (<code style="color:var(--emerald);">Tax_ID/SSN</code>, <code style="color:var(--emerald);">Account_IBAN</code>, <code style="color:var(--emerald);">UniProt_Accession</code>, <code style="color:var(--emerald);">InChIKey/SMILES</code>, <code style="color:var(--emerald);">NCT_ID</code>).<br>
                  • <strong>Cypher Binding Script:</strong> The backend executes Cypher <code style="color:var(--mono);">MERGE</code> commands that bind document chunk nodes directly to primary structured entity nodes:<br>
                  <code style="color:var(--mono); display:block; background:#121824; padding:8px; border-radius:6px; margin-top:6px; font-size:11.5px;">MATCH (chunk:Chunk {id: $chunk_id}), (acc:Account {iban: $extracted_iban}) MERGE (chunk)-[:EVIDENCE_FOR]->(acc)</code>
                </p>
              </div>

              <!-- Breakdown 3 -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:#60A5FA; margin-top:0; font-size:15px;">3. Ultimate Joined Data Structure (Property Graph Model)</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  The ultimate unified data structure is a <strong>Multi-Modal Property Graph</strong> in Neo4j comprising:<br>
                  • <strong>Domain Nodes:</strong> <code style="color:var(--mono);">Customer</code>, <code style="color:var(--mono);">Account</code>, <code style="color:var(--mono);">Compound</code>, <code style="color:var(--mono);">TargetProtein</code>, <code style="color:var(--mono);">Pathway</code>, <code style="color:var(--mono);">Disease</code>.<br>
                  • <strong>Document Metadata Nodes:</strong> <code style="color:var(--mono);">Document</code>, <code style="color:var(--mono);">Chunk</code>, <code style="color:var(--mono);">ClinicalTrial</code>.<br>
                  • <strong>Properties:</strong> Biological/financial quantitative attributes (<code style="color:var(--mono); font-size:11px;">ic50_nm: 2.3</code>, <code style="color:var(--mono); font-size:11px;">amount_usd: 45000</code>), timestamps, and complete audit provenance (<code style="color:var(--mono); font-size:11px;">source_file: "sar_09.pdf"</code>, <code style="color:var(--mono); font-size:11px;">page: 4</code>).<br>
                  • <strong>Typed Relationships:</strong> <code style="color:var(--mono); font-size:11px;">OWNS</code>, <code style="color:var(--mono); font-size:11px;">TRANSFERRED_FUNDS</code>, <code style="color:var(--mono); font-size:11px;">BINDS_TO</code>, <code style="color:var(--mono); font-size:11px;">PART_OF_PATHWAY</code>, <code style="color:var(--mono); font-size:11px;">EVIDENCE_FOR</code>.
                </p>
              </div>

              <!-- Breakdown 4 -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--amber); margin-top:0; font-size:15px;">4. How Pattern Recognition Works</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  Unlike statistical machine learning, pattern recognition in GRAPHEN operates via <strong>Graph Topology Motif Matching & Graph Algorithms</strong>:<br>
                  • <strong>Structural Motif Matching:</strong> Declarative Cypher queries search for multi-hop graph sub-structures, such as circular layering paths <code style="color:var(--mono);">(acc)-[:TRANSFERRED*3..6]->(acc)</code> or compound-target-pathway chains.<br>
                  • <strong>PageRank Centrality:</strong> Ranks entity node importance to discover central money laundering kingpins or key biological hub proteins.<br>
                  • <strong>Louvain Community Detection:</strong> Identifies tightly connected sub-networks (e.g. hidden synthetic identity fraud rings sharing IP addresses or off-target kinase toxicity clusters).
                </p>
              </div>

              <!-- Breakdown 5 -->
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--emerald); margin-top:0; font-size:15px;">5. Precise Executive Leadership Outputs</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  Instead of generic summaries, leadership receives concrete, quantifiable business outcomes:<br>
                  • <strong>Financial AML Output:</strong> Exact dollar laundering exposure identified (<strong>$14.25M across 3 layering rings</strong>), specific bad actors (`Acme Shell LLC`, `John Doe`), shared device IPs (`192.168.1.50`), and an automated 1-click Regulatory SAR filing package.<br>
                  • <strong>Drug Discovery Output:</strong> Validated lead candidate (<strong>Gefitinib / LG-772</strong> targeting EGFR L858R mutation with nanomolar affinity <strong>IC50 = 2.3 nM</strong>), exact chemical active site binding recipe (Quinazoline core interacting with Met793 hinge), and off-target HER2 cross-binding toxicity alerts.
                </p>
              </div>

            </div>
          </div>
        </div>

        <!-- TAB 5: TECH STACK & CONTRIBUTION OF NEO4J, PROTEGE & CYPHER -->
        <div id="archContent-techstack" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:16px; font-weight:700;">⚙️ Technical Stack & Architectural Contributions</h3>
            
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(280px, 1fr)); gap:18px;">
              
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
                  <h4 style="color:var(--tx-0); margin:0; font-size:15px;">Neo4j Property Graph Database</h4>
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

# Update JS helper function showArchTab in index.html to handle breakdown tab
show_arch_tab_js = '''    window.showArchTab = function(tabName) {
      const tabs = ['pipeline', 'fintech', 'health', 'breakdown', 'techstack'];
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
    };'''

# Replace view-arch in index.html
start_pos = txt.find('<div class="view" id="view-arch">')
end_pos = txt.find('<!-- ============ STRUCTURED PIPELINE ============ -->')
if start_pos != -1 and end_pos != -1:
    txt = txt[:start_pos] + view_arch_html + '\n\n      ' + txt[end_pos:]
    print("Successfully replaced view-arch block in index.html.")

# Update showArchTab
get_tab_pattern = r'window\.showArchTab\s*=\s*function\s*\([^\)]*\)\s*\{[\s\S]*?\};'
if re.search(get_tab_pattern, txt):
    txt = re.sub(get_tab_pattern, show_arch_tab_js, txt, count=1)
    print("Updated showArchTab JS helper.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Updated index.html with complete 5-step technical mechanics and updated diagrams.")
