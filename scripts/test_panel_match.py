with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

for i in range(1, 7):
    m = re.search(rf'(<div id="snapshot-aml-{i}"[\s\S]*?</div>\s*</div>)', html)
    print(f"AML {i} found:", bool(m))
    if m:
        # print length of match
        print(f"  Length of AML {i}: {len(m.group(0))}")

for i in range(1, 7):
    m = re.search(rf'(<div id="snapshot-med-{i}"[\s\S]*?</div>\s*</div>)', html)
    print(f"Med {i} found:", bool(m))
    if m:
        print(f"  Length of Med {i}: {len(m.group(0))}")
