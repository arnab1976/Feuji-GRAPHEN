# -*- coding: utf-8 -*-
"""
Deploy AML Workflow Final:
1. Embeds the full interactive SVG canvas directly in #archContent-aml-workflow (in-page tab).
2. Appends #amlModalOverlay as a direct child of <body> right before </body></html>.
3. Wires reparenting logic: openAmlModal() moves #amlWorkflowMainContainer into #amlModalBody;
   closeAmlModal() moves it back to #archContent-aml-workflow.
4. Auto-Play, progress bars, countdown timer badge, and animations work seamlessly in both views.
5. Verifies via node --check.
"""
import sys
import os
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load build_aml_workflow_content.py
with open('scripts/build_aml_workflow_content.py', 'r', encoding='utf-8') as f:
    content_raw = f.read()

# Extract CSS
css_match = re.search(r'(<style id="aml-workflow-modal-styles">.*?</style>)', content_raw, re.DOTALL)
if not css_match:
    print("ERROR: Could not find CSS block in build_aml_workflow_content.py")
    sys.exit(1)
css_block = css_match.group(1)

# Ensure .aml-modal-card uses 100% width and height within overlay
css_block = css_block.replace(
    'width: 98vw;\n            height: 96vh;',
    'width: calc(100vw - 28px);\n            height: calc(100vh - 28px);'
)

# Extract inner interactive canvas content (from <!-- HEADER --> up to <!-- MODAL FOOTER CONTROLS -->)
header_idx = content_raw.find('<!-- HEADER -->')
footer_idx = content_raw.find('<!-- MODAL FOOTER CONTROLS -->')
if header_idx == -1 or footer_idx == -1:
    print(f"ERROR: Indices not found: header={header_idx}, footer={footer_idx}")
    sys.exit(1)

inner_body = content_raw[header_idx:footer_idx].strip()
print(f"Extracted inner body: {len(inner_body)} characters.")

# In the header, add the prominent "Open in Full-Scale Pop-up Window" button
btn_html = """
              <div style="display:flex; align-items:center; gap:10px;">
                <button type="button" id="amlExpandModalBtn" onclick="openAmlModal()" class="btn btn-primary" style="font-size:13.5px; font-weight:800; padding:10px 22px; background:linear-gradient(135deg, #FF9F0A 0%, #EA580C 100%); border:none; box-shadow:0 0 20px rgba(255,159,10,0.5); cursor:pointer;">
                  <span style="font-size:16px; margin-right:4px;">⤢</span> Open in Full-Scale Pop-Up Window
                </button>
              </div>
"""

target_header_badge = '<div style="font-size:16px; font-weight:800; color:var(--tx-0);">7-Step Master Simulation</div>\n              </div>'
if target_header_badge in inner_body:
    inner_body = inner_body.replace(target_header_badge, target_header_badge + '\n' + btn_html)
    print("Injected amlExpandModalBtn into header.")
else:
    print("Warning: target_header_badge not found in inner_body, appending button.")
    inner_body = btn_html + '\n' + inner_body

# Build in-page archContent-aml-workflow containing amlWorkflowMainContainer directly!
inpage_html = f"""
        <!-- ==================== STYLES FOR AML MODAL & ANIMATIONS ==================== -->
        {css_block}

        <!-- ==================== TAB 0: ANIMATED AML WORKFLOW (INTERACTIVE CANVAS DIRECTLY VISIBLE ON PAGE) ==================== -->
        <div id="archContent-aml-workflow" class="arch-tab-content">
          <div id="amlWorkflowMainContainer" style="background:var(--surface); border:1.5px solid var(--amber); border-radius:14px; padding:22px; margin-bottom:24px; box-shadow:0 8px 36px rgba(255,159,10,0.22);">
            {inner_body}
          </div>
        </div>
"""

# Build modal overlay (to be placed as direct child of <body>)
modal_overlay_html = """
    <!-- ==================== FULL-SCALE SEPARATE POPUP MODAL WINDOW (ATTACHED TO BODY) ==================== -->
    <div id="amlModalOverlay" class="aml-modal-overlay" onclick="if(event.target===this)closeAmlModal()">
      <div id="amlModalCard" class="aml-modal-card" onclick="event.stopPropagation()">
        
        <!-- MODAL HEADER BAR -->
        <div id="amlModalHeader" class="aml-modal-header">
          <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
            <span class="aml-badge amber">⚡ FULL-SCREEN INTERACTIVE SIMULATOR</span>
            <span class="aml-badge blue">FINANCIAL AML & FRAUD USE CASE</span>
            <span class="aml-badge emerald">7-STAGE MASTER WORKFLOW</span>
            <span class="aml-badge purple">HYBRID GRAPH-RAG</span>
            <h2 style="color:#F8FAFC; font-size:16px; margin:0; font-weight:800; display:inline-flex; align-items:center; gap:8px;">
              Interactive AML Knowledge Graph Simulator: Data Unification & Pattern Recognition
            </h2>
          </div>

          <!-- RIGHT SIDE: STATUS & CROSS (X) CLOSE BUTTON -->
          <div style="display:flex; align-items:center; gap:14px;">
            <div style="background:rgba(255,159,10,0.12); border:1px solid rgba(255,159,10,0.4); border-radius:8px; padding:4px 12px; text-align:right;">
              <div style="font-size:10px; color:var(--amber); font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">Executive Panel Mode</div>
              <div id="amlModalStageIndicator" style="font-size:12.5px; font-weight:800; color:#FFFFFF;">Stage 1 of 7 Active</div>
            </div>

            <!-- TOP-RIGHT CROSS (X) BUTTON -->
            <button type="button" onclick="closeAmlModal()" id="amlModalCloseBtn" class="aml-modal-close-btn" title="Close Window (Esc)" aria-label="Close interactive window">
              ✕
            </button>
          </div>
        </div>

        <!-- MODAL BODY -->
        <div id="amlModalBody" style="flex:1; overflow-y:auto; padding:18px 22px; display:flex; flex-direction:column; gap:14px;">
          <!-- #amlWorkflowMainContainer is smoothly reparented here when openAmlModal() is called -->
        </div>

      </div>
    </div>
"""

# Update scripts/build_aml_workflow_js.py
with open('scripts/build_aml_workflow_js.py', 'r', encoding='utf-8') as f:
    js_raw = f.read()

new_modal_handlers = """
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
"""

js_raw = re.sub(
    r'// Modal Window Controls.*?window\.openAmlModalWithStep = function\(stepNum\) \{.*?\};',
    lambda m: new_modal_handlers.strip(),
    js_raw,
    flags=re.DOTALL
)

with open('scripts/build_aml_workflow_js.py', 'w', encoding='utf-8') as f:
    f.write(js_raw)
print("Updated scripts/build_aml_workflow_js.py with reparenting handlers.")

# Load index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update showArchTab in <head>
old_show_arch_pattern = r'window\.showArchTab = function\(tabName\) \{.*?if \(tabName === \'aml-workflow\'\) \{.*?\};?\s*\};'
new_show_arch = """window.showArchTab = function(tabName) {
      const tabs = ['aml-workflow', 'pipeline', 'fintech', 'health', 'breakdown', 'techstack'];
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
      }
    };"""

html = re.sub(old_show_arch_pattern, lambda m: new_show_arch, html, flags=re.DOTALL)
print("Updated showArchTab function in <head>.")

# 2. Add pop-up button right in the navigation pills bar if not already present
pill_btn_html = """          <button type="button" onclick="showArchTab('aml-workflow')" id="archTab-aml-workflow" class="btn btn-sm btn-primary" style="padding:8px 18px; font-weight:700; background:linear-gradient(135deg, rgba(255,159,10,0.3) 0%, rgba(96,165,250,0.3) 100%); border:1.5px solid var(--amber); color:var(--tx-0); box-shadow:0 0 16px rgba(255,159,10,0.35);"><span style="display:inline-block; animation:pulse 1.8s infinite;">⚡</span> Interactive AML Workflow (Panel-Ready)</button>
          <button type="button" onclick="openAmlModal()" id="archTab-aml-modal-btn" class="btn btn-sm btn-primary" style="padding:8px 16px; font-weight:800; background:linear-gradient(135deg, #FF9F0A 0%, #EA580C 100%); border:none; box-shadow:0 0 16px rgba(255,159,10,0.45); cursor:pointer;"><span style="font-size:14px; margin-right:4px;">⤢</span> Pop-up Large Window</button>"""

if 'id="archTab-aml-modal-btn"' not in html:
    html = re.sub(
        r'<button type="button" onclick="showArchTab\(\'aml-workflow\'\)" id="archTab-aml-workflow"[^>]*>.*?</button>',
        lambda m: pill_btn_html,
        html
    )
    print("Added Pop-up Large Window button to section navigation pills.")

# 3. Replace in-page AML tab content (between section pills and <!-- TAB 1: 10-STEP PIPELINE)
tab1_marker = '<!-- TAB 1: 10-STEP PIPELINE'
tab1_idx = html.find(tab1_marker)
if tab1_idx == -1:
    print("ERROR: Could not find TAB 1 marker in index.html")
    sys.exit(1)

# Find where AML styles or tab begins after the pills
pills_marker = 'id="archTab-aml-modal-btn"'
if pills_marker not in html:
    pills_marker = 'id="archTab-techstack"'
pills_end_idx = html.find('</div>', html.find(pills_marker)) + 6

# Slice and replace
html = html[:pills_end_idx] + '\n\n' + inpage_html.strip() + '\n\n        ' + html[tab1_idx:]
print("Replaced in-page AML tab content with fully visible canvas!")

# 4. Remove any existing amlModalOverlay in the document
html = re.sub(r'<!-- ==================== FULL-SCALE SEPARATE POPUP MODAL WINDOW.*?<!-- end #amlModalOverlay -->\s*', '', html, flags=re.DOTALL)
html = re.sub(r'<div id="amlModalOverlay".*?<!-- end #amlModalCard -->\s*</div>\s*', '', html, flags=re.DOTALL)

# 5. Remove any old aml-workflow-script
html = re.sub(r'<script id="aml-workflow-script">.*?</script>\s*', '', html, flags=re.DOTALL)

# 6. Get updated JS
sys.path.insert(0, os.path.abspath('scripts'))
from build_aml_workflow_js import get_aml_workflow_js
updated_js = get_aml_workflow_js()

# 7. Locate the true closing </body></html> at the end of the file
final_target = '</body>\n\n</html>'
if final_target not in html:
    final_target = '</body>\n</html>'
if final_target not in html:
    final_target = '</body></html>'

last_idx = html.rfind(final_target)
if last_idx == -1:
    print("ERROR: Could not find closing </body></html> tag!")
    sys.exit(1)

html = html[:last_idx] + f"{modal_overlay_html.strip()}\n\n{updated_js.strip()}\n\n{final_target}\n"

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved updated index.html successfully!")

# 8. Node syntax verification
with open('temp_check_script.js', 'w', encoding='utf-8') as tf:
    m = re.search(r'<script id="aml-workflow-script">(.*?)</script>', html, re.DOTALL)
    if m:
        tf.write(m.group(1))

res = subprocess.run(['node', '--check', 'temp_check_script.js'], capture_output=True, text=True)
if os.path.exists('temp_check_script.js'):
    os.remove('temp_check_script.js')

if res.returncode == 0:
    print("[SUCCESS] node --check passed with exit code 0!")
else:
    print(f"[FAIL] Node check failed:\n{res.stderr}")
    sys.exit(1)
