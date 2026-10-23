with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's inspect Step 6 AML
pos_btn6 = html.find("toggleDataSnapshot('snapshot-aml-6'")
pos_panel6 = html.find('id="snapshot-aml-6"')
print(f"AML 6: btn at {pos_btn6}, panel at {pos_panel6}, distance = {pos_panel6 - pos_btn6}")

# Let's inspect Step 6 Med
pos_btn_med6 = html.find("toggleDataSnapshot('snapshot-med-6'")
pos_panel_med6 = html.find('id="snapshot-med-6"')
print(f"Med 6: btn at {pos_btn_med6}, panel at {pos_panel_med6}, distance = {pos_panel_med6 - pos_btn_med6}")
