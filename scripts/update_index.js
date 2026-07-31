const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Replace Text
content = content.replace(/LeaseGuard/g, 'GRAPHEN');
content = content.replace(/Lease intelligence, <span class="text-transparent bg-clip-text bg-gradient-to-r from-\[#588BFA\] to-\[#00E5FF\]">grounded in a graph<\/span> — not a guess\./g, 'GRAPHEN');
content = content.replace(/Knowledge Graph Lease Intelligence/g, 'Graph-powered Reasoning Agentic Platform for Hierarchical Enterprise Networks');
content = content.replace(/GRAPHEN reads commercial lease PDFs, builds a live ontology-driven\s+knowledge graph of every property, tenant, clause and obligation, then\s+answers questions with AI that cites the exact graph nodes behind every claim\./g, '"One query thin. Infinitely strong. Inspired by the world\'s strongest material."');

// Replace dark theme CSS with light theme
content = content.replace(/--bg-base:\s*#[0-9a-fA-F]{6};/g, '--bg-base: #f0f7ff;');
content = content.replace(/--bg-surface:\s*#[0-9a-fA-F]{6};/g, '--bg-surface: #ffffff;');
content = content.replace(/--bg-surface-elevated:\s*#[0-9a-fA-F]{6};/g, '--bg-surface-elevated: #f8fafc;');
content = content.replace(/--bg-panel:\s*#[0-9a-fA-F]{6};/g, '--bg-panel: #ffffff;');
content = content.replace(/--text-primary:\s*#[0-9a-fA-F]{6};/g, '--text-primary: #1e293b;');
content = content.replace(/--text-secondary:\s*#[0-9a-fA-F]{6};/g, '--text-secondary: #475569;');
content = content.replace(/--text-muted:\s*#[0-9a-fA-F]{6};/g, '--text-muted: #94a3b8;');
content = content.replace(/--border-light:\s*rgba\([^)]+\);/g, '--border-light: rgba(0, 0, 0, 0.08);');
content = content.replace(/--border-glow:\s*rgba\([^)]+\);/g, '--border-glow: rgba(88, 139, 250, 0.2);');
content = content.replace(/--shadow-panel:\s*[^;]+;/g, '--shadow-panel: 0 4px 12px rgba(0, 0, 0, 0.05);');

// Change text-white to text-text-primary inside the HTML string
content = content.replace(/text-white/g, 'text-text-primary');

// Specific replacements for rgba borders/bg in HTML strings
content = content.replace(/rgba\(255,255,255,/g, 'rgba(0,0,0,');
content = content.replace(/white\/10/g, 'black/10');
content = content.replace(/white\/20/g, 'black/20');

// Header G logo fix
content = content.replace(/>LG</g, '>G<');

fs.writeFileSync(path, content);
