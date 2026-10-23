import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos5_aml = html.find('5. How Pattern Recognition Works Here')
pos_next_tab = html.find('<!-- ====================', pos5_aml)
print("=== AFTER AML STEP 5 ===")
print(html[pos5_aml:pos5_aml+2500])
