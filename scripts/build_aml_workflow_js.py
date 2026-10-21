# -*- coding: utf-8 -*-
"""
Full JavaScript Logic for Interactive Animated AML Workflow in index.html
Contains step data, element inspector dictionary, animation engine, and UI handlers.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

def get_aml_workflow_js():
    return '''
<script id="aml-workflow-script">
(function() {
  window.currentAmlStep = 1;
  window.currentAmlSubTab = 'talk';
  window.amlPlaying = false;
  window.amlTimer = null;
  window.amlSpeed = 1; // 1 = 8s, 2 = 4s, 0.5 = 14s

  // Seamless Modal Reparenting Controls
  window.openAmlModal = function(autoStart) {
    const modal = document.getElementById('amlModalOverlay');
    const modalBody = document.getElementById('amlModalBody');
    const container = document.getElementById('amlWorkflowMainContainer');
    const expandBtn = document.getElementById('amlExpandModalBtn');
    if (modal && modalBody && container) {
      modalBody.appendChild(container);
      if (expandBtn) expandBtn.style.display = 'none';
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
      if (window.setAmlStep) window.setAmlStep(window.currentAmlStep || 1);
      if (autoStart && !window.amlPlaying) {
        window.toggleAmlPlay();
      }
    }
  };

  window.closeAmlModal = function() {
    const modal = document.getElementById('amlModalOverlay');
    const inPageSlot = document.getElementById('archContent-aml-workflow');
    const container = document.getElementById('amlWorkflowMainContainer');
    const expandBtn = document.getElementById('amlExpandModalBtn');
    if (modal) {
      modal.style.display = 'none';
      document.body.style.overflow = '';
      if (inPageSlot && container) {
        inPageSlot.appendChild(container);
        if (expandBtn) expandBtn.style.display = 'inline-flex';
      }
    }
  };

  window.openAmlModalWithStep = function(stepNum) {
    window.openAmlModal(false);
    window.setAmlStep(stepNum);
  };

  window.openAmlInspectorHelp = function() {
    alert(`How to use the Interactive Inspector:

1. Click on any SQL table or PDF document on the left.
2. Click on any Account or Customer node in the central graph.
3. Click on any transaction edge to inspect its Cypher query and ISO validation.
4. Use the deep-dive tabs below the canvas for full interview talk-tracks!`);
  };

  // Keyboard Escape listener
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' || e.key === 'Esc') {
      window.closeAmlModal();
    }
  });

  window.amlElapsedMs = 0;




  // Master Step Data
  window.amlStepData = {
    1: {
      badge: "STAGE 1 DEEP-DIVE",
      title: "Multi-Source Structured Data Mapping via Relational Keys",
      highlightZones: ["svgZoneStructured", "svgZoneTopology"],
      activeNodes: ["nodeCustJohn", "nodeAccDE", "nodeAccCH", "nodeAccCY", "edgeOwns", "edgeWire1", "edgeWire2"],
      talkTrack: `
        <div style="font-size:13.5px; line-height:1.6; color:var(--tx-1);">
          <p style="margin-top:0;"><strong>🎙️ What to say to the Panel:</strong></p>
          <blockquote style="border-left:3px solid var(--amber); margin:8px 0; padding:8px 14px; background:rgba(255,159,10,0.06); font-style:italic; color:var(--tx-0);">
            "In enterprise AML compliance, our core structured data resides in separate relational silos: customer KYC in Oracle, transaction deposits in PostgreSQL, SWIFT wires in Kafka/MQ feeds, and sanctions lists in OFAC databases.
            Instead of executing expensive, multi-table SQL recursive joins that crash on high-velocity transactions, we ingest these records as first-class nodes and map their foreign keys directly into directed graph relationships in Neo4j.
            For example, matching <code>KYC.cust_id == Accounts.cust_id</code> creates an <code>(:Customer)-[:OWNS]->(:Account)</code> relationship. Matching <code>Wires.from_iban</code> and <code>Wires.to_iban</code> creates instant directional transaction edges <code>(:Account)-[:TRANSFERRED]->(:Account)</code>.
            Because Neo4j uses <em>index-free adjacency</em>, following a wire transfer path requires simple memory pointer dereferencing in $O(1)$ constant time, rather than repeated B-tree index lookups."
          </blockquote>
        </div>
      `,
      mechanics: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">1. Canonical Mapping Keys Used:</h5>
          <ul style="margin:0 0 10px; padding-left:18px;">
            <li><code>cust_id: "C-901"</code> ➔ Primary Key in KYC, Foreign Key in Accounts table.</li>
            <li><code>iban: "DE89370001"</code> ➔ Unique international account identifier for Originator.</li>
            <li><code>iban: "CH93000002"</code> ➔ Intermediary Swiss Correspondent account.</li>
            <li><code>tax_id: "99-887711"</code> ➔ Tax ID linking Customer John Doe to OFAC Sanctions List.</li>
          </ul>

          <h5 style="color:#60A5FA; margin:10px 0 6px; font-size:13px;">2. How Nodes & Relationships are Created (Cypher Execution):</h5>
          <pre style="background:#0D121F; padding:10px; border-radius:6px; font-size:11px; font-family:var(--mono); color:#CBD5E1; overflow-x:auto;">
// A. Create Customer Node from KYC Table
MERGE (c:Customer {tax_id: "99-887711"})
ON CREATE SET c.id = "C-901", c.name = "John Doe", c.risk_tier = "HIGH", c.pep_flag = true;

// B. Create Account Nodes from Core Banking Table
MERGE (a1:Account {iban: "DE89370001"})
ON CREATE SET a1.bank = "Deutsche Bank AG", a1.balance = 4520000.00, a1.currency = "EUR";
MERGE (a2:Account {iban: "CH93000002"})
ON CREATE SET a2.bank = "Credit Suisse AG", a2.balance = 120000.00, a2.currency = "EUR";

// C. Build Relationships from Primary/Foreign Key Matches
MERGE (c)-[:OWNS {since: "2021-03-01"}]->(a1);
MERGE (a1)-[:TRANSFERRED {tx_id: "W-8821", amount: 4500000.00, timestamp: "2026-09-12 09:14:00"}]->(a2);</pre>

          <h5 style="color:#3DDC97; margin:10px 0 6px; font-size:13px;">3. Why Graph Beats Relational SQL Here:</h5>
          <p style="margin:0;">
            A multi-hop money trail across 6 bank accounts in SQL requires 6 <code>INNER JOIN</code> operations over tables with hundreds of millions of rows, generating exponential intermediate Cartesian products. In Neo4j, each node holds double-linked pointers directly to its adjacent edges in RAM. Traversal is local, not global.
          </p>
        </div>
      `,
      tools: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">System Components at Work:</h5>
          <p style="margin:0 0 8px;"><strong>Neo4j Property Graph Database:</strong> Houses the persistent physical schema. Uses unique constraint indexes on <code>Account(iban)</code> and <code>Customer(tax_id)</code> to ensure idempotent ingestion via <code>MERGE</code>.</p>
          <p style="margin:0 0 8px;"><strong>Protégé OWL 2 Ontology:</strong> Enforces the semantic class hierarchy: <code>BankingEntity ⊑ Entity</code>, <code>Account ⊑ Asset</code>, and ensures object property domain/range: <code>domain(transferredTo) = Account</code>, <code>range(transferredTo) = Account</code>.</p>
          <p style="margin:0;"><strong>Kafka / Debezium Ingestion Connector:</strong> Streams Change Data Capture (CDC) events from transactional RDBMS databases directly to the Neo4j bolt driver.</p>
        </div>
      `,
      qa: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <div style="margin-bottom:12px;">
            <strong style="color:var(--amber);">Q: "Why not just use Snowflake or PostgreSQL with foreign keys?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> Relational databases index records, not connections. When querying an unknown transaction chain ($N$-hops), SQL requires recursive Common Table Expressions (CTEs) or multiple self-joins. Query execution time grows exponentially $O(k^d)$ with depth $d$. Neo4j's index-free adjacency traverses pointers in $O(1)$ time per hop, executing in milliseconds regardless of overall database size.</p>
          </div>
          <div>
            <strong style="color:var(--amber);">Q: "What happens if account balance data updates continuously?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> We maintain balance as a node property updated via CDC triggers, while discrete wire events are stored as timestamped directed relationships <code>[:TRANSFERRED {amount, timestamp}]</code>. This creates an immutable temporal transaction ledger in graph topology.</p>
          </div>
        </div>
      `
    },
    2: {
      badge: "STAGE 2 DEEP-DIVE",
      title: "Multi-Source Unstructured Data Mapping (Inter-Document Linking)",
      highlightZones: ["svgZoneUnstructured", "svgZoneTopology"],
      activeNodes: ["doc_sar", "doc_loan", "doc_email", "nodeChunkSAR", "nodeChunkLoan", "edgeVectorSim", "edgeMentions"],
      talkTrack: `
        <div style="font-size:13.5px; line-height:1.6; color:var(--tx-1);">
          <p style="margin-top:0;"><strong>🎙️ What to say to the Panel:</strong></p>
          <blockquote style="border-left:3px solid var(--amber); margin:8px 0; padding:8px 14px; background:rgba(255,159,10,0.06); font-style:italic; color:var(--tx-0);">
            "In compliance investigations, over 80% of critical risk intelligence is trapped in unstructured text: FinCEN Suspicious Activity Report (SAR) narrative PDFs, corporate loan application memos, and whistleblower email threads.
            Notice that unstructured documents don't have natural primary or foreign keys. So how do we link them together?
            We deploy four complementary mechanisms:
            First, <em>Co-Occurrence Entity Bridges</em>: when both a SAR narrative and a loan application mention the entity 'Acme Shell Corp' and Tax ID '99-887711', a shared entity node acts as the bridge connecting both documents.
            Second, <em>Explicit Citation Parsing</em>: extracting formal case references like 'CITES SAR-2026-09'.
            Third, <em>Dense Vector Similarity via ChromaDB</em>: generating 384-dimensional embeddings of text chunks; pairs with cosine similarity greater than 0.82 create semantic similarity edges.
            Fourth, <em>Cross-Document Coreference Resolution</em>: resolving ambiguous pronouns and aliases like 'the Cyprus front company' across multiple files."
          </blockquote>
        </div>
      `,
      mechanics: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">The 4 Unstructured Mapping Mechanisms in Detail:</h5>
          <ol style="margin:0 0 10px; padding-left:18px;">
            <li><strong>Co-Occurrence Entity Linking:</strong> Document chunks mentioning identical extracted entities link through the shared entity node: <code>(Doc1)-[:MENTIONS]->(Entity:Acme Shell)<-[:MENTIONS]-(Doc2)</code>.</li>
            <li><strong>Cross-Document Citation Extraction:</strong> LoanApp-410 explicitly cites FinCEN SAR-2026-09 via case number regex, creating an explicit <code>(Doc2)-[:CITES]->(Doc1)</code> relationship.</li>
            <li><strong>Dense Vector Embedding Distance (ChromaDB):</strong> Text chunks embedded with <code>all-MiniLM-L6-v2</code>; cosine similarity $> 0.82$ creates a semantic link <code>(Chunk1)-[:SIMILAR_TOPIC {cosine: 0.89}]->(Chunk2)</code>.</li>
            <li><strong>Coreference Resolution:</strong> An LLM pass identifies that <em>"the offshore vehicle"</em> in Doc 1 refers to <em>"Acme Shell Corp"</em> in Doc 2, consolidating aliases to one canonical entity.</li>
          </ol>

          <h5 style="color:#60A5FA; margin:10px 0 6px; font-size:13px;">Cypher Representation of Inter-Document Links:</h5>
          <pre style="background:#0D121F; padding:10px; border-radius:6px; font-size:11px; font-family:var(--mono); color:#CBD5E1; overflow-x:auto;">
// Inter-document vector similarity relationship created from ChromaDB
MATCH (c1:DocumentChunk {id: "CHK-SAR-09-P4"}), (c2:DocumentChunk {id: "CHK-LOAN-410-P2"})
WHERE gds.similarity.cosine(c1.embedding, c2.embedding) > 0.82
MERGE (c1)-[:SIMILAR_TOPIC {score: 0.89}]->(c2);

// Explicit citation link
MERGE (c2)-[:CITES {case_ref: "SAR-2026-09"}]->(c1);</pre>
        </div>
      `,
      tools: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">Tools Involved:</h5>
          <p style="margin:0 0 8px;"><strong>ChromaDB Vector Store:</strong> Embeds text chunks into dense 384-dimensional vectors using <code>sentence-transformers/all-MiniLM-L6-v2</code>. Indexes using HNSW (Hierarchical Navigable Small World) for sub-millisecond nearest neighbor search.</p>
          <p style="margin:0;"><strong>PyMuPDF & spaCy:</strong> Extracts PDF text streams, bounding boxes, and detects co-occurring entity spans across document pages.</p>
        </div>
      `,
      qa: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <div style="margin-bottom:12px;">
            <strong style="color:var(--amber);">Q: "Why not just use Vector Search alone to find related documents?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> Pure vector search suffers from semantic ambiguity—two documents describing totally different fraud cases can have high cosine similarity simply because they both discuss 'money laundering and offshore shell corporations'. By combining Vector Similarity with Co-Occurrence Entity Bridges, we guarantee both topical relevance and factual identity precision.</p>
          </div>
        </div>
      `
    },
    3: {
      badge: "STAGE 3 DEEP-DIVE",
      title: "Data Transformation Pipeline: From Unstructured Text to Structured Schema",
      highlightZones: ["svgZoneTransform"],
      activeNodes: ["step_regex", "step_spacy", "step_llm_json", "canonical_keys"],
      talkTrack: `
        <div style="font-size:13.5px; line-height:1.6; color:var(--tx-1);">
          <p style="margin-top:0;"><strong>🎙️ What to say to the Panel:</strong></p>
          <blockquote style="border-left:3px solid var(--amber); margin:8px 0; padding:8px 14px; background:rgba(255,159,10,0.06); font-style:italic; color:var(--tx-0);">
            "Here is the pivotal question every architecture panel asks: <em>How can you join free-text paragraphs with structured SQL table keys?</em>
            You cannot simply regex an entire PDF and hope for clean keys. Nor can you blindly trust an LLM to output arbitrary text.
            We implement a strict 3-tier Transformation Pipeline:
            First, <strong>Deterministic Regex & ISO Checksum Validation</strong>: we run mathematical validation like the ISO 7064 Mod-97 algorithm for IBANs and strict SSN/Tax ID regex. If an IBAN fails the mod-97 check, it is flagged immediately without wasting LLM tokens.
            Second, <strong>Linguistic NER with spaCy</strong>: fast, local tokenization to tag entity spans (PERSON, ORG, MONEY, GPE).
            Third, <strong>LLM Structured Extraction with Pydantic JSON Schema</strong>: we invoke our model (<code>gpt-4o-mini</code> at temperature 0.0) with a strict schema. The LLM extracts canonical identifiers, entity roles, and flags.
            Finally, <strong>Entity Normalization & Disambiguation</strong>: stripping punctuation, standardizing corporate suffixes ('Acme Shell LLC' = 'Acme Shell Corp'), and outputting guaranteed canonical mapping keys."
          </blockquote>
        </div>
      `,
      mechanics: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">The 3-Tier Pipeline Step-by-Step:</h5>
          <div style="background:#0D121F; padding:10px; border-radius:6px; margin-bottom:10px; font-size:11px; font-family:var(--mono); color:#CBD5E1;">
<span style="color:#A855F7;">Raw Unstructured Sentence:</span>
"During our SAR review of customer John Doe (Tax ID 99-887711), we noted multiple round-dollar wire transfers from German account DE89370001 to Swiss entity Acme Shell Corp..."

            ⬇ Tier 1: Regex & Checksum
            IBAN detected: DE89370001 ➔ Mod-97 validation: PASSED
            Tax ID detected: 99-887711 ➔ Pattern \\d{2}-\\d{7}: PASSED

            ⬇ Tier 2: spaCy NER
            [John Doe](PERSON), [99-887711](IDENTIFIER), [DE89370001](IBAN), [Acme Shell Corp](ORG)

            ⬇ Tier 3: Pydantic LLM Structured Extraction (JSON Schema)
            {
              "entities": [
                {"name": "John Doe", "type": "Customer", "tax_id": "99-887711", "role": "Beneficial Owner"},
                {"name": "Acme Shell Corp", "type": "ShellCompany", "jurisdiction": "CY"},
                {"iban": "DE89370001", "bank": "Deutsche Bank AG", "role": "Originator"}
              ],
              "red_flags": ["layering", "round_dollar_amount", "cross_border"]
            }
          </div>
        </div>
      `,
      tools: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">Tools Involved:</h5>
          <p style="margin:0 0 8px;"><strong>spaCy 3.7 (en_core_web_sm):</strong> Local NLP model running on CPU; performs POS tagging, dependency parsing, and NER boundaries.</p>
          <p style="margin:0 0 8px;"><strong>OpenAI gpt-4o-mini (Loaded via .env):</strong> Executes structured JSON mode with strict Pydantic class schemas at zero temperature for deterministic outputs.</p>
          <p style="margin:0;"><strong>Python ISO 13616 / ISO 7064 Validators:</strong> Mathematical checksum library ensuring zero garbage data enters the database.</p>
        </div>
      `,
      qa: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <div style="margin-bottom:12px;">
            <strong style="color:var(--amber);">Q: "How do you prevent the LLM from hallucinating an account number or Tax ID?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> We enforce an exact <em>Span Verification Cross-Check</em>: any key extracted by the LLM must exist as an exact substring in the source text chunk. Furthermore, banking keys must pass mathematical checksums (e.g. IBAN Mod-97). If a key fails substring verification or checksum, it is discarded before graph insertion.</p>
          </div>
        </div>
      `
    },
    4: {
      badge: "STAGE 4 DEEP-DIVE",
      title: "Unstructured-to-Structured Key Binding Engine",
      highlightZones: ["svgZoneTransform", "svgZoneTopology"],
      activeNodes: ["canonical_keys", "nodeChunkSAR", "nodeAccDE", "edgeEvidence", "nodeCustJohn"],
      talkTrack: `
        <div style="font-size:13.5px; line-height:1.6; color:var(--tx-1);">
          <p style="margin-top:0;"><strong>🎙️ What to say to the Panel:</strong></p>
          <blockquote style="border-left:3px solid var(--amber); margin:8px 0; padding:8px 14px; background:rgba(255,159,10,0.06); font-style:italic; color:var(--tx-0);">
            "Now we arrive at the foundational breakthrough of our architecture: <strong>The Key Binding Engine</strong>.
            In traditional systems, compliance PDF reports sit in SharePoint, while SQL databases sit in Oracle. They never talk.
            Once our transformation pipeline extracts the canonical mapping keys—in this case, <code>iban: 'DE89370001'</code> and <code>tax_id: '99-887711'</code>—we execute an idempotent Cypher <code>MERGE</code> command.
            This command matches the existing structured <code>Account</code> node and creates an <code>[:EVIDENCE_FOR]</code> edge directly from the unstructured text chunk to that exact account.
            Think about what this means: the text narrative is no longer isolated prose! It is now physically anchored as an evidentiary relationship in the live graph topology, complete with provenance properties: source document, page number, confidence score, and timestamp."
          </blockquote>
        </div>
      `,
      mechanics: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">Exact Cypher Binding Script:</h5>
          <pre style="background:#0D121F; padding:10px; border-radius:6px; font-size:11px; font-family:var(--mono); color:#CBD5E1; overflow-x:auto;">
// 1. Locate the pre-existing structured account node
MATCH (acc:Account {iban: $extracted_iban})

// 2. Create the document chunk node preserving complete audit provenance
MERGE (chunk:DocumentChunk {id: $chunk_id})
ON CREATE SET
  chunk.source_file = "SAR-2026-09.pdf",
  chunk.page_number = 4,
  chunk.text_snippet = $text_snippet,
  chunk.ingested_at = datetime()

// 3. Physically BIND the unstructured chunk to the structured account
MERGE (chunk)-[rel:EVIDENCE_FOR]->(acc)
ON CREATE SET
  rel.confidence = 0.96,
  rel.binding_key = "DE89370001",
  rel.extracted_by = "LLM_JSON_SCHEMA",
  rel.verified = true;</pre>

          <h5 style="color:#60A5FA; margin:10px 0 6px; font-size:13px;">Graph Entities Created:</h5>
          <ul style="margin:0; padding-left:18px;">
            <li><strong>Node:</strong> <code>(:DocumentChunk {id: 'CHK-SAR-09-P4', page: 4})</code></li>
            <li><strong>Relationship:</strong> <code>(chunk)-[:EVIDENCE_FOR {confidence: 0.96}]->(acc:Account)</code></li>
            <li><strong>Relationship:</strong> <code>(chunk)-[:ALERTS_ON {reason: 'Layering'}]->(cust:Customer)</code></li>
          </ul>
        </div>
      `,
      tools: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">Tools Involved:</h5>
          <p style="margin:0 0 8px;"><strong>Neo4j Cypher Engine:</strong> Executes ACID transactional <code>MERGE</code> statements ensuring thread-safe concurrent binding during batch ingestion.</p>
          <p style="margin:0;"><strong>Protégé OWL 2:</strong> Governs the <code>hasEvidence</code> object property, defining its domain as <code>ComplianceDocument</code> and range as <code>FinancialAccount</code>.</p>
        </div>
      `,
      qa: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <div style="margin-bottom:12px;">
            <strong style="color:var(--amber);">Q: "What if the document mentions an account number that doesn't exist yet in the structured SQL tables?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> The Cypher script creates a placeholder <em>External Account Node</em> marked with <code>{status: 'UNVERIFIED_EXTERNAL', source: 'DOCUMENT_EXTRACTED'}</code>. When the corresponding core banking feed arrives later, a reconciliation query resolves and enriches the placeholder node.</p>
          </div>
        </div>
      `
    },
    5: {
      badge: "STAGE 5 DEEP-DIVE",
      title: "How the 5 Core Enterprise Tools Cooperate to Build the Knowledge Graph",
      highlightZones: ["svgZoneTools", "svgZoneTopology"],
      activeNodes: ["tool_protege", "tool_chroma", "tool_neo4j", "tool_cypher", "tool_graphrag"],
      talkTrack: `
        <div style="font-size:13.5px; line-height:1.6; color:var(--tx-1);">
          <p style="margin-top:0;"><strong>🎙️ What to say to the Panel:</strong></p>
          <blockquote style="border-left:3px solid var(--amber); margin:8px 0; padding:8px 14px; background:rgba(255,159,10,0.06); font-style:italic; color:var(--tx-0);">
            "One of the most frequent misconceptions is thinking that a Knowledge Graph is just a graph database or just a vector database.
            In our architecture, five open-source tools work in strict serial harmony with zero functional overlap:
            1. <strong>Protégé (OWL 2)</strong> is the <em>Constitutional Law</em>: it defines formal ontology classes, relationship directions, and cardinality laws BEFORE data enters the graph.
            2. <strong>ChromaDB</strong> is the <em>Semantic Memory</em>: it handles fuzzy semantic vector recall, allowing investigators to search compliance prose by topic.
            3. <strong>Neo4j</strong> is the <em>Physical Graph Brain</em>: it stores the interconnected entities in RAM using index-free adjacency for sub-millisecond traversals.
            4. <strong>Cypher</strong> is the <em>Surgical Query Scalpel</em>: it executes deterministic pattern matching, finding multi-hop loops and cycles.
            5. <strong>Hybrid Graph-RAG</strong> is the <em>Executive Synthesizer</em>: it fuses structured Cypher subgraphs with ChromaDB vector passages to produce audit-ready, 100% verified answers with zero hallucination."
          </blockquote>
        </div>
      `,
      mechanics: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">The Serial Responsibilities Breakdown:</h5>
          <table style="width:100%; border-collapse:collapse; font-size:11.5px; margin-top:8px;">
            <thead>
              <tr style="background:#0F172A; color:#F8FAFC; border-bottom:1px solid #334155;">
                <th style="padding:6px 8px;">Tool</th>
                <th style="padding:6px 8px;">Primary Responsibility</th>
                <th style="padding:6px 8px;">What Happens Without It?</th>
              </tr>
            </thead>
            <tbody>
              <tr style="border-bottom:1px solid #1E293B;">
                <td style="padding:6px 8px; font-weight:700; color:#FF9F0A;">Protégé (OWL 2)</td>
                <td style="padding:6px 8px;">Ontology governance, validation constraints</td>
                <td style="padding:6px 8px; color:var(--tx-3);">Schema drift, arbitrary ad-hoc properties, failed compliance audits</td>
              </tr>
              <tr style="border-bottom:1px solid #1E293B;">
                <td style="padding:6px 8px; font-weight:700; color:#A855F7;">ChromaDB</td>
                <td style="padding:6px 8px;">384-d dense vector index for unstructured chunks</td>
                <td style="padding:6px 8px; color:var(--tx-3);">Cannot do fuzzy semantic similarity or query free-form natural language</td>
              </tr>
              <tr style="border-bottom:1px solid #1E293B;">
                <td style="padding:6px 8px; font-weight:700; color:#60A5FA;">Neo4j 5.x</td>
                <td style="padding:6px 8px;">Physical property graph engine, index-free adjacency</td>
                <td style="padding:6px 8px; color:var(--tx-3);">Multi-hop queries timeout; relational databases collapse</td>
              </tr>
              <tr style="border-bottom:1px solid #1E293B;">
                <td style="padding:6px 8px; font-weight:700; color:#3DDC97;">Cypher Engine</td>
                <td style="padding:6px 8px;">Declarative path queries, GDS algorithms (PageRank)</td>
                <td style="padding:6px 8px; color:var(--tx-3);">Cannot express circular loops or variable-length path matching</td>
              </tr>
              <tr>
                <td style="padding:6px 8px; font-weight:700; color:#F43F5E;">Hybrid Graph-RAG</td>
                <td style="padding:6px 8px;">Dual-channel synthesis (Vector Context + Graph Subgraph)</td>
                <td style="padding:6px 8px; color:var(--tx-3);">Pure vector RAG hallucinates calculations; pure graph misses narrative nuance</td>
              </tr>
            </tbody>
          </table>
        </div>
      `,
      tools: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">Architecture Code Example (Hybrid Graph-RAG Pipeline):</h5>
          <pre style="background:#0D121F; padding:10px; border-radius:6px; font-size:11px; font-family:var(--mono); color:#CBD5E1; overflow-x:auto;">
def hybrid_graph_rag_query(user_question: str):
    # Channel 1: ChromaDB Dense Vector Search (Unstructured Narrative Context)
    vector_docs = chromadb_client.similarity_search(user_question, k=3)
    
    # Channel 2: Cypher Deterministic Subgraph Traversal (Topological Facts)
    cypher_query = text_to_cypher_llm(user_question)
    graph_facts = neo4j_driver.execute_query(cypher_query)
    
    # Synthesis: LLM fuses both channels with strict node citation
    final_response = llm.generate(
        system_prompt="Answer ONLY using the provided Graph Facts and Vector Docs. "
                      "Cite exact Node IDs for every dollar amount or account.",
        context={"graph_subgraph": graph_facts, "vector_narratives": vector_docs}
    )
    return final_response</pre>
        </div>
      `,
      qa: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <div style="margin-bottom:12px;">
            <strong style="color:var(--amber);">Q: "Neo4j now has built-in vector search. Why do you still keep ChromaDB?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> Architecture separation of concerns! High-frequency vector indexing and vector distance filtering can be memory-intensive. Keeping ChromaDB as a dedicated vector cache offloads GPU/CPU memory pressure from Neo4j, allowing Neo4j to dedicate 100% of its buffer pool to index-free graph adjacency caching.</p>
          </div>
        </div>
      `
    },
    6: {
      badge: "STAGE 6 DEEP-DIVE",
      title: "How Pattern Recognition Works: Detecting Layering Rings & Mule Hubs",
      highlightZones: ["svgZoneTopology", "svgZoneOutputs"],
      activeNodes: ["nodeAccDE", "nodeAccCH", "nodeAccCY", "edgeWire1", "edgeWire2", "edgeWire3", "nodeDevice", "pattern_ring", "pattern_device"],
      talkTrack: `
        <div style="font-size:13.5px; line-height:1.6; color:var(--tx-1);">
          <p style="margin-top:0;"><strong>🎙️ What to say to the Panel:</strong></p>
          <blockquote style="border-left:3px solid var(--amber); margin:8px 0; padding:8px 14px; background:rgba(255,159,10,0.06); font-style:italic; color:var(--tx-0);">
            "Now let's examine the heart of AML detection: <strong>How Pattern Recognition Works in a Knowledge Graph</strong>.
            Traditional fraud systems rely on threshold rules like 'flag any wire over $10,000'. Criminals easily evade this by structuring transfers across multiple shell companies.
            In a Knowledge Graph, pattern recognition is <em>topological motif matching</em>, not statistical guesswork:
            Look at this diagram: Account DE89370001 transfers $4.5M to Swiss Account CH93000002. From there, $4.48M is routed to Cyprus Account CY12000003. Within 26 hours, $4.46M returns right back to German Account DE89370001!
            That is a classic <strong>3-Hop Circular Layering Cycle</strong> designed to obfuscate audit trails.
            A single Cypher query detects this cycle across 100 million accounts in 12 milliseconds.
            Simultaneously, we detect a <strong>Shared Device Fraud Hub</strong>: both John Doe and Acme Shell Corp login from the identical MAC address <code>00:14:22:A9:BC:11</code> and IP <code>192.168.1.50</code>.
            Graph topology unmasks what tabular SQL is completely blind to."
          </blockquote>
        </div>
      `,
      mechanics: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">1. Declarative Cypher Pattern Query (Circular Wire Layering):</h5>
          <pre style="background:#0D121F; padding:10px; border-radius:6px; font-size:11px; font-family:var(--mono); color:#CBD5E1; overflow-x:auto;">
MATCH path = (origin:Account)-[wires:TRANSFERRED*3..6]->(origin)
WHERE all(w IN wires WHERE w.amount >= 500000.00)
  AND duration.inHours(wires[0].timestamp, last(wires).timestamp).hours <= 48
RETURN origin.iban AS origin_account,
       [w IN wires | w.amount] AS amounts,
       reduce(total = 0, w IN wires | total + w.amount) AS total_laundered,
       length(path) AS hop_count;</pre>

          <h5 style="color:#A855F7; margin:10px 0 6px; font-size:13px;">2. Shared Device / Mule Hub Cypher Query:</h5>
          <pre style="background:#0D121F; padding:10px; border-radius:6px; font-size:11px; font-family:var(--mono); color:#CBD5E1; overflow-x:auto;">
MATCH (c1:Customer)-[:OPERATES_FROM]->(dev:Device)<-[:OPERATES_FROM]-(c2:Customer)
WHERE c1 <> c2
RETURN dev.mac_address, dev.ip_address, collect(c1.name) AS linked_suspects;</pre>

          <h5 style="color:#60A5FA; margin:10px 0 6px; font-size:13px;">3. Graph Data Science (GDS) Algorithms:</h5>
          <p style="margin:0;">
            • <strong>PageRank Centrality:</strong> Unmasks the shadow ringleader who orchestrates funds without appearing on frontline accounts.<br>
            • <strong>Louvain Community Detection:</strong> Automatically partitions the graph into criminal syndicates based on modularity clustering.
          </p>
        </div>
      `,
      tools: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">Tools Involved:</h5>
          <p style="margin:0 0 8px;"><strong>Neo4j Graph Data Science (GDS) Library:</strong> Executes in-memory projected graph algorithms (PageRank, Weakly Connected Components, Louvain).</p>
          <p style="margin:0;"><strong>Cypher Query Engine:</strong> Executes variable-length path expansion <code>*3..6</code> using DFS with pruning for optimal execution speed.</p>
        </div>
      `,
      qa: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <div style="margin-bottom:12px;">
            <strong style="color:var(--amber);">Q: "Can machine learning (like Random Forest or XGBoost) catch this circular ring?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> Tabular ML algorithms examine row-level features in isolation (e.g. single transaction amount). They cannot easily perceive topological cycle motifs spanning multiple hops without extensive manual feature engineering. Even if they flag an anomaly score, they cannot generate the explainable circular path evidence required by FinCEN auditors.</p>
          </div>
        </div>
      `
    },
    7: {
      badge: "STAGE 7 DEEP-DIVE",
      title: "Concrete Executive Leadership Deliverables & Regulatory SAR Filing",
      highlightZones: ["svgZoneOutputs"],
      activeNodes: ["pattern_ring", "pattern_device", "pattern_pagerank", "exec_deliverable"],
      talkTrack: `
        <div style="font-size:13.5px; line-height:1.6; color:var(--tx-1);">
          <p style="margin-top:0;"><strong>🎙️ What to say to the Panel:</strong></p>
          <blockquote style="border-left:3px solid var(--amber); margin:8px 0; padding:8px 14px; background:rgba(255,159,10,0.06); font-style:italic; color:var(--tx-0);">
            "Finally, how do we present our results to executive leadership and federal regulators?
            Executives and compliance officers do not want raw Cypher queries or high-dimensional vector embeddings. They need concrete, quantifiable business outcomes:
            1. <strong>Quantified Money Laundering Exposure:</strong> Exact dollar value—<strong>$14,250,000.00 USD</strong>—identified across 3 active circular layering rings spanning 14 accounts in 4 jurisdictions.
            2. <strong>Identified Criminal Syndicate:</strong> Unmasking the beneficial owners and shell vehicles: <code>John Doe</code> (Sanctioned individual), <code>Acme Shell Corp</code> (Cyprus vehicle), and <code>Alpine Asset Holdco</code> (Swiss shell).
            3. <strong>Regulatory Deliverable:</strong> An automated, 1-click FinCEN Suspicious Activity Report (SAR Form 111) filing package.
            Because every single assertion in the report is grounded in a specific graph node ID, our output has <strong>100% cryptographic audit provenance and zero hallucination</strong>."
          </blockquote>
        </div>
      `,
      mechanics: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--emerald); margin:0 0 6px; font-size:13px;">The 3 Concrete Executive Deliverables:</h5>
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:12px; margin-top:8px;">
            <div style="background:#0F172A; border:1px solid #334155; border-radius:6px; padding:12px;">
              <span style="color:#F43F5E; font-size:10px; font-weight:700;">DELIVERABLE 1: EXPOSURE</span>
              <div style="font-size:18px; font-weight:800; color:#F43F5E; margin:4px 0;">$14,250,000.00</div>
              <p style="font-size:11px; color:#94A3B8; margin:0;">Immediate freezing request issued across Correspondent banks in Germany, Switzerland, and Cyprus.</p>
            </div>
            <div style="background:#0F172A; border:1px solid #334155; border-radius:6px; padding:12px;">
              <span style="color:#FF9F0A; font-size:10px; font-weight:700;">DELIVERABLE 2: SYNDICATE</span>
              <div style="font-size:12px; font-weight:700; color:#F8FAFC; margin:4px 0;">John Doe & 3 Shell Fronts</div>
              <p style="font-size:11px; color:#94A3B8; margin:0;">Linked by beneficial ownership filings, co-located device logins (MAC: 00:14:22:A9:BC:11), and wire loops.</p>
            </div>
            <div style="background:#0F172A; border:1px solid #334155; border-radius:6px; padding:12px;">
              <span style="color:#3DDC97; font-size:10px; font-weight:700;">DELIVERABLE 3: REGULATORY</span>
              <div style="font-size:12px; font-weight:700; color:#3DDC97; margin:4px 0;">FinCEN Form 111 XML Package</div>
              <p style="font-size:11px; color:#94A3B8; margin:0;">Pre-populated with full visual evidentiary subgraph, timestamps, and SAR narrative citations.</p>
            </div>
          </div>
        </div>
      `,
      tools: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <h5 style="color:var(--amber); margin:0 0 6px; font-size:13px;">Hybrid Graph-RAG Report Generation:</h5>
          <p style="margin:0 0 8px;">The final filing is assembled by the <strong>Hybrid Graph-RAG Agent</strong>:</p>
          <pre style="background:#0D121F; padding:10px; border-radius:6px; font-size:11px; font-family:var(--mono); color:#CBD5E1; overflow-x:auto;">
POST /api/aml/sar-package
Response: {
  "status": "READY_FOR_FILING",
  "total_exposure_usd": 14250000.00,
  "suspects": ["John Doe", "Acme Shell Corp", "Alpine Asset Holdco"],
  "evidence_graph_nodes": ["C-901", "DE89370001", "CH93000002", "CY12000003", "CHK-SAR-09-P4"],
  "audit_trail_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}</pre>
        </div>
      `,
      qa: `
        <div style="font-size:13px; line-height:1.6; color:var(--tx-1);">
          <div style="margin-bottom:12px;">
            <strong style="color:var(--amber);">Q: "How do you guarantee to FinCEN and internal auditors that your GenAI did not hallucinate this SAR report?"</strong>
            <p style="margin:4px 0 0; color:var(--tx-2);"><strong>A:</strong> Every entity name, transaction dollar amount, and date is physically constrained to deterministic nodes in Neo4j. The LLM only formats the text narrative; it has zero freedom to invent account numbers or dollar figures. Every claim in the generated FinCEN document includes a direct hyperlink to the underlying graph node and source PDF bounding box.</p>
          </div>
        </div>
      `
    }
  };

  // Clickable SVG Elements Metadata Dictionary
  window.amlElementData = {
    "tbl_kyc": {
      name: "KYC Customer Registry",
      type: "Structured SQL Table",
      source: "Oracle Enterprise DB (Table: KYC_MASTER)",
      protege: "Class: :CustomerInstance ⊑ :Person",
      props: "cust_id: 'C-901'\\nfull_name: 'John Doe'\\ntax_id: '99-887711'\\nrisk_tier: 'HIGH'\\npep_flag: true\\ncountry: 'DE'",
      cypher: "MERGE (c:Customer {tax_id: '99-887711'})\\nON CREATE SET c.id='C-901', c.name='John Doe', c.risk_tier='HIGH';"
    },
    "tbl_accounts": {
      name: "Core Banking Accounts",
      type: "Structured SQL Table",
      source: "PostgreSQL Production DB (Table: ACCOUNT_LEDGER)",
      protege: "Class: :FinancialAccount ⊑ :Asset",
      props: "acc_id: 'A101'\\niban: 'DE89370001'\\ncust_id: 'C-901'\\nbalance: 4520000.00\\ncurrency: 'EUR'\\nstatus: 'ACTIVE'",
      cypher: "MERGE (a:Account {iban: 'DE89370001'})\\nON CREATE SET a.balance=4520000.00, a.currency='EUR';"
    },
    "tbl_wires": {
      name: "SWIFT MT103 Wire Messages",
      type: "Structured Event Stream",
      source: "Kafka MQ (Topic: swift.wire.transfers.v1)",
      protege: "ObjectProperty: :transferredFunds",
      props: "wire_id: 'W-8821'\\nfrom_iban: 'DE89370001'\\nto_iban: 'CH93000002'\\namount: 4500000.00\\ncurrency: 'EUR'\\ntimestamp: '2026-09-12 09:14:00'",
      cypher: "MATCH (a1:Account {iban: 'DE89370001'}), (a2:Account {iban: 'CH93000002'})\\nMERGE (a1)-[:TRANSFERRED {tx_id: 'W-8821', amount: 4500000.00}]->(a2);"
    },
    "tbl_ofac": {
      name: "OFAC Sanctions & PEP List",
      type: "External Watchlist Feed",
      source: "US Treasury OFAC Sanctions XML Feed",
      protege: "Class: :SanctionedEntity",
      props: "tax_id: '99-887711'\\nentity_name: 'John Doe'\\nprogram: 'SDNTK'\\nlisted_date: '2024-05-18'\\nseverity: 'BLOCKING'",
      cypher: "MATCH (c:Customer {tax_id: '99-887711'})\\nSET c.sanctioned = true, c.sanction_program = 'SDNTK';"
    },
    "doc_sar": {
      name: "FinCEN SAR-2026-09 Narrative PDF",
      type: "Unstructured Compliance Document",
      source: "Compliance DMS (Path: /reports/2026/sar_09.pdf)",
      protege: "Class: :ComplianceReport ⊑ :Document",
      props: "file_name: 'SAR-2026-09.pdf'\\npages: 14\\ncase_id: 'SAR-2026-09'\\nauthor: 'Financial Intelligence Unit'\\nchunk_count: 28",
      cypher: "MERGE (d:Document {case_id: 'SAR-2026-09', type: 'SAR_NARRATIVE'});"
    },
    "doc_loan": {
      name: "Commercial Loan Application PDF",
      type: "Unstructured Credit Underwriting Document",
      source: "Commercial Lending Portal (Path: /loans/app_410.pdf)",
      protege: "Class: :CreditApplication ⊑ :Document",
      props: "file_name: 'LoanApp-410.pdf'\\napplicant: 'Acme Shell Corp'\\nbeneficial_owner: 'John Doe'\\ndeclared_iban: 'DE89370001'",
      cypher: "MERGE (d:Document {case_id: 'LoanApp-410', type: 'LOAN_APPLICATION'});"
    },
    "doc_email": {
      name: "Compliance Alert Email Thread",
      type: "Unstructured Email Message (.eml)",
      source: "Microsoft Exchange Compliance Mailbox",
      protege: "Class: :InternalCommunication",
      props: "thread_id: 'Email-88'\\nsubject: 'Urgent: Cross-border structuring in Cyprus/Swiss accounts'\\nflagged_ip: '192.168.1.50'",
      cypher: "MERGE (d:Document {id: 'Email-88', type: 'COMPLIANCE_EMAIL'});"
    },
    "step_regex": {
      name: "Regex & Checksum Validator",
      type: "Deterministic Transformation Stage",
      source: "Python re module + ISO 7064 Mod-97 checksum calculator",
      protege: "ValidationRule: :ValidIBANRule",
      props: "algorithm: 'ISO 7064 Mod-97 Checksum'\\nregex_iban: '^[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}$'\\nregex_taxid: '^\\\\d{2}-\\\\d{7}$'\\nstatus: 'PASSED'",
      cypher: "// Checksum validation runs in Python prior to Cypher execution."
    },
    "step_spacy": {
      name: "spaCy 3.7 Linguistic NER",
      type: "NLP Entity Extraction Stage",
      source: "spaCy en_core_web_sm pipeline",
      protege: "AnnotationProperty: :namedEntitySpan",
      props: "model: 'en_core_web_sm'\\nentity_classes: ['PERSON', 'ORG', 'MONEY', 'GPE']\\ntokenizer: 'spaCy standard'",
      cypher: "// Extracts tokens and offsets for LLM verification."
    },
    "step_llm_json": {
      name: "LLM Structured JSON Schema Extractor",
      type: "Generative Structured Extractor",
      source: "OpenAI gpt-4o-mini via .env (Structured Outputs)",
      protege: "OntologyMapper: :JsonSchemaToOwl",
      props: "model: 'gpt-4o-mini'\\ntemperature: 0.0\\nresponse_format: 'json_object'\\nschema: 'Pydantic AMLSchema'",
      cypher: "// Outputs strictly typed JSON payload for Cypher MERGE."
    },
    "canonical_keys": {
      name: "Canonical Mapping Keys",
      type: "Unified Resolution Bus",
      source: "Harmonized Primary Identifiers",
      protege: "DataProperty: :hasCanonicalIdentifier",
      props: "tax_id: '99-887711'\\niban_origin: 'DE89370001'\\niban_target: 'CH93000002'\\ndevice_mac: '00:14:22:A9:BC:11'",
      cypher: "// Keys used as parameters in Cypher MATCH & MERGE."
    },
    "node_cust_john": {
      name: "Customer: John Doe",
      type: "Domain Entity Node (Person)",
      source: "KYC Database + SAR Narrative",
      protege: "Class: :CustomerInstance (Sanctioned Individual)",
      props: "id: 'C-901'\\nname: 'John Doe'\\ntax_id: '99-887711'\\nrisk_tier: 'HIGH'\\nsanctioned: true\\npep: true",
      cypher: "MATCH (c:Customer {tax_id: '99-887711'}) RETURN c;"
    },
    "node_acc_de": {
      name: "Account: DE89370001",
      type: "Domain Entity Node (Financial Account)",
      source: "Core Banking SQL + Loan Application PDF",
      protege: "Class: :FinancialAccount",
      props: "iban: 'DE89370001'\\nbank: 'Deutsche Bank AG'\\ncurrency: 'EUR'\\nbalance: 4520000.00\\njurisdiction: 'Germany'",
      cypher: "MATCH (a:Account {iban: 'DE89370001'}) RETURN a;"
    },
    "node_acc_ch": {
      name: "Account: CH93000002",
      type: "Domain Entity Node (Intermediary Account)",
      source: "SWIFT Wire MT103",
      protege: "Class: :CorrespondentAccount",
      props: "iban: 'CH93000002'\\nbank: 'Credit Suisse AG'\\ncurrency: 'EUR'\\nbalance: 120000.00\\njurisdiction: 'Switzerland'",
      cypher: "MATCH (a:Account {iban: 'CH93000002'}) RETURN a;"
    },
    "node_acc_cy": {
      name: "Account: CY12000003",
      type: "Domain Entity Node (Layering Account)",
      source: "SWIFT Wire MT103",
      protege: "Class: :OffshoreAccount",
      props: "iban: 'CY12000003'\\nbank: 'Bank of Cyprus'\\ncurrency: 'EUR'\\nbalance: 85000.00\\njurisdiction: 'Cyprus'",
      cypher: "MATCH (a:Account {iban: 'CY12000003'}) RETURN a;"
    },
    "node_cust_acme": {
      name: "Customer: Acme Shell Corp",
      type: "Domain Entity Node (Shell Corporate Entity)",
      source: "Commercial Loan Application PDF + FinCEN SAR",
      protege: "Class: :CorporateCustomer ⊑ :ShellCompany",
      props: "name: 'Acme Shell Corp'\\njurisdiction: 'Cyprus'\\nincorporation_date: '2024-01-10'\\nbeneficial_owner: 'John Doe'",
      cypher: "MATCH (s:Customer {name: 'Acme Shell Corp'}) RETURN s;"
    },
    "node_device": {
      name: "Device: MAC 00:14:22:A9:BC:11",
      type: "Digital Fingerprint Node",
      source: "Web Banking Access Logs + Email Thread Alert",
      protege: "Class: :DigitalDevice",
      props: "mac_address: '00:14:22:A9:BC:11'\\nip_address: '192.168.1.50'\\nuser_agent: 'Chrome/128 Windows 11'\\nfraud_score: 94",
      cypher: "MATCH (d:Device {mac_address: '00:14:22:A9:BC:11'}) RETURN d;"
    },
    "node_chunk_sar": {
      name: "DocumentChunk: SAR-09 Page 4",
      type: "Unstructured Document Provenance Node",
      source: "FinCEN SAR-2026-09.pdf (Page 4)",
      protege: "Class: :DocumentChunk",
      props: "id: 'CHK-SAR-09-P4'\\nsource: 'SAR-2026-09.pdf'\\npage: 4\\nembedding_dims: 384\\nconfidence: 0.96",
      cypher: "MATCH (c:DocumentChunk {id: 'CHK-SAR-09-P4'}) RETURN c;"
    },
    "node_chunk_loan": {
      name: "DocumentChunk: LoanApp Page 2",
      type: "Unstructured Document Provenance Node",
      source: "LoanApp-410.pdf (Page 2)",
      protege: "Class: :DocumentChunk",
      props: "id: 'CHK-LOAN-410-P2'\\nsource: 'LoanApp-410.pdf'\\npage: 2\\nembedding_dims: 384",
      cypher: "MATCH (c:DocumentChunk {id: 'CHK-LOAN-410-P2'}) RETURN c;"
    },
    "edge_owns": {
      name: "Relationship: [:OWNS]",
      type: "Direct Ownership Edge",
      source: "Core Banking SQL Foreign Key Match",
      protege: "ObjectProperty: :ownsAccount",
      props: "since: '2021-03-01'\\nverified: true\\nsigning_authority: 'SOLE'",
      cypher: "MERGE (c)-[:OWNS {since: '2021-03-01'}]->(a);"
    },
    "edge_wire1": {
      name: "Relationship: [:TRANSFERRED] (Leg 1)",
      type: "Financial Wire Transfer Edge",
      source: "SWIFT MT103 Wire Feed",
      protege: "ObjectProperty: :transferredFunds",
      props: "tx_id: 'W-8821'\\namount: 4500000.00\\ncurrency: 'EUR'\\ntimestamp: '2026-09-12 09:14:00'\\nrouting: 'DE ➔ CH'",
      cypher: "CREATE (a1)-[:TRANSFERRED {tx_id: 'W-8821', amount: 4500000.00}]->(a2);"
    },
    "edge_wire2": {
      name: "Relationship: [:TRANSFERRED] (Leg 2)",
      type: "Financial Wire Transfer Edge",
      source: "SWIFT MT103 Wire Feed",
      protege: "ObjectProperty: :transferredFunds",
      props: "tx_id: 'W-8824'\\namount: 4485000.00\\ncurrency: 'EUR'\\ntimestamp: '2026-09-12 17:30:00'\\nrouting: 'CH ➔ CY'",
      cypher: "CREATE (a2)-[:TRANSFERRED {tx_id: 'W-8824', amount: 4485000.00}]->(a3);"
    },
    "edge_wire3": {
      name: "Relationship: [:TRANSFERRED] (Leg 3 - Circular Return)",
      type: "Layering Round-Trip Wire Edge",
      source: "SWIFT MT103 Wire Feed",
      protege: "ObjectProperty: :transferredFunds (Circular Flagged)",
      props: "tx_id: 'W-8830'\\namount: 4460000.00\\ncurrency: 'EUR'\\ntimestamp: '2026-09-13 11:05:00'\\nrouting: 'CY ➔ DE (Return Loop)'",
      cypher: "CREATE (a3)-[:TRANSFERRED {tx_id: 'W-8830', amount: 4460000.00, cycle: true}]->(a1);"
    },
    "edge_evidence": {
      name: "Relationship: [:EVIDENCE_FOR] (Canonical Key Binding)",
      type: "Unstructured-to-Structured Binding Edge",
      source: "Key Binding Engine Match on IBAN: 'DE89370001'",
      protege: "ObjectProperty: :isEvidentiarySupportFor",
      props: "confidence: 0.96\\nbinding_key: 'DE89370001'\\nextracted_by: 'LLM_JSON_SCHEMA'\\nverified: true",
      cypher: "MERGE (chunk)-[:EVIDENCE_FOR {confidence: 0.96}]->(acc);"
    },
    "pattern_ring": {
      name: "Pattern: 3-Hop Circular Wire Layering Ring",
      type: "Graph Topology Fraud Motif",
      source: "Cypher Pattern Recognition Engine",
      protege: "InferenceRule: :CircularLayeringDetectionRule",
      props: "cycle_length: 3\\ntotal_amount: $13,445,000.00\\nelapsed_hours: 25.8\\nrisk_score: 99.8",
      cypher: "MATCH path = (origin:Account)-[wires:TRANSFERRED*3..6]->(origin)\\nWHERE all(w IN wires WHERE w.amount >= 500000.00)\\nRETURN path;"
    },
    "pattern_device": {
      name: "Pattern: Mule Device / IP Fraud Hub",
      type: "Graph Topology Hub Motif",
      source: "Cypher Entity Clustering",
      protege: "InferenceRule: :MuleHubRule",
      props: "mac_address: '00:14:22:A9:BC:11'\\nshared_accounts: 4\\nlinked_customers: ['John Doe', 'Acme Shell Corp']",
      cypher: "MATCH (c1)-[:OPERATES_FROM]->(d:Device)<-[:OPERATES_FROM]-(c2)\\nWHERE c1 <> c2 RETURN d, c1, c2;"
    },
    "pattern_pagerank": {
      name: "Graph Data Science: PageRank Centrality",
      type: "Centrality Algorithm",
      source: "Neo4j Graph Data Science (GDS)",
      protege: "Algorithm: :PageRank",
      props: "kingpin_node: 'John Doe'\\nscore: 0.884\\nincoming_influence: 0.92\\nclassification: 'SYNDICATE_RINGLEADER'",
      cypher: "CALL gds.pageRank.stream('amlGraph')\\nYIELD nodeId, score\\nRETURN gds.util.asNode(nodeId).name, score ORDER BY score DESC LIMIT 1;"
    },
    "exec_deliverable": {
      name: "Executive Deliverables & Regulatory SAR Filing",
      type: "Executive Leadership Compliance Package",
      source: "Hybrid Graph-RAG Synthesis Agent",
      protege: "Deliverable: :FinCENSARFilingPackage",
      props: "quantified_exposure: '$14,250,000.00 USD'\\nrings_detected: 3\\nsar_form: 'FinCEN Form 111 (XML)'\\naudit_trail: '100% Graph Grounded'",
      cypher: "MATCH (n:Customer)-[:OWNS]->(a:Account)\\nWHERE a.cycle_flag = true\\nRETURN sum(a.laundered_usd) AS total_exposure;"
    }
  };

  // Switch Active Step
  window.setAmlStep = function(stepNum) {
    if (stepNum < 1 || stepNum > 7) return;
    window.currentAmlStep = stepNum;

    // Update Step Buttons
    for (let i = 1; i <= 7; i++) {
      const btn = document.getElementById('amlStepBtn-' + i);
      if (btn) {
        if (i === stepNum) {
          btn.className = 'aml-step-btn active';
          const badge = btn.querySelector('span:first-child');
          if (badge) { badge.style.background = 'var(--amber)'; badge.style.color = '#000'; }
        } else {
          btn.className = 'aml-step-btn';
          const badge = btn.querySelector('span:first-child');
          if (badge) { badge.style.background = 'var(--line-strong)'; badge.style.color = '#FFF'; }
        }
      }
    }

    // Update Progress Bar
    const pbar = document.getElementById('amlProgressBar');
    if (pbar) {
      pbar.style.width = (stepNum / 7 * 100) + '%';
    }

    // Update Modal Header Stage Indicator
    const modalInd = document.getElementById('amlModalStageIndicator');
    if (modalInd) modalInd.innerText = `Stage ${stepNum} of 7 Active`;

    // Update Step Label
    const lbl = document.getElementById('amlStepLabel');
    const data = window.amlStepData[stepNum];
    if (lbl && data) {
      lbl.innerText = `Stage ${stepNum}/7: ${data.title}`;
    }

    // Update Deep-Dive Badge & Title
    const curBadge = document.getElementById('amlCurrentStageBadge');
    const curTitle = document.getElementById('amlCurrentStageTitle');
    if (curBadge && data) curBadge.innerText = data.badge;
    if (curTitle && data) curTitle.innerText = data.title;

    // Update Deep-Dive Panes
    const talkPane = document.getElementById('amlSubContent-talk');
    const mechPane = document.getElementById('amlSubContent-mechanics');
    const toolsPane = document.getElementById('amlSubContent-tools');
    const qaPane = document.getElementById('amlSubContent-qa');

    if (talkPane && data) talkPane.innerHTML = data.talkTrack;
    if (mechPane && data) mechPane.innerHTML = data.mechanics;
    if (toolsPane && data) toolsPane.innerHTML = data.tools;
    if (qaPane && data) qaPane.innerHTML = data.qa;

    // Highlight Canvas Elements
    updateSvgHighlights(stepNum);
  };

  function updateAmlTimerDisplay() {
    const badge = document.getElementById('amlTimerBadge');
    const pbar = document.getElementById('amlStepProgressBar');
    const overallBar = document.getElementById('amlOverallProgressBar');

    const totalMs = 8000 / (window.amlSpeed || 1);
    const remainingSec = Math.max(0, (totalMs - window.amlElapsedMs) / 1000).toFixed(1);
    const stepPct = Math.min(100, (window.amlElapsedMs / totalMs) * 100);

    if (badge) {
      badge.style.display = 'inline-flex';
      badge.innerHTML = `<span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#FF9F0A; animation:amlDotPulse 0.8s infinite;"></span> Auto-advancing in <strong>${remainingSec}s</strong>`;
    }
    if (pbar) {
      pbar.style.width = stepPct + '%';
    }
    if (overallBar) {
      const overallPct = (((window.currentAmlStep - 1) + (stepPct / 100)) / 7) * 100;
      overallBar.style.width = overallPct + '%';
    }
  }

  function amlTick() {
    if (!window.amlPlaying) return;
    window.amlElapsedMs += 50;
    const totalMs = 8000 / (window.amlSpeed || 1);
    updateAmlTimerDisplay();

    if (window.amlElapsedMs >= totalMs) {
      window.amlElapsedMs = 0;
      window.nextAmlStep();
    }
  }

  function startAmlTimer() {
    clearInterval(window.amlTimer);
    window.amlElapsedMs = 0;
    updateAmlTimerDisplay();
    window.amlTimer = setInterval(amlTick, 50);
  }

  function stopAmlTimer() {
    clearInterval(window.amlTimer);
    window.amlTimer = null;
    const badge = document.getElementById('amlTimerBadge');
    if (badge) {
      badge.innerHTML = `⏸ Tour Paused (Stage ${window.currentAmlStep}/7)`;
    }
  }

  window.toggleAmlPlay = function() {
    const btn = document.getElementById('amlPlayPauseBtn');
    if (window.amlPlaying) {
      window.amlPlaying = false;
      stopAmlTimer();
      if (btn) {
        btn.innerHTML = '▶ Auto-Play Tour';
        btn.className = 'btn btn-sm btn-primary';
        btn.style.background = '';
        btn.style.color = '';
        btn.style.boxShadow = '';
      }
    } else {
      window.amlPlaying = true;
      startAmlTimer();
      if (btn) {
        btn.innerHTML = '<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#EF4444; margin-right:6px; animation:amlDotPulse 0.8s infinite;"></span> ⏸ Pause Tour';
        btn.className = 'btn btn-sm btn-secondary';
        btn.style.borderColor = 'var(--amber)';
        btn.style.color = 'var(--amber)';
      }
    }
  };

  window.prevAmlStep = function() {
    let prev = window.currentAmlStep - 1;
    if (prev < 1) prev = 7;
    window.amlElapsedMs = 0;
    window.setAmlStep(prev);
  };

  window.nextAmlStep = function() {
    let next = window.currentAmlStep + 1;
    if (next > 7) next = 1;
    window.amlElapsedMs = 0;
    window.setAmlStep(next);
  };

  window.resetAmlTour = function() {
    if (window.amlPlaying) window.toggleAmlPlay();
    window.amlElapsedMs = 0;
    const badge = document.getElementById('amlTimerBadge');
    if (badge) badge.style.display = 'none';
    const pbar = document.getElementById('amlStepProgressBar');
    if (pbar) pbar.style.width = '0%';
    const overallBar = document.getElementById('amlOverallProgressBar');
    if (overallBar) overallBar.style.width = '14.28%';
    const btn = document.getElementById('amlPlayPauseBtn');
    if (btn) btn.innerHTML = '▶ Auto-Play Tour';
    window.setAmlStep(1);
    window.closeAmlInspector();
  };

  window.changeAmlSpeed = function(val) {
    window.amlSpeed = parseFloat(val) || 1;
    if (window.amlPlaying) {
      window.amlElapsedMs = 0;
      updateAmlTimerDisplay();
    }
  };

  window.setAmlSubTab = function(subTab) {
    window.currentAmlSubTab = subTab;
    const tabs = ['talk', 'mechanics', 'tools', 'qa'];
    tabs.forEach(t => {
      const btn = document.getElementById('amlSubTabBtn-' + t);
      const pane = document.getElementById('amlSubContent-' + t);
      if (btn) {
        if (t === subTab) {
          btn.className = 'aml-tab-pill active';
        } else {
          btn.className = 'aml-tab-pill';
        }
      }
      if (pane) {
        pane.style.display = (t === subTab) ? 'block' : 'none';
      }
    });
  };

  // Inspect element
  window.inspectAmlElement = function(elemId) {
    const item = window.amlElementData[elemId];
    if (!item) return;

    const box = document.getElementById('amlInspectorBox');
    const badge = document.getElementById('amlInspBadge');
    const title = document.getElementById('amlInspTitle');
    const props = document.getElementById('amlInspProps');
    const src = document.getElementById('amlInspSource');
    const protege = document.getElementById('amlInspProtege');
    const cyp = document.getElementById('amlInspCypher');

    if (badge) badge.innerText = item.type;
    if (title) title.innerText = item.name;
    if (props) props.innerText = item.props;
    if (src) src.innerText = item.source;
    if (protege) protege.innerText = item.protege;
    if (cyp) cyp.innerText = item.cypher;

    if (box) {
      box.style.display = 'block';
      box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  };

  window.closeAmlInspector = function() {
    const box = document.getElementById('amlInspectorBox');
    if (box) box.style.display = 'none';
  };

  // Visual SVG Highlights depending on step
  function updateSvgHighlights(step) {
    const allZones = ['svgZoneStructured', 'svgZoneUnstructured', 'svgZoneTransform', 'svgZoneTools', 'svgZoneTopology', 'svgZoneOutputs'];
    
    // Set default opacities
    allZones.forEach(z => {
      const el = document.getElementById(z);
      if (el) el.setAttribute('opacity', '0.45');
    });

    // Reset all node pulses
    const allSvgNodes = document.querySelectorAll('.aml-node');
    allSvgNodes.forEach(n => {
      n.style.filter = 'none';
      n.style.transform = 'none';
    });

    const data = window.amlStepData[step];
    if (!data) return;

    // Highlight target zones
    if (data.highlightZones) {
      data.highlightZones.forEach(z => {
        const el = document.getElementById(z);
        if (el) el.setAttribute('opacity', '1');
      });
    }

    // Pulse active nodes
    if (data.activeNodes) {
      data.activeNodes.forEach(nId => {
        const el = document.getElementById(nId);
        if (el) {
          el.style.filter = (step === 6) ? 'url(#glowRed)' : 'url(#glowAmber)';
          el.style.transform = 'scale(1.04)';
        }
      });
    }

    // Circular ring special animation in Step 6
    const wire3 = document.getElementById('edgeWire3');
    if (wire3) {
      if (step === 6) {
        wire3.setAttribute('stroke', '#F43F5E');
        wire3.setAttribute('stroke-width', '4');
        wire3.style.filter = 'url(#glowRed)';
      } else {
        wire3.setAttribute('stroke', '#F43F5E');
        wire3.setAttribute('stroke-width', '3');
        wire3.style.filter = 'none';
      }
    }
  }

  // Initializer
  window.amlWorkflowInit = function() {
    setAmlStep(window.currentAmlStep || 1);
  };

  // Trigger on DOM load if tab is active
  document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('archContent-aml-workflow')) {
      window.amlWorkflowInit();
    }
  });

})();
</script>
'''

print("get_aml_workflow_js prepared.")
