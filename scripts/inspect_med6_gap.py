with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_btn_med6 = html.find("toggleDataSnapshot('snapshot-med-6'")
pos_deliv3_med = html.find('Deliverable 3', pos_btn_med6)
print("Med 6 Deliverable 3 at:", pos_deliv3_med)
pos_card_end_med = html.find('</div>\n                </div>', pos_deliv3_med)
print("Med 6 card end near deliv 3:", pos_card_end_med)

pos_panel_med6 = html.find('id="snapshot-med-6"')
print("Med 6 panel at:", pos_panel_med6)
print("Context around Med 6 panel:")
print(repr(html[pos_panel_med6-200:pos_panel_med6]))
