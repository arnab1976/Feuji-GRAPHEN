import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

panel_ids = re.findall(r'id=[\'"](snapshot-[^\'"]+)[\'"]', html)
print(f"Total snapshot panels found: {len(panel_ids)}")
print("Panel IDs:", panel_ids)

button_calls = re.findall(r'toggleDataSnapshot\([\'"]([^\'"]+)[\'"]', html)
print(f"Total button calls found: {len(button_calls)}")
print("Button target IDs:", button_calls)

missing = [b for b in button_calls if b not in panel_ids]
print("Missing panel IDs for button calls:", missing)
