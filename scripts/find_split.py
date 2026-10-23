with open('scripts/inject_snapshots_into_cards.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'aml_replacements = ' in line or 'med_replacements = ' in line:
        print(f"Line {i+1}: {line.strip()}")
