import re

with open('c:/CBRE_Ontology/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Shrink Hero
content = content.replace(
    '<div style="text-align: center; margin-bottom: 24px;">',
    '<div style="text-align: center; margin-bottom: 16px;">'
)
content = content.replace(
    'text-transform: uppercase; margin-bottom: 16px;',
    'text-transform: uppercase; margin-bottom: 8px;'
)
content = content.replace(
    'font-size: 56px; font-weight: 800; color: var(--tx-0); margin: 0 0 16px 0;',
    'font-size: 42px; font-weight: 800; color: var(--tx-0); margin: 0 0 10px 0;'
)
content = content.replace(
    'font-size: 16px; color: var(--tx-1); max-width: 700px; margin: 0 auto 24px auto; line-height: 1.6;',
    'font-size: 14px; color: var(--tx-1); max-width: 700px; margin: 0 auto 16px auto; line-height: 1.4;'
)

# Shrink Cards Container
content = content.replace(
    'display: flex; gap: 24px; max-width: 1000px; width: 100%;',
    'display: flex; gap: 20px; max-width: 900px; width: 100%;'
)

# Shrink Left Card
content = content.replace(
    'border: 2px solid var(--emerald); border-radius: 8px; background: var(--bg-1); padding: 32px;',
    'border: 2px solid var(--emerald); border-radius: 8px; background: var(--bg-1); padding: 20px 24px;'
)
content = content.replace(
    'font-size: 28px; font-weight: 800; color: var(--emerald); margin: 0 0 8px 0;',
    'font-size: 22px; font-weight: 800; color: var(--emerald); margin: 0 0 4px 0;'
)
content = content.replace(
    'font-size: 14px; font-style: italic; color: var(--emerald); margin-bottom: 24px;',
    'font-size: 13px; font-style: italic; color: var(--emerald); margin-bottom: 12px;'
)
content = content.replace(
    'font-size: 14px; color: var(--tx-1); margin: 0 0 24px 0; line-height: 1.5;',
    'font-size: 13px; color: var(--tx-1); margin: 0 0 16px 0; line-height: 1.4;'
)
content = content.replace(
    'padding: 0; margin: 0 0 40px 0; font-size: 13px; color: var(--tx-1); display: flex; flex-direction: column; gap: 12px;',
    'padding: 0; margin: 0 0 24px 0; font-size: 12px; color: var(--tx-1); display: flex; flex-direction: column; gap: 8px;'
)
content = content.replace(
    'padding: 14px; background: var(--emerald); color: #fff; font-weight: 700; font-size: 16px;',
    'padding: 10px; background: var(--emerald); color: #fff; font-weight: 700; font-size: 14px;'
)

# Shrink Right Card
content = content.replace(
    'border: 2px solid var(--blue); border-radius: 8px; background: var(--bg-1); padding: 32px;',
    'border: 2px solid var(--blue); border-radius: 8px; background: var(--bg-1); padding: 20px 24px;'
)
content = content.replace(
    'font-size: 28px; font-weight: 800; color: var(--blue); margin: 0 0 8px 0;',
    'font-size: 22px; font-weight: 800; color: var(--blue); margin: 0 0 4px 0;'
)
content = content.replace(
    'font-size: 14px; font-style: italic; color: var(--blue); margin-bottom: 24px;',
    'font-size: 13px; font-style: italic; color: var(--blue); margin-bottom: 12px;'
)
content = content.replace(
    'font-size: 14px; color: var(--tx-1); margin: 0 0 24px 0; line-height: 1.5;',
    'font-size: 13px; color: var(--tx-1); margin: 0 0 16px 0; line-height: 1.4;'
)
content = content.replace(
    'padding: 0; margin: 0 0 40px 0; font-size: 13px; color: var(--tx-1); display: flex; flex-direction: column; gap: 12px;',
    'padding: 0; margin: 0 0 24px 0; font-size: 12px; color: var(--tx-1); display: flex; flex-direction: column; gap: 8px;'
)
content = content.replace(
    'padding: 14px; background: var(--blue); color: #fff; font-weight: 700; font-size: 16px;',
    'padding: 10px; background: var(--blue); color: #fff; font-weight: 700; font-size: 14px;'
)

with open('c:/CBRE_Ontology/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
