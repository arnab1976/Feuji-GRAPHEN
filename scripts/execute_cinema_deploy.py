# -*- coding: utf-8 -*-
"""
Replace simWidgetCard-fin and simWidgetCard-med with Holographic Architecture Command Center
"""
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

index_path = 'index.html'

with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

from deploy_cinematic_architecture import generate_cinema_html, cinema_css, cinema_js

# Replace simWidgetCard-fin
start_marker_fin = '<div class="sim-card" id="simWidgetCard-fin">'
if start_marker_fin in html:
    pos_start = html.find(start_marker_fin)
    # Find matching closing </div>\n before Technical Deep Dive: The 6 Core Mechanics in Financial AML
    deep_dive_pos = html.find('Technical Deep Dive: The 6 Core Mechanics in Financial AML', pos_start)
    pos_end = html.rfind('</div>', pos_start, deep_dive_pos) + 6
    cinema_fin = generate_cinema_html('fin')
    html = html[:pos_start] + cinema_fin + html[pos_end:]
    print("Replaced simWidgetCard-fin successfully.")

# Replace simWidgetCard-med
start_marker_med = '<div class="sim-card" id="simWidgetCard-med">'
if start_marker_med in html:
    pos_start = html.find(start_marker_med)
    deep_dive_pos = html.find('Technical Deep Dive: The 6 Core Mechanics in Drug Discovery', pos_start)
    pos_end = html.rfind('</div>', pos_start, deep_dive_pos) + 6
    cinema_med = generate_cinema_html('med')
    html = html[:pos_start] + cinema_med + html[pos_end:]
    print("Replaced simWidgetCard-med successfully.")

# Ensure CSS is present
if '.cinema-viewport' not in html:
    head_pos = html.find('</head>')
    if head_pos != -1:
        html = html[:head_pos] + '<style>' + cinema_css + '</style>\n' + html[head_pos:]
        print("Injected cinema CSS.")

# Ensure JS is present
if 'cinemaSelectAct' not in html:
    body_pos = html.rfind('</body>')
    if body_pos != -1:
        html = html[:body_pos] + cinema_js + '\n' + html[body_pos:]
        print("Injected cinema JS.")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS: index.html updated with Cinematic Command Center in both views!")
