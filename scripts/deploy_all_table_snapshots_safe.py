# -*- coding: utf-8 -*-
"""
Safe, deterministic deployment of all 12 enhanced data snapshot panels.
Replaces each of the 12 panels by exact index boundary in reverse order.
Includes:
1. Tech Stack Bar (Neo4j, Protégé, ChromaDB, spaCy, Cypher, etc.)
2. Formatted Input Data Snapshot Table (with tags, columns, rows)
3. Formatted Output Data Snapshot Table (with tags, relationships, joins)
4. Raw Data Payload / Cypher Query (JSON / Cypher snippet)
5. Visual Graph SVG Diagram
6. Mechanics Footer
"""

import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

print("Starting deterministic deployment of all 12 table snapshots...")

with open('scripts/build_all_enhanced_panels.py', 'r', encoding='utf-8') as f:
    builder_code = f.read()

# Execute builder script in scope to get definitions
scope = {}
exec(builder_code, scope)

build_panel = scope['build_panel']
extract_svg = scope['extract_svg']
extract_pre = scope['extract_pre']
extract_footer = scope['extract_footer']
scope_orig = scope['scope']

aml_panels_data = scope['aml_panels_data']
med_panels_data = scope['med_panels_data']

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Enhanced CSS
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

if '.snapshot-tech-bar' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>\n' + enhanced_css + '\n</style>\n' + html[head_pos:]
        print("Injected Enhanced CSS into <head>.")

# 2. Locate all 12 panels in html and compute their exact [start, end] slices
panel_replacements = []

# Collect AML panels (1 to 6)
for step_num, title, fmt, tech, in_t, out_t, raw_title in aml_panels_data:
    pid = f"snapshot-aml-{step_num}"
    pos = html.find(f'id="{pid}"')
    if pos == -1:
        print(f"ERROR: Could not find {pid} in html")
        continue
    p_start = html.rfind('<div', 0, pos)
    pos_foot = html.find('snapshot-mechanics-footer', pos)
    pos_foot_end = html.find('</div>', pos_foot)
    p_end = html.find('</div>', pos_foot_end + 6) + 6
    
    base_panel = scope_orig[f'panel_aml_{step_num}']
    svg_code = extract_svg(base_panel)
    pre_code = extract_pre(base_panel)
    footer_text = extract_footer(base_panel)
    
    new_panel = build_panel(pid, title, fmt, tech, in_t, out_t, pre_code, raw_title, svg_code, footer_text, is_med=False)
    panel_replacements.append((p_start, p_end, pid, new_panel.strip()))

# Collect Med panels (1 to 6)
for step_num, title, fmt, tech, in_t, out_t, raw_title in med_panels_data:
    pid = f"snapshot-med-{step_num}"
    pos = html.find(f'id="{pid}"')
    if pos == -1:
        print(f"ERROR: Could not find {pid} in html")
        continue
    p_start = html.rfind('<div', 0, pos)
    pos_foot = html.find('snapshot-mechanics-footer', pos)
    pos_foot_end = html.find('</div>', pos_foot)
    p_end = html.find('</div>', pos_foot_end + 6) + 6
    
    base_panel = scope_orig[f'panel_med_{step_num}']
    svg_code = extract_svg(base_panel)
    pre_code = extract_pre(base_panel)
    footer_text = extract_footer(base_panel)
    
    new_panel = build_panel(pid, title, fmt, tech, in_t, out_t, pre_code, raw_title, svg_code, footer_text, is_med=True)
    panel_replacements.append((p_start, p_end, pid, new_panel.strip()))

print(f"Total panels identified for replacement: {len(panel_replacements)}")

# Sort by start position in descending order (replace from bottom of document upwards)
panel_replacements.sort(key=lambda x: x[0], reverse=True)

# Replace each panel
for p_start, p_end, pid, new_code in panel_replacements:
    html = html[:p_start] + new_code + html[p_end:]
    print(f"Successfully replaced {pid} at range [{p_start}:{p_end}].")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully updated with all 12 enhanced Table Snapshots & Tech Stacks!")
