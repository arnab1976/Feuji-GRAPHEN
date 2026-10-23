import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('margin-top:32px;')
print("Context before margin-top:32px;:")
print(repr(html[pos-300:pos]))

pos_med6 = 659002
pos_med6_next = html.find('<!-- ====================', pos_med6)
print("Context after Med 6 before next section:")
print(repr(html[pos_med6_next-300:pos_med6_next]))
