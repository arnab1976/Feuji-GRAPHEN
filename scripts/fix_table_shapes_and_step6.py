# -*- coding: utf-8 -*-
"""
Full fix for:
1. Table stretching beyond window (stacks Input & Output tables vertically, word-wrap, overflow containment)
2. Step 6 Data Snapshots (places snapshot-aml-6 and snapshot-med-6 directly inside their cards below the 3 Deliverables)
"""

import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ---------------------------------------------------------------------------
# 1. CSS RESHAPE FOR TABLES & PREVENT OVERFLOW
# ---------------------------------------------------------------------------
old_css_marker = '/* ================= ENHANCED TABLE SNAPSHOTS & TECH STACKS ================= */'
if old_css_marker in html:
    css_start = html.find(old_css_marker)
    css_end = html.find('</style>', css_start)
    
    reshaped_css = '''/* ================= ENHANCED TABLE SNAPSHOTS & TECH STACKS ================= */
    .snapshot-panel {
      background: #070B14;
      border: 1.5px solid #23314E;
      border-radius: 10px;
      padding: 18px;
      margin-top: 18px;
      box-shadow: inset 0 0 30px rgba(0,0,0,0.65), 0 8px 24px rgba(0,0,0,0.35);
      animation: snapSlideDown 0.25s ease-out;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      overflow: hidden;
    }
    .snapshot-tech-bar {
      background: #080E1C;
      border: 1px solid #1E2D4A;
      border-radius: 8px;
      padding: 12px 14px;
      margin-bottom: 16px;
      width: 100%;
      box-sizing: border-box;
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
    
    /* VERTICAL STACKING: EACH TABLE GETS 100% WIDTH OF THE CARD WITHOUT OVERFLOW */
    .snapshot-tables-container {
      display: flex;
      flex-direction: column;
      gap: 16px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      margin-bottom: 16px;
    }
    .snapshot-table-box {
      background: #090E1A;
      border: 1px solid #1E293B;
      border-radius: 8px;
      padding: 14px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      overflow: hidden;
    }
    .snapshot-table-title {
      font-size: 12px;
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
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      overflow-x: auto;
      border-radius: 6px;
      border: 1px solid #1A253A;
      -webkit-overflow-scrolling: touch;
    }
    .snapshot-table {
      width: 100%;
      max-width: 100%;
      border-collapse: collapse;
      font-size: 11.5px;
      font-family: var(--mono, monospace);
      text-align: left;
      table-layout: auto;
    }
    .snapshot-table th {
      background: #0E1726;
      color: #00F0FF;
      padding: 8px 12px;
      font-weight: 700;
      border-bottom: 1px solid #23314E;
      position: sticky;
      top: 0;
      z-index: 2;
      font-size: 10.5px;
      letter-spacing: 0.5px;
      text-transform: uppercase;
      white-space: nowrap;
    }
    .snapshot-table.med th {
      color: #3DDC97;
    }
    .snapshot-table td {
      padding: 8px 12px;
      border-bottom: 1px solid #141E33;
      color: #CBD5E1;
      vertical-align: middle;
      line-height: 1.5;
      white-space: normal;
      word-break: break-word;
      overflow-wrap: break-word;
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
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 10px;
      font-weight: 700;
      white-space: nowrap;
    }
    .tag-cyan { background: rgba(0, 240, 255, 0.15); color: #00F0FF; border: 1px solid rgba(0, 240, 255, 0.3); }
    .tag-green { background: rgba(61, 220, 151, 0.15); color: #3DDC97; border: 1px solid rgba(61, 220, 151, 0.3); }
    .tag-amber { background: rgba(255, 159, 10, 0.15); color: #FF9F0A; border: 1px solid rgba(255, 159, 10, 0.3); }
    .tag-rose { background: rgba(255, 69, 58, 0.15); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.3); }
    .tag-purple { background: rgba(191, 90, 242, 0.15); color: #BF5AF2; border: 1px solid rgba(191, 90, 242, 0.3); }
    
    .snapshot-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      margin-bottom: 14px;
    }
    @media (max-width: 900px) {
      .snapshot-grid {
        grid-template-columns: 1fr;
      }
    }
    .snapshot-col-box {
      background: #090E1A;
      border: 1px solid #1E293B;
      border-radius: 8px;
      padding: 12px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      overflow: hidden;
    }
    .snapshot-col-box pre {
      margin: 0;
      background: #050811 !important;
      border: 1px solid #141E33;
      border-radius: 6px;
      padding: 12px;
      font-size: 11px;
      font-family: var(--mono, monospace);
      color: #94A3B8;
      max-height: 260px;
      overflow: auto;
      max-width: 100%;
      box-sizing: border-box;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .snapshot-graph-vis {
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 180px;
      background: #050811;
      border: 1px solid #141E33;
      border-radius: 6px;
      padding: 10px;
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
      overflow: hidden;
    }
    .snapshot-graph-vis svg {
      width: 100%;
      height: auto;
      max-height: 240px;
    }
    '''
    html = html[:css_start] + reshaped_css + html[css_end:]
    print("Updated CSS with vertically stacked, 100% width, non-overflowing table layout.")

# ---------------------------------------------------------------------------
# 2. EXTRACT AND RE-INSERT STEP 6 PANELS DIRECTLY INSIDE THEIR RESPECTIVE CARDS
# ---------------------------------------------------------------------------

# Locate current snapshot-aml-6
pos_aml6 = html.find('id="snapshot-aml-6"')
if pos_aml6 != -1:
    p_start_aml6 = html.rfind('<div', 0, pos_aml6)
    pos_foot_aml6 = html.find('snapshot-mechanics-footer', pos_aml6)
    pos_foot_end_aml6 = html.find('</div>', pos_foot_aml6)
    p_end_aml6 = html.find('</div>', pos_foot_end_aml6 + 6) + 6
    panel_aml_6_html = html[p_start_aml6:p_end_aml6]
    # Remove from old position
    html = html[:p_start_aml6] + html[p_end_aml6:]
    print(f"Extracted snapshot-aml-6 ({len(panel_aml_6_html)} chars) and removed from displaced location.")

# Locate current snapshot-med-6
pos_med6 = html.find('id="snapshot-med-6"')
if pos_med6 != -1:
    p_start_med6 = html.rfind('<div', 0, pos_med6)
    pos_foot_med6 = html.find('snapshot-mechanics-footer', pos_med6)
    pos_foot_end_med6 = html.find('</div>', pos_foot_med6)
    p_end_med6 = html.find('</div>', pos_foot_end_med6 + 6) + 6
    panel_med_6_html = html[p_start_med6:p_end_med6]
    # Remove from old position
    html = html[:p_start_med6] + html[p_end_med6:]
    print(f"Extracted snapshot-med-6 ({len(panel_med_6_html)} chars) and removed from displaced location.")

# Insert snapshot-aml-6 right inside AML Step 6 card after Deliverables grid
aml6_marker = 'Immediate Asset Recovery:</strong> Recommended freezing of 4 target accounts containing <strong>$3,840,000</strong> in active liquidity, mitigating regulatory penalty exposure up to $50M+.</li>'
pos_marker_aml6 = html.find(aml6_marker)
if pos_marker_aml6 != -1:
    # Find the closing </div> of Deliverable 3, then closing </div> of Deliverables grid
    d3_close = html.find('</div>', pos_marker_aml6)
    grid_close = html.find('</div>', d3_close + 6)
    insert_pos_aml6 = grid_close + 6
    html = html[:insert_pos_aml6] + '\n\n                  ' + panel_aml_6_html + html[insert_pos_aml6:]
    print("Successfully injected snapshot-aml-6 directly inside AML Step 6 card!")
else:
    print("ERROR: Could not find AML Step 6 marker!")

# Insert snapshot-med-6 right inside Med Step 6 card after Deliverables grid
med6_marker = 'Hit-to-lead timeline compressed from 18 months to <strong>6 weeks</strong>; $2.8B global addressable market.</li>'
pos_marker_med6 = html.find(med6_marker)
if pos_marker_med6 != -1:
    d3_close_med = html.find('</div>', pos_marker_med6)
    grid_close_med = html.find('</div>', d3_close_med + 6)
    insert_pos_med6 = grid_close_med + 6
    html = html[:insert_pos_med6] + '\n\n                  ' + panel_med_6_html + html[insert_pos_med6:]
    print("Successfully injected snapshot-med-6 directly inside Med Step 6 card!")
else:
    print("ERROR: Could not find Med Step 6 marker!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully updated!")
