with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_btn6 = html.find("toggleDataSnapshot('snapshot-aml-6'")
# Let's see the context around pos_btn6 (the Step 6 card)
# Find where the 3 Deliverables end
pos_deliv3 = html.find('Deliverable 3', pos_btn6)
print("Deliverable 3 at:", pos_deliv3)
pos_card_end = html.find('</div>\n                </div>', pos_deliv3)
print("Card end near deliverable 3:", pos_card_end)
print("Context around card end near deliv 3:")
print(repr(html[pos_card_end-100:pos_card_end+200]))

pos_panel6 = html.find('id="snapshot-aml-6"')
print("\nContext before panel 6:")
print(repr(html[pos_panel6-200:pos_panel6]))
