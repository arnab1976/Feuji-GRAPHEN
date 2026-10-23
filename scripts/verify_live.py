import urllib.request

with urllib.request.urlopen('http://127.0.0.1:8004/') as res:
    print('Status:', res.status)
    content = res.read().decode('utf-8')
    print('Content Length:', len(content))
    print('Has flex-direction: column:', 'flex-direction: column' in content)
    print('Has word-break: break-word:', 'word-break: break-word' in content)
    pos_aml6 = content.find('id="snapshot-aml-6"')
    pos_tab3 = content.find('<!-- TAB 3')
    print('snapshot-aml-6 before TAB 3:', pos_aml6 < pos_tab3, f"(aml6: {pos_aml6}, tab3: {pos_tab3})")
