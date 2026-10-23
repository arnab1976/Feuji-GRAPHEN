import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

panels = re.findall(r'<div id="(snapshot-[^"]+)"[^>]*>([\s\S]*?)<div class="snapshot-mechanics-footer', text)
for pid, pcontent in panels:
    print(f"=== {pid} ===")
    titles = re.findall(r'<div class="snapshot-col-title"><span>[^<]*</span>\s*([^<]+)</div>', pcontent)
    print("  Col titles:", titles)
