import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos6_aml = 609415
# Find what comes after AML Step 6
pos_med1 = 639045
sub = html[pos6_aml:pos_med1]
print("AML 6 length to Med 1:", len(sub))
# Look for where the card closes or next section
lines = sub.splitlines()
print("First 15 lines of AML 6:")
for l in lines[:15]:
    print("  ", l[:100])
print("...")
print("Last 15 lines before Med 1:")
for l in lines[-15:]:
    print("  ", l[:100])
