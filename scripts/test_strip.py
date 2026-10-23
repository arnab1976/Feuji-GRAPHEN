# -*- coding: utf-8 -*-
"""
Test generation of rich table data snapshots and tech stack badges for Step 1 AML.
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

tech_strip_aml_1 = '''
<div class="snapshot-tech-bar">
  <div class="snapshot-tech-bar-title">🛠️ REQUIRED TOOLS & TECH STACK FOR THIS STEP:</div>
  <div class="snapshot-tech-pills">
    <div class="snapshot-tech-pill"><span>🔍</span><strong>spaCy & GLiNER:</strong> Domain NER for extracting Person, Organization, Shell Company, and Jurisdiction</div>
    <div class="snapshot-tech-pill"><span>🔮</span><strong>ChromaDB:</strong> Dense 384-dimensional vector embeddings & semantic cosine similarity (>0.84)</div>
    <div class="snapshot-tech-pill"><span>🏛️</span><strong>Protégé & OWL 2:</strong> FIBO Financial Ontological classification & semantic entity taxonomy</div>
    <div class="snapshot-tech-pill"><span>⚡</span><strong>FastCoref / LLM:</strong> Cross-document coreference resolution for anonymous shell entities</div>
  </div>
</div>
'''

print("Tech strip length:", len(tech_strip_aml_1))
