import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find matches for "6." in the HTML
for m in re.finditer(r'<span[^>]*font-size:14\.5px[^>]*>(.*?)</span>', html):
    print("Found Step Header:", m.group(1))
