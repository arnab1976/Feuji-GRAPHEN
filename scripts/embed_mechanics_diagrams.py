import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# Build updated view-arch HTML containing embedded deep-dive mechanics across all 3 diagrams + dedicated breakdown flowchart
view_arch_html = '''      <!-- ============ SOLUTION ARCHITECTURE & TECHNICAL BLUEPRINT ============ -->
      <div class="view" id="view-arch">
        <div class="page-head">
          <div class="eyebrow">APPENDIX · TECHNICAL BLUEPRINT & SOLUTION ARCHITECTURE</div>
          <div class="page-title">Knowledge Graph Solution Architecture</div>
          <div class="page-sub">Comprehensive architectural specification with 5 embedded technical mechanics: inter-unstructured document mapping, key binding engine, property graph data structure, Cypher pattern recognition, and concrete executive deliverables.</div>
        </div>

        <!-- Section Navigation Pills -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" onclick="showArchTab('pipeline')" id="archTab-pipeline" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:600;">📌 10-Step Master Pipeline Diagram</button>
          <button type="button" onclick="showArchTab('fintech')" id="archTab-fintech" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">💳 Financial Services — AML Diagram & Outputs</button>
          <button type="button" onclick="showArchTab('health')" id="archTab-health" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">🧬 Healthcare — Drug Discovery Diagram & Outputs</button>
          <button type="button" onclick="showArchTab('breakdown')" id="archTab-breakdown" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">🔍 5-Step Technical Mechanics Flowchart & Text</button>
          <button type="button" onclick="showArchTab('techstack')" id="archTab-techstack" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">⚙️ Neo4j, Protégé OWL & Cypher Roles</button>
        </div>

        <!-- TAB 1: 10-STEP PIPELINE BLUEPRINT & MASTER EMBEDDED DIAGRAM -->
        <div id="archContent-pipeline" class="arch-tab-content">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:8px; font-weight:700;">🌐 Diagram 1: Master Architecture with Embedded 5-Step Mechanics</h3>
            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Master architectural flow showing multi-source ingestion, ingestion pipelines, key binding, Neo4j graph storage, Cypher pattern recognition, and executive deliverables with the 5 core mechanics embedded into each stage.
            </p>

            <!-- DIAGRAM 1 FLOWCHART WITH EMBEDDED MECHANICS -->
            <div style="display:flex; justify-content:center;">
              <div class="arch-flowchart-container">
                
                <!-- Stage 1 & 2: Ingestion & Pipelines + Mechanic 1 Embedded -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">1. Multi-Source Ingestion & Pipelines <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Mechanic 1 Embedded: Inter-Unstructured Mapping]</span></div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured CSV / SQL Feeds<span class="arch-sub-note">(Transactions, Assays, KYC)</span></div>
                    <div class="arch-sub-box">Unstructured PDF / Word Docs<span class="arch-sub-note">(SAR Narratives, Protocols, Papers)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--amber);">Mechanic 1 (Document-to-Document Mapping):</strong> Co-occurrence entity bridges <code style="color:var(--mono);">(Doc1)-[:MENTIONS]->(Entity)<-[:MENTIONS]-(Doc2)</code>, Citation reference parsing (PMID/NCT), ChromaDB vector similarity ($>0.82$ Cosine), and cross-document coreference resolution.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 3 + Mechanic 2 Embedded -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">2. Unification & Key Binding Engine <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Mechanic 2 Embedded: Key Binding]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box amber">Canonical Business Mapping Keys<span class="arch-sub-note">(Tax_ID, IBAN, UniProt_ID, SMILES, NCT_ID)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box">Entity Resolution & Binding Script<span class="arch-sub-note">Executing Cypher: MERGE (Chunk)-[:EVIDENCE_FOR]->(StructuredEntity)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--amber);">Mechanic 2 (Structured Key Binding):</strong> Parses canonical keys via regex + LLM JSON Schema, then anchors unstructured text chunks directly to primary relational record nodes in Neo4j.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 4 Part A + Mechanic 3 Embedded -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">3. Neo4j Property Graph Storage <span style="float:right; color:#60A5FA; font-size:11px; font-weight:600;">[Mechanic 3 Embedded: Graph Data Structure]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Protégé OWL 2 Ontology Governance Schema</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box blue">Multi-Modal Property Graph Data Structure<span class="arch-sub-note">(Domain Nodes + Document Nodes + Attributes + Relationships + Provenance Metadata)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:#60A5FA;">Mechanic 3 (Ultimate Data Structure):</strong> Property graph unifying domain nodes (Customer/Compound) and document nodes (Chunk) with attributes (<code style="color:var(--mono);">ic50_nm</code>, <code style="color:var(--mono);">amount_usd</code>) and full source provenance.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 4 Part B + Mechanic 4 Embedded -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">4. Pattern Recognition Engine <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Mechanic 4 Embedded: Graph Pattern Recognition]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box amber">Cypher Pattern Recognition Engine<span class="arch-sub-note">(Topology Motif Matching, N-Hop Cycle Traversal, PageRank Centrality & Louvain Communities)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--amber);">Mechanic 4 (Pattern Recognition):</strong> Replaces black-box ML with explicit Cypher graph motif queries, N-hop cycle detection, PageRank entity centrality, and Louvain community clustering.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 5 + Mechanic 5 Embedded -->
                <div class="arch-stage-box">
                  <div class="arch-stage-title">5. Hybrid Graph-RAG & Leadership Output <span style="float:right; color:var(--emerald); font-size:11px; font-weight:600;">[Mechanic 5 Embedded: Executive Outputs]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Concrete Executive Leadership Deliverables<span class="arch-sub-note">(Quantified Dollar Laundering Exposure, Suspect List, Discovered Lead Drug & Affinity Recipe)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--emerald);">Mechanic 5 (Leadership Deliverables):</strong> Delivers precise, actionable outputs: exact dollar laundering exposure ($14.25M), suspect accounts, validated lead drug candidates (Gefitinib IC50=2.3nM), and binding recipes.
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
                <h3 style="color:var(--tx-0); font-size:20px; margin:8px 0 0; font-weight:700;">Diagram 2: Financial AML Architecture with Embedded Mechanics</h3>
              </div>
              <span style="font-size:32px;">💳</span>
            </div>

            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Customized architectural flow specifying core banking SQL, SWIFT wires, OFAC sanctions, SAR narratives, financial entity resolution, and AML layering ring detection with the 5 mechanics embedded into every stage.
            </p>

            <!-- DIAGRAM 2 FLOWCHART (FINANCIAL CUSTOMIZED WITH EMBEDDED MECHANICS) -->
            <div style="display:flex; justify-content:center;">
              <div class="arch-flowchart-container">
                
                <!-- Stage 1 & 2 + Mechanic 1 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">1. Financial Data Ingestion & Pipelines <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Mechanic 1: Financial Document Mapping]</span></div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Banking Feeds<span class="arch-sub-note">(Core Banking SQL, SWIFT Wires, KYC, OFAC Sanctions)</span></div>
                    <div class="arch-sub-box">Unstructured Compliance Docs<span class="arch-sub-note">(Loan Application PDFs, SAR Narratives, Emails)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--amber);">Mechanic 1 (Financial Document Mapping):</strong> Links SAR Narratives to Loan Applications via co-occurrence customer bridges, SAR case reference citations (<code style="color:var(--mono);">SAR-2026-09</code>), and ChromaDB compliance vector similarity.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 3 + Mechanic 2 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">2. Financial Unification & Key Binding <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Mechanic 2: Financial Key Binding]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box amber">Canonical Financial Mapping Keys<span class="arch-sub-note">(Customer_TaxID, Account_IBAN, LEI_Code, Device_ID)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box">Financial Entity Resolution Script<span class="arch-sub-note">Executing Cypher: MERGE (Chunk)-[:EVIDENCE_FOR]->(Account)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--amber);">Mechanic 2 (Financial Key Binding):</strong> Extracts <code style="color:var(--emerald);">Customer_TaxID</code> and <code style="color:var(--emerald);">Account_IBAN</code> from unstructured SAR narratives to anchor document text directly to SQL account nodes.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 4 Part A + Mechanic 3 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">3. Neo4j AML Property Graph Storage <span style="float:right; color:#60A5FA; font-size:11px; font-weight:600;">[Mechanic 3: AML Property Graph Structure]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Financial Services OWL 2 Ontology Schema</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box blue">AML Multi-Modal Property Graph Data Structure<span class="arch-sub-note">(Nodes: Customer/Account/Device/Chunk, Edges: OWNS/TRANSFERRED/MENTIONS)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:#60A5FA;">Mechanic 3 (AML Data Structure):</strong> Graph topology uniting customer accounts, SWIFT wire transaction amounts (<code style="color:var(--mono);">amount_usd</code>), timestamps, and SAR chunk source provenance.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 4 Part B + Mechanic 4 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">4. AML Pattern Recognition Engine <span style="float:right; color:var(--amber); font-size:11px; font-weight:600;">[Mechanic 4: Wire Ring Recognition]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box amber">Cypher AML Pattern Recognition Engine<span class="arch-sub-note">(3-6 Hop Circular Wire Layering Rings, Shared Device Fraud Hubs, PageRank Centrality)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--amber);">Mechanic 4 (AML Pattern Recognition):</strong> Executes declarative Cypher queries searching for N-hop circular wire paths <code style="color:var(--mono);">(acc)-[:TRANSFERRED*3..6]->(acc)</code> and PageRank ringleaders.
                  </div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <!-- Stage 5 + Mechanic 5 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">5. AML Graph-RAG & Executive Output <span style="float:right; color:var(--emerald); font-size:11px; font-weight:600;">[Mechanic 5: AML Leadership Outputs]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Financial Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Concrete Executive Leadership AML Deliverables<span class="arch-sub-note">($14.25M Laundering Exposure, Identified Suspects & Shell Co, 1-Click SAR Package)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--emerald);">Mechanic 5 (AML Deliverables):</strong> Delivers exact dollar laundering exposure ($14.25M across 3 rings), suspect entities (`Acme Shell LLC`, `John Doe`, `IP 192.168.1.50`), and automated FinCEN SAR filing packages.
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
                <h3 style="color:var(--tx-0); font-size:20px; margin:8px 0 0; font-weight:700;">Diagram 3: Drug Discovery Architecture with Embedded Mechanics</h3>
              </div>
              <span style="font-size:32px;">🧬</span>
            </div>

            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Customized architectural flow specifying ChEMBL bioassays, UniProtKB protein targets, PubChem SMILES structures, PubMed preprints, bio-entity resolution, and nanomolar affinity path discovery with the 5 mechanics embedded into every stage.
            </p>

            <!-- DIAGRAM 3 FLOWCHART (HEALTHCARE CUSTOMIZED WITH EMBEDDED MECHANICS) -->
            <div style="display:flex; justify-content:center;">
              <div class="arch-flowchart-container">
                
                <!-- Stage 1 & 2 + Mechanic 1 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">1. Bio Data Ingestion & Pipelines <span style="float:right; color:var(--emerald); font-size:11px; font-weight:600;">[Mechanic 1: Bio Literature Mapping]</span></div>
                  <div class="arch-sub-grid">
                    <div class="arch-sub-box">Structured Life Sciences Feeds<span class="arch-sub-note">(ChEMBL Bioassays, UniProtKB, PubChem, ClinicalTrials)</span></div>
                    <div class="arch-sub-box">Unstructured Scientific Literature<span class="arch-sub-note">(PubMed Papers, bioRxiv Preprints, Patent PDFs, Protocols)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--emerald);">Mechanic 1 (Bio Literature Mapping):</strong> Links PubMed papers to bioRxiv preprints via PubMed citations (<code style="color:var(--mono);">PMID:3829102</code>), target gene co-occurrences (<code style="color:var(--mono);">EGFR L858R</code>), and ChromaDB vector similarity.
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 3 + Mechanic 2 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">2. Bio Unification & Key Binding <span style="float:right; color:var(--emerald); font-size:11px; font-weight:600;">[Mechanic 2: Bio Key Binding]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box emerald">Canonical Life Sciences Mapping Keys<span class="arch-sub-note">(UniProt_ID, InChIKey/SMILES, NCBI_Gene_ID, NCT_ID)</span></div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box">Bio Entity Resolution Script<span class="arch-sub-note">Executing Cypher: MERGE (Chunk)-[:EVIDENCE_FOR]->(TargetProtein)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--emerald);">Mechanic 2 (Bio Key Binding):</strong> Extracts <code style="color:var(--emerald);">UniProt_Accession</code> and <code style="color:var(--emerald);">InChIKey</code> from literature chunks to anchor paper text directly to ChEMBL compound nodes in Neo4j.
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 4 Part A + Mechanic 3 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">3. Neo4j Bio Property Graph Storage <span style="float:right; color:#60A5FA; font-size:11px; font-weight:600;">[Mechanic 3: Bio Property Graph Structure]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Life Sciences OWL 2 Ontology Schema</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box blue">Bio Multi-Modal Property Graph Data Structure<span class="arch-sub-note">(Nodes: Compound/Target/Pathway/Disease, Edges: BINDS_TO/PATHWAY)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:#60A5FA;">Mechanic 3 (Bio Data Structure):</strong> Graph topology uniting compounds, binding affinities (<code style="color:var(--mono);">ic50_nm: 2.3</code>), pathways (<code style="color:var(--mono);">ErbB</code>), and PubMed literature chunk source provenance.
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 4 Part B + Mechanic 4 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">4. Bio Cypher Pattern Recognition Engine <span style="float:right; color:var(--emerald); font-size:11px; font-weight:600;">[Mechanic 4: Affinity Path Recognition]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box emerald">Cypher Drug Discovery Pattern Engine<span class="arch-sub-note">(Nanomolar Affinity Paths IC50<50nM, Off-Target Toxicity Scans, Pathway Validation)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--emerald);">Mechanic 4 (Bio Pattern Recognition):</strong> Executes Cypher queries traversing <code style="color:var(--mono);">(Compound)-[:BINDS_TO]->(TargetProtein)-[:PATHWAY]->(Disease)</code> to discover high-affinity leads and off-target HER2 toxicity risks.
                  </div>
                </div>
                <div class="arch-arrow-down" style="color:var(--emerald);">↓</div>

                <!-- Stage 5 + Mechanic 5 Embedded -->
                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">5. Bio Graph-RAG & Leadership Output <span style="float:right; color:var(--emerald); font-size:11px; font-weight:600;">[Mechanic 5: Bio Leadership Outputs]</span></div>
                  <div class="arch-sub-stack">
                    <div class="arch-sub-box">Hybrid Bio Graph-RAG Q&A Engine</div>
                    <div class="arch-arrow-inner">↓</div>
                    <div class="arch-sub-box emerald">Concrete Executive Leadership Bio Deliverables<span class="arch-sub-note">(Lead Candidate Gefitinib/LG-772, IC50=2.3nM, Active Site Interaction Recipe)</span></div>
                  </div>
                  <div style="margin-top:10px; padding:8px 12px; background:var(--bg-2); border:1px dashed var(--line-soft); border-radius:6px; font-size:11.5px; color:var(--tx-2);">
                    <strong style="color:var(--emerald);">Mechanic 5 (Bio Deliverables):</strong> Delivers validated lead drug candidates (Gefitinib / LG-772, IC50=2.3nM), chemical active site binding recipes (Quinazoline core + Met793 hinge), and off-target HER2 toxicity heatmaps.
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

        <!-- TAB 4: 5-STEP TECHNICAL MECHANICS FLOWCHART & TEXT -->
        <div id="archContent-breakdown" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1px solid var(--line); border-radius:12px; padding:24px; margin-bottom:24px; box-shadow:0 8px 24px rgba(0,0,0,0.18);">
            
            <h3 style="color:var(--tx-0); font-size:18px; margin-top:0; margin-bottom:8px; font-weight:700;">🔍 Diagram 4: 5-Step Deep-Dive Technical Mechanics Flowchart</h3>
            <p style="color:var(--tx-2); font-size:13px; line-height:1.5; margin-bottom:20px;">
              Visual flowchart representation showing how unstructured documents map together, bind to structured composite data via mapping keys, build the ultimate property graph data structure, execute pattern recognition, and produce concrete executive leadership deliverables.
            </p>

            <!-- DEDICATED DIAGRAM 4 FLOWCHART FOR MECHANICS TAB -->
            <div style="display:flex; justify-content:center; margin-bottom:24px;">
              <div class="arch-flowchart-container">
                
                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">Mechanic 1: Inter-Unstructured Document Mapping</div>
                  <div class="arch-sub-box">Co-occurrence Entity Bridges + Citation Extraction (PMID/NCT) + ChromaDB Vector Similarity (&gt;0.82) + Coreference Resolution</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">Mechanic 2: Unstructured-to-Structured Mapping Key Binding</div>
                  <div class="arch-sub-box amber">Canonical Keys (Tax_ID, IBAN, UniProt_ID, SMILES, NCT_ID) &rarr; Cypher MERGE (Chunk)-[:EVIDENCE_FOR]-&gt;(StructuredEntity)</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <div class="arch-stage-box" style="border-color:rgba(96,165,250,0.5);">
                  <div class="arch-stage-title" style="color:#60A5FA;">Mechanic 3: Ultimate Joined Property Graph Data Structure</div>
                  <div class="arch-sub-box blue">Multi-Modal Property Graph: Domain Nodes (Customer/Compound) + Document Nodes (Chunk) + Quantitative Attributes + Audit Provenance</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <div class="arch-stage-box" style="border-color:rgba(255,159,10,0.5);">
                  <div class="arch-stage-title" style="color:var(--amber);">Mechanic 4: Graph Topology Pattern Recognition Engine</div>
                  <div class="arch-sub-box amber">Cypher Structural Motif Queries + N-Hop Wire Layering Cycles + PageRank Centrality + Louvain Community Detection</div>
                </div>
                <div class="arch-arrow-down">↓</div>

                <div class="arch-stage-box" style="border-color:rgba(61,220,151,0.5);">
                  <div class="arch-stage-title" style="color:var(--emerald);">Mechanic 5: Precise Executive Leadership Deliverables</div>
                  <div class="arch-sub-box emerald">Financial AML ($14.25M Exposure, Suspect List, 1-Click SAR) | Drug Discovery (Gefitinib IC50=2.3nM, Active Site Binding Recipe)</div>
                </div>

              </div>
            </div>

            <!-- 5-STEP DETAILED TEXT DESCRIPTION BOXES -->
            <div style="display:flex; flex-direction:column; gap:18px;">
              
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

# Replace view-arch in index.html
start_pos = txt.find('<div class="view" id="view-arch">')
end_pos = txt.find('<!-- ============ STRUCTURED PIPELINE ============ -->')
if start_pos != -1 and end_pos != -1:
    txt = txt[:start_pos] + view_arch_html + '\n\n      ' + txt[end_pos:]
    print("Successfully replaced view-arch block in index.html with embedded mechanics.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Updated index.html with embedded 5-step mechanics in all 3 diagrams and dedicated Diagram 4.")
