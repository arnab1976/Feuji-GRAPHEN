import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# 1. Update window.getApiUrl
new_get_api_url = '''    window.getApiUrl = function(path) {
        if (!path) return '';
        if (typeof path !== 'string') return path;
        if (/^http:\\/\\/(localhost|127\\.0\\.0\\.1):(8000|8010|8011)/i.test(path)) {
            path = path.replace(/^http:\\/\\/[^\\/]+/, '');
        }
        const cleanPath = path.startsWith('/') ? path : '/' + path;
        if (window.location.protocol !== 'file:') {
            return cleanPath;
        }
        return 'http://127.0.0.1:8000' + cleanPath;
    };'''

# Replace getApiUrl block
get_api_pattern = r'window\.getApiUrl\s*=\s*function\s*\([^\)]*\)\s*\{[\s\S]*?\};'
if re.search(get_api_pattern, txt):
    txt = re.sub(get_api_pattern, new_get_api_url, txt, count=1)
    print("Replaced window.getApiUrl block.")
else:
    print("WARNING: window.getApiUrl block not found!")

# 2. Replace hardcoded 8010/8011 fallbacks
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/domain/trending-use-cases', options);", "return fetch(getApiUrl('/api/domain/trending-use-cases'), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/domain/configure', options);", "return fetch(getApiUrl('/api/domain/configure'), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/schema/registry', options);", "return fetch(getApiUrl('/api/schema/registry'), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010' + path, options);", "return fetch(getApiUrl(path), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/crossdoc/discover', options);", "return fetch(getApiUrl('/api/crossdoc/discover'), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/intelligence/report', options);", "return fetch(getApiUrl('/api/intelligence/report'), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/intelligence/report/summarize', options);", "return fetch(getApiUrl('/api/intelligence/report/summarize'), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/final-report', options);", "return fetch(getApiUrl('/api/final-report'), options);")
txt = txt.replace("return fetch('http://127.0.0.1:8010/api/final-report/summarize', options);", "return fetch(getApiUrl('/api/final-report/summarize'), options);")
txt = txt.replace("Could not load scenarios - check API on port 8010.", "Could not load scenarios - check API connection.")

# 3. Check for any remaining fetch('/api/... without getApiUrl
# Ensure fetch('/api/crossdoc/discover' uses getApiUrl
txt = txt.replace("fetch('/api/crossdoc/discover'", "fetch(getApiUrl('/api/crossdoc/discover')")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("Successfully patched index.html with universal getApiUrl and removed port 8010 hardcodes.")
