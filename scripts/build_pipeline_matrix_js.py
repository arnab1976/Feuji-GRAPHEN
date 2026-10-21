# -*- coding: utf-8 -*-
"""
JavaScript logic for Tab: End-to-End Knowledge Graph Pipeline Matrix
Handles the 7-stage animated interactive workflow simulator in Card 3.
"""

def get_pipeline_matrix_js():
    return '''
<script id="pipeline-matrix-script">
(function() {
  window.currentMatrixStep = 1;
  window.matrixPlaying = false;
  window.matrixTimer = null;
  window.matrixSpeed = 1;
  window.matrixElapsedMs = 0;

  window.matrixStepData = {
    1: {
      badge: "STAGE 1 DEEP-DIVE",
      title: "Stage 1: Semantic Ontology & Rule Governance",
      tool: "PROTÉGÉ 5.6 & OWL 2",
      badgeColor: "purple",
      input: "Banking regulatory guidelines (FATF 40 Recommendations, FinCEN CDD Rule), core banking entity catalogs, and transaction risk classification criteria.",
      process: "Formulates the formal class taxonomy (Account as a subclass of FinancialAsset; PEP as a subclass of Customer). Enforces Domain/Range constraints so edges cannot connect invalid types. Uses HermiT automated reasoning to infer high-risk classifications without hardcoded SQL IF/ELSE rules.",
      output: "Serialized W3C semantic ontology contract file (aml_ontology.ttl / .owl) that establishes the inviolable schema rules before any database code executes.",
      toolContrib: "Protégé is the irreplaceable architectural blueprint. Prevents corrupted schema creation across teams, eliminates data swamps, and guarantees mathematical consistency.",
      visualText: "🎙️ What to say to the Panel: \\"We start with Protégé because Neo4j is schema-optional by default. Protégé establishes our constitutional vocabulary, defines class hierarchies, and enforces that wire transfers can only happen between accounts, eliminating corrupt data before ingestion.\\""
    },
    2: {
      badge: "STAGE 2 DEEP-DIVE",
      title: "Stage 2: Structured Data Manipulation & Ingestion",
      tool: "KAFKA, DEBEZIUM & SQL",
      badgeColor: "blue",
      input: "Relational database tables: Oracle KYC customer profiles, PostgreSQL real-time account balances, Kafka SWIFT MT103 wire messages, and OFAC Sanctions CSV lists.",
      process: "Ingests tabular records directly as native network objects without executing expensive Cartesian multi-table joins. Table rows become discrete Nodes (Customer with tax_id, Account with iban). Foreign key matches become directional Edges (:Customer)-[:OWNS]->(:Account) and (:Account)-[:TRANSFERRED]->(:Account). Relational columns become node/edge properties.",
      output: "Discrete, validated graph entities and directional transaction edges staged and indexed inside graph memory.",
      toolContrib: "Kafka & Debezium CDC stream transactions in real time; Python maps relational foreign keys into native graph relationship pointers without memory bloat.",
      visualText: "🎙️ What to say to the Panel: \\"In enterprise AML, banking records live in separate relational silos. Rather than performing exponential SQL multi-table joins that crash on high-velocity feeds, we convert entities into nodes and transaction events into directional edges.\\""
    },
    3: {
      badge: "STAGE 3 DEEP-DIVE",
      title: "Stage 3: Unstructured Data Transformation",
      tool: "CHROMADB & SPACY NER",
      badgeColor: "amber",
      input: "Unstructured compliance documents: FinCEN Suspicious Activity Reports (SAR PDFs), commercial loan credit memos (DOCX), compliance investigator emails, and sanctions notices.",
      process: "Free-flowing text cannot fit into static table columns. Executes a 3-tier NLP pipeline: (1) ISO 7064 Mod-97 IBAN checksums and Tax ID RegEx; (2) spaCy Named Entity Recognition tagging Persons and Organizations; (3) LLM Pydantic JSON schema extracting structured triples. Chunks text into 500-token windows and computes dense 384-d vector embeddings.",
      output: "Extracted canonical identifiers (IBANs, Tax IDs), document chunk nodes (:DocumentChunk), entity triples, and ChromaDB vector collections.",
      toolContrib: "ChromaDB manages vector indexing for semantic similarity discovery (>0.82 cosine similarity); spaCy and LLMs parse free-flowing text into deterministic entities and canonical keys.",
      visualText: "🎙️ What to say to the Panel: \\"Documents have variable context, so we never force them into rigid table columns. We parse entities with spaCy, extract canonical identifiers like Tax IDs, and store text embeddings in ChromaDB to link related investigations semantically.\\""
    },
    4: {
      badge: "STAGE 4 DEEP-DIVE",
      title: "Stage 4: Binding Structured & Unstructured Data",
      tool: "CYPHER MERGE RESOLUTION",
      badgeColor: "emerald",
      input: "Structured core banking nodes from Stage 2 + Extracted canonical identifiers and document chunk nodes from Stage 3.",
      process: "Resolves shared canonical business keys (e.g., Tax ID 99-887711 or IBAN DE89370001 mentioned in a PDF narrative). Executes Cypher MERGE queries to attach the document chunk node directly to the banking nodes via [:EVIDENCE_FOR] and [:CORROBORATES] relationship edges. Creates full evidentiary audit lineage.",
      output: "Unified Knowledge Graph fabric where high-velocity transaction records and legal documentary narratives are physically interconnected.",
      toolContrib: "Cypher MERGE provides idempotent graph binding that searches for matching keys and attaches evidence relationships without duplicate records or corrupted topology.",
      visualText: "🎙️ What to say to the Panel: \\"This is how we bridge both worlds. When our NLP pipeline extracts an IBAN or Tax ID from a compliance narrative, Cypher MERGE attaches that document chunk directly to the existing account node, giving every risk flag complete legal provenance.\\""
    },
    5: {
      badge: "STAGE 5 DEEP-DIVE",
      title: "Stage 5: In-Memory Storage & Topology Hosting",
      tool: "NEO4J LPG ENGINE (RAM)",
      badgeColor: "cyan",
      input: "Connected graph nodes, edges, labels, and properties across all structured and unstructured modalities.",
      process: "Stores the graph persistently on disk while caching active relationship networks in RAM. Utilizes Index-Free Adjacency (IFA): each node holds direct physical 64-bit RAM pointers to its adjacent relationship records. Graph traversal is simply dereferencing memory pointers in O(1) constant time, completely bypassing index scans.",
      output: "High-performance operational graph database running in RAM with ACID transactional durability on disk.",
      toolContrib: "Neo4j is the physical engine. Its Index-Free Adjacency in RAM allows deep graph traversals to execute in milliseconds regardless of overall database size.",
      visualText: "🎙️ What to say to the Panel: \\"Relational databases index records; Neo4j indexes connections. Because Neo4j uses Index-Free Adjacency, following a wire transfer path requires simple memory pointer dereferencing in O(1) constant time, not repeated B-tree index lookups.\\""
    },
    6: {
      badge: "STAGE 6 DEEP-DIVE",
      title: "Stage 6: Topological Pattern Recognition (Hopping)",
      tool: "CYPHER TRAVERSAL & GDS",
      badgeColor: "rose",
      input: "Unified accounts, customers, mobile devices, and wire transactions hosted in Neo4j RAM.",
      process: "Launderers use multi-stage layering to hide money trails. Executes Cypher variable-length path traversal across sequential edge memory pointers: Hop 1 (German Account -> Swiss Account: $4.50M) ➔ Hop 2 (Swiss Account -> Cyprus Account: $4.48M) ➔ Hop 3 (Cyprus Account -> Back to German Account: $4.46M). Detects circular layering cycles and shared device hubs (multiple users logging in from one mobile MAC address).",
      output: "Flagged fraud subgraphs, isolated syndicate accounts, and quantified circular financial exposure ($14.25M loop).",
      toolContrib: "Cypher Pattern Matching Engine and Neo4j Graph Data Science (GDS) execute multi-hop variable path recognition (*3..5 hops) in single-digit milliseconds, which times out or crashes in relational SQL.",
      visualText: "🎙️ What to say to the Panel: \\"Hopping is stepping across sequential edge pointers. Cypher searches paths between 3 and 5 hops away and finds our $14.25M circular laundering ring in under 10 milliseconds, which would require impossible recursive SQL CTEs.\\""
    },
    7: {
      badge: "STAGE 7 DEEP-DIVE",
      title: "Stage 7: Hybrid Graph-RAG & Compliance Filing",
      tool: "HYBRID GRAPH-RAG & LLM",
      badgeColor: "emerald",
      input: "Flagged multi-hop fraud subgraph from Neo4j (accounts, amounts, timestamps) + Contextual evidence text retrieved from ChromaDB.",
      process: "Traditional Vector RAG searches fuzzy text and frequently hallucinates financial sums. Hybrid Graph-RAG pairs the exact mathematical graph truth from Neo4j with verbatim narrative quotes from ChromaDB. Feeds structured context to an LLM restricted to verified facts, generating the official FinCEN Form 111 XML payload and executive brief.",
      output: "Programmatic FinCEN Form 111 XML filing package, auditable $14.25M exposure brief, and zero-hallucination executive report.",
      toolContrib: "Hybrid Graph-RAG combines the structural precision of Neo4j with the semantic breadth of ChromaDB, delivering complete auditability and zero hallucination for executive leadership.",
      visualText: "🎙️ What to say to the Panel: \\"We don't give management fuzzy summaries; we give them $14.25M in mathematically verified exposure, verbatim evidence citations, and a 1-click filed FinCEN Form 111 SAR with complete audit provenance.\\""
    }
  };

  // Switch Active Matrix Step
  window.setMatrixStep = function(stepNum) {
    if (stepNum < 1 || stepNum > 7) return;
    window.currentMatrixStep = stepNum;

    // 1. Update Step Buttons
    for (let i = 1; i <= 7; i++) {
      const btn = document.getElementById('matrixStepBtn-' + i);
      if (btn) {
        if (i === stepNum) {
          btn.className = 'aml-step-btn active';
          const badge = btn.querySelector('span:first-child');
          if (badge) { badge.style.background = '#2DD4D4'; badge.style.color = '#000'; }
        } else {
          btn.className = 'aml-step-btn';
          const badge = btn.querySelector('span:first-child');
          if (badge) { badge.style.background = 'var(--line-strong)'; badge.style.color = '#FFF'; }
        }
      }
    }

    // 2. Update Progress Bar
    const overallBar = document.getElementById('matrixOverallProgressBar');
    if (overallBar) {
      overallBar.style.width = (stepNum / 7 * 100) + '%';
    }
    const lblProg = document.getElementById('matrixProgressStepLabel');
    if (lblProg) lblProg.innerText = `Stage ${stepNum} of 7`;
    const lblPct = document.getElementById('matrixProgressPercent');
    if (lblPct) lblPct.innerText = `${Math.round(stepNum / 7 * 100)}% Complete`;

    // 3. Update Inspector
    const data = window.matrixStepData[stepNum];
    if (data) {
      const stageInd = document.getElementById('matrixStageIndicator');
      if (stageInd) stageInd.innerText = `${data.title.replace('Stage ' + stepNum + ': ', '')}`;

      const b = document.getElementById('matrixInspBadge');
      if (b) {
        b.className = `aml-badge ${data.badgeColor}`;
        b.innerText = data.badge;
      }
      const t = document.getElementById('matrixInspTitle');
      if (t) t.innerText = data.title;
      const tb = document.getElementById('matrixInspToolBadge');
      if (tb) {
        tb.className = `aml-badge ${data.badgeColor}`;
        tb.innerText = data.tool;
      }

      const inp = document.getElementById('matrixInspInput');
      if (inp) inp.innerText = data.input;
      const prc = document.getElementById('matrixInspProcess');
      if (prc) prc.innerText = data.process;
      const out = document.getElementById('matrixInspOutput');
      if (out) out.innerText = data.output;
      const tc = document.getElementById('matrixInspTool');
      if (tc) tc.innerText = data.toolContrib;
      const vt = document.getElementById('matrixInspVisualText');
      if (vt) vt.innerText = data.visualText;
    }

    // 4. Update SVG Visual Elements
    for (let i = 1; i <= 7; i++) {
      const rect = document.getElementById('svgMatrixRect-' + i);
      const circle = document.getElementById('svgMatrixCircle-' + i);
      const num = document.getElementById('svgMatrixNum-' + i);
      const edge = document.getElementById('svgMatrixEdge-' + i);

      if (rect) {
        if (i === stepNum) {
          rect.setAttribute('stroke', '#2DD4D4');
          rect.setAttribute('stroke-width', '2.5');
          rect.setAttribute('filter', 'url(#matrixFilterActive)');
          if (circle) circle.setAttribute('fill', '#2DD4D4');
          if (num) num.setAttribute('fill', '#000');
        } else {
          rect.setAttribute('stroke', '#334155');
          rect.setAttribute('stroke-width', '1.5');
          rect.removeAttribute('filter');
          if (circle) circle.setAttribute('fill', '#1E293B');
          if (num) num.setAttribute('fill', '#FFF');
        }
      }

      if (edge) {
        if (i < stepNum) {
          edge.setAttribute('stroke', '#38BDF8');
          edge.setAttribute('stroke-width', '2.5');
          edge.setAttribute('stroke-dasharray', '6 4');
          edge.classList.add('aml-flowing-edge');
        } else if (i === stepNum) {
          edge.setAttribute('stroke', '#2DD4D4');
          edge.setAttribute('stroke-width', '2.5');
          edge.setAttribute('stroke-dasharray', '6 4');
          edge.classList.add('aml-flowing-edge');
        } else {
          edge.setAttribute('stroke', '#334155');
          edge.setAttribute('stroke-width', '2');
          edge.removeAttribute('stroke-dasharray');
          edge.classList.remove('aml-flowing-edge');
        }
      }
    }
  };

  function updateMatrixTimerDisplay() {
    const badge = document.getElementById('matrixTimerBadge');
    const pbar = document.getElementById('matrixStepProgressBar');
    const overallBar = document.getElementById('matrixOverallProgressBar');

    const totalMs = 7000 / (window.matrixSpeed || 1);
    const remainingSec = Math.max(0, (totalMs - window.matrixElapsedMs) / 1000).toFixed(1);
    const stepPct = Math.min(100, (window.matrixElapsedMs / totalMs) * 100);

    if (badge) {
      badge.style.display = 'inline-flex';
      badge.innerHTML = `<span style="display:inline-block; width:7px; height:7px; border-radius:50%; background:#2DD4D4; animation:amlDotPulse 0.8s infinite;"></span> Auto-advancing in <strong>${remainingSec}s</strong>`;
    }
    if (pbar) {
      pbar.style.width = stepPct + '%';
    }
    if (overallBar) {
      const overallPct = (((window.currentMatrixStep - 1) + (stepPct / 100)) / 7) * 100;
      overallBar.style.width = overallPct + '%';
    }
  }

  function matrixTick() {
    if (!window.matrixPlaying) return;
    window.matrixElapsedMs += 50;
    const totalMs = 7000 / (window.matrixSpeed || 1);
    updateMatrixTimerDisplay();

    if (window.matrixElapsedMs >= totalMs) {
      window.matrixElapsedMs = 0;
      window.nextMatrixStep();
    }
  }

  function startMatrixTimer() {
    clearInterval(window.matrixTimer);
    window.matrixElapsedMs = 0;
    updateMatrixTimerDisplay();
    window.matrixTimer = setInterval(matrixTick, 50);
  }

  function stopMatrixTimer() {
    clearInterval(window.matrixTimer);
    window.matrixTimer = null;
    const badge = document.getElementById('matrixTimerBadge');
    if (badge) {
      badge.innerHTML = `⏸ Tour Paused (Stage ${window.currentMatrixStep}/7)`;
    }
  }

  window.toggleMatrixPlay = function() {
    const btn = document.getElementById('matrixPlayPauseBtn');
    if (window.matrixPlaying) {
      window.matrixPlaying = false;
      stopMatrixTimer();
      if (btn) {
        btn.innerHTML = '▶ Auto-Play Tour';
        btn.className = 'btn btn-sm btn-primary';
        btn.style.background = 'linear-gradient(135deg, #2DD4D4 0%, #0284C7 100%)';
        btn.style.color = '#000';
      }
    } else {
      window.matrixPlaying = true;
      startMatrixTimer();
      if (btn) {
        btn.innerHTML = '<span style="display:inline-block; width:8px; height:8px; border-radius:50%; background:#EF4444; margin-right:6px; animation:amlDotPulse 0.8s infinite;"></span> ⏸ Pause Tour';
        btn.className = 'btn btn-sm btn-secondary';
        btn.style.borderColor = '#2DD4D4';
        btn.style.color = '#2DD4D4';
        btn.style.background = 'transparent';
      }
    }
  };

  window.prevMatrixStep = function() {
    let prev = window.currentMatrixStep - 1;
    if (prev < 1) prev = 7;
    window.matrixElapsedMs = 0;
    window.setMatrixStep(prev);
  };

  window.nextMatrixStep = function() {
    let next = window.currentMatrixStep + 1;
    if (next > 7) next = 1;
    window.matrixElapsedMs = 0;
    window.setMatrixStep(next);
  };

  window.resetMatrixTour = function() {
    if (window.matrixPlaying) window.toggleMatrixPlay();
    window.matrixElapsedMs = 0;
    const badge = document.getElementById('matrixTimerBadge');
    if (badge) badge.style.display = 'none';
    const pbar = document.getElementById('matrixStepProgressBar');
    if (pbar) pbar.style.width = '0%';
    const overallBar = document.getElementById('matrixOverallProgressBar');
    if (overallBar) overallBar.style.width = '14.28%';
    const btn = document.getElementById('matrixPlayPauseBtn');
    if (btn) btn.innerHTML = '▶ Auto-Play Tour';
    window.setMatrixStep(1);
  };

  window.changeMatrixSpeed = function(val) {
    window.matrixSpeed = parseFloat(val) || 1;
    if (window.matrixPlaying) {
      window.matrixElapsedMs = 0;
      updateMatrixTimerDisplay();
    }
  };

  window.matrixWorkflowInit = function() {
    window.setMatrixStep(window.currentMatrixStep || 1);
  };

  document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('archContent-pipeline-matrix')) {
      window.matrixWorkflowInit();
    }
  });

})();
</script>
'''
