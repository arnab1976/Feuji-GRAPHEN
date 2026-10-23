with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_aml6_btn = html.find("toggleDataSnapshot('snapshot-aml-6'")
pos_deliv3 = html.find('Deliverable 3', pos_aml6_btn)
print("Context after AML 6 Deliverable 3:")
print(repr(html[pos_deliv3:pos_deliv3+1800]))
