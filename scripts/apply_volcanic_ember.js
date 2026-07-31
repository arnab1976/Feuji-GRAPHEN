const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Volcanic Ember Theme CSS Variables
content = content.replace(/--bg-0:\s*[^;]+;/g, '--bg-0: #120907;'); 
content = content.replace(/--bg-1:\s*[^;]+;/g, '--bg-1: #1A0C0A;'); 
content = content.replace(/--bg-2:\s*[^;]+;/g, '--bg-2: #24110E;');
content = content.replace(/--bg-3:\s*[^;]+;/g, '--bg-3: #361A15;');

content = content.replace(/--line:\s*[^;]+;/g, '--line: rgba(255, 51, 0, 0.25);'); 
content = content.replace(/--line-soft:\s*[^;]+;/g, '--line-soft: rgba(255, 51, 0, 0.1);');

content = content.replace(/--tx-0:\s*[^;]+;/g, '--tx-0: #FFECE8;'); 
content = content.replace(/--tx-1:\s*[^;]+;/g, '--tx-1: #FFC2B5;');
content = content.replace(/--tx-2:\s*[^;]+;/g, '--tx-2: #F78E77;');
content = content.replace(/--tx-3:\s*[^;]+;/g, '--tx-3: #C2563F;');

// Map the old "blue" to the new primary Deep Red-Orange
content = content.replace(/--blue:\s*[^;]+;/g, '--blue: #FF3300;');
content = content.replace(/--blue-dim:\s*[^;]+;/g, '--blue-dim: #4D0F00;');

// Map the old "emerald" to Dark Orange/Amber
content = content.replace(/--emerald:\s*[^;]+;/g, '--emerald: #FF8C00;');
content = content.replace(/--emerald-dim:\s*[^;]+;/g, '--emerald-dim: #4D2A00;');

// Box shadow replacement to volcanic glow
content = content.replace(/box-shadow:\s*0\s*0\s*20px\s*rgba[^;]+;/g, 'box-shadow: 0 0 20px rgba(255, 51, 0, 0.15);');
content = content.replace(/box-shadow:\s*0\s*10px\s*40px\s*-10px\s*rgba[^;]+;/g, 'box-shadow: 0 0 20px rgba(255, 51, 0, 0.15);');

fs.writeFileSync(path, content);
