with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re

for i in range(1, 7):
    pid = f"snapshot-aml-{i}"
    pos = html.find(f'id="{pid}"')
    if pos != -1:
        # Find next panel or next step
        pos_foot = html.find('snapshot-mechanics-footer', pos)
        pos_foot_end = html.find('</div>', pos_foot) # end of footer div
        pos_panel_end = html.find('</div>', pos_foot_end + 6) # end of snapshot-panel div
        print(f"{pid}: start={pos}, foot={pos_foot}, panel_end={pos_panel_end}")
        snippet = html[pos:pos_panel_end+6]
        # check that this snippet does not contain another snapshot-
        other_snapshots = re.findall(r'id="snapshot-(?:aml|med)-\d"', snippet)
        print(f"  Panels inside snippet: {other_snapshots}, total length: {len(snippet)}")

for i in range(1, 7):
    pid = f"snapshot-med-{i}"
    pos = html.find(f'id="{pid}"')
    if pos != -1:
        pos_foot = html.find('snapshot-mechanics-footer', pos)
        pos_foot_end = html.find('</div>', pos_foot)
        pos_panel_end = html.find('</div>', pos_foot_end + 6)
        print(f"{pid}: start={pos}, foot={pos_foot}, panel_end={pos_panel_end}")
        snippet = html[pos:pos_panel_end+6]
        other_snapshots = re.findall(r'id="snapshot-(?:aml|med)-\d"', snippet)
        print(f"  Panels inside snippet: {other_snapshots}, total length: {len(snippet)}")
