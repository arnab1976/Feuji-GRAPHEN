with open('scripts/inject_snapshots_into_cards.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(615, 635):
    print(f"Line {i+1}: {repr(lines[i])}")
