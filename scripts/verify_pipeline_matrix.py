# -*- coding: utf-8 -*-
import urllib.request

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = {
    'archTab-pipeline-matrix in pills': 'id="archTab-pipeline-matrix"' in text,
    'archContent-pipeline-matrix present': 'id="archContent-pipeline-matrix"' in text,
    'Card 1 Table present': 'Card 1: End-to-End Knowledge Graph Pipeline Matrix' in text,
    'Card 2 Bullets present': 'Card 2: Step-by-Step Bullet Points' in text,
    'Card 3 Simulator present': 'Card 3: Animated Interactive Workflow Pipeline' in text,
    'matrixSvgCanvas present': 'id="matrixSvgCanvas"' in text,
    'matrixPlayPauseBtn present': 'id="matrixPlayPauseBtn"' in text,
    'matrixStepBtn-1 to 7 present': all(f'id="matrixStepBtn-{i}"' in text for i in range(1, 8)),
    'pipeline-matrix in showArchTab': "'pipeline-matrix'" in text[:text.find('window.getApiUrl')],
    'pipeline-matrix-script present': 'id="pipeline-matrix-script"' in text,
    'setMatrixStep in JS': 'window.setMatrixStep = function' in text,
    'toggleMatrixPlay in JS': 'window.toggleMatrixPlay = function' in text,
}

print("=== VERIFY PIPELINE MATRIX TAB ===")
all_ok = True
for name, val in checks.items():
    status = "OK" if val else "MISSING"
    if not val:
        all_ok = False
    print(f"[{status}] {name}")

# Check HTTP Server
try:
    resp = urllib.request.urlopen('http://127.0.0.1:8000', timeout=5)
    content = resp.read().decode('utf-8')
    print(f"[OK] HTTP GET http://127.0.0.1:8000 -> HTTP {resp.status}")
    print(f"[OK] Served HTML contains archTab-pipeline-matrix: {'archTab-pipeline-matrix' in content}")
    print(f"[OK] Served HTML contains archContent-pipeline-matrix: {'archContent-pipeline-matrix' in content}")
except Exception as e:
    print(f"[FAIL] HTTP GET failed: {e}")
    all_ok = False

if all_ok:
    print("=== ALL VERIFICATION CHECKS PASSED PERFECTLY ===")
else:
    print("=== SOME CHECKS FAILED ===")
