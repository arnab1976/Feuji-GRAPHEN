# -*- coding: utf-8 -*-
"""
Main Injection Script: Integrates HTML, CSS, and JS for Animated AML Workflow into index.html
"""
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

from build_aml_workflow_content import get_aml_workflow_html
from build_aml_workflow_js import get_aml_workflow_js

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update window.showArchTab function
old_show_tab = """        window.showArchTab = function(tabName) {
      const tabs = ['pipeline', 'fintech', 'health', 'breakdown', 'techstack'];"""

new_show_tab = """        window.showArchTab = function(tabName) {
      const tabs = ['aml-workflow', 'pipeline', 'fintech', 'health', 'breakdown', 'techstack'];"""

if old_show_tab in html:
    html = html.replace(old_show_tab, new_show_tab)
    print("Updated window.showArchTab array.")

# Ensure amlWorkflowInit is invoked when aml-workflow is selected
if "if (tabName === 'aml-workflow' && window.amlWorkflowInit)" not in html:
    html = re.sub(
        r"content\.style\.display = \(t === tabName\) \? 'block' : 'none';\s*\}\s*\}\);\s*\};",
        "content.style.display = (t === tabName) ? 'block' : 'none';\n        }\n      });\n      if (tabName === 'aml-workflow' && window.amlWorkflowInit) { window.amlWorkflowInit(); }\n    };",
        html
    )
    print("Added amlWorkflowInit callback in showArchTab.")

# 2. Update navigation pills in view-arch
nav_pills_pattern = r'<!-- Section Navigation Pills -->\s*<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">\s*<button type="button" onclick="showArchTab\(\'pipeline\'\)" id="archTab-pipeline".*?</button>'

new_nav_pills = """<!-- Section Navigation Pills -->
        <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
          <button type="button" onclick="showArchTab('aml-workflow')" id="archTab-aml-workflow" class="btn btn-sm btn-primary" style="padding:8px 18px; font-weight:700; background:linear-gradient(135deg, rgba(255,159,10,0.3) 0%, rgba(96,165,250,0.3) 100%); border:1.5px solid var(--amber); color:var(--tx-0); box-shadow:0 0 16px rgba(255,159,10,0.35);"><span style="display:inline-block; animation:pulse 1.8s infinite;">⚡</span> Interactive AML Workflow (Panel-Ready)</button>
          <button type="button" onclick="showArchTab('pipeline')" id="archTab-pipeline" class="btn btn-sm btn-secondary" style="padding:8px 16px; font-weight:600;">📌 10-Step Master Pipeline Diagram</button>"""

if 'id="archTab-aml-workflow"' not in html:
    html = re.sub(nav_pills_pattern, new_nav_pills, html, flags=re.DOTALL)
    print("Added archTab-aml-workflow pill button.")

# Make sure archContent-pipeline is hidden by default if aml-workflow is first
if '<div id="archContent-pipeline" class="arch-tab-content">\n          <div style="background:var(--surface);' in html:
    html = html.replace(
        '<div id="archContent-pipeline" class="arch-tab-content">\n          <div style="background:var(--surface);',
        '<div id="archContent-pipeline" class="arch-tab-content" style="display:none;">\n          <div style="background:var(--surface);'
    )
    print("Set archContent-pipeline to display:none by default.")

# 3. Inject archContent-aml-workflow
aml_content_html = get_aml_workflow_html()

if 'id="archContent-aml-workflow"' in html:
    # Replace existing version
    html = re.sub(
        r'<!-- ==================== TAB 0: ANIMATED AML WORKFLOW.*?<!-- TAB 1: 10-STEP PIPELINE',
        aml_content_html + '\n        <!-- TAB 1: 10-STEP PIPELINE',
        html,
        flags=re.DOTALL
    )
    print("Replaced existing archContent-aml-workflow.")
else:
    # Inject before TAB 1
    target = '<!-- TAB 1: 10-STEP PIPELINE'
    if target in html:
        html = html.replace(target, aml_content_html + '\n        ' + target)
        print("Injected archContent-aml-workflow before TAB 1.")

# 4. Inject JavaScript before </body>
aml_js = get_aml_workflow_js()

if '<script id="aml-workflow-script">' in html:
    html = re.sub(r'<script id="aml-workflow-script">.*?</script>', aml_js.strip(), html, flags=re.DOTALL)
    print("Replaced existing aml-workflow JavaScript.")
else:
    html = html.replace('</body>', aml_js + '\n</body>')
    print("Injected aml-workflow JavaScript before </body>.")

# Write back to index.html
with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Successfully injected all animated AML workflow code into index.html!")
