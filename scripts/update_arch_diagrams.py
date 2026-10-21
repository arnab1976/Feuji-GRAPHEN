import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# 1. Add CSS for flowchart diagrams if not present
arch_css = '''
    .arch-flowchart-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 10px;
      margin: 20px 0 30px;
      width: 100%;
      max-width: 820px;
    }
    .arch-stage-box {
      border: 1.5px solid var(--line-strong, #3A4763);
      border-radius: 10px;
      background: var(--surface, #1A2234);
      padding: 14px 18px;
      width: 100%;
      box-shadow: 0 4px 16px rgba(0,0,0,0.22);
    }
    .arch-stage-title {
      font-size: 13.5px;
      font-weight: 700;
      color: var(--tx-0, #FFFFFF);
      margin-bottom: 10px;
      padding-bottom: 6px;
      border-bottom: 1px solid var(--line-soft, #2A364F);
      letter-spacing: 0.02em;
    }
    .arch-sub-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
    }
    .arch-sub-stack {
      display: flex;
      flex-direction: column;
      gap: 8px;
      align-items: center;
      width: 100%;
    }
    .arch-sub-box {
      border: 1px solid var(--line, #2E3B54);
      border-radius: 6px;
      background: var(--bg-2, #121824);
      padding: 10px 14px;
      text-align: center;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--tx-1, #E2E8F0);
      width: 100%;
    }
    .arch-sub-box.amber {
      border-color: rgba(255, 159, 10, 0.45);
      background: rgba(255, 159, 10, 0.07);
      color: var(--amber, #FF9F0A);
    }
    .arch-sub-box.emerald {
      border-color: rgba(61, 220, 151, 0.45);
      background: rgba(61, 220, 151, 0.07);
      color: var(--emerald, #3DDC97);
    }
    .arch-sub-box.blue {
      border-color: rgba(96, 165, 250, 0.45);
      background: rgba(96, 165, 250, 0.07);
      color: #60A5FA;
    }
    .arch-sub-note {
      display: block;
      font-size: 11px;
      font-weight: 400;
      color: var(--tx-2, #94A3B8);
      margin-top: 3px;
    }
    .arch-arrow-down {
      font-size: 18px;
      color: var(--amber, #FF9F0A);
      font-weight: 700;
      margin: -2px 0;
    }
    .arch-arrow-inner {
      font-size: 14px;
      color: var(--tx-3, #64748B);
      margin: -4px 0;
    }'''

if '.arch-flowchart-container' not in txt:
    head_pos = txt.find('</head>')
    if head_pos != -1:
        txt = txt[:head_pos] + '<style>' + arch_css + '</style>\n' + txt[head_pos:]
        print("Added flowchart CSS styles.")

# 2. Build updated view-arch HTML containing all 3 customized diagrams
view_arch_html = '''      <!-- ============ SOLUTION ARCHITECTURE & TECHNICAL BLUEPRINT ============ -->
      <div class="view" id="view-arch">
        <div class="page-head">
          <div class="eyebrow">APPENDIX · TECHNICAL BLUEPRINT & SOLUTION ARCHITECTURE</div>
          <div class="page-title">Knowledge Graph Solution Architecture</div>
          <div class="page-sub">End-to-end architectural specification, structured & unstructured data unification, entity resolution framework, Cypher pattern detection, and executive leadership outcomes for Financial AML/Fraud Risk & Healthcare Drug Discovery.</div>
        </div>

        <!-- Section Navigation Pills -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" onclick="showArchTab('pipeline')" id="archTab-pipeline" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:600;">📌 10-Step Pipeline Architecture Diagram</button>
          <button type="button" onclick="showArchTab('fintech')" id="archTab-fintech" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">💳 Financial Services — AML & Fraud Diagram</button>
          <button type="button" onclick="showArchTab('health')" id="archTab-health" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">🧬 Healthcare — Drug Discovery Diagram</button>
          <button type="button" onclick="showArchTab('techstack')" id="archTab-techstack" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">⚙️ Tech Stack & Role of Neo4j, Protégé & Cypher</button>
        </div>

        <!-- TAB 1: 10-STEP PIPELINE BLUEPRINT & GENERAL DIAGRAM -->
        <div id="archContent-pipeline" class="arch-tab-content">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:8px; font-weight:700;">🌐 Diagram 1: Overall 10-Step Knowledge Graph Architecture</h3>
            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Master architectural flow detailing multi-source ingestion, dual structured/unstructured processing pipelines, mapping key unification, Neo4j graph storage, Cypher pattern detection, and executive output.
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
                    <div class="arch-sub-box amber">Unified Mapping Keys<span class="arch-sub-note">(Tax_ID, IBAN, UniProt_ID, SMILES, NCT_ID)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box">Entity Resolution Engine<span class="arch-sub-note">Fuzzy, Phonetic, Vector & Rules</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 4 -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">4. Neo4j & Cypher Detection Layer</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Protégé OWL 2 Ontology Schema</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box blue">Neo4j Property Graph Storage<span class="arch-sub-note">MERGE Nodes & Directed Edges</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box amber">Cypher Pattern Detection Engine<span class="arch-sub-note">(Layering Rings, Affinity Paths, Fraud Hubs)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 5 -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">5. Hybrid Graph-RAG & Leadership Output</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Executive Leadership Deliverables<span class="arch-sub-note">(Risk Maps, SAR Package, Target-Lead Matrix)</span></div>
                  </div>
                </div>

              </div>
            </div>

            <!-- 10-STEP SUMMARY GRID -->
            <h4 style="color:var(--tx-0); font-size:15px; margin:24px 0 12px; font-weight:700;">📋 10-Step Pipeline Execution Summary</h4>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:14px;">
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 1</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Objective & Ontology Definition</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Imports Protégé OWL 2 taxonomy and defines domain entity/relationship schemas.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 2</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Multi-Source Data Ingestion</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Ingests structured tables (SQL, CSV) and unstructured documents (PDFs, Word docs).</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 3</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Structured Pipeline</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Schema validation, foreign key mapping, data type coercion, and relational join tuple building.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 4</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Unstructured Pipeline</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">PyMuPDF extraction, sentence chunking, spaCy NER, LLM JSON extraction & ChromaDB vectors.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 5</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Modality Unification</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Joins document chunks and structured record nodes via unified business mapping keys.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 6</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Entity Resolution Engine</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Fuzzy string, phonetic, vector similarity, and deterministic rules merge duplicate nodes.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 7</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Neo4j Graph Construction</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Executes Cypher MERGE scripts to build property nodes and directed topology edges.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 8</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Cypher Pattern Detection</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Executes graph pattern matching for circular layering, affinity paths, and fraud hubs.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 9</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Hybrid Graph-RAG</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Synthesizes ChromaDB semantic vectors with Neo4j graph context for zero-hallucination Q&A.</p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:8px; padding:14px;">
                <div style="color:var(--amber); font-size:11px; font-weight:700;">STEP 10</div>
                <h5 style="color:var(--tx-0); margin:2px 0 4px; font-size:13px;">Executive Deliverables</h5>
                <p style="color:var(--tx-2); font-size:11.5px; margin:0;">Delivers interactive dashboards, decision scorecards, and regulatory compliance packages.</p>
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

            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Customized architectural flow specifying core banking feeds, SWIFT wire transfers, OFAC sanctions, SAR narratives, financial entity resolution, and AML layering ring detection.
            </p>

            <!-- DIAGRAM 2 FLOWCHART (FINANCIAL CUSTOMIZED) -->
            <div style="display:flex; justify-content:center;">
              <div class="arch-flowchart-container">
                
                <!-- Stage 1 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">1. Multi-Source Financial Data Ingestion</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Banking Feeds<span class="arch-sub-note">(Core Banking SQL, SWIFT Wires, KYC, OFAC)</span></div>
                    <div class="arch-sub-box">Unstructured Compliance Docs<span class="arch-sub-note">(Loan Application PDFs, SAR Narratives, Emails)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 2 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">2. Financial Ingestion Pipelines</div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Banking Pipeline<span class="arch-sub-note">Banking Schema Validation & Foreign Keys</span></div>
                    <div class="arch-sub-box">Unstructured Financial Pipeline<span class="arch-sub-note">PyMuPDF, Chunking, Financial NER & Vectors</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 3 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">3. Financial Unification & Entity Resolution</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box amber">Unified Financial Mapping Keys<span class="arch-sub-note">(Customer_TaxID, Account_IBAN, LEI_Code, Device_ID)</span></div>
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
                    <div class="arch-sub-box blue">Neo4j AML Property Graph Storage<span class="arch-sub-note">(Customer)-[:OWNS]->(Account)-[:TRANSFERRED]->(Account)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box amber">Cypher AML Pattern Detection Engine<span class="arch-sub-note">(Circular Wire Layering Rings, Shared Device Hubs)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 5 -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">5. AML Graph-RAG & Leadership Output</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Financial Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Executive Leadership AML Deliverables<span class="arch-sub-note">(Interactive Network Explorer, Automated SAR Package, Risk Score Matrix)</span></div>
                  </div>
                </div>

              </div>
            </div>

            <!-- EXECUTIVE LEADERSHIP SECTION -->
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:24px;">
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--amber); margin-top:0; font-size:14px;">🎯 Purpose & Executive Objective</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  Uncover sophisticated multi-account circular wire transfers, shell company networks, shared device/IP fraud rings, and undisclosed Ultimate Beneficial Owners (UBOs) that single-table SQL rule engines fail to detect.
                </p>
              </div>
              <div style="background:var(--bg-2); border:1px solid var(--line-soft); border-radius:10px; padding:18px;">
                <h4 style="color:var(--emerald); margin-top:0; font-size:14px;">🚀 Executive Leadership Deliverable</h4>
                <p style="color:var(--tx-2); font-size:12.5px; line-height:1.6; margin:0;">
                  <strong>1. Interactive Financial Network Explorer:</strong> Real-time 360° graph view of high-risk account clusters.<br>
                  <strong>2. Automated SAR Generator:</strong> One-click regulatory Suspicious Activity Report with graph evidence traces.<br>
                  <strong>3. AML Risk Score Matrix:</strong> Quantified entity risk score based on PageRank & Cypher cycle counts.
                </p>
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

            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Customized architectural flow specifying ChEMBL bioassays, UniProtKB protein targets, PubChem SMILES structures, PubMed preprints, bio-entity resolution, and nanomolar affinity path discovery.
            </p>

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
                    <div class="arch-sub-box emerald">Unified Life Sciences Mapping Keys<span class="arch-sub-note">(UniProt_ID, InChIKey/SMILES, NCBI_Gene_ID, NCT_ID)</span></div>
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
                    <div class="arch-sub-box emerald">Cypher Drug Discovery Pattern Engine<span class="arch-sub-note">(Nanomolar Affinity Paths, Off-Target Toxicity Scans)</span></div>
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 5 -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">5. Bio Graph-RAG & Leadership Output</div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Bio Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Executive Leadership Bio Deliverables<span class="arch-sub-note">(High-Confidence Target-Lead Matrix, Off-Target Toxicity Heatmap, Insight Brief)</span></div>
                  </div>
                </div>

              </div>
            </div>

            <!-- EXECUTIVE LEADERSHIP SECTION -->
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:18px; margin-top:24px;">
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

          </div>
        </div>

        <!-- TAB 4: TECH STACK & CONTRIBUTION OF NEO4J, PROTEGE & CYPHER -->
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

# Replace view-arch in index.html
start_pos = txt.find('<div class="view" id="view-arch">')
end_pos = txt.find('<!-- ============ STRUCTURED PIPELINE ============ -->')
if start_pos != -1 and end_pos != -1:
    txt = txt[:start_pos] + view_arch_html + '\n\n      ' + txt[end_pos:]
    print("Successfully replaced view-arch block in index.html.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Updated index.html with all 3 customized architectural diagrams.")
