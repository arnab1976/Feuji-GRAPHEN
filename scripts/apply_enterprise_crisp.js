const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Enterprise Crisp Light Theme CSS Variables
content = content.replace(/--bg-0:\s*#[0-9a-fA-F]{6};/g, '--bg-0: #f4f7fc;');
content = content.replace(/--bg-1:\s*#[0-9a-fA-F]{6};/g, '--bg-1: #ffffff;');
content = content.replace(/--bg-2:\s*#[0-9a-fA-F]{6};/g, '--bg-2: #f8fafc;');
content = content.replace(/--bg-3:\s*#[0-9a-fA-F]{6};/g, '--bg-3: #e2e8f0;');
content = content.replace(/--line:\s*[^;]+;/g, '--line: rgba(0,0,0,0.1);');
content = content.replace(/--line-soft:\s*[^;]+;/g, '--line-soft: rgba(0,0,0,0.05);');

content = content.replace(/--tx-0:\s*#[0-9a-fA-F]{6};/g, '--tx-0: #0f172a;');
content = content.replace(/--tx-1:\s*#[0-9a-fA-F]{6};/g, '--tx-1: #334155;');
content = content.replace(/--tx-2:\s*#[0-9a-fA-F]{6};/g, '--tx-2: #64748b;');
content = content.replace(/--tx-3:\s*#[0-9a-fA-F]{6};/g, '--tx-3: #94a3b8;');

content = content.replace(/--blue:\s*#[0-9a-fA-F]{6};/g, '--blue: #2563eb;');
content = content.replace(/--blue-dim:\s*#[0-9a-fA-F]{6};/g, '--blue-dim: #dbeafe;');
content = content.replace(/--emerald:\s*#[0-9a-fA-F]{6};/g, '--emerald: #10b981;');
content = content.replace(/--emerald-dim:\s*#[0-9a-fA-F]{6};/g, '--emerald-dim: #d1fae5;');

// Also fix box shadows for the Enterprise Crisp look
content = content.replace(/box-shadow:\s*var\(--shadow\);/g, 'box-shadow: 0 10px 40px -10px rgba(0,0,0,0.08);');

// Remove/Replace "Lease" from everywhere
content = content.replace(/Leases/g, 'Documents');
content = content.replace(/leases/g, 'documents');
content = content.replace(/Lease/g, 'Document');
content = content.replace(/lease/g, 'document');

fs.writeFileSync(path, content);
