# -*- coding: utf-8 -*-
"""
Deploys enhanced Data Snapshots with:
1. Required Tools & Tech Stacks strip (Neo4j, Protégé, ChromaDB, spaCy, Cypher, etc.)
2. Formatted Input Data Snapshot (interactive table format)
3. Formatted Output Data Snapshot (interactive table format)
4. Raw Data Payload / Cypher Code (JSON / Cypher snippet)
5. Visual Graph Representation (SVG diagram)
6. Engine mechanics summary
for all 6 steps in Financial AML and all 6 steps in Biomedical Drug Discovery.
"""

import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

print("Starting Enhanced Table Snapshots & Tech Stack Deployment...")

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# CSS Enhancements for Table Snapshots & Tech Stack
enhanced_css = '''
    /* ================= ENHANCED TABLE SNAPSHOTS & TECH STACKS ================= */
    .snapshot-tech-bar {
      background: #080E1C;
      border: 1px solid #1E2D4A;
      border-radius: 8px;
      padding: 12px 14px;
      margin-bottom: 16px;
    }
    .snapshot-tech-bar-title {
      font-size: 11px;
      font-weight: 800;
      color: #94A3B8;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      margin-bottom: 8px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .snapshot-tech-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .snapshot-tech-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: #0D172B;
      border: 1px solid #243556;
      border-radius: 6px;
      padding: 5px 11px;
      font-size: 11px;
      color: #E2E8F0;
      line-height: 1.4;
    }
    .snapshot-tech-pill strong {
      color: #00F0FF;
    }
    .snapshot-tech-pill.med strong {
      color: #3DDC97;
    }
    .snapshot-tables-container {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-bottom: 16px;
    }
    @media (max-width: 1024px) {
      .snapshot-tables-container {
        grid-template-columns: 1fr;
      }
    }
    .snapshot-table-box {
      background: #090E1A;
      border: 1px solid #1E293B;
      border-radius: 8px;
      padding: 12px;
      display: flex;
      flex-direction: column;
    }
    .snapshot-table-title {
      font-size: 11.5px;
      font-weight: 800;
      color: #00F0FF;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .snapshot-table-title.med {
      color: #3DDC97;
    }
    .snapshot-table-wrapper {
      overflow-x: auto;
      max-height: 280px;
      border-radius: 6px;
      border: 1px solid #1A253A;
    }
    .snapshot-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 11px;
      font-family: var(--mono, monospace);
      text-align: left;
    }
    .snapshot-table th {
      background: #0E1726;
      color: #00F0FF;
      padding: 7px 10px;
      font-weight: 700;
      border-bottom: 1px solid #23314E;
      position: sticky;
      top: 0;
      z-index: 2;
      font-size: 10px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .snapshot-table.med th {
      color: #3DDC97;
    }
    .snapshot-table td {
      padding: 7px 10px;
      border-bottom: 1px solid #141E33;
      color: #CBD5E1;
      vertical-align: middle;
      line-height: 1.4;
    }
    .snapshot-table tr:nth-child(even) td {
      background: rgba(255, 255, 255, 0.015);
    }
    .snapshot-table tr:hover td {
      background: rgba(0, 240, 255, 0.05);
    }
    .snapshot-table.med tr:hover td {
      background: rgba(61, 220, 151, 0.05);
    }
    .table-tag {
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-size: 9.5px;
      font-weight: 700;
      white-space: nowrap;
    }
    .tag-cyan { background: rgba(0, 240, 255, 0.15); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.3); }
    .tag-green { background: rgba(61, 220, 151, 0.15); color: #3DDC97; border: 1px solid rgba(61, 220, 151, 0.3); }
    .tag-amber { background: rgba(255, 159, 10, 0.15); color: #FF9F0A; border: 1px solid rgba(255, 159, 10, 0.3); }
    .tag-rose { background: rgba(255, 69, 58, 0.15); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.3); }
    .tag-purple { background: rgba(191, 90, 242, 0.15); color: #BF5AF2; border: 1px solid rgba(191, 90, 242, 0.3); }
'''

# Check if enhanced CSS already exists, if not add it
if '.snapshot-tech-bar' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>\n' + enhanced_css + '\n</style>\n' + html[head_pos:]
        print("Injected Enhanced Table CSS into <head>.")

# We extract original visual graph SVGs and payloads from inject_snapshots_into_cards.py
with open('scripts/inject_snapshots_into_cards.py', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.splitlines()
code_aml = "\n".join(lines[26:576])
code_med = "\n".join(lines[629:995])

scope = {}
exec(code_aml, scope)
exec(code_med, scope)

# Helper to extract existing SVG from panel
def extract_svg(panel_html):
    m = re.search(r'(<svg[\s\S]*?</svg>)', panel_html)
    return m.group(1) if m else ''

# Helper to extract existing pre / code payload from panel
def extract_pre(panel_html):
    m = re.search(r'(<pre[\s\S]*?</pre>)', panel_html)
    return m.group(1) if m else ''

def extract_footer(panel_html):
    m = re.search(r'<div class="snapshot-mechanics-footer[^"]*">([\s\S]*?)</div>', panel_html)
    return m.group(1).strip() if m else ''

print("Loaded base panels and helper extractors.")
