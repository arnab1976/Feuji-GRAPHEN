# -*- coding: utf-8 -*-
"""
Injects Tab: End-to-End Knowledge Graph Pipeline Matrix into index.html
1. Updates showArchTab in <head>
2. Adds nav pill button in section navigation pills
3. Inserts #archContent-pipeline-matrix before Tab 1
4. Inserts #pipeline-matrix-script before </body>
5. Verifies via node --check
"""
import sys
import os
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('scripts'))
from build_pipeline_matrix_content import get_pipeline_matrix_html
from build_pipeline_matrix_js import get_pipeline_matrix_js

matrix_html = get_pipeline_matrix_html()
matrix_js = get_pipeline_matrix_js()

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update showArchTab in <head>
new_show_arch = """window.showArchTab = function(tabName) {
      const tabs = ['aml-workflow', 'pipeline-matrix', 'pipeline', 'fintech', 'health', 'breakdown', 'techstack'];
      tabs.forEach(t => {
        const btn = document.getElementById('archTab-' + t);
        const content = document.getElementById('archContent-' + t);
        if (btn) {
          if (t === tabName) {
            btn.className = 'btn btn-sm btn-primary';
          } else {
            btn.className = 'btn btn-sm btn-secondary';
          }
        }
        if (content) {
          content.style.display = (t === tabName) ? 'block' : 'none';
        }
      });
      if (tabName === 'aml-workflow') {
        if (window.amlWorkflowInit) { window.amlWorkflowInit(); }
      } else if (tabName === 'pipeline-matrix') {
        if (window.matrixWorkflowInit) { window.matrixWorkflowInit(); }
      }
    };"""

html = re.sub(
    r'window\.showArchTab = function\(tabName\) \{.*?\};\s*(?=window\.getApiUrl|\s*<\/script>)',
    lambda m: new_show_arch + '\n\n',
    html,
    flags=re.DOTALL
)
print("Updated showArchTab in <head>.")

# 2. Add navigation button to pills
pill_btn = """          <button type="button" onclick="showArchTab('pipeline-matrix')" id="archTab-pipeline-matrix" class="btn btn-sm btn-secondary" style="padding:8px 18px; font-weight:700; border:1.5px solid #3DDC97; color:var(--tx-0);"><span style="display:inline-block; animation:pulse 1.8s infinite;">📊</span> End-to-End Pipeline Matrix</button>"""

if 'id="archTab-pipeline-matrix"' not in html:
    html = html.replace(
        'id="archTab-aml-modal-btn" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:800; background:linear-gradient(135deg, #FF9F0A 0%, #EA580C 100%); border:none; box-shadow:0 0 16px rgba(255,159,10,0.45); cursor:pointer;"><span style="font-size:14px; margin-right:4px;">⤢</span> Pop-up Large Window</button>',
        'id="archTab-aml-modal-btn" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:800; background:linear-gradient(135deg, #FF9F0A 0%, #EA580C 100%); border:none; box-shadow:0 0 16px rgba(255,159,10,0.45); cursor:pointer;"><span style="font-size:14px; margin-right:4px;">⤢</span> Pop-up Large Window</button>\n' + pill_btn
    )
    print("Added archTab-pipeline-matrix to navigation pills.")
else:
    print("archTab-pipeline-matrix already in navigation pills.")

# 3. Insert or update #archContent-pipeline-matrix
# Remove existing if any
html = re.sub(r'<!-- ==================== TAB: END-TO-END KNOWLEDGE GRAPH PIPELINE MATRIX ==================== -->.*?<!-- TAB 1: 10-STEP PIPELINE', '<!-- TAB 1: 10-STEP PIPELINE', html, flags=re.DOTALL)

tab1_marker = '<!-- TAB 1: 10-STEP PIPELINE'
tab1_idx = html.find(tab1_marker)
if tab1_idx == -1:
    print("ERROR: Could not find TAB 1 marker in index.html")
    sys.exit(1)

html = html[:tab1_idx] + matrix_html.strip() + '\n\n        ' + html[tab1_idx:]
print("Inserted archContent-pipeline-matrix before Tab 1.")

# 4. Insert or update #pipeline-matrix-script
html = re.sub(r'<script id="pipeline-matrix-script">.*?</script>\s*', '', html, flags=re.DOTALL)

# Locate right before closing </body>
target_body = '</body>'
body_idx = html.rfind(target_body)
if body_idx == -1:
    print("ERROR: Could not find closing </body> tag!")
    sys.exit(1)

html = html[:body_idx] + matrix_js.strip() + '\n\n' + html[body_idx:]
print("Inserted pipeline-matrix-script before </body>.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved updated index.html successfully!")

# 5. Node syntax verification
with open('temp_matrix_verify.js', 'w', encoding='utf-8') as tf:
    m = re.search(r'<script id="pipeline-matrix-script">(.*?)</script>', html, re.DOTALL)
    if m:
        tf.write(m.group(1))

res = subprocess.run(['node', '--check', 'temp_matrix_verify.js'], capture_output=True, text=True)
if os.path.exists('temp_matrix_verify.js'):
    os.remove('temp_matrix_verify.js')

if res.returncode == 0:
    print("[SUCCESS] node --check passed with exit code 0 for pipeline matrix script!")
else:
    print(f"[FAIL] Node check failed:\n{res.stderr}")
    sys.exit(1)
