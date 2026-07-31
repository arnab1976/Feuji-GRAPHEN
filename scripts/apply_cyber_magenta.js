const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Cyber-Magenta Theme CSS Variables
content = content.replace(/--bg-0:\s*[^;]+;/g, '--bg-0: #1F0E1C;'); // Deep plum/eggplant
content = content.replace(/--bg-1:\s*[^;]+;/g, '--bg-1: #2D1B2E;'); // Rich dark magenta-black panel
content = content.replace(/--bg-2:\s*[^;]+;/g, '--bg-2: #3E2440;');
content = content.replace(/--bg-3:\s*[^;]+;/g, '--bg-3: #523154;');

content = content.replace(/--line:\s*[^;]+;/g, '--line: rgba(255, 0, 127, 0.25);'); // Neon pink line
content = content.replace(/--line-soft:\s*[^;]+;/g, '--line-soft: rgba(255, 0, 127, 0.1);');

content = content.replace(/--tx-0:\s*[^;]+;/g, '--tx-0: #F3E8FF;'); // Icy white/pink-gray
content = content.replace(/--tx-1:\s*[^;]+;/g, '--tx-1: #D8B4E2;');
content = content.replace(/--tx-2:\s*[^;]+;/g, '--tx-2: #B386C1;');
content = content.replace(/--tx-3:\s*[^;]+;/g, '--tx-3: #8C5B9E;');

// Map the old "blue" to the new primary Neon Pink
content = content.replace(/--blue:\s*[^;]+;/g, '--blue: #FF007F;');
content = content.replace(/--blue-dim:\s*[^;]+;/g, '--blue-dim: #4D0026;');

// Map the old "emerald" to Electric Orange
content = content.replace(/--emerald:\s*[^;]+;/g, '--emerald: #FF7300;');
content = content.replace(/--emerald-dim:\s*[^;]+;/g, '--emerald-dim: #4D2300;');

// Box shadow replacement to cyberpunk neon pink glow
content = content.replace(/box-shadow:\s*0\s*0\s*20px\s*rgba[^;]+;/g, 'box-shadow: 0 0 20px rgba(255, 0, 127, 0.15);');
content = content.replace(/box-shadow:\s*0\s*10px\s*40px\s*-10px\s*rgba[^;]+;/g, 'box-shadow: 0 0 20px rgba(255, 0, 127, 0.15);');

fs.writeFileSync(path, content);
