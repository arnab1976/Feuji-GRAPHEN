with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

for pid in ["snapshot-aml-1", "snapshot-aml-2", "snapshot-med-1", "snapshot-med-6"]:
    pos = html.find(f'id="{pid}"')
    p_start = html.rfind('<div', 0, pos)
    pos_foot = html.find('snapshot-mechanics-footer', pos)
    pos_foot_end = html.find('</div>', pos_foot)
    p_end = html.find('</div>', pos_foot_end + 6) + 6
    block = html[p_start:p_end]
    print(f"=== {pid} ===")
    print("Start:", repr(block[:60]))
    print("End:", repr(block[-60:]))
