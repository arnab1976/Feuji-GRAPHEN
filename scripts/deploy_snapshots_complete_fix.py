import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

print("Starting clean deployment of Data Snapshots and Visual Graphs...")

# 1. Read index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 2. Extract panel definitions and CSS from inject_snapshots_into_cards.py
with open('scripts/inject_snapshots_into_cards.py', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.splitlines()
code_aml = "\n".join(lines[26:576])
code_med = "\n".join(lines[629:995])

scope = {}
exec(code_aml, scope)
exec(code_med, scope)

snapshot_css = scope['snapshot_css']

# Robust Toggle Script
snapshot_js = '''<script>
window.toggleDataSnapshot = function(panelId, btnElement) {
  var panel = document.getElementById(panelId);
  if (!panel) {
    console.warn("Snapshot panel not found:", panelId);
    return;
  }
  var isHidden = (window.getComputedStyle(panel).display === 'none' || panel.style.display === 'none' || panel.style.display === '');
  if (isHidden) {
    panel.style.display = 'block';
    if (btnElement) {
      btnElement.classList.add('open');
      btnElement.innerHTML = '<span>✕</span> Hide Data Snapshot ▲';
    }
  } else {
    panel.style.display = 'none';
    if (btnElement) {
      btnElement.classList.remove('open');
      btnElement.innerHTML = '<span>📊</span> View Data Snapshot & Visual Graph ▼';
    }
  }
};
</script>'''

# 3. Clean up any existing snapshot buttons and panels from index.html first
html = re.sub(r'\s*<button[^>]*class="btn-snapshot-toggle[^"]*"[^>]*>.*?</button>', '', html)
html = re.sub(r'\s*<div id="snapshot-(?:aml|med)-\d"[^>]*>[\s\S]*?</div>\s*</div>\s*</div>\s*</div>', '', html)
html = re.sub(r'\s*<div id="snapshot-(?:aml|med)-\d" class="snapshot-panel"[\s\S]*?</div>\s*</div>\s*</div>', '', html)

# Also remove any previous window.toggleDataSnapshot definition
html = re.sub(r'<script>\s*window\.toggleDataSnapshot\s*=\s*function[\s\S]*?</script>', '', html)

print("Cleaned up existing snapshot buttons, panels, and scripts.")

# 4. Now find the AML and Med sections
med_header_pos = html.find('Tech Stack Execution Details: Multi-Source Inputs, Biomedical Mapping Keys')
if med_header_pos == -1:
    med_header_pos = html.find('Biomedical Drug Discovery & Target Identification')
if med_header_pos == -1:
    med_header_pos = html.find('1. How Multiple Unstructured Biomedical Data Map Within Each Other')

print("Med section starts around position:", med_header_pos)

# AML step titles
aml_step_titles = [
    '1. How Multiple Unstructured Data Map Within Each Other',
    '2. How Multiple Structured Data Map Within Each Other',
    '3. Unstructured-to-Structured Mapping via Mapping Keys',
    '4. Ultimate Joined Data Structure (Multi-Modal Property Graph)',
    '5. How Pattern Recognition Works Here',
    '6. What Exactly You Provide to Leadership (Executive Deliverables)'
]

# Med step titles
med_step_titles = [
    '1. How Multiple Unstructured Biomedical Data Map Within Each Other',
    '2. How Multiple Structured Life Sciences Data Map Within Each Other',
    '3. Unstructured-to-Structured Mapping via Biomedical Mapping Keys',
    '4. Ultimate Joined Data Structure (Biomedical Knowledge Graph)',
    '5. How Pattern Recognition Works Here',
    '6. What Exactly You Provide to Leadership (Executive Deliverables)'
]

# Process AML steps (only search in html[:med_header_pos])
aml_part = html[:med_header_pos]
med_part = html[med_header_pos:]

for i in range(1, 7):
    title = aml_step_titles[i-1]
    panel_content = scope[f'panel_aml_{i}']
    btn_html = f'''<button type="button" class="btn-snapshot-toggle" onclick="toggleDataSnapshot('snapshot-aml-{i}', this)"><span>📊</span> View Data Snapshot & Visual Graph ▼</button>'''
    
    t_idx = aml_part.find(title)
    if t_idx == -1:
        print(f"ERROR: Could not find AML step {i} title: {title}")
        continue
    
    # 1. Insert button right inside the flex header closing </div>
    h_end = aml_part.find('</div>', t_idx)
    if h_end != -1:
        aml_part = aml_part[:h_end] + '\n                    ' + btn_html + aml_part[h_end:]
    
    # 2. Insert panel at the end of the card
    # Find next step or end of AML section
    if i < 6:
        next_step_str = f'<!-- STEP {i + 1} -->'
        next_pos = aml_part.find(next_step_str, t_idx)
    else:
        next_pos = len(aml_part)
    
    # The card's outer closing tag is the last </div> before next_pos
    card_closing = aml_part.rfind('</div>', t_idx, next_pos)
    if card_closing != -1:
        aml_part = aml_part[:card_closing] + '\n' + panel_content + '\n                ' + aml_part[card_closing:]
        print(f"Successfully injected AML Step {i} Button & Panel.")
    else:
        print(f"ERROR: Could not find closing div for AML Step {i}")

# Process Med steps (search in med_part)
for i in range(1, 7):
    title = med_step_titles[i-1]
    panel_content = scope[f'panel_med_{i}']
    btn_html = f'''<button type="button" class="btn-snapshot-toggle med" onclick="toggleDataSnapshot('snapshot-med-{i}', this)"><span>📊</span> View Data Snapshot & Visual Graph ▼</button>'''
    
    t_idx = med_part.find(title)
    if t_idx == -1:
        print(f"ERROR: Could not find Med step {i} title: {title}")
        continue
    
    # 1. Insert button right inside the flex header closing </div>
    h_end = med_part.find('</div>', t_idx)
    if h_end != -1:
        med_part = med_part[:h_end] + '\n                    ' + btn_html + med_part[h_end:]
    
    # 2. Insert panel at the end of the card
    if i < 6:
        next_step_str = f'<!-- STEP {i + 1} -->'
        next_pos = med_part.find(next_step_str, t_idx)
    else:
        # Step 6 ends before TAB 4 or next container
        next_pos = med_part.find('<!-- TAB 4', t_idx)
        if next_pos == -1:
            next_pos = med_part.find('id="archContent-breakdown"', t_idx)
    
    card_closing = med_part.rfind('</div>', t_idx, next_pos)
    if card_closing != -1:
        med_part = med_part[:card_closing] + '\n' + panel_content + '\n                ' + med_part[card_closing:]
        print(f"Successfully injected Med Step {i} Button & Panel.")
    else:
        print(f"ERROR: Could not find closing div for Med Step {i}")

# Combine back
html = aml_part + med_part

# Ensure CSS is present
if '.btn-snapshot-toggle' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>\n' + snapshot_css + '\n</style>\n' + html[head_pos:]
        print("Injected Snapshot CSS into <head>.")

# Ensure JS is present before </body>
body_pos = html.rfind('</body>')
if body_pos != -1:
    html = html[:body_pos] + '\n' + snapshot_js + '\n' + html[body_pos:]
    print("Injected Snapshot JS engine before </body>.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html fully rewritten with 12 buttons, 12 panels, CSS, and JS engine!")
