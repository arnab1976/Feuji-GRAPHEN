const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Colors replacement for light theme
content = content.replace(/--bg-0:\s*#[0-9a-fA-F]{6};/g, '--bg-0: #f4f7fc;'); // Very light blue/white bg
content = content.replace(/--bg-1:\s*#[0-9a-fA-F]{6};/g, '--bg-1: #ffffff;'); // White panel
content = content.replace(/--bg-2:\s*#[0-9a-fA-F]{6};/g, '--bg-2: #f8fafc;'); // Slight tint
content = content.replace(/--bg-3:\s*#[0-9a-fA-F]{6};/g, '--bg-3: #e2e8f0;'); // Deeper tint
content = content.replace(/--line:\s*#[0-9a-fA-F]{6};/g, '--line: rgba(0,0,0,0.1);'); // Light border
content = content.replace(/--line-soft:\s*#[0-9a-fA-F]{6};/g, '--line-soft: rgba(0,0,0,0.05);'); // Very soft border

content = content.replace(/--tx-0:\s*#[0-9a-fA-F]{6};/g, '--tx-0: #0f172a;'); // Dark slate text
content = content.replace(/--tx-1:\s*#[0-9a-fA-F]{6};/g, '--tx-1: #334155;');
content = content.replace(/--tx-2:\s*#[0-9a-fA-F]{6};/g, '--tx-2: #64748b;');
content = content.replace(/--tx-3:\s*#[0-9a-fA-F]{6};/g, '--tx-3: #94a3b8;');

// Update logo LG to G
content = content.replace(/LG<\/div>/g, 'G</div>');

// Ensure the title is changed
content = content.replace(/<title>GRAPHEN.*<\/title>/, '<title>GRAPHEN — Graph-powered Reasoning Agentic Platform</title>');
content = content.replace(/<title>LeaseGuard.*<\/title>/, '<title>GRAPHEN — Graph-powered Reasoning Agentic Platform</title>');

fs.writeFileSync(path, content);
