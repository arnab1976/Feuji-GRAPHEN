# -*- coding: utf-8 -*-
"""
Injects the Animated Interactive 6-Step Architecture Diagram into index.html
Features:
- Step-by-step interactive navigation (Steps 1 through 6)
- Auto-play / Pause / Prev / Next controls with animated progress bar
- Domain Switcher (Financial AML vs Drug Discovery)
- Animated visual flow diagram with active step highlighting and pulsing dataflow
- Simplistic plain-English 30-second talk track ("How to explain to others")
- Dedicated breakdown of all 7 core technologies at each step:
  1. Mapping Key
  2. Multi-Source Inputs
  3. Protégé & OWL 2 Ontology
  4. ChromaDB Vector Store
  5. Neo4j Property Graph DB
  6. Cypher Query Engine
  7. Hybrid Graph-RAG Engine
"""

import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# ---------------------------------------------------------------------------
# CSS FOR THE ANIMATED INTERACTIVE SIMULATOR
# ---------------------------------------------------------------------------
sim_css = '''
    /* ================= ANIMATED INTERACTIVE ARCHITECTURE SIMULATOR ================= */
    .sim-card {
      background: var(--surface, #1A2234);
      border: 1.5px solid var(--line, #2E3B54);
      border-radius: 14px;
      padding: 24px;
      margin-bottom: 28px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.28);
      position: relative;
      overflow: hidden;
    }
    .sim-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      flex-wrap: wrap;
      gap: 16px;
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 1px solid var(--line-soft, #2A364F);
    }
    .sim-title-group h3 {
      font-size: 19px;
      font-weight: 700;
      color: var(--tx-0, #FFFFFF);
      margin: 0 0 4px;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .sim-title-group p {
      font-size: 13px;
      color: var(--tx-2, #94A3B8);
      margin: 0;
    }
    .sim-controls {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .sim-btn {
      background: var(--bg-2, #121824);
      border: 1px solid var(--line-strong, #3A4763);
      color: var(--tx-1, #E2E8F0);
      padding: 6px 14px;
      border-radius: 6px;
      font-size: 12.5px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s ease;
    }
    .sim-btn:hover {
      background: var(--surface-hover, #242F46);
      border-color: var(--amber, #FF9F0A);
      color: #FFFFFF;
    }
    .sim-btn.primary {
      background: rgba(255,159,10,0.18);
      border-color: var(--amber, #FF9F0A);
      color: var(--amber, #FF9F0A);
    }
    .sim-btn.primary:hover {
      background: var(--amber, #FF9F0A);
      color: #000000;
    }
    .sim-domain-toggle {
      display: flex;
      background: var(--bg-2, #0B0F17);
      padding: 3px;
      border-radius: 8px;
      border: 1px solid var(--line-soft, #2A364F);
    }
    .sim-toggle-btn {
      background: transparent;
      border: none;
      color: var(--tx-2, #94A3B8);
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .sim-toggle-btn.active {
      background: var(--surface, #1A2234);
      color: var(--tx-0, #FFFFFF);
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    .sim-toggle-btn.active.fin {
      color: var(--amber, #FF9F0A);
    }
    .sim-toggle-btn.active.med {
      color: var(--emerald, #3DDC97);
    }

    /* STEP NAVIGATION TABS */
    .sim-step-tabs {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 8px;
      margin-bottom: 22px;
    }
    @media (max-width: 900px) {
      .sim-step-tabs {
        grid-template-columns: repeat(3, 1fr);
      }
    }
    @media (max-width: 580px) {
      .sim-step-tabs {
        grid-template-columns: repeat(2, 1fr);
      }
    }
    .sim-step-tab {
      background: var(--bg-2, #121824);
      border: 1px solid var(--line-soft, #2A364F);
      border-radius: 8px;
      padding: 10px 12px;
      text-align: left;
      cursor: pointer;
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }
    .sim-step-tab:hover {
      border-color: var(--line-strong, #3A4763);
      transform: translateY(-2px);
    }
    .sim-step-tab.active {
      background: rgba(255, 159, 10, 0.12);
      border-color: var(--amber, #FF9F0A);
      box-shadow: 0 0 14px rgba(255,159,10,0.25);
    }
    .sim-step-tab.active.med {
      background: rgba(61, 220, 151, 0.12);
      border-color: var(--emerald, #3DDC97);
      box-shadow: 0 0 14px rgba(61,220,151,0.25);
    }
    .sim-step-num {
      font-size: 10.5px;
      font-weight: 700;
      color: var(--tx-3, #64748B);
      margin-bottom: 4px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .sim-step-tab.active .sim-step-num {
      color: var(--amber, #FF9F0A);
    }
    .sim-step-tab.active.med .sim-step-num {
      color: var(--emerald, #3DDC97);
    }
    .sim-step-title {
      font-size: 12px;
      font-weight: 700;
      color: var(--tx-1, #E2E8F0);
      line-height: 1.3;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .sim-step-tab.active .sim-step-title {
      color: #FFFFFF;
    }

    /* PROGRESS BAR */
    .sim-progress-track {
      height: 4px;
      background: var(--bg-2, #0B0F17);
      border-radius: 2px;
      margin-bottom: 22px;
      overflow: hidden;
    }
    .sim-progress-fill {
      height: 100%;
      width: 16.66%;
      background: linear-gradient(90deg, var(--amber, #FF9F0A), var(--emerald, #3DDC97));
      transition: width 0.35s ease;
    }

    /* ANIMATED VISUAL FLOW DIAGRAM CANVAS */
    .sim-canvas {
      background: var(--bg-2, #0B0F17);
      border: 1px solid var(--line-soft, #2A364F);
      border-radius: 10px;
      padding: 20px;
      margin-bottom: 22px;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
    }
    .sim-pipeline-flow {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      max-width: 900px;
      gap: 8px;
      overflow-x: auto;
      padding: 10px 4px;
    }
    .sim-flow-node {
      flex: 1;
      min-width: 120px;
      background: var(--surface, #1A2234);
      border: 1.5px solid var(--line, #2E3B54);
      border-radius: 8px;
      padding: 10px 8px;
      text-align: center;
      transition: all 0.3s ease;
      position: relative;
    }
    .sim-flow-node.active {
      border-color: var(--amber, #FF9F0A);
      background: rgba(255, 159, 10, 0.14);
      transform: scale(1.05);
      box-shadow: 0 0 16px rgba(255, 159, 10, 0.35);
    }
    .sim-flow-node.active.med {
      border-color: var(--emerald, #3DDC97);
      background: rgba(61, 220, 151, 0.14);
      box-shadow: 0 0 16px rgba(61, 220, 151, 0.35);
    }
    .sim-flow-node-icon {
      font-size: 20px;
      margin-bottom: 4px;
    }
    .sim-flow-node-name {
      font-size: 11px;
      font-weight: 700;
      color: var(--tx-1, #E2E8F0);
      line-height: 1.25;
    }
    .sim-flow-node-sub {
      font-size: 9.5px;
      color: var(--tx-3, #64748B);
      margin-top: 2px;
    }
    .sim-flow-arrow {
      font-size: 16px;
      color: var(--tx-3, #475569);
      transition: all 0.3s ease;
      flex-shrink: 0;
    }
    .sim-flow-arrow.active {
      color: var(--amber, #FF9F0A);
      animation: simPulse 1s infinite alternate;
    }
    @keyframes simPulse {
      0% { opacity: 0.4; transform: translateX(-2px); }
      100% { opacity: 1; transform: translateX(2px); }
    }

    /* 30-SECOND PLAIN ENGLISH TALK TRACK BOX */
    .sim-explain-box {
      background: linear-gradient(135deg, rgba(255,159,10,0.08) 0%, rgba(96,165,250,0.06) 100%);
      border: 1.5px solid rgba(255,159,10,0.35);
      border-radius: 10px;
      padding: 16px 20px;
      margin-bottom: 22px;
    }
    .sim-explain-box.med {
      background: linear-gradient(135deg, rgba(61,220,151,0.08) 0%, rgba(96,165,250,0.06) 100%);
      border-color: rgba(61,220,151,0.35);
    }
    .sim-explain-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 8px;
    }
    .sim-explain-badge {
      background: var(--amber, #FF9F0A);
      color: #000000;
      font-size: 10.5px;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 4px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .sim-explain-badge.med {
      background: var(--emerald, #3DDC97);
    }
    .sim-explain-title {
      font-size: 15px;
      font-weight: 700;
      color: var(--tx-0, #FFFFFF);
    }
    .sim-explain-body {
      font-size: 13.5px;
      color: var(--tx-1, #E2E8F0);
      line-height: 1.6;
      margin: 0 0 10px;
    }
    .sim-why-matters {
      font-size: 12px;
      color: var(--tx-2, #94A3B8);
      background: rgba(0,0,0,0.25);
      padding: 8px 12px;
      border-radius: 6px;
      border-left: 3px solid var(--amber, #FF9F0A);
    }
    .sim-why-matters.med {
      border-left-color: var(--emerald, #3DDC97);
    }

    /* 7-TECH CONTRIBUTION GRID */
    .sim-tech-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
    }
    .sim-tech-box {
      background: var(--bg-2, #121824);
      border: 1px solid var(--line-soft, #2A364F);
      border-radius: 8px;
      padding: 12px 14px;
      transition: all 0.2s ease;
    }
    .sim-tech-box.highlight {
      border-color: rgba(255,159,10,0.5);
      background: rgba(255,159,10,0.06);
    }
    .sim-tech-box.highlight.med {
      border-color: rgba(61,220,151,0.5);
      background: rgba(61,220,151,0.06);
    }
    .sim-tech-box-header {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }
    .sim-tech-icon {
      font-size: 16px;
    }
    .sim-tech-name {
      font-size: 12px;
      font-weight: 700;
      color: var(--tx-0, #FFFFFF);
    }
    .sim-tech-role-badge {
      font-size: 9.5px;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 3px;
      background: var(--surface, #1A2234);
      color: var(--tx-2, #94A3B8);
      margin-left: auto;
    }
    .sim-tech-role-badge.star {
      background: rgba(255,159,10,0.2);
      color: var(--amber, #FF9F0A);
    }
    .sim-tech-role-badge.star.med {
      background: rgba(61,220,151,0.2);
      color: var(--emerald, #3DDC97);
    }
    .sim-tech-desc {
      font-size: 11.5px;
      color: var(--tx-2, #94A3B8);
      line-height: 1.5;
      margin: 0;
    }
'''

# ---------------------------------------------------------------------------
# JAVASCRIPT FOR INTERACTIVE ARCHITECTURE SIMULATOR
# ---------------------------------------------------------------------------
sim_js = '''
<script>
// ================= INTERACTIVE 6-STEP ARCHITECTURE SIMULATOR =================
(function() {
  const stepsData = {
    fin: [
      {
        num: "Step 1",
        title: "Unstructured Mapping",
        shortName: "1. Unstructured Mapping",
        icon: "📄",
        plainTitle: "Reading & Bridging Unstructured Documents",
        plainEnglish: "We ingest messy documents that don't have database keys connecting them—like SAR reports, loan PDF contracts, and officer emails. The system uses AI to extract named entities (people, companies, addresses) and creates bridges between documents that mention the same entities or cite the same investigation tracking codes.",
        whyMatters: "Traditional systems analyze each PDF in isolation. Graph-bridging instantly connects a loan application in New York to a suspicious activity report filed 6 months earlier in London.",
        tech: {
          key: { role: "Candidate Discovery", star: false, desc: "Scans text for candidate financial keys like Tax IDs or IBAN patterns to prepare for binding." },
          inputs: { role: "Primary Feed", star: true, desc: "Ingests raw SAR narratives, loan application PDFs, whistleblower emails, and court filings." },
          protege: { role: "Class Taxonomy", star: false, desc: "Provides OWL 2 classes (LegalEntity, NaturalPerson, SuspiciousEvent) guiding NER." },
          chroma: { role: "Vector Similarity", star: true, desc: "Embeds narrative chunks into 384-dim vectors; links chunks with >0.84 cosine similarity." },
          neo4j: { role: "Initial Ingest", star: false, desc: "Stores Document and TextChunk nodes with preliminary [:MENTIONS] co-occurrence edges." },
          cypher: { role: "Citation Query", star: false, desc: "Executes queries to link documents citing identical case IDs: (Doc1)-[:CITES]->(Doc2)." },
          rag: { role: "Semantic Search", star: false, desc: "Enables natural-language similarity search over raw narrative text paragraphs." }
        }
      },
      {
        num: "Step 2",
        title: "Structured Mapping",
        shortName: "2. Structured Mapping",
        icon: "💳",
        plainTitle: "Transforming Relational Tables into a Graph Network",
        plainEnglish: "At the same time, we ingest clean structured data from core banking SQL databases, SWIFT wire transfer tables, and corporate registries. Instead of leaving them locked in rigid SQL tables, we transform rows and foreign keys into nodes (Customers, Accounts) and directed arrows (Wires, Beneficial Ownership).",
        whyMatters: "SQL tables choke when tracing transactions across more than 2 or 3 joins. Converting tabular data into graph edges enables instantaneous, multi-hop relationship traversal.",
        tech: {
          key: { role: "Canonical IDs", star: true, desc: "Enforces canonical primary keys: ISO Account_IBAN, Customer_TaxID, LEI codes." },
          inputs: { role: "Relational Feeds", star: true, desc: "Consumes Core Banking SQL, SWIFT MT103 wire feeds, and corporate registry records." },
          protege: { role: "Object Properties", star: true, desc: "Defines formal OWL properties: ownsAccount, transferredTo, hasBeneficialOwner." },
          chroma: { role: "Standby", star: false, desc: "Holds vector indexes ready to be joined with structured entities in Step 3." },
          neo4j: { role: "Graph Backbone", star: true, desc: "Instantiates (:Customer), (:Account), and (:Device) nodes linked by directed transaction edges." },
          cypher: { role: "Schema Constraints", star: false, desc: "Applies unique constraints: CREATE CONSTRAINT FOR (a:Account) REQUIRE a.iban IS UNIQUE." },
          rag: { role: "Metadata Grounding", star: false, desc: "Prepares structured entity metadata for hybrid context expansion." }
        }
      },
      {
        num: "Step 3",
        title: "Key Binding Engine",
        shortName: "3. Key Binding Engine",
        icon: "🔑",
        plainTitle: "The Magic Bridge: Glueing Unstructured Text to Structured Records",
        plainEnglish: "This is the core breakthrough! The system extracts canonical business keys (like an Account IBAN or Tax ID) directly from the text of our PDFs, and fuses the text paragraphs directly onto the clean bank account nodes. If a borrower confessed a suspicious intent in a loan PDF, that sentence is now permanently attached to their bank account in the graph.",
        whyMatters: "Eliminates the 'hallucination' of pure LLMs and the blindness of SQL. Unstructured narrative qualitative evidence is anchored directly to quantitative transaction records.",
        tech: {
          key: { role: "The Universal Bridge", star: true, desc: "The hero of this step: Account_IBAN, Tax_ID, and LEI extracted via regex + LLM JSON Schema." },
          inputs: { role: "Cross-Modal Junction", star: false, desc: "Brings together text chunks from Step 1 and database records from Step 2." },
          protege: { role: "Semantic Validation", star: false, desc: "Validates that TextChunk can only be an evidenceFor relationship to a ValidEntity." },
          chroma: { role: "Vector Association", star: false, desc: "Synchronizes vector chunk IDs with Neo4j node IDs for bidirectional hybrid querying." },
          neo4j: { role: "Binding Edge Storage", star: true, desc: "Stores cross-modal edges: (:TextChunk)-[:EVIDENCE_FOR {confidence: 0.96}]->(:Account)." },
          cypher: { role: "MERGE Engine", star: true, desc: "Executes: MATCH (a:Account {iban: $iban}), (c:Chunk {id: $id}) MERGE (c)-[:EVIDENCE_FOR]->(a)." },
          rag: { role: "Grounded Index", star: true, desc: "Constructs the unified dual-layer retrieval index combining embeddings and graph topology." }
        }
      },
      {
        num: "Step 4",
        title: "Multi-Modal Graph",
        shortName: "4. Multi-Modal Graph",
        icon: "🕸️",
        plainTitle: "One Unified Digital Brain: The Multi-Modal Property Graph",
        plainEnglish: "We now have one unified knowledge graph in Neo4j. Bank accounts, corporate officers, wire transfers, device IP addresses, and every supporting sentence from our PDFs exist together in a single connected graph. Nothing is lost, and every connection is queryable in milliseconds.",
        whyMatters: "Breaks down all enterprise silos. Investigators can see the full picture: who owns the account, what device they logged in from, which shell companies they control, and what compliance red flags were cited.",
        tech: {
          key: { role: "Entity Resolution", star: true, desc: "Guarantees zero duplicate entities across enterprise silos via canonical mapping keys." },
          inputs: { role: "Unified Storage", star: false, desc: "All multi-source inputs reside harmoniously within a single connected graph topology." },
          protege: { role: "Enterprise Blueprint", star: true, desc: "Guarantees full OWL 2 ontology compliance, type hierarchy, and relationship semantics." },
          chroma: { role: "Synchronized Vectors", star: true, desc: "Maintains HNSW vector indices mapped directly to Neo4j graph node IDs." },
          neo4j: { role: "Native Graph Engine", star: true, desc: "Stores labeled nodes and first-class edge properties with index-free adjacency." },
          cypher: { role: "Graph Query Interface", star: true, desc: "Enables declarative querying across both relational attributes and document text." },
          rag: { role: "Knowledge Subgraphs", star: true, desc: "Extracts localized subgraphs for highly targeted, hallucination-free AI generation." }
        }
      },
      {
        num: "Step 5",
        title: "Pattern Recognition",
        shortName: "5. Pattern Recognition",
        icon: "⚡",
        plainTitle: "Detecting Hidden Fraud Rings with Cypher & Graph Algorithms",
        plainEnglish: "Instead of running slow SQL queries that take hours, the Cypher query engine traverses the graph like a spider web. In milliseconds, it detects complex money laundering patterns—such as 3-to-6 hop circular wire rings where money leaves an account and returns disguised as clean funds, or mule rings sharing the same mobile device.",
        whyMatters: "Criminals use multi-layered shell companies specifically to evade SQL and rules engines. Graph pattern recognition makes multi-hop layering immediately transparent and visual.",
        tech: {
          key: { role: "Cycle Key Matching", star: false, desc: "Tracks origin and destination IBANs across multi-hop circular wire paths." },
          inputs: { role: "Full Flow Analysis", star: false, desc: "Processes millions of historical SWIFT wire records simultaneously." },
          protege: { role: "Inference Rules", star: false, desc: "SWRL rules infer high-risk classifications based on jurisdictional exposure." },
          chroma: { role: "Contextual Rationale", star: false, desc: "Surfaces qualitative text evidence explaining why the detected pattern is suspicious." },
          neo4j: { role: "GDS Algorithms", star: true, desc: "Executes Louvain Community Detection (mule rings) and PageRank (shadow controllers)." },
          cypher: { role: "Star Pattern Engine", star: true, desc: "Executes: MATCH path = (a:Account)-[:TRANSFERRED*3..6]->(a) to uncover closed layering cycles." },
          rag: { role: "Evidence Synthesis", star: true, desc: "Packages the detected subgraph anomaly into structured context for the LLM report." }
        }
      },
      {
        num: "Step 6",
        title: "Leadership Outputs",
        shortName: "6. Leadership Deliverables",
        icon: "🎯",
        plainTitle: "Boardroom-Ready Executive Deliverables & Asset Recovery",
        plainEnglish: "The system provides leadership with exact, defensible answers: $14.25M in quantified laundering exposure across 3 specific circular rings, the exact names and shell companies engaged (Vladimir S., Apex Global, BlueStar Trading), and an automated 1-click FinCEN SAR filing package with 100% graph audit provenance.",
        whyMatters: "Leadership gets actionable, defensible proof that protects the bank from catastrophic regulatory fines (up to $50M+) and preserves $3.84M in immediately frozen assets.",
        tech: {
          key: { role: "Actionable Identifiers", star: true, desc: "Delivers exact Tax IDs, Passport numbers, and IBANs needed for freezing and enforcement." },
          inputs: { role: "Provenance Links", star: false, desc: "Cites original source PDF page numbers and SWIFT UETR transaction hashes." },
          protege: { role: "Regulatory Compliance", star: false, desc: "Formats outputs to meet strict FinCEN SAR Form 111 XML reporting standards." },
          chroma: { role: "Evidence Retrieval", star: false, desc: "Retrieves specific text excerpts to substantiate each suspicion in the executive brief." },
          neo4j: { role: "Audit Trail Source", star: true, desc: "Supplies the complete mathematical graph evidence lineage required for legal defense." },
          cypher: { role: "Aggregation Engine", star: true, desc: "Calculates total dollar exposure: sum(w.amount_usd) = $14,250,000.00." },
          rag: { role: "Executive Report AI", star: true, desc: "Hybrid Graph-RAG synthesizes the final board-quality briefing with zero hallucination." }
        }
      }
    ],
    med: [
      {
        num: "Step 1",
        title: "Biomedical Literature",
        shortName: "1. Biomedical Literature",
        icon: "📚",
        plainTitle: "Mining PubMed Papers, Preprints & Patents",
        plainEnglish: "Biomedical knowledge is trapped across millions of research papers, bioRxiv preprints, and patent disclosures. The system uses BioBERT to extract genes, proteins (EGFR), resistance mutations (L858R, C797S), and chemical compounds, linking papers together through shared targets and citation networks.",
        whyMatters: "Scientists spend months manually reading papers. Unstructured graph mapping automatically uncovers hidden correlations between preprints published on opposite sides of the globe.",
        tech: {
          key: { role: "Bio-Key Extraction", star: false, desc: "Extracts candidate protein gene symbols (EGFR) and chemical drug trade names." },
          inputs: { role: "Literature Streams", star: true, desc: "Consumes PubMed XML, bioRxiv preprints, and USPTO/EPO patent filings." },
          protege: { role: "Gene/Disease Ontology", star: false, desc: "Aligns with GO, DOID, and MeSH formal class hierarchies." },
          chroma: { role: "Bio-Embeddings", star: true, desc: "Embeds scientific abstracts via PubMedBERT; clusters corroborating mechanistic findings." },
          neo4j: { role: "Literature Graph", star: false, desc: "Stores Paper and TextChunk nodes connected by (:Paper)-[:CITES]->(:Paper) edges." },
          cypher: { role: "Bibliographic Search", star: false, desc: "Traverses scientific citation chains to map prior art and patent precedence." },
          rag: { role: "Literature QA", star: false, desc: "Enables natural language queries over millions of biomedical research paragraphs." }
        }
      },
      {
        num: "Step 2",
        title: "Assays & Crystals",
        shortName: "2. Assays & Crystals",
        icon: "🧬",
        plainTitle: "Unifying High-Throughput Assays & 3D Crystallography",
        plainEnglish: "Next, we ingest structured life sciences databases: ChEMBL bioactivity assays (IC50, Ki readings), UniProtKB protein sequences, and PDB 3D crystal structures. We convert these tables into a graph network of small molecules, target active sites, and quantitative binding affinity edges.",
        whyMatters: "Siloed bioassay data cannot explain *why* a molecule binds. Graphing PDB 3D pocket geometry directly with ChEMBL binding data reveals the exact physical mechanism.",
        tech: {
          key: { role: "Canonical Hashes", star: true, desc: "Unifies structures via Standard InChIKey (14-char hash) and UniProt Accession P00533." },
          inputs: { role: "Bioinformatics Feeds", star: true, desc: "Ingests ChEMBL IC50 assays, UniProtKB target sequences, and PDB 3D coordinates." },
          protege: { role: "Biomedical OWL", star: true, desc: "Defines object properties: bindsToTarget, hasBindingPocket, inhibitsPathway." },
          chroma: { role: "Standby", star: false, desc: "Stands ready to index target functional descriptions for hybrid discovery." },
          neo4j: { role: "Molecular Graph", star: true, desc: "Stores (:SmallMolecule), (:Target), and (:BindingPocket) nodes with affinity properties." },
          cypher: { role: "Assay Ingest", star: false, desc: "Creates quantitative affinity edges: (:SmallMolecule)-[:BINDS_TO {ic50_nm: 1.8}]->(:Target)." },
          rag: { role: "Target Grounding", star: false, desc: "Prepares verified target sequences and assay baselines for candidate scoring." }
        }
      },
      {
        num: "Step 3",
        title: "Bio Key Binding",
        shortName: "3. Bio Key Binding",
        icon: "🔑",
        plainTitle: "Binding Literature Claims Directly to Wet-Lab Assays",
        plainEnglish: "Here we fuse the literature with the laboratory. The engine extracts canonical bio-keys (UniProt_ID, InChIKey, PDB_ID) from paper texts, and connects published claims directly to our structured ChEMBL compound nodes. If a preprint claims a molecule overcomes C797S resistance, that claim is directly attached to the physical molecule in the graph.",
        whyMatters: "Reconciles published assertions with empirical wet-lab measurements, immediately flagging discrepancies or corroborating novel breakthrough hypotheses.",
        tech: {
          key: { role: "Canonical Bio-Bridge", star: true, desc: "UniProt_ID (P00533), InChIKey, PDB_ID (6S9B), and NCT_ID ground literature to databases." },
          inputs: { role: "Cross-Modal Linking", star: false, desc: "Fuses published patent text with physical chemical and target nodes." },
          protege: { role: "Semantic Constraints", star: false, desc: "Ensures evidence assertions conform to clinical pharmacology ontology rules." },
          chroma: { role: "Evidence Vectors", star: false, desc: "Indexes evidence snippets so researchers can query molecular properties in natural language." },
          neo4j: { role: "Corroboration Edges", star: true, desc: "Stores: (:TextChunk)-[:REPORTS_INHIBITION {ic50_nm: 1.8, cell: 'H1975'}]->(:Target)." },
          cypher: { role: "Binding Execution", star: true, desc: "Executes MERGE statements anchoring publication paragraphs directly to small molecules." },
          rag: { role: "Dual-Modal Index", star: true, desc: "Constructs the unified hybrid index combining chemical SMILES and scientific prose." }
        }
      },
      {
        num: "Step 4",
        title: "Biomedical Graph",
        shortName: "4. Biomedical Graph",
        icon: "🕸️",
        plainTitle: "The Unified Biomedical Knowledge Graph",
        plainEnglish: "We now have a comprehensive biomedical property graph in Neo4j. Chemical lead candidates, protein targets, resistance mutations, 3D active site residues, disease indications, adverse side effects, and supporting scientific literature reside in one cohesive, queryable network.",
        whyMatters: "Empowers drug discovery teams to ask complex questions across chemistry, biology, and clinical literature simultaneously—a process that previously took months.",
        tech: {
          key: { role: "Structural Integrity", star: true, desc: "Guarantees exact chemical and protein identity across all experimental datasets." },
          inputs: { role: "All Modalities", star: false, desc: "Unifies chemistry, genomics, proteomics, crystallography, and scientific text." },
          protege: { role: "Life Sciences Schema", star: true, desc: "Enforces strict OWL 2 biological hierarchy and drug-target interaction semantics." },
          chroma: { role: "Pharmacophore Vectors", star: true, desc: "Embeds target functional descriptions and literature assertions in vector space." },
          neo4j: { role: "Multi-Modal Graph", star: true, desc: "Houses nodes for compounds, kinases, pockets, diseases, and literature chunks." },
          cypher: { role: "Traversal Backbone", star: true, desc: "Indexes binding affinities, selectivity ratios, and molecular weights for rapid filtering." },
          rag: { role: "Clinical Context", star: true, desc: "Enables rich multi-hop context extraction for generative drug discovery AI." }
        }
      },
      {
        num: "Step 5",
        title: "Affinity Pattern Engine",
        shortName: "5. Affinity Pattern Engine",
        icon: "⚡",
        plainTitle: "Multi-Objective Optimization: Potency vs Off-Target Safety",
        plainEnglish: "Developing a drug requires multi-objective optimization: the molecule must kill the cancer mutation (EGFR C797S), spare healthy cells (wild-type EGFR), and avoid toxic anti-targets (hERG cardiotoxicity). Cypher traverses the graph to find chemical candidates that satisfy all these conditions at once.",
        whyMatters: "90% of clinical drug candidates fail due to lack of efficacy or unexpected toxicity. Graph pattern filtering eliminates toxic and non-selective candidates before expensive synthesis.",
        tech: {
          key: { role: "Target ID Filtering", star: false, desc: "Identifies specific mutant vs wild-type protein accessions in the traversal." },
          inputs: { role: "High-Throughput Screen", star: false, desc: "Evaluates thousands of candidate chemical graphs against multi-target criteria." },
          protege: { role: "Axiomatic Reasoning", star: false, desc: "Infers potential off-target toxicity based on homologous kinase family hierarchies." },
          chroma: { role: "Phenotype Similarity", star: false, desc: "Compares cellular phenotype response profiles using high-dimensional vector search." },
          neo4j: { role: "Link Prediction", star: true, desc: "Runs FastRP embeddings to predict novel target interactions for uncharacterized leads." },
          cypher: { role: "Selectivity Cypher", star: true, desc: "Executes multi-target traversal: mutant IC50 < 10nM AND wt/mutant >= 50 AND hERG > 5000nM." },
          rag: { role: "Lead Packaging", star: true, desc: "Extracts the winning candidate subgraph for chemical recipe generation." }
        }
      },
      {
        num: "Step 6",
        title: "Clinical Lead Deliverable",
        shortName: "6. Clinical Lead Deliverable",
        icon: "🎯",
        plainTitle: "Discovered Lead Drug, Chemical Recipe & Commercial Impact",
        plainEnglish: "The system delivers a concrete lead drug candidate to the Chief Scientific Officer: molecule FEU-EGFR-904, its exact chemical formula and SMILES string, the active site binding recipe (how the acrylamide warhead bypasses C797S resistance), verified 180x wild-type selectivity, zero cardiotoxicity, and a clear path to market.",
        whyMatters: "Compresses the hit-to-lead discovery timeline from 18 months down to 6 weeks, targeting a $2.8B addressable market for resistant non-small cell lung cancer.",
        tech: {
          key: { role: "Chemical Recipe Keys", star: true, desc: "Delivers exact SMILES and InChIKey required for wet-lab chemical synthesis." },
          inputs: { role: "Experimental Proof", star: false, desc: "Provides direct links to underlying PDB crystal coordinates and assay readouts." },
          protege: { role: "Regulatory Standards", star: false, desc: "Outputs formatted for FDA IND (Investigational New Drug) application filing." },
          chroma: { role: "Literature Evidence", star: false, desc: "Retrieves corroborating pre-clinical evidence for the final discovery dossier." },
          neo4j: { role: "Evidence Lineage", star: true, desc: "Provides complete audit provenance from initial paper citation to binding affinity." },
          cypher: { role: "Safety Verification", star: true, desc: "Verifies therapeutic window: 180-fold selectivity over wild-type EGFR." },
          rag: { role: "Discovery Dossier AI", star: true, desc: "Synthesizes the complete R&D investment package and chemical synthesis recipe." }
        }
      }
    ]
  };

  let currentDomain = 'fin';
  let currentStep = 0;
  let isPlaying = false;
  let playTimer = null;

  function renderStep(stepIndex, domain) {
    currentStep = stepIndex;
    currentDomain = domain;
    const data = stepsData[domain][stepIndex];
    const isMed = domain === 'med';

    // Update Step Tabs
    document.querySelectorAll('.sim-step-tab').forEach((tab, idx) => {
      if (idx === stepIndex) {
        tab.classList.add('active');
        if (isMed) tab.classList.add('med');
        else tab.classList.remove('med');
      } else {
        tab.classList.remove('active', 'med');
      }
    });

    // Update Progress Fill
    const progressFill = document.getElementById('simProgressFill');
    if (progressFill) {
      progressFill.style.width = ((stepIndex + 1) / 6 * 100) + '%';
    }

    // Update Flow Nodes
    document.querySelectorAll('.sim-flow-node').forEach((node, idx) => {
      if (idx === stepIndex) {
        node.classList.add('active');
        if (isMed) node.classList.add('med');
        else node.classList.remove('med');
      } else {
        node.classList.remove('active', 'med');
      }
    });

    // Update Flow Arrows
    document.querySelectorAll('.sim-flow-arrow').forEach((arrow, idx) => {
      if (idx === stepIndex - 1 || (stepIndex === 0 && idx === 0)) {
        arrow.classList.add('active');
      } else {
        arrow.classList.remove('active');
      }
    });

    // Update 30-Second Explain Box
    const explainBox = document.getElementById('simExplainBox');
    const explainBadge = document.getElementById('simExplainBadge');
    const explainTitle = document.getElementById('simExplainTitle');
    const explainBody = document.getElementById('simExplainBody');
    const explainWhy = document.getElementById('simExplainWhy');

    if (explainBox) {
      if (isMed) explainBox.classList.add('med');
      else explainBox.classList.remove('med');
    }
    if (explainBadge) {
      explainBadge.textContent = data.num + ' of 6';
      if (isMed) explainBadge.classList.add('med');
      else explainBadge.classList.remove('med');
    }
    if (explainTitle) explainTitle.textContent = data.plainTitle;
    if (explainBody) explainBody.textContent = data.plainEnglish;
    if (explainWhy) {
      explainWhy.innerHTML = '<strong>💡 Why this matters to stakeholders:</strong> ' + data.whyMatters;
      if (isMed) explainWhy.classList.add('med');
      else explainWhy.classList.remove('med');
    }

    // Update 7 Tech Contribution Boxes
    const techKeys = [
      { id: 'simTechKey', key: 'key', name: 'Mapping Key', icon: '🔑' },
      { id: 'simTechInputs', key: 'inputs', name: 'Multi-Source Inputs', icon: '📥' },
      { id: 'simTechProtege', key: 'protege', name: 'Protégé & OWL 2', icon: '🦉' },
      { id: 'simTechChroma', key: 'chroma', name: 'ChromaDB Vector Store', icon: '⚡' },
      { id: 'simTechNeo4j', key: 'neo4j', name: 'Neo4j Property Graph', icon: '🕸️' },
      { id: 'simTechCypher', key: 'cypher', name: 'Cypher Query Engine', icon: '🔍' },
      { id: 'simTechRag', key: 'rag', name: 'Hybrid Graph-RAG Engine', icon: '🤖' }
    ];

    techKeys.forEach(t => {
      const box = document.getElementById(t.id);
      if (box && data.tech[t.key]) {
        const item = data.tech[t.key];
        if (item.star) {
          box.classList.add('highlight');
          if (isMed) box.classList.add('med');
          else box.classList.remove('med');
        } else {
          box.classList.remove('highlight', 'med');
        }
        
        const badge = box.querySelector('.sim-tech-role-badge');
        if (badge) {
          badge.textContent = item.role;
          if (item.star) {
            badge.classList.add('star');
            if (isMed) badge.classList.add('med');
            else badge.classList.remove('med');
          } else {
            badge.classList.remove('star', 'med');
          }
        }

        const desc = box.querySelector('.sim-tech-desc');
        if (desc) desc.textContent = item.desc;
      }
    });

    // Update Step Indicator in Header
    const stepLabel = document.getElementById('simCurrentStepLabel');
    if (stepLabel) {
      stepLabel.textContent = data.num + ': ' + data.title;
    }
  }

  window.simSelectStep = function(stepIdx) {
    renderStep(stepIdx, currentDomain);
  };

  window.simNextStep = function() {
    const next = (currentStep + 1) % 6;
    renderStep(next, currentDomain);
  };

  window.simPrevStep = function() {
    const prev = (currentStep - 1 + 6) % 6;
    renderStep(prev, currentDomain);
  };

  window.simTogglePlay = function() {
    const btn = document.getElementById('simPlayBtn');
    if (!isPlaying) {
      isPlaying = true;
      if (btn) btn.innerHTML = '<span>⏸</span> Pause Auto-Tour';
      playTimer = setInterval(function() {
        simNextStep();
      }, 4200);
    } else {
      isPlaying = false;
      if (btn) btn.innerHTML = '<span>▶</span> Auto-Play Flow';
      clearInterval(playTimer);
      playTimer = null;
    }
  };

  window.simSetDomain = function(domain) {
    currentDomain = domain;
    const btnFin = document.getElementById('simToggleFin');
    const btnMed = document.getElementById('simToggleMed');
    if (btnFin && btnMed) {
      if (domain === 'fin') {
        btnFin.classList.add('active', 'fin');
        btnMed.classList.remove('active', 'med');
      } else {
        btnMed.classList.add('active', 'med');
        btnFin.classList.remove('active', 'fin');
      }
    }
    renderStep(currentStep, domain);
  };

  window.initSimWidget = function(defaultDomain) {
    if (defaultDomain) currentDomain = defaultDomain;
    simSetDomain(currentDomain);
    renderStep(0, currentDomain);
  };

  // Auto initialize on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      initSimWidget('fin');
    });
  } else {
    setTimeout(function() {
      initSimWidget('fin');
    }, 100);
  }
})();
</script>
'''

# ---------------------------------------------------------------------------
# HTML WIDGET TEMPLATE FOR THE INTERACTIVE ARCHITECTURE SIMULATOR
# ---------------------------------------------------------------------------
def generate_sim_widget_html(default_domain='fin'):
    is_med = (default_domain == 'med')
    fin_active = "" if is_med else "active fin"
    med_active = "active med" if is_med else ""
    amber_or_emerald = "var(--emerald)" if is_med else "var(--amber)"
    
    return f'''            <!-- ================= ANIMATED INTERACTIVE 6-STEP ARCHITECTURE SIMULATOR ================= -->
            <div class="sim-card" id="simWidgetCard-{default_domain}">
              
              <!-- SIMULATOR HEADER & CONTROLS -->
              <div class="sim-header">
                <div class="sim-title-group">
                  <h3>
                    <span style="display:inline-block; animation:simPulse 1.8s infinite;">⚡</span>
                    Animated Interactive 6-Step Architecture Flow
                  </h3>
                  <p>Simplistic visual walkthrough explaining the exact contribution of all 7 core technologies at each step.</p>
                </div>

                <div class="sim-controls">
                  <!-- Domain Toggle -->
                  <div class="sim-domain-toggle">
                    <button type="button" id="simToggleFin" class="sim-toggle-btn {fin_active}" onclick="simSetDomain('fin')">💳 Financial AML</button>
                    <button type="button" id="simToggleMed" class="sim-toggle-btn {med_active}" onclick="simSetDomain('med')">🧬 Drug Discovery</button>
                  </div>

                  <!-- Playback Controls -->
                  <button type="button" id="simPlayBtn" class="sim-btn primary" onclick="simTogglePlay()">
                    <span>▶</span> Auto-Play Flow
                  </button>
                  <button type="button" class="sim-btn" onclick="simPrevStep()">◀ Prev</button>
                  <button type="button" class="sim-btn" onclick="simNextStep()">Next ▶</button>
                </div>
              </div>

              <!-- PROGRESS BAR -->
              <div class="sim-progress-track">
                <div id="simProgressFill" class="sim-progress-fill" style="width: 16.66%;"></div>
              </div>

              <!-- 6 CLICKABLE STEP TABS -->
              <div class="sim-step-tabs">
                <div class="sim-step-tab active" onclick="simSelectStep(0)">
                  <div class="sim-step-num">Step 1</div>
                  <div class="sim-step-title">1. Unstructured Mapping</div>
                </div>
                <div class="sim-step-tab" onclick="simSelectStep(1)">
                  <div class="sim-step-num">Step 2</div>
                  <div class="sim-step-title">2. Structured Mapping</div>
                </div>
                <div class="sim-step-tab" onclick="simSelectStep(2)">
                  <div class="sim-step-num">Step 3</div>
                  <div class="sim-step-title">3. Key Binding Engine</div>
                </div>
                <div class="sim-step-tab" onclick="simSelectStep(3)">
                  <div class="sim-step-num">Step 4</div>
                  <div class="sim-step-title">4. Multi-Modal Graph</div>
                </div>
                <div class="sim-step-tab" onclick="simSelectStep(4)">
                  <div class="sim-step-num">Step 5</div>
                  <div class="sim-step-title">5. Pattern Recognition</div>
                </div>
                <div class="sim-step-tab" onclick="simSelectStep(5)">
                  <div class="sim-step-num">Step 6</div>
                  <div class="sim-step-title">6. Leadership Output</div>
                </div>
              </div>

              <!-- ANIMATED VISUAL PIPELINE FLOW CANVAS -->
              <div class="sim-canvas">
                <div style="font-size:11px; font-weight:700; color:var(--tx-3); text-transform:uppercase; letter-spacing:0.05em; margin-bottom:12px; width:100%; display:flex; justify-content:space-between;">
                  <span>End-to-End Dataflow Pipeline</span>
                  <span id="simCurrentStepLabel" style="color:{amber_or_emerald}; font-weight:800;">Step 1: Unstructured Mapping</span>
                </div>
                
                <div class="sim-pipeline-flow">
                  <div class="sim-flow-node active" onclick="simSelectStep(0)">
                    <div class="sim-flow-node-icon">📄</div>
                    <div class="sim-flow-node-name">1. Unstructured</div>
                    <div class="sim-flow-node-sub">PDFs, NER & Citations</div>
                  </div>

                  <div class="sim-flow-arrow">➔</div>

                  <div class="sim-flow-node" onclick="simSelectStep(1)">
                    <div class="sim-flow-node-icon">💳</div>
                    <div class="sim-flow-node-name">2. Structured</div>
                    <div class="sim-flow-node-sub">SQL Tables & Wires</div>
                  </div>

                  <div class="sim-flow-arrow">➔</div>

                  <div class="sim-flow-node" onclick="simSelectStep(2)">
                    <div class="sim-flow-node-icon">🔑</div>
                    <div class="sim-flow-node-name">3. Key Binding</div>
                    <div class="sim-flow-node-sub">The Magic Bridge</div>
                  </div>

                  <div class="sim-flow-arrow">➔</div>

                  <div class="sim-flow-node" onclick="simSelectStep(3)">
                    <div class="sim-flow-node-icon">🕸️</div>
                    <div class="sim-flow-node-name">4. Property Graph</div>
                    <div class="sim-flow-node-sub">Neo4j Unified LPG</div>
                  </div>

                  <div class="sim-flow-arrow">➔</div>

                  <div class="sim-flow-node" onclick="simSelectStep(4)">
                    <div class="sim-flow-node-icon">⚡</div>
                    <div class="sim-flow-node-name">5. Cypher Engine</div>
                    <div class="sim-flow-node-sub">Pattern Matching</div>
                  </div>

                  <div class="sim-flow-arrow">➔</div>

                  <div class="sim-flow-node" onclick="simSelectStep(5)">
                    <div class="sim-flow-node-icon">🎯</div>
                    <div class="sim-flow-node-name">6. Leadership</div>
                    <div class="sim-flow-node-sub">Exact Deliverables</div>
                  </div>
                </div>
              </div>

              <!-- SIMPLISTIC 30-SECOND TALK TRACK BOX -->
              <div id="simExplainBox" class="sim-explain-box">
                <div class="sim-explain-head">
                  <span id="simExplainBadge" class="sim-explain-badge">Step 1 of 6</span>
                  <span id="simExplainTitle" class="sim-explain-title">Reading & Bridging Unstructured Documents</span>
                </div>
                <p id="simExplainBody" class="sim-explain-body">
                  We ingest messy documents that don't have database keys connecting them—like SAR reports, loan PDF contracts, and officer emails. The system uses AI to extract named entities (people, companies, addresses) and creates bridges between documents that mention the same entities or cite the same investigation tracking codes.
                </p>
                <div id="simExplainWhy" class="sim-why-matters">
                  <strong>💡 Why this matters to stakeholders:</strong> Traditional systems analyze each PDF in isolation. Graph-bridging instantly connects a loan application in New York to a suspicious activity report filed 6 months earlier in London.
                </div>
              </div>

              <!-- 7-TECH CONTRIBUTION GRID AT CURRENT STEP -->
              <div>
                <div style="font-size:12px; font-weight:700; color:var(--tx-1); margin-bottom:10px; display:flex; align-items:center; gap:8px;">
                  <span>⚙️ Contribution of Each Core Technology at this Step:</span>
                  <span style="font-size:11px; font-weight:400; color:var(--tx-3);">(Dynamic active roles updated in real-time)</span>
                </div>

                <div class="sim-tech-grid">
                  <!-- 1. Mapping Key -->
                  <div class="sim-tech-box" id="simTechKey">
                    <div class="sim-tech-box-header">
                      <span class="sim-tech-icon">🔑</span>
                      <span class="sim-tech-name">Mapping Key</span>
                      <span class="sim-tech-role-badge">Candidate Discovery</span>
                    </div>
                    <p class="sim-tech-desc">Scans text for candidate financial keys like Tax IDs or IBAN patterns to prepare for binding.</p>
                  </div>

                  <!-- 2. Multi-Source Inputs -->
                  <div class="sim-tech-box highlight" id="simTechInputs">
                    <div class="sim-tech-box-header">
                      <span class="sim-tech-icon">📥</span>
                      <span class="sim-tech-name">Multi-Source Inputs</span>
                      <span class="sim-tech-role-badge star">Primary Feed</span>
                    </div>
                    <p class="sim-tech-desc">Ingests raw SAR narratives, loan application PDFs, whistleblower emails, and court filings.</p>
                  </div>

                  <!-- 3. Protégé & OWL 2 -->
                  <div class="sim-tech-box" id="simTechProtege">
                    <div class="sim-tech-box-header">
                      <span class="sim-tech-icon">🦉</span>
                      <span class="sim-tech-name">Protégé & OWL 2</span>
                      <span class="sim-tech-role-badge">Class Taxonomy</span>
                    </div>
                    <p class="sim-tech-desc">Provides OWL 2 classes (LegalEntity, NaturalPerson, SuspiciousEvent) guiding NER.</p>
                  </div>

                  <!-- 4. ChromaDB -->
                  <div class="sim-tech-box highlight" id="simTechChroma">
                    <div class="sim-tech-box-header">
                      <span class="sim-tech-icon">⚡</span>
                      <span class="sim-tech-name">ChromaDB Vector Store</span>
                      <span class="sim-tech-role-badge star">Vector Similarity</span>
                    </div>
                    <p class="sim-tech-desc">Embeds narrative chunks into 384-dim vectors; links chunks with &gt;0.84 cosine similarity.</p>
                  </div>

                  <!-- 5. Neo4j Graph DB -->
                  <div class="sim-tech-box" id="simTechNeo4j">
                    <div class="sim-tech-box-header">
                      <span class="sim-tech-icon">🕸️</span>
                      <span class="sim-tech-name">Neo4j Property Graph</span>
                      <span class="sim-tech-role-badge">Initial Ingest</span>
                    </div>
                    <p class="sim-tech-desc">Stores Document and TextChunk nodes with preliminary [:MENTIONS] co-occurrence edges.</p>
                  </div>

                  <!-- 6. Cypher Engine -->
                  <div class="sim-tech-box" id="simTechCypher">
                    <div class="sim-tech-box-header">
                      <span class="sim-tech-icon">🔍</span>
                      <span class="sim-tech-name">Cypher Query Engine</span>
                      <span class="sim-tech-role-badge">Citation Query</span>
                    </div>
                    <p class="sim-tech-desc">Executes queries to link documents citing identical case IDs: (Doc1)-[:CITES]-&gt;(Doc2).</p>
                  </div>

                  <!-- 7. Hybrid Graph-RAG -->
                  <div class="sim-tech-box" id="simTechRag">
                    <div class="sim-tech-box-header">
                      <span class="sim-tech-icon">🤖</span>
                      <span class="sim-tech-name">Hybrid Graph-RAG</span>
                      <span class="sim-tech-role-badge">Semantic Search</span>
                    </div>
                    <p class="sim-tech-desc">Enables natural-language similarity search over raw narrative text paragraphs.</p>
                  </div>
                </div>
              </div>

            </div>
'''

# 1. Inject CSS if not present
if '.sim-card' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>' + sim_css + '</style>\n' + html[head_pos:]
        print("Injected Simulator CSS styles.")

# 2. Inject JS if not present
if 'simSelectStep' not in html:
    body_pos = html.rfind('</body>')
    if body_pos != -1:
        html = html[:body_pos] + sim_js + '\n' + html[body_pos:]
        print("Injected Simulator JavaScript engine.")

# 3. Inject Simulator Widget into archContent-fintech (before Technical Deep Dive)
fin_target = 'Technical Deep Dive: The 6 Core Mechanics in Financial AML'
if fin_target in html and 'simWidgetCard-fin' not in html:
    pos = html.find(fin_target)
    # find preceding <div style="margin-top:32px;">
    div_pos = html.rfind('<div style="margin-top:32px;">', 0, pos)
    if div_pos != -1:
        widget_code = generate_sim_widget_html('fin')
        html = html[:div_pos] + widget_code + '\n\n            ' + html[div_pos:]
        print("Injected Simulator Widget into Financial AML view.")

# 4. Inject Simulator Widget into archContent-health (before Technical Deep Dive)
health_target = 'Technical Deep Dive: The 6 Core Mechanics in Drug Discovery'
if health_target in html and 'simWidgetCard-med' not in html:
    pos = html.find(health_target)
    div_pos = html.rfind('<div style="margin-top:32px;">', 0, pos)
    if div_pos != -1:
        widget_code = generate_sim_widget_html('med')
        html = html[:div_pos] + widget_code + '\n\n            ' + html[div_pos:]
        print("Injected Simulator Widget into Healthcare Drug Discovery view.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully updated with Animated Interactive 6-Step Architecture Simulators!")
