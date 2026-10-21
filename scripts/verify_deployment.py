# -*- coding: utf-8 -*-
import urllib.request
import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

s_arch = text.find('id="archContent-aml-workflow"')
e_tab1 = text.find('<!-- TAB 1: 10-STEP PIPELINE')
inpage_slice = text[s_arch:e_tab1]

checks = {
    'amlSvgCanvas in archContent-aml-workflow': 'id="amlSvgCanvas"' in inpage_slice,
    'amlWorkflowMainContainer present': 'id="amlWorkflowMainContainer"' in inpage_slice,
    'amlExpandModalBtn in inpage': 'id="amlExpandModalBtn"' in inpage_slice,
    'amlModalOverlay present': 'id="amlModalOverlay"' in text,
    'amlModalCloseBtn present': 'id="amlModalCloseBtn"' in text,
    'archTab-aml-modal-btn in pills': 'id="archTab-aml-modal-btn"' in text,
    'openAmlModal in JS': 'window.openAmlModal = function' in text,
    'closeAmlModal in JS': 'window.closeAmlModal = function' in text,
    'toggleAmlPlay in JS': 'window.toggleAmlPlay = function' in text,
    'amlTimerBadge present': 'id="amlTimerBadge"' in inpage_slice,
    'amlPlayPauseBtn present': 'id="amlPlayPauseBtn"' in inpage_slice,
    'all 7 steps in SVG': all(f'amlStepBtn-{i}' in inpage_slice for i in range(1, 8)),
    'all 6 SVG zones': all(z in inpage_slice for z in ['svgZoneStructured', 'svgZoneUnstructured', 'svgZoneTransform', 'svgZoneTools', 'svgZoneTopology', 'svgZoneOutputs']),
}

print("=== VERIFICATION RESULTS ===")
all_ok = True
for name, val in checks.items():
    status = "OK" if val else "MISSING"
    if not val:
        all_ok = False
    print(f"[{status}] {name}")

# Check HTTP Server
try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000', timeout=5)
    print(f"[OK] HTTP GET http://127.0.0.1:8000 -> HTTP {resp.status}")
except Exception as e:
    print(f"[FAIL] HTTP GET failed: {e}")
    all_ok = False

if all_ok:
    print("=== ALL CHECKS PASSED PERFECTLY ===")
else:
    print("=== SOME CHECKS FAILED ===")
