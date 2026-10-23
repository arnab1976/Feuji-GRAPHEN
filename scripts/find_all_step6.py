import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = [m.start() for m in re.finditer(r'6\. What Exactly You Provide to Leadership', html)]
print("Step 6 occurrences:", matches)
for m in matches:
    print("--- Occur at", m)
    print(html[m-100:m+200])
