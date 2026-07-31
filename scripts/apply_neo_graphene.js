const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Neo-Graphene Dark Theme CSS Variables
content = content.replace(/--bg-0:\s*[^;]+;/g, '--bg-0: #050814;');
content = content.replace(/--bg-1:\s*[^;]+;/g, '--bg-1: #0A0F24;'); // Dark translucent panel base
content = content.replace(/--bg-2:\s*[^;]+;/g, '--bg-2: #121A33;');
content = content.replace(/--bg-3:\s*[^;]+;/g, '--bg-3: #1A2447;');

content = content.replace(/--line:\s*[^;]+;/g, '--line: rgba(0, 229, 255, 0.2);'); // Glowing cyan border
content = content.replace(/--line-soft:\s*[^;]+;/g, '--line-soft: rgba(255, 255, 255, 0.05);');

content = content.replace(/--tx-0:\s*[^;]+;/g, '--tx-0: #FFFFFF;');
content = content.replace(/--tx-1:\s*[^;]+;/g, '--tx-1: #E2E8F0;');
content = content.replace(/--tx-2:\s*[^;]+;/g, '--tx-2: #94A3B8;');
content = content.replace(/--tx-3:\s*[^;]+;/g, '--tx-3: #64748B;');

content = content.replace(/--blue:\s*[^;]+;/g, '--blue: #00E5FF;'); // Electric Cyan
content = content.replace(/--blue-dim:\s*[^;]+;/g, '--blue-dim: #00333D;'); // Very dark cyan
content = content.replace(/--emerald:\s*[^;]+;/g, '--emerald: #7B61FF;'); // Neon purple for contrast instead of green if we want
content = content.replace(/--emerald-dim:\s*[^;]+;/g, '--emerald-dim: #291A54;'); // Dark neon purple

// Re-adjust box shadows for dark glow instead of light shadow
content = content.replace(/box-shadow: 0 10px 40px -10px rgba\(0,0,0,0.08\);/g, 'box-shadow: 0 0 20px rgba(0, 229, 255, 0.05);');

fs.writeFileSync(path, content);
