# -*- coding: utf-8 -*-
"""
Builds the complete HTML and CSS for Tab: End-to-End Knowledge Graph Pipeline Matrix
Contains:
1. Card 1: 5-Column Master Matrix Table (Steps, Input, Process Execution Methodology with Nodes/Edges/Hopping, Output, Tools & Tech Stacks Contribution)
2. Card 2: Step-by-Step Bullet Points (Quick Revision for the Panel) (7 focused conceptual revision cards)
3. Card 3: Animated Interactive Workflow Pipeline Simulator (7-stage SVG with auto-play, live countdown timer, and visual node/edge/hopping breakdown - NO CODE).
"""

def get_pipeline_matrix_html():
    return '''
        <!-- ==================== TAB: END-TO-END KNOWLEDGE GRAPH PIPELINE MATRIX ==================== -->
        <div id="archContent-pipeline-matrix" class="arch-tab-content" style="display:none;">
          <div style="background:var(--surface); border:1.5px solid #3DDC97; border-radius:14px; padding:26px; margin-bottom:24px; box-shadow:0 8px 36px rgba(61,220,151,0.18);">
            
            <!-- HEADER BAR -->
            <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:16px; margin-bottom:24px; border-bottom:1px solid #1E293B; padding-bottom:18px;">
              <div>
                <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px; flex-wrap:wrap;">
                  <span class="aml-badge emerald">📊 ARCHITECTURE & EXECUTION MATRIX</span>
                  <span class="aml-badge blue">7-STAGE MASTER LIFECYCLE</span>
                  <span class="aml-badge amber">NODES · EDGES · HOPPING</span>
                  <span class="aml-badge purple">PANEL TALK-TRACK READY</span>
                </div>
                <h2 style="color:var(--tx-0); font-size:24px; margin:0 0 6px; font-weight:800; letter-spacing:-0.01em;">
                  End-to-End Knowledge Graph Pipeline Matrix
                </h2>
                <p style="color:var(--tx-2); font-size:13.5px; line-height:1.6; margin:0; max-width:1050px;">
                  Complete 3-card operational blueprint covering raw heterogeneous data manipulation, unstructured entity extraction, canonical key binding, in-memory topological hosting with Index-Free Adjacency, multi-hop circular ring detection, and Hybrid Graph-RAG regulatory reporting. Designed for senior executive and technical panel interviews.
                </p>
              </div>
              <div style="background:rgba(61,220,151,0.1); border:1px solid rgba(61,220,151,0.35); border-radius:10px; padding:10px 18px; text-align:right;">
                <div style="font-size:11px; color:#3DDC97; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">3-Card Master System</div>
                <div style="font-size:17px; font-weight:800; color:#FFFFFF;">Matrix · Points · Simulator</div>
              </div>
            </div>

            <!-- ==================== CARD 1: 5-COLUMN MASTER MATRIX TABLE ==================== -->
            <div style="background:#090E1A; border:1.5px solid rgba(61,220,151,0.4); border-radius:12px; padding:22px; margin-bottom:28px; box-shadow:0 6px 24px rgba(0,0,0,0.35);">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="font-size:24px;">📊</span>
                  <div>
                    <h3 style="color:#FFFFFF; font-size:18px; margin:0; font-weight:800;">
                      Card 1: End-to-End Knowledge Graph Pipeline Matrix (5-Column Specification)
                    </h3>
                    <div style="color:#94A3B8; font-size:12.5px; margin-top:2px;">
                      Exhaustive operational matrix detailing inputs, graph-level execution methodology (nodes, edges, hopping), outputs, and the specific role of each tool.
                    </div>
                  </div>
                </div>
                <span class="aml-badge emerald" style="font-size:11.5px; font-weight:700;">Executive Reference Table</span>
              </div>

              <!-- RESPONSIVE TABLE CONTAINER -->
              <div style="overflow-x:auto; border:1px solid #1E293B; border-radius:10px; background:#0A0F1D;">
                <table style="width:100%; min-width:1150px; border-collapse:collapse; text-align:left; font-size:12.5px; line-height:1.55;">
                  <thead>
                    <tr style="background:#0F172A; border-bottom:2px solid #334155; color:#F8FAFC;">
                      <th style="padding:14px 14px; width:15%; font-weight:800; letter-spacing:0.02em;">Steps</th>
                      <th style="padding:14px 14px; width:18%; font-weight:800; letter-spacing:0.02em;">Input</th>
                      <th style="padding:14px 16px; width:33%; font-weight:800; letter-spacing:0.02em;">Process Execution Methodology<br><span style="font-size:11px; font-weight:500; color:#94A3B8;">(High-Level Interpretation, Nodes, Edges & Hopping)</span></th>
                      <th style="padding:14px 14px; width:16%; font-weight:800; letter-spacing:0.02em;">Output</th>
                      <th style="padding:14px 14px; width:18%; font-weight:800; letter-spacing:0.02em;">Tools & Tech Stacks Contribution</th>
                    </tr>
                  </thead>
                  <tbody style="color:#CBD5E1;">
                    <!-- ROW 1 -->
                    <tr style="border-bottom:1px solid #1E293B; background:rgba(15,23,42,0.4);">
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge purple" style="margin-bottom:6px;">Stage 1</span>
                        <div style="font-weight:800; color:#F8FAFC; font-size:13.5px;">Semantic Ontology & Rule Governance</div>
                        <div style="font-size:11px; color:#A855F7; margin-top:3px;">Constitutional Blueprint</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        Banking regulatory rulebooks, compliance directives (FATF 40, FinCEN CDD), entity definitions, transaction classification standards.
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <div style="margin-bottom:6px;"><strong style="color:#A855F7;">• High-Level:</strong> Establishes the constitutional vocabulary and formal rulebook before any database code executes.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#38BDF8;">• Class Taxonomy:</strong> Formalizes entity hierarchies (e.g., <em>Account</em> is a subclass of <em>FinancialAsset</em>; <em>PEP</em> is a subclass of <em>Customer</em>).</div>
                        <div style="margin-bottom:6px;"><strong style="color:#34D399;">• Domain & Range Enforcement:</strong> Restricts relationship validity: <em>transferredTo</em> can only originate from an <em>Account</em> and terminate at an <em>Account</em> (cannot accidentally transfer to a PDF or person).</div>
                        <div><strong style="color:#F59E0B;">• Automated Inference:</strong> HermiT reasoner infers risk tiers automatically (e.g., entity owning an account in a sanctioned country is inferred as <em>HighRiskCustomer</em> without hardcoded SQL IF/ELSE).</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span style="font-weight:700; color:#38BDF8;">Formal Schema Definition</span>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Serialized W3C semantic ontology file (<code style="color:#A855F7;">.owl</code> / <code style="color:#A855F7;">.ttl</code>) serving as the inviolable ingestion contract.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge purple" style="margin-bottom:6px;">Protégé 5.6</span>
                        <div style="font-size:11.5px; line-height:1.45; color:#E2E8F0;">
                          <strong>Architectural Constitution:</strong> Eliminates data swamp corruption, guarantees mathematical consistency across teams, and executes OWL 2 HermiT semantic reasoning.
                        </div>
                      </td>
                    </tr>

                    <!-- ROW 2 -->
                    <tr style="border-bottom:1px solid #1E293B;">
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge blue" style="margin-bottom:6px;">Stage 2</span>
                        <div style="font-weight:800; color:#F8FAFC; font-size:13.5px;">Structured Data Manipulation & Ingestion</div>
                        <div style="font-size:11px; color:#60A5FA; margin-top:3px;">Relational to Graph</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        Relational database tables: Oracle KYC database, PostgreSQL Account balances, Kafka SWIFT MT103 wire messages, OFAC Sanctions CSV.
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <div style="margin-bottom:6px;"><strong style="color:#60A5FA;">• High-Level:</strong> Ingests tables as native network objects without executing slow, memory-intensive multi-table SQL joins.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#38BDF8;">• Nodes Created (Nouns):</strong> Distinct entities like <em>Customer</em> (with tax_id, name) and <em>Account</em> (with iban, bank, balance).</div>
                        <div style="margin-bottom:6px;"><strong style="color:#34D399;">• Edges Created (Verbs):</strong> Foreign key matches become directed relationship pointers: <em>(:Customer)-[:OWNS]->(:Account)</em> and <em>(:Account)-[:TRANSFERRED]->(:Account)</em>.</div>
                        <div><strong style="color:#F59E0B;">• Properties (Adjectives):</strong> Relational table columns become key-value attributes on nodes and edges (timestamp, currency, amount, risk_tier).</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span style="font-weight:700; color:#34D399;">Discrete Graph Entities</span>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Validated, typed node records and directional wire transfer edges loaded into graph storage.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge blue" style="margin-bottom:6px;">Kafka & Python</span>
                        <div style="font-size:11.5px; line-height:1.45; color:#E2E8F0;">
                          <strong>Debezium CDC & Streamers:</strong> Captures relational transaction commits and maps foreign keys into directional network relationships in real time.
                        </div>
                      </td>
                    </tr>

                    <!-- ROW 3 -->
                    <tr style="border-bottom:1px solid #1E293B; background:rgba(15,23,42,0.4);">
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge amber" style="margin-bottom:6px;">Stage 3</span>
                        <div style="font-weight:800; color:#F8FAFC; font-size:13.5px;">Unstructured Data Transformation</div>
                        <div style="font-size:11px; color:#F59E0B; margin-top:3px;">NLP, Entities & Vectors</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        Unstructured compliance narratives: FinCEN SAR PDFs, commercial loan credit memos (DOCX), compliance officer emails, investigative notes.
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <div style="margin-bottom:6px;"><strong style="color:#F59E0B;">• High-Level:</strong> Converts free-flowing human text into structured semantic facts without forcing text into rigid, artificial table columns.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#38BDF8;">• 3-Tier Pipeline:</strong> (1) ISO 7064 Mod-97 IBAN checksums & RegEx; (2) spaCy Named Entity Recognition tagging Persons/Orgs; (3) LLM Pydantic JSON schema extracting Subject-Predicate-Object facts.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#34D399;">• Nodes Created:</strong> <em>(:DocumentChunk)</em> holding raw text provenance; <em>(:ExtractedEntity)</em> for unmasked shell companies.</div>
                        <div><strong style="color:#A855F7;">• Vectorization:</strong> 500-token chunks are embedded into dense 384-d vectors stored in ChromaDB for similarity discovery (>0.82 cosine similarity).</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span style="font-weight:700; color:#F59E0B;">Semantic Triples & Vectors</span>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Extracted canonical keys (IBANs, Tax IDs), document chunk nodes, and dense vector collections.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge amber" style="margin-bottom:6px;">ChromaDB & spaCy</span>
                        <div style="font-size:11.5px; line-height:1.45; color:#E2E8F0;">
                          <strong>ChromaDB & NER:</strong> ChromaDB manages dense semantic vector indexing; spaCy and LLMs parse unstructured text into deterministic entities and canonical keys.
                        </div>
                      </td>
                    </tr>

                    <!-- ROW 4 -->
                    <tr style="border-bottom:1px solid #1E293B;">
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge emerald" style="margin-bottom:6px;">Stage 4</span>
                        <div style="font-weight:800; color:#F8FAFC; font-size:13.5px;">Binding Structured & Unstructured Data</div>
                        <div style="font-size:11px; color:#10B981; margin-top:3px;">Canonical Key Resolution</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        Core banking nodes from Stage 2 + Extracted canonical identifiers and document chunk nodes from Stage 3.
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <div style="margin-bottom:6px;"><strong style="color:#10B981;">• High-Level:</strong> Glues legal narrative evidence directly to banking accounts, establishing a single interconnected source of truth.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#38BDF8;">• Identity Resolution:</strong> Resolves shared canonical keys (matching Tax ID or IBAN mentioned in a PDF narrative to the corresponding bank account).</div>
                        <div style="margin-bottom:6px;"><strong style="color:#34D399;">• Edges Created:</strong> <em>(:DocumentChunk)-[:EVIDENCE_FOR]->(:Account)</em> and <em>(:DocumentChunk)-[:CORROBORATES]->(:Customer)</em>.</div>
                        <div><strong style="color:#F59E0B;">• Audit Provenance:</strong> Every transaction and risk flag now points directly to the underlying legal document with 100% trace evidence.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span style="font-weight:700; color:#10B981;">Unified Knowledge Graph</span>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Single interconnected fabric uniting high-velocity financial wires with unstructured compliance evidence.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge emerald" style="margin-bottom:6px;">Cypher (MERGE)</span>
                        <div style="font-size:11.5px; line-height:1.45; color:#E2E8F0;">
                          <strong>Declarative GQL:</strong> Idempotent Cypher MERGE binds text chunks to existing entities without duplicating records or corrupting topology.
                        </div>
                      </td>
                    </tr>

                    <!-- ROW 5 -->
                    <tr style="border-bottom:1px solid #1E293B; background:rgba(15,23,42,0.4);">
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge cyan" style="margin-bottom:6px;">Stage 5</span>
                        <div style="font-weight:800; color:#F8FAFC; font-size:13.5px;">In-Memory Storage & Topology Hosting</div>
                        <div style="font-size:11px; color:#06B6D4; margin-top:3px;">Index-Free Adjacency (IFA)</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        Connected graph nodes, edges, labels, and properties across all modalities.
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <div style="margin-bottom:6px;"><strong style="color:#06B6D4;">• High-Level:</strong> Stores the interconnected graph persistently on disk while caching active relationship networks in RAM for instant access.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#38BDF8;">• Index-Free Adjacency (IFA):</strong> Nodes do not search an index table to find connections; each node holds direct physical 64-bit RAM pointers to its adjacent relationship records.</div>
                        <div><strong style="color:#34D399;">• Constant-Time Traversal:</strong> Traversing from one account to another takes constant time [O(1)] whether the graph has 1,000 nodes or 500 million nodes.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span style="font-weight:700; color:#06B6D4;">High-Speed In-Memory Graph</span>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Operational graph database running in RAM with ACID transactional safety on persistent disk.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge cyan" style="margin-bottom:6px;">Neo4j Engine</span>
                        <div style="font-size:11.5px; line-height:1.45; color:#E2E8F0;">
                          <strong>LPG Database Engine:</strong> Houses the physical graph in RAM; provides the lightning-fast memory pointer architecture that makes deep multi-hop traversals feasible.
                        </div>
                      </td>
                    </tr>

                    <!-- ROW 6 -->
                    <tr style="border-bottom:1px solid #1E293B;">
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge rose" style="margin-bottom:6px;">Stage 6</span>
                        <div style="font-weight:800; color:#F8FAFC; font-size:13.5px;">Topological Pattern Recognition (Hopping)</div>
                        <div style="font-size:11px; color:#F43F5E; margin-top:3px;">Multi-Hop Cycles & Hubs</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        Unified accounts, customers, mobile devices, and wire transactions in Neo4j RAM.
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <div style="margin-bottom:6px;"><strong style="color:#F43F5E;">• High-Level:</strong> Detects complex financial crime syndicates that hide across multiple intermediary steps.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#38BDF8;">• Hopping Mechanics:</strong> Sequentially dereferencing pointers across edges: Hop 1 (DE -> CH: $4.50M) ➔ Hop 2 (CH -> CY: $4.48M) ➔ Hop 3 (CY -> DE: $4.46M) returning to origin!</div>
                        <div style="margin-bottom:6px;"><strong style="color:#34D399;">• Device Sharing Hubs:</strong> Detects multiple distinct customers sharing the exact same mobile device IMEI or MAC address.</div>
                        <div><strong style="color:#A855F7;">• Graph Data Science:</strong> Executes PageRank and Weakly Connected Components to unmask the syndicate ringleader in single-digit milliseconds.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span style="font-weight:700; color:#F43F5E;">Flagged Fraud Subgraph</span>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Unmasked circular layering ring, quantified exposure ($14.25M), and identified ringleader accounts.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge rose" style="margin-bottom:6px;">Cypher Traversal & GDS</span>
                        <div style="font-size:11.5px; line-height:1.45; color:#E2E8F0;">
                          <strong>Pattern Matching Engine:</strong> Executes variable-length path traversal (3-5 hops) across RAM in ~6 milliseconds, which times out or crashes in relational SQL.
                        </div>
                      </td>
                    </tr>

                    <!-- ROW 7 -->
                    <tr>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge emerald" style="margin-bottom:6px;">Stage 7</span>
                        <div style="font-weight:800; color:#F8FAFC; font-size:13.5px;">Hybrid Graph-RAG & Compliance Filing</div>
                        <div style="font-size:11px; color:#10B981; margin-top:3px;">Zero-Hallucination Reporting</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        Flagged multi-hop fraud subgraph from Neo4j + Contextual document text retrieved from ChromaDB.
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <div style="margin-bottom:6px;"><strong style="color:#10B981;">• High-Level:</strong> Delivers an auditable, zero-hallucination regulatory package to executive leadership and government regulators.</div>
                        <div style="margin-bottom:6px;"><strong style="color:#38BDF8;">• Hybrid Synthesis:</strong> Combines the exact mathematical facts from Neo4j (dollar sums, account IDs, timestamps) with verbatim evidence text from ChromaDB.</div>
                        <div><strong style="color:#34D399;">• Zero-Hallucination Constraint:</strong> LLM is restricted to strictly pre-verified subgraph facts, generating the official FinCEN Form 111 XML filing package with exact citations.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span style="font-weight:700; color:#10B981;">FinCEN Filing & Executive Brief</span>
                        <div style="font-size:11.5px; color:#94A3B8; margin-top:4px;">Official FinCEN Form 111 XML payload, quantified $14.25M audit report, and executive brief.</div>
                      </td>
                      <td style="padding:14px; vertical-align:top;">
                        <span class="aml-badge emerald" style="margin-bottom:6px;">Hybrid Graph-RAG</span>
                        <div style="font-size:11.5px; line-height:1.45; color:#E2E8F0;">
                          <strong>Grounded LLM Synthesis:</strong> Fuses Neo4j deterministic subgraph facts with ChromaDB vector context to guarantee 100% auditability and zero hallucination.
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- ==================== CARD 2: STEP-BY-STEP BULLET POINTS ==================== -->
            <div style="background:#090E1A; border:1.5px solid rgba(96,165,250,0.4); border-radius:12px; padding:22px; margin-bottom:28px; box-shadow:0 6px 24px rgba(0,0,0,0.35);">
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:18px;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="font-size:24px;">🎯</span>
                  <div>
                    <h3 style="color:#FFFFFF; font-size:18px; margin:0; font-weight:800;">
                      Card 2: Step-by-Step Bullet Points (Quick Revision for the Panel)
                    </h3>
                    <div style="color:#94A3B8; font-size:12.5px; margin-top:2px;">
                      The 7 core takeaways and executive soundbites to memorize and present confidently during your panel interview.
                    </div>
                  </div>
                </div>
                <span class="aml-badge blue" style="font-size:11.5px; font-weight:700;">Interview Talk-Track Guide</span>
              </div>

              <!-- 7 BULLET CARDS GRID -->
              <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:14px;">
                
                <!-- POINT 1 -->
                <div style="background:#0F172A; border:1px solid #1E293B; border-left:4px solid #A855F7; border-radius:8px; padding:14px 16px;">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#A855F7; font-size:13.5px;">1. Ontology Modeling (Protégé)</strong>
                    <span class="aml-badge purple" style="font-size:10.5px;">Blueprint</span>
                  </div>
                  <div style="font-size:12.5px; color:#E2E8F0; line-height:1.5; margin-bottom:8px;">
                    Protégé is our architectural constitution. It establishes class taxonomies (Account as FinancialAsset), validates domain/range constraints, and infers high-risk classifications via OWL 2 reasoning before database ingestion.
                  </div>
                  <div style="background:rgba(168,85,247,0.08); border-radius:6px; padding:6px 10px; font-size:11.5px; color:#C084FC;">
                    <strong>🎙️ Panel Soundbite:</strong> "Neo4j is schema-optional; without Protégé, you get an unmaintainable data swamp. Protégé guarantees strict semantic integrity."
                  </div>
                </div>

                <!-- POINT 2 -->
                <div style="background:#0F172A; border:1px solid #1E293B; border-left:4px solid #60A5FA; border-radius:8px; padding:14px 16px;">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#60A5FA; font-size:13.5px;">2. Structured Ingestion (Kafka/Python)</strong>
                    <span class="aml-badge blue" style="font-size:10.5px;">Tables ➔ Graph</span>
                  </div>
                  <div style="font-size:12.5px; color:#E2E8F0; line-height:1.5; margin-bottom:8px;">
                    Relational tables are converted directly into Nodes (Nouns: Customer, Account) and Edges (Verbs: OWNS, TRANSFERRED). Foreign keys become memory pointers, completely eliminating Cartesian-heavy multi-table SQL joins.
                  </div>
                  <div style="background:rgba(96,165,250,0.08); border-radius:6px; padding:6px 10px; font-size:11.5px; color:#93C5FD;">
                    <strong>🎙️ Panel Soundbite:</strong> "We never flatten tables into one giant data warehouse view. We turn entities into nodes and transactions into directional edges."
                  </div>
                </div>

                <!-- POINT 3 -->
                <div style="background:#0F172A; border:1px solid #1E293B; border-left:4px solid #F59E0B; border-radius:8px; padding:14px 16px;">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#F59E0B; font-size:13.5px;">3. Unstructured NLP (ChromaDB)</strong>
                    <span class="aml-badge amber" style="font-size:10.5px;">NLP & Vectors</span>
                  </div>
                  <div style="font-size:12.5px; color:#E2E8F0; line-height:1.5; margin-bottom:8px;">
                    Documents cannot fit into static table columns. A 3-tier NLP pipeline (Checksums ➔ spaCy NER ➔ LLM JSON Schema) pulls canonical keys and entity triples, while ChromaDB indexes 384-d vector embeddings for semantic discovery.
                  </div>
                  <div style="background:rgba(245,158,11,0.08); border-radius:6px; padding:6px 10px; font-size:11.5px; color:#FCD34D;">
                    <strong>🎙️ Panel Soundbite:</strong> "Natural language has variable context. ChromaDB enables semantic similarity search across investigations with cosine similarity > 0.82."
                  </div>
                </div>

                <!-- POINT 4 -->
                <div style="background:#0F172A; border:1px solid #1E293B; border-left:4px solid #10B981; border-radius:8px; padding:14px 16px;">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#10B981; font-size:13.5px;">4. Canonical Binding (Cypher MERGE)</strong>
                    <span class="aml-badge emerald" style="font-size:10.5px;">Key Resolution</span>
                  </div>
                  <div style="font-size:12.5px; color:#E2E8F0; line-height:1.5; margin-bottom:8px;">
                    Using normalized canonical identifiers (IBANs, Tax IDs), Cypher connects text chunks directly to banking nodes (DocumentChunk -[:EVIDENCE_FOR]-> Account), creating a single unified source of truth with complete audit provenance.
                  </div>
                  <div style="background:rgba(16,185,129,0.08); border-radius:6px; padding:6px 10px; font-size:11.5px; color:#6EE7B7;">
                    <strong>🎙️ Panel Soundbite:</strong> "This bridges structured transaction ledgers and unstructured legal narratives into a unified graph where every node retains evidence provenance."
                  </div>
                </div>

                <!-- POINT 5 -->
                <div style="background:#0F172A; border:1px solid #1E293B; border-left:4px solid #06B6D4; border-radius:8px; padding:14px 16px;">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#06B6D4; font-size:13.5px;">5. In-Memory Graph Storage (Neo4j)</strong>
                    <span class="aml-badge cyan" style="font-size:10.5px;">Index-Free Adjacency</span>
                  </div>
                  <div style="font-size:12.5px; color:#E2E8F0; line-height:1.5; margin-bottom:8px;">
                    Neo4j stores physical 64-bit RAM memory pointers from nodes directly to adjacent edges. Traversal is O(1) constant time per hop, completely bypassing index lookups and Cartesian join explosions that cripple relational SQL.
                  </div>
                  <div style="background:rgba(6,182,212,0.08); border-radius:6px; padding:6px 10px; font-size:11.5px; color:#67E8F9;">
                    <strong>🎙️ Panel Soundbite:</strong> "Relational databases index records; Neo4j indexes connections. Traversing an edge in RAM is simply dereferencing a memory pointer."
                  </div>
                </div>

                <!-- POINT 6 -->
                <div style="background:#0F172A; border:1px solid #1E293B; border-left:4px solid #F43F5E; border-radius:8px; padding:14px 16px;">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#F43F5E; font-size:13.5px;">6. Hopping & Pattern Recognition (Cypher)</strong>
                    <span class="aml-badge rose" style="font-size:10.5px;">Multi-Hop Cycles</span>
                  </div>
                  <div style="font-size:12.5px; color:#E2E8F0; line-height:1.5; margin-bottom:8px;">
                    Hopping means stepping across sequential edge pointers. Cypher traverses 3 to 5 hops across accounts (DE ➔ CH ➔ CY ➔ DE) to uncover circular laundering rings and shared device hubs in under 10 milliseconds.
                  </div>
                  <div style="background:rgba(244,63,94,0.08); border-radius:6px; padding:6px 10px; font-size:11.5px; color:#FDA4AF;">
                    <strong>🎙️ Panel Soundbite:</strong> "Launderers use multi-hop layering to hide trails. In SQL, a 5-hop query times out; in Neo4j, Cypher finds the $14.25M loop in single-digit milliseconds."
                  </div>
                </div>

                <!-- POINT 7 -->
                <div style="background:#0F172A; border:1px solid #1E293B; border-left:4px solid #10B981; border-radius:8px; padding:14px 16px; grid-column:1 / -1;">
                  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:6px;">
                    <strong style="color:#10B981; font-size:13.5px;">7. Grounded Reporting (Hybrid Graph-RAG)</strong>
                    <span class="aml-badge emerald" style="font-size:10.5px;">Zero-Hallucination Reporting</span>
                  </div>
                  <div style="font-size:12.5px; color:#E2E8F0; line-height:1.5; margin-bottom:8px;">
                    Hybrid Graph-RAG marries the mathematical certainty of the Neo4j graph (exact transaction sums, timestamps, verified accounts) with ChromaDB's contextual text narrative to produce a 100% auditable, zero-hallucination FinCEN Form 111 SAR filing package.
                  </div>
                  <div style="background:rgba(16,185,129,0.08); border-radius:6px; padding:6px 10px; font-size:11.5px; color:#6EE7B7;">
                    <strong>🎙️ Panel Soundbite:</strong> "Traditional Vector RAG hallucinates financial numbers. Hybrid Graph-RAG forces the LLM to ground its output strictly on verified graph facts, giving management complete auditability."
                  </div>
                </div>

              </div>
            </div>

            <!-- ==================== CARD 3: ANIMATED INTERACTIVE WORKFLOW PIPELINE SIMULATOR ==================== -->
            <div style="background:#090E1A; border:1.5px solid #2DD4D4; border-radius:14px; padding:22px; box-shadow:0 8px 36px rgba(45,212,212,0.18);">
              
              <!-- SIMULATOR HEADER -->
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="font-size:24px;">⚡</span>
                  <div>
                    <h3 style="color:#FFFFFF; font-size:18px; margin:0; font-weight:800;">
                      Card 3: Animated Interactive Workflow Pipeline (Matrix Explainer Simulator)
                    </h3>
                    <div style="color:#94A3B8; font-size:12.5px; margin-top:2px;">
                      Step dynamically through all 7 stages to see how Input data transforms through Node, Edge, and Hopping mechanics into Output deliverables via each tool.
                    </div>
                  </div>
                </div>
                <div style="background:rgba(45,212,212,0.1); border:1px solid rgba(45,212,212,0.3); border-radius:8px; padding:6px 14px; text-align:right;">
                  <div style="font-size:10px; color:#2DD4D4; font-weight:700; text-transform:uppercase;">Active Stage Simulation</div>
                  <div id="matrixStageIndicator" style="font-size:13.5px; font-weight:800; color:#FFFFFF;">Stage 1 of 7: Protégé Ontology</div>
                </div>
              </div>

              <!-- PLAYBACK CONTROLS BAR -->
              <div style="background:#0F172A; border:1px solid #1E293B; border-radius:10px; padding:10px 16px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-bottom:16px;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <button type="button" class="btn btn-sm btn-secondary" onclick="prevMatrixStep()" title="Previous Stage">◀ Prev Stage</button>
                  <button type="button" class="btn btn-sm btn-primary" id="matrixPlayPauseBtn" onclick="toggleMatrixPlay()" style="min-width:130px; font-weight:800; background:linear-gradient(135deg, #2DD4D4 0%, #0284C7 100%); border:none; color:#000;">
                    ▶ Auto-Play Tour
                  </button>
                  <button type="button" class="btn btn-sm btn-secondary" onclick="nextMatrixStep()" title="Next Stage">Next Stage ▶</button>
                  <button type="button" class="btn btn-sm btn-secondary" onclick="resetMatrixTour()" title="Reset to Stage 1" style="color:var(--tx-3);">↺ Reset</button>
                  
                  <!-- COUNTDOWN TIMER BADGE -->
                  <span id="matrixTimerBadge" style="display:none; align-items:center; gap:6px; background:rgba(45,212,212,0.12); border:1px solid rgba(45,212,212,0.4); color:#2DD4D4; border-radius:20px; padding:3px 12px; font-size:11.5px; font-weight:700; font-family:monospace;">
                    ⏱ Auto-advancing in 7.0s
                  </span>
                </div>

                <div style="display:flex; align-items:center; gap:12px;">
                  <span style="font-size:12px; color:var(--tx-2);">Speed:</span>
                  <select id="matrixSpeedSelect" onchange="changeMatrixSpeed(this.value)" style="background:#090E1A; color:#E2E8F0; border:1px solid #334155; border-radius:6px; padding:4px 8px; font-size:12px;">
                    <option value="1">1x (Normal - 7s)</option>
                    <option value="2">2x (Fast - 3.5s)</option>
                    <option value="0.5">0.5x (Detailed - 14s)</option>
                  </select>
                </div>
              </div>

              <!-- DUAL PROGRESS BARS -->
              <div style="margin-bottom:14px;">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#94A3B8; margin-bottom:4px;">
                  <span>Stage Progression (<span id="matrixProgressStepLabel">Stage 1 of 7</span>)</span>
                  <span id="matrixProgressPercent">14% Complete</span>
                </div>
                <div style="height:6px; background:#1E293B; border-radius:999px; overflow:hidden;">
                  <div id="matrixOverallProgressBar" style="height:100%; width:14.28%; background:linear-gradient(90deg, #2DD4D4 0%, #3DDC97 100%); transition:width 0.3s ease;"></div>
                </div>
                <div style="height:3px; background:#1E293B; border-radius:999px; overflow:hidden; margin-top:3px;">
                  <div id="matrixStepProgressBar" style="height:100%; width:0%; background:#2DD4D4; transition:width 0.05s linear;"></div>
                </div>
              </div>

              <!-- INTERACTIVE STAGE SELECTOR PILLS -->
              <div style="display:flex; gap:8px; overflow-x:auto; padding-bottom:8px; margin-bottom:18px;" id="matrixStepSelectorBar">
                <button type="button" class="aml-step-btn active" onclick="setMatrixStep(1)" id="matrixStepBtn-1">
                  <span style="background:#2DD4D4; color:#000; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">1</span>
                  <span>1. Protégé Ontology</span>
                </button>
                <button type="button" class="aml-step-btn" onclick="setMatrixStep(2)" id="matrixStepBtn-2">
                  <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">2</span>
                  <span>2. Structured Ingestion</span>
                </button>
                <button type="button" class="aml-step-btn" onclick="setMatrixStep(3)" id="matrixStepBtn-3">
                  <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">3</span>
                  <span>3. Unstructured NLP</span>
                </button>
                <button type="button" class="aml-step-btn" onclick="setMatrixStep(4)" id="matrixStepBtn-4">
                  <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">4</span>
                  <span>4. Canonical Binding</span>
                </button>
                <button type="button" class="aml-step-btn" onclick="setMatrixStep(5)" id="matrixStepBtn-5">
                  <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">5</span>
                  <span>5. Neo4j IFA Storage</span>
                </button>
                <button type="button" class="aml-step-btn" onclick="setMatrixStep(6)" id="matrixStepBtn-6">
                  <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">6</span>
                  <span>6. Hopping & Patterns</span>
                </button>
                <button type="button" class="aml-step-btn" onclick="setMatrixStep(7)" id="matrixStepBtn-7">
                  <span style="background:var(--line-strong); color:#FFF; border-radius:50%; width:18px; height:18px; display:inline-flex; align-items:center; justify-content:center; font-size:10.5px; font-weight:800;">7</span>
                  <span>7. Hybrid Graph-RAG</span>
                </button>
              </div>

              <!-- ANIMATED SVG PIPELINE FLOWCHART -->
              <div style="background:#070C16; border:1px solid #1E293B; border-radius:12px; padding:16px; margin-bottom:18px; overflow-x:auto;">
                <svg id="matrixSvgCanvas" viewBox="0 0 1150 170" style="width:100%; min-width:980px; height:auto; display:block;" xmlns="http://www.w3.org/2000/svg">
                  <defs>
                    <linearGradient id="matrixGradGlow" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" stop-color="#2DD4D4" stop-opacity="0.9" />
                      <stop offset="100%" stop-color="#0284C7" stop-opacity="0.7" />
                    </linearGradient>
                    <filter id="matrixFilterActive" x="-20%" y="-20%" width="140%" height="140%">
                      <feDropShadow dx="0" dy="0" stdDeviation="6" flood-color="#2DD4D4" flood-opacity="0.8" />
                    </filter>
                    <marker id="matrixArrowMarker" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
                      <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8" />
                    </marker>
                  </defs>

                  <!-- 7 HORIZONTAL STAGE CARDS IN SVG -->
                  <!-- Stage 1 -->
                  <g id="svgMatrixStage-1" onclick="setMatrixStep(1)" style="cursor:pointer;" class="matrix-svg-stage active">
                    <rect x="10" y="30" width="135" height="110" rx="10" fill="#0E1628" stroke="#2DD4D4" stroke-width="2.5" id="svgMatrixRect-1" filter="url(#matrixFilterActive)"/>
                    <circle cx="35" cy="55" r="14" fill="#2DD4D4" id="svgMatrixCircle-1"/>
                    <text x="35" y="60" font-size="12" font-weight="800" fill="#000" text-anchor="middle" id="svgMatrixNum-1">1</text>
                    <text x="56" y="52" font-size="10" font-weight="700" fill="#A855F7">PROTÉGÉ</text>
                    <text x="56" y="64" font-size="8.5" fill="#94A3B8">OWL 2 Ontology</text>
                    <text x="18" y="90" font-size="11" font-weight="700" fill="#FFFFFF">Semantic Model</text>
                    <text x="18" y="105" font-size="9.5" fill="#CBD5E1">Taxonomy & Rules</text>
                    <text x="18" y="125" font-size="8.5" fill="#34D399">Blueprint Contract</text>
                  </g>

                  <!-- Edge 1 -> 2 -->
                  <line x1="145" y1="85" x2="175" y2="85" stroke="#38BDF8" stroke-width="2.5" stroke-dasharray="6 4" class="aml-flowing-edge" marker-end="url(#matrixArrowMarker)" id="svgMatrixEdge-1"/>

                  <!-- Stage 2 -->
                  <g id="svgMatrixStage-2" onclick="setMatrixStep(2)" style="cursor:pointer;" class="matrix-svg-stage">
                    <rect x="175" y="30" width="135" height="110" rx="10" fill="#0E1628" stroke="#334155" stroke-width="1.5" id="svgMatrixRect-2"/>
                    <circle cx="200" cy="55" r="14" fill="#1E293B" id="svgMatrixCircle-2"/>
                    <text x="200" y="60" font-size="12" font-weight="800" fill="#FFF" text-anchor="middle" id="svgMatrixNum-2">2</text>
                    <text x="221" y="52" font-size="10" font-weight="700" fill="#60A5FA">KAFKA / SQL</text>
                    <text x="221" y="64" font-size="8.5" fill="#94A3B8">Relational Feeds</text>
                    <text x="183" y="90" font-size="11" font-weight="700" fill="#FFFFFF">Structured Feeds</text>
                    <text x="183" y="105" font-size="9.5" fill="#CBD5E1">Tables ➔ Nodes</text>
                    <text x="183" y="125" font-size="8.5" fill="#60A5FA">:Customer & :Account</text>
                  </g>

                  <!-- Edge 2 -> 3 -->
                  <line x1="310" y1="85" x2="340" y2="85" stroke="#334155" stroke-width="2" marker-end="url(#matrixArrowMarker)" id="svgMatrixEdge-2"/>

                  <!-- Stage 3 -->
                  <g id="svgMatrixStage-3" onclick="setMatrixStep(3)" style="cursor:pointer;" class="matrix-svg-stage">
                    <rect x="340" y="30" width="135" height="110" rx="10" fill="#0E1628" stroke="#334155" stroke-width="1.5" id="svgMatrixRect-3"/>
                    <circle cx="365" cy="55" r="14" fill="#1E293B" id="svgMatrixCircle-3"/>
                    <text x="365" y="60" font-size="12" font-weight="800" fill="#FFF" text-anchor="middle" id="svgMatrixNum-3">3</text>
                    <text x="386" y="52" font-size="10" font-weight="700" fill="#F59E0B">CHROMADB</text>
                    <text x="386" y="64" font-size="8.5" fill="#94A3B8">spaCy & Vectors</text>
                    <text x="348" y="90" font-size="11" font-weight="700" fill="#FFFFFF">Unstructured NLP</text>
                    <text x="348" y="105" font-size="9.5" fill="#CBD5E1">Checksums & NER</text>
                    <text x="348" y="125" font-size="8.5" fill="#F59E0B">Triples & Vectors</text>
                  </g>

                  <!-- Edge 3 -> 4 -->
                  <line x1="475" y1="85" x2="505" y2="85" stroke="#334155" stroke-width="2" marker-end="url(#matrixArrowMarker)" id="svgMatrixEdge-3"/>

                  <!-- Stage 4 -->
                  <g id="svgMatrixStage-4" onclick="setMatrixStep(4)" style="cursor:pointer;" class="matrix-svg-stage">
                    <rect x="505" y="30" width="135" height="110" rx="10" fill="#0E1628" stroke="#334155" stroke-width="1.5" id="svgMatrixRect-4"/>
                    <circle cx="530" cy="55" r="14" fill="#1E293B" id="svgMatrixCircle-4"/>
                    <text x="530" y="60" font-size="12" font-weight="800" fill="#FFF" text-anchor="middle" id="svgMatrixNum-4">4</text>
                    <text x="551" y="52" font-size="10" font-weight="700" fill="#10B981">CYPHER</text>
                    <text x="551" y="64" font-size="8.5" fill="#94A3B8">MERGE Binding</text>
                    <text x="513" y="90" font-size="11" font-weight="700" fill="#FFFFFF">Canonical Binding</text>
                    <text x="513" y="105" font-size="9.5" fill="#CBD5E1">IBAN & Tax ID Keys</text>
                    <text x="513" y="125" font-size="8.5" fill="#10B981">:EVIDENCE_FOR Edge</text>
                  </g>

                  <!-- Edge 4 -> 5 -->
                  <line x1="640" y1="85" x2="670" y2="85" stroke="#334155" stroke-width="2" marker-end="url(#matrixArrowMarker)" id="svgMatrixEdge-4"/>

                  <!-- Stage 5 -->
                  <g id="svgMatrixStage-5" onclick="setMatrixStep(5)" style="cursor:pointer;" class="matrix-svg-stage">
                    <rect x="670" y="30" width="135" height="110" rx="10" fill="#0E1628" stroke="#334155" stroke-width="1.5" id="svgMatrixRect-5"/>
                    <circle cx="695" cy="55" r="14" fill="#1E293B" id="svgMatrixCircle-5"/>
                    <text x="695" y="60" font-size="12" font-weight="800" fill="#FFF" text-anchor="middle" id="svgMatrixNum-5">5</text>
                    <text x="716" y="52" font-size="10" font-weight="700" fill="#06B6D4">NEO4J RAM</text>
                    <text x="716" y="64" font-size="8.5" fill="#94A3B8">Index-Free Adjacency</text>
                    <text x="678" y="90" font-size="11" font-weight="700" fill="#FFFFFF">In-Memory Engine</text>
                    <text x="678" y="105" font-size="9.5" fill="#CBD5E1">Memory Pointers</text>
                    <text x="678" y="125" font-size="8.5" fill="#06B6D4">O(1) Edge Pointers</text>
                  </g>

                  <!-- Edge 5 -> 6 -->
                  <line x1="805" y1="85" x2="835" y2="85" stroke="#334155" stroke-width="2" marker-end="url(#matrixArrowMarker)" id="svgMatrixEdge-5"/>

                  <!-- Stage 6 -->
                  <g id="svgMatrixStage-6" onclick="setMatrixStep(6)" style="cursor:pointer;" class="matrix-svg-stage">
                    <rect x="835" y="30" width="135" height="110" rx="10" fill="#0E1628" stroke="#334155" stroke-width="1.5" id="svgMatrixRect-6"/>
                    <circle cx="860" cy="55" r="14" fill="#1E293B" id="svgMatrixCircle-6"/>
                    <text x="860" y="60" font-size="12" font-weight="800" fill="#FFF" text-anchor="middle" id="svgMatrixNum-6">6</text>
                    <text x="881" y="52" font-size="10" font-weight="700" fill="#F43F5E">CYPHER GDS</text>
                    <text x="881" y="64" font-size="8.5" fill="#94A3B8">Path Traversal</text>
                    <text x="843" y="90" font-size="11" font-weight="700" fill="#FFFFFF">Hopping Detection</text>
                    <text x="843" y="105" font-size="9.5" fill="#CBD5E1">Circular 3-Hop Loop</text>
                    <text x="843" y="125" font-size="8.5" fill="#F43F5E">$14.25M Ring</text>
                  </g>

                  <!-- Edge 6 -> 7 -->
                  <line x1="970" y1="85" x2="1000" y2="85" stroke="#334155" stroke-width="2" marker-end="url(#matrixArrowMarker)" id="svgMatrixEdge-6"/>

                  <!-- Stage 7 -->
                  <g id="svgMatrixStage-7" onclick="setMatrixStep(7)" style="cursor:pointer;" class="matrix-svg-stage">
                    <rect x="1000" y="30" width="140" height="110" rx="10" fill="#0E1628" stroke="#334155" stroke-width="1.5" id="svgMatrixRect-7"/>
                    <circle cx="1025" cy="55" r="14" fill="#1E293B" id="svgMatrixCircle-7"/>
                    <text x="1025" y="60" font-size="12" font-weight="800" fill="#FFF" text-anchor="middle" id="svgMatrixNum-7">7</text>
                    <text x="1046" y="52" font-size="10" font-weight="700" fill="#10B981">GRAPH-RAG</text>
                    <text x="1046" y="64" font-size="8.5" fill="#94A3B8">FinCEN Filing</text>
                    <text x="1008" y="90" font-size="11" font-weight="700" fill="#FFFFFF">Grounded Output</text>
                    <text x="1008" y="105" font-size="9.5" fill="#CBD5E1">Zero-Hallucination</text>
                    <text x="1008" y="125" font-size="8.5" fill="#10B981">FinCEN Form 111</text>
                  </g>
                </svg>
              </div>

              <!-- DYNAMIC STAGE INSPECTOR DETAILS -->
              <div id="matrixInspectorCard" style="background:#0F172A; border:1px solid #1E293B; border-radius:12px; padding:20px;">
                
                <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; margin-bottom:16px; border-bottom:1px solid #1E293B; padding-bottom:12px;">
                  <div style="display:flex; align-items:center; gap:10px;">
                    <span id="matrixInspBadge" class="aml-badge purple">STAGE 1 DEEP-DIVE</span>
                    <h4 id="matrixInspTitle" style="color:#F8FAFC; margin:0; font-size:16px; font-weight:800;">
                      Stage 1: Semantic Ontology & Rule Governance
                    </h4>
                  </div>
                  <span id="matrixInspToolBadge" class="aml-badge purple">PROTÉGÉ 5.6 & OWL 2</span>
                </div>

                <!-- 4 METRIC COLUMNS -->
                <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(230px, 1fr)); gap:14px; margin-bottom:18px;">
                  
                  <!-- INPUT -->
                  <div style="background:#090E1A; border:1px solid #1E293B; border-radius:8px; padding:14px;">
                    <div style="font-size:11px; color:#94A3B8; font-weight:700; text-transform:uppercase; margin-bottom:6px;">1. Raw Input</div>
                    <div id="matrixInspInput" style="font-size:12.5px; color:#E2E8F0; line-height:1.5;">
                      Banking regulatory compliance guidelines (FATF 40, FinCEN CDD Rule), financial entity catalogs, transaction classification standards.
                    </div>
                  </div>

                  <!-- PROCESS EXECUTION -->
                  <div style="background:#090E1A; border:1px solid #1E293B; border-radius:8px; padding:14px;">
                    <div style="font-size:11px; color:#38BDF8; font-weight:700; text-transform:uppercase; margin-bottom:6px;">2. Process (Nodes, Edges, Hopping)</div>
                    <div id="matrixInspProcess" style="font-size:12.5px; color:#E2E8F0; line-height:1.5;">
                      Defines allowed Node classes (:Customer, :Account) and Edge types (:OWNS, :TRANSFERRED). Enforces Domain/Range constraints so edges cannot connect invalid types.
                    </div>
                  </div>

                  <!-- OUTPUT -->
                  <div style="background:#090E1A; border:1px solid #1E293B; border-radius:8px; padding:14px;">
                    <div style="font-size:11px; color:#34D399; font-weight:700; text-transform:uppercase; margin-bottom:6px;">3. Concrete Output</div>
                    <div id="matrixInspOutput" style="font-size:12.5px; color:#E2E8F0; line-height:1.5;">
                      Serialized W3C semantic ontology contract file (aml_ontology.ttl / .owl) enforcing schema governance across all subsequent pipeline code.
                    </div>
                  </div>

                  <!-- TOOL CONTRIBUTION -->
                  <div style="background:#090E1A; border:1px solid #1E293B; border-radius:8px; padding:14px;">
                    <div style="font-size:11px; color:#A855F7; font-weight:700; text-transform:uppercase; margin-bottom:6px;">4. Tool Contribution</div>
                    <div id="matrixInspTool" style="font-size:12.5px; color:#E2E8F0; line-height:1.5;">
                      Protégé is the irreplaceable blueprint. Prevents corrupted schema creation and provides automated logical inference (HermiT reasoner) without brittle SQL code.
                    </div>
                  </div>

                </div>

                <!-- CONCEPTUAL VISUAL DEMO CARD (NO CODE) -->
                <div style="background:#070C16; border:1px dashed #334155; border-radius:8px; padding:14px 18px;" id="matrixInspVisualBox">
                  <div style="font-size:11px; color:#F59E0B; font-weight:700; text-transform:uppercase; margin-bottom:6px;">💡 Stage Conceptual Representation & Panel Talk-Track</div>
                  <div id="matrixInspVisualText" style="font-size:13px; color:#CBD5E1; line-height:1.55;">
                    "We start with Protégé because Neo4j is schema-optional by default. Protégé establishes our class taxonomy (Account as a subclass of FinancialAsset) and guarantees mathematical consistency before any data touches the database."
                  </div>
                </div>

              </div>

            </div>

          </div>
        </div>
    '''
