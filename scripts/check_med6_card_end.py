with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_med6_btn = html.find("toggleDataSnapshot('snapshot-med-6'")
pos_deliv3_med = html.find('Deliverable 3', pos_med6_btn)
print("Context after Med 6 Deliverable 3:")
print(repr(html[pos_deliv3_med:pos_deliv3_med+1800]))
