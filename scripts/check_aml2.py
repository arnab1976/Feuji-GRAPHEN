with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('snapshot-aml-2')
print("snapshot-aml-2 at index:", idx)
print(html[idx-20:idx+300])
