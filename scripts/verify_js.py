with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx = html.find('window.toggleDataSnapshot')
print("Function defined at index:", idx)
print(html[idx-10:idx+350])
