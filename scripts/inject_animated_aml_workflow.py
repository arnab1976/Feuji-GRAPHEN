# -*- coding: utf-8 -*-
"""
Injects the comprehensive, interactive, animated AML Knowledge Graph Workflow into index.html
Fulfills all requirements:
1. Multi-source structured mapping via mapping keys (KYC, Core Banking, SWIFT, OFAC)
2. Multi-source unstructured mapping (SAR narratives, Loan Apps, Emails)
3. Transformation pipeline from unstructured to structured (Regex, spaCy NER, LLM JSON Schema)
4. Canonical Key Binding (extacting canonical keys to create [:EVIDENCE_FOR] and [:MENTIONS])
5. Role of Protégé, ChromaDB, Neo4j, Cypher, and Hybrid Graph-RAG
6. Pattern recognition (3-6 hop circular wire layering ring, shared device mule hub, PageRank)
7. Concrete executive deliverables ($14.25M exposure, 1-click SAR)
8. Interview-ready simple explanations, talk tracks, and defense Q&A at every step.
"""
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update window.showArchTab to include 'aml-workflow' as the first tab
old_show_tab = """        window.showArchTab = function(tabName) {
      const tabs = ['pipeline', 'fintech', 'health', 'breakdown', 'techstack'];"""

new_show_tab = """        window.showArchTab = function(tabName) {
      const tabs = ['aml-workflow', 'pipeline', 'fintech', 'health', 'breakdown', 'techstack'];"""

if old_show_tab in html:
    html = html.replace(old_show_tab, new_show_tab)
    print("Updated window.showArchTab array.")

# Ensure showArchTab calls amlWorkflowInit if tab is aml-workflow
if "if (tabName === 'aml-workflow' && window.amlWorkflowInit)" not in html:
    html = html.replace(
        "content.style.display = (t === tabName) ? 'block' : 'none';\n        }\n      });",
        "content.style.display = (t === tabName) ? 'block' : 'none';\n        }\n      });\n      if (tabName === 'aml-workflow' && window.amlWorkflowInit) { window.amlWorkflowInit(); }"
    )
    print("Added amlWorkflowInit hook in showArchTab.")

# 2. Update navigation pills in view-arch
old_pills = """        <!-- Section Navigation Pills -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" onclick="showArchTab('pipeline')" id="archTab-pipeline" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:600;">📌 10-Step Master Pipeline Diagram</button>"""

new_pills = """        <!-- Section Navigation Pills -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" onclick="showArchTab('aml-workflow')" id="archTab-aml-workflow" class="btn btn-sm btn-primary" style="padding:8px 18px; font-weight:700; background:linear-gradient(135deg, rgba(255,159,10,0.3) 0%, rgba(96,165,250,0.3) 100%); border:1.5px solid var(--amber); color:var(--tx-0); box-shadow:0 0 16px rgba(255,159,10,0.35);"><span style="display:inline-block; animation:pulse 1.8s infinite;">⚡</span> Interactive AML Workflow (Interview-Ready)</button>
          <button type="button" onclick="showArchTab('pipeline')" id="archTab-pipeline" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">📌 10-Step Master Pipeline Diagram</button>"""

if old_pills in html:
    html = html.replace(old_pills, new_pills)
    print("Added Animated AML Workflow navigation pill.")

# Also add jump banner to archContent-pipeline and archContent-fintech
banner_html = """            <!-- HERO JUMP TO ANIMATED AML SIMULATOR -->
            <div style="background:linear-gradient(135deg, rgba(255,159,10,0.14), rgba(96,165,250,0.14)); border:1.5px solid var(--amber); border-radius:10px; padding:12px 18px; margin-bottom:20px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
              <div>
                <strong style="color:var(--amber); font-size:13.5px;">⚡ Looking for the Interactive Animated Workflow & Interview Talk-Track?</strong>
                <p style="color:var(--tx-2); font-size:12px; margin:2px 0 0;">Interactive animated simulation of multi-source structured/unstructured mapping, transformation, key binding, Protégé/ChromaDB/Neo4j/Cypher roles, and circular layering detection.</p>
              </div>
              <button type="button" onclick="showArchTab('aml-workflow')" class="btn btn-sm btn-primary" style="font-weight:700; background:var(--amber); color:#000; border:none; padding:7px 16px;">Launch Interactive AML Animation ➔</button>
            </div>"""

if 'id="archContent-pipeline"' in html and 'HERO JUMP TO ANIMATED AML SIMULATOR' not in html:
    html = html.replace(
        '<div id="archContent-pipeline" class="arch-tab-content">\n          <div style="background:var(--surface);',
        '<div id="archContent-pipeline" class="arch-tab-content">\n' + banner_html + '\n          <div style="background:var(--surface);'
    )
    print("Added jump banner in Pipeline tab.")

if 'id="archContent-fintech"' in html and 'HERO JUMP TO ANIMATED AML SIMULATOR' not in html:
    html = html.replace(
        '<div id="archContent-fintech" class="arch-tab-content" style="display:none;">\n          <div style="background:var(--surface);',
        '<div id="archContent-fintech" class="arch-tab-content" style="display:none;">\n' + banner_html + '\n          <div style="background:var(--surface);'
    )
    print("Added jump banner in Fintech tab.")

# 3. Add CSS for Animated AML Workflow
aml_css = """
<style id="aml-workflow-styles">
  /* Animated AML Workflow Styles */
  @keyframes pulseGlow {
    0%, 100% { filter: drop-shadow(0 0 6px rgba(255,159,10,0.7)); }
    50% { filter: drop-shadow(0 0 20px rgba(255,159,10,1)); }
  }
  @keyframes pulseBlue {
    0%, 100% { filter: drop-shadow(0 0 6px rgba(96,165,250,0.7)); }
    50% { filter: drop-shadow(0 0 20px rgba(96,165,250,1)); }
  }
  @keyframes pulseEmerald {
    0%, 100% { filter: drop-shadow(0 0 6px rgba(61,220,151,0.7)); }
    50% { filter: drop-shadow(0 0 20px rgba(61,220,151,1)); }
  }
  @keyframes pulsePurple {
    0%, 100% { filter: drop-shadow(0 0 6px rgba(168,85,247,0.7)); }
    50% { filter: drop-shadow(0 0 20px rgba(168,85,247,1)); }
  }
  @keyframes pulseRedAlert {
    0%, 100% { filter: drop-shadow(0 0 8px rgba(244,63,94,0.8)); transform: scale(1); }
    50% { filter: drop-shadow(0 0 28px rgba(244,63,94,1)); transform: scale(1.02); }
  }
  @keyframes dashFlow {
    from { stroke-dashoffset: 40; }
    to { stroke-dashoffset: 0; }
  }
  @keyframes ringTravel {
    0% { stroke-dashoffset: 120; }
    100% { stroke-dashoffset: 0; }
  }
  @keyframes progressTimer {
    from { width: 0%; }
    to { width: 100%; }
  }
  .aml-node {
    cursor: pointer;
    transition: transform 0.25s ease, filter 0.25s ease, opacity 0.3s ease;
  }
  .aml-node:hover {
    transform: scale(1.06);
    filter: brightness(1.25) drop-shadow(0 0 16px rgba(255,255,255,0.6));
  }
  .aml-edge {
    cursor: pointer;
    transition: stroke-width 0.25s ease, stroke 0.25s ease, opacity 0.3s ease;
  }
  .aml-edge:hover {
    stroke-width: 4 !important;
    filter: drop-shadow(0 0 10px #FF9F0A);
  }
  .aml-step-btn {
    background: var(--bg-2, #121824);
    border: 1px solid var(--line, #2E3B54);
    color: var(--tx-2, #94A3B8);
    padding: 8px 12px;
    border-radius: 8px;
    font-size: 11.5px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    gap: 6px;
    text-align: left;
    white-space: nowrap;
  }
  .aml-step-btn:hover {
    background: var(--surface, #1A2234);
    color: var(--tx-0, #FFF);
    border-color: var(--line-strong, #3A4763);
  }
  .aml-step-btn.active {
    background: linear-gradient(135deg, rgba(255,159,10,0.25), rgba(96,165,250,0.2));
    border-color: var(--amber, #FF9F0A);
    color: var(--amber, #FF9F0A);
    box-shadow: 0 0 12px rgba(255,159,10,0.35);
  }
  .aml-card-box {
    background: var(--bg-2, #121824);
    border: 1px solid var(--line-soft, #2A364F);
    border-radius: 10px;
    padding: 16px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.2);
  }
  .aml-badge {
    font-size: 10.5px;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }
  .aml-badge.amber { background: rgba(255,159,10,0.15); color: var(--amber, #FF9F0A); border: 1px solid rgba(255,159,10,0.3); }
  .aml-badge.blue { background: rgba(96,165,250,0.15); color: #60A5FA; border: 1px solid rgba(96,165,250,0.3); }
  .aml-badge.emerald { background: rgba(61,220,151,0.15); color: #3DDC97; border: 1px solid rgba(61,220,151,0.3); }
  .aml-badge.purple { background: rgba(168,85,247,0.15); color: #A855F7; border: 1px solid rgba(168,85,247,0.3); }
  .aml-badge.rose { background: rgba(244,63,94,0.15); color: #F43F5E; border: 1px solid rgba(244,63,94,0.3); }
  .aml-tab-pill {
    padding: 6px 14px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    background: transparent;
    color: var(--tx-2);
    border: 1px solid transparent;
    transition: all 0.2s;
  }
  .aml-tab-pill.active {
    background: var(--surface);
    color: var(--amber);
    border-color: var(--line-soft);
    box-shadow: 0 2px 8px rgba(0,0,0,0.25);
  }
</style>
"""

if '<style id="aml-workflow-styles">' not in html:
    html = html.replace('</head>', aml_css + '\n</head>')
    print("Injected aml-workflow CSS.")
else:
    # replace existing
    html = re.sub(r'<style id="aml-workflow-styles">.*?</style>', aml_css, html, flags=re.DOTALL)
    print("Updated aml-workflow CSS.")

# Save intermediate html
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated CSS and pills.")
