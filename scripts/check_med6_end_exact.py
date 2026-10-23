import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('Hit-to-lead timeline compressed', 659000)
print(html[pos:pos+1200])
