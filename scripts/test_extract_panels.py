import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scripts/inject_snapshots_into_cards.py', 'r', encoding='utf-8') as f:
    code = f.read()

lines = code.splitlines()

code_aml = "\n".join(lines[26:576])
code_med = "\n".join(lines[629:995])

scope = {}
exec(code_aml, scope)
exec(code_med, scope)

print("AML Panels extracted:", [k for k in sorted(scope.keys()) if k.startswith('panel_aml_')])
print("Med Panels extracted:", [k for k in sorted(scope.keys()) if k.startswith('panel_med_')])
print("CSS present:", 'snapshot_css' in scope)
print("JS present:", 'snapshot_js' in scope)
