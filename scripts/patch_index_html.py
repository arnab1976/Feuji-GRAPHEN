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
        if (path.startsWith('http://127.0.0.1:8010')) return path;
        if (path.startsWith('http://localhost:8010') || path.startsWith('http://localhost:8000') || path.startsWith('http://127.0.0.1:8000')) {
            return 'http://127.0.0.1:8010' + path.replace(/^http:\\/\\/[^\\/]+/, '');
        }
        const cleanPath = path.startsWith('/') ? path : '/' + path;
        if (window.location.protocol !== 'file:' && window.location.hostname === '127.0.0.1' && window.location.port === '8010') {
            return cleanPath;
        }
        return 'http://127.0.0.1:8010' + cleanPath;
    };
'''

# Insert getApiUrl near top script tag if not present
if 'window.getApiUrl' not in txt:
    script_pos = txt.find('<script>')
    if script_pos != -1:
        txt = txt[:script_pos + 8] + get_api_url_def + txt[script_pos + 8:]

replacements = [
    ("fetch('/api/summary')", "fetch(getApiUrl('/api/summary'))"),
    ("fetch('/api/health')", "fetch(getApiUrl('/api/health'))"),
    ("fetch('/api/uploads/recent')", "fetch(getApiUrl('/api/uploads/recent'))"),
    ("fetch('/api/graph/tabs'", "fetch(getApiUrl('/api/graph/tabs')"),
    ("fetch('/api/cypher/detections'", "fetch(getApiUrl('/api/cypher/detections')"),
    ("fetch('/api/ingest/step1_extract'", "fetch(getApiUrl('/api/ingest/step1_extract')"),
    ("fetch(`/api/files/${id}`)", "fetch(getApiUrl(`/api/files/${id}`))"),
    ("fetch(url, { method: 'POST', body: formData })", "fetch(getApiUrl(url), { method: 'POST', body: formData })"),
    ("fetch(`/api/uploads/${window.currentTrackingId}/files`)", "fetch(getApiUrl(`/api/uploads/${window.currentTrackingId}/files`))"),
    ("fetch(`/api/uploads/${trackingId}/files`)", "fetch(getApiUrl(`/api/uploads/${trackingId}/files`))"),
]

for old_str, new_str in replacements:
    txt = txt.replace(old_str, new_str)

# Also fix delete tracking session
txt = txt.replace(
    "fetch(\n              `/api/uploads/${encodeURIComponent(trackingId)}`",
    "fetch(getApiUrl(`/api/uploads/${encodeURIComponent(trackingId)}`)"
)
txt = txt.replace(
    "fetch(`/api/uploads/${encodeURIComponent(trackingId)}`",
    "fetch(getApiUrl(`/api/uploads/${encodeURIComponent(trackingId)}`)"
)

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Successfully updated index.html with getApiUrl helper")
