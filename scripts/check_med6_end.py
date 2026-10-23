import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_med6 = 659002
pos_script = html.find('<script', pos_med6)
print("Distance from Med 6 to next script:", pos_script - pos_med6)
print("Context right before script:")
print(repr(html[pos_script-300:pos_script]))
