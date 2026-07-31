import re
with open('c:/CBRE_Ontology/index.html', 'r', encoding='utf-8') as f:
    text = f.read()
matches = re.finditer(r'<div class="view(?: active)?" id="view-([^"]+)">', text)
for m in matches:
    print(f'View: {m.group(1)}')
