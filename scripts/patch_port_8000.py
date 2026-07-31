import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

get_api_url_def = '''
    window.getApiUrl = function(path) {
        if (!path) return '';
        if (typeof path !== 'string') return path;
        if (path.startsWith('http://127.0.0.1:8000')) return path;
        if (path.startsWith('http://localhost:8010') || path.startsWith('http://localhost:8000') || path.startsWith('http://127.0.0.1:8010')) {
            return 'http://127.0.0.1:8000' + path.replace(/^http:\\/\\/[^\\/]+/, '');
        }
        const cleanPath = path.startsWith('/') ? path : '/' + path;
        if (window.location.protocol !== 'file:' && window.location.hostname === '127.0.0.1' && window.location.port === '8000') {
            return cleanPath;
        }
        return 'http://127.0.0.1:8000' + cleanPath;
    };
'''

# Update getApiUrl implementation
if 'window.getApiUrl =' in txt:
    pos_start = txt.find('window.getApiUrl =')
    pos_end = txt.find('};', pos_start) + 2
    txt = txt[:pos_start-4] + get_api_url_def + txt[pos_end:]
else:
    script_pos = txt.find('<script>')
    if script_pos != -1:
        txt = txt[:script_pos + 8] + get_api_url_def + txt[script_pos + 8:]

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Updated index.html getApiUrl to target http://127.0.0.1:8000")

# Update Dashboard.jsx
dash_path = 'portal-ui/src/pages/Dashboard.jsx'
if os.path.exists(dash_path):
    with open(dash_path, 'r', encoding='utf-8') as f:
        d_txt = f.read()
    d_txt = d_txt.replace("const API_BASE = 'http://127.0.0.1:8010';", "const API_BASE = 'http://127.0.0.1:8000';")
    d_txt = d_txt.replace("const API_BASE = 'http://localhost:8010';", "const API_BASE = 'http://127.0.0.1:8000';")
    with open(dash_path, 'w', encoding='utf-8') as f:
        f.write(d_txt)
    print("Updated Dashboard.jsx API_BASE to http://127.0.0.1:8000")
