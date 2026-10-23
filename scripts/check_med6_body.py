import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_med6 = 659002
# Let's find "Deliverable 3" or whatever the last deliverable in Med 6 is
pos_deliv3 = html.find('Deliverable 3', pos_med6)
print("Deliverable 3 pos:", pos_deliv3)
print(html[pos_deliv3:pos_deliv3+1500])
