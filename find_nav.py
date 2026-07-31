import re
with open('c:/CBRE_Ontology/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("--- nav function ---")
nav_match = re.search(r'function nav\([^)]*\)\s*\{[^}]*\}', text)
if nav_match:
    print(nav_match.group(0))
else:
    nav_match2 = re.search(r'function nav\([^)]*\)\s*\{(?:[^{}]*\{(?:[^{}]*\{(?:[^{}]*\{(?:[^{}]*\})*[^{}]*\})*[^{}]*\})*[^{}]*\})*[^{}]*\}', text)
    if nav_match2: print(nav_match2.group(0)[:500])

print("\n--- view-eval ---")
eval_idx = text.find('id="view-eval"')
if eval_idx != -1:
    print(text[eval_idx-50:eval_idx+200])
