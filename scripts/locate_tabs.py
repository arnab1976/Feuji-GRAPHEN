import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Look for tab containers or titles
for m in re.finditer(r'<section[^>]*id=[\'"]([^\'"]+)[\'"]|<div[^>]*id=[\'"]([^\'"]+)[\'"]', text):
    id_val = m.group(1) or m.group(2)
    if any(k in id_val.lower() for k in ['tab', 'aml', 'drug', 'med', 'step', 'breakdown', 'workflow']):
        print(f"ID: {id_val} at position {m.start()}")
