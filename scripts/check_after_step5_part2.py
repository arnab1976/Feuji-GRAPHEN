import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos5_aml = html.find('5. How Pattern Recognition Works Here')
print(html[pos5_aml+2500:pos5_aml+5500])
