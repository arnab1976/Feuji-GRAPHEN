import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/inject_snapshots_into_cards.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'card_end = ' in line or 'closing_div = ' in line or 'snapshot-aml' in line or 'snapshot-med' in line:
        print(f"Line {i+1}: {line.strip()}")
