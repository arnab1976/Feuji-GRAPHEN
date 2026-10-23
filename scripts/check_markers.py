import sys
import re
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's locate the AML tab and the Med tab
# In update_aml_drug_breakdown.py:
# AML header:
# "Financial Crime & AML Investigation" or the step markers
aml_markers = [
    '<span style="font-size:14.5px; font-weight:700; color:var(--amber);">1. How Multiple Unstructured Data Map Within Each Other</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--amber);">2. How Multiple Structured Data Map Within Each Other</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--amber);">3. Unstructured-to-Structured Mapping via Mapping Keys</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--amber);">4. Ultimate Joined Data Structure (Multi-Modal Property Graph)</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--amber);">5. How Pattern Recognition Works Here</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--amber);">6. What Exactly You Provide to Leadership (Executive Deliverables)</span>',
]

med_markers = [
    '<span style="font-size:14.5px; font-weight:700; color:var(--emerald);">1. How Multiple Unstructured Biomedical Data Map Within Each Other</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--emerald);">2. How Multiple Structured Life Sciences Data Map Within Each Other</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--emerald);">3. Unstructured-to-Structured Mapping via Biomedical Mapping Keys</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--emerald);">4. Ultimate Joined Data Structure (Biomedical Knowledge Graph)</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--emerald);">5. How Pattern Recognition Works Here</span>',
    '<span style="font-size:14.5px; font-weight:700; color:var(--emerald);">6. What Exactly You Provide to Leadership (Executive Deliverables)</span>',
]

print("=== CHECKING AML MARKERS ===")
for i, m in enumerate(aml_markers):
    pos = html.find(m)
    print(f"AML {i+1}: pos = {pos}")

print("=== CHECKING MED MARKERS ===")
for i, m in enumerate(med_markers):
    pos = html.find(m)
    print(f"MED {i+1}: pos = {pos}")
