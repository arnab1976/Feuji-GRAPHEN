const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Sunset Glass Theme CSS Variables
content = content.replace(/--bg-0:\s*[^;]+;/g, '--bg-0: #FFF5F3;'); // Warm off-white
content = content.replace(/--bg-1:\s*[^;]+;/g, '--bg-1: #FFFFFF;'); // White panel
content = content.replace(/--bg-2:\s*[^;]+;/g, '--bg-2: #FFF0ED;'); 
content = content.replace(/--bg-3:\s*[^;]+;/g, '--bg-3: #FFE4DE;');

content = content.replace(/--line:\s*[^;]+;/g, '--line: rgba(255, 77, 109, 0.15);'); // Soft pink line
content = content.replace(/--line-soft:\s*[^;]+;/g, '--line-soft: rgba(255, 77, 109, 0.05);');

content = content.replace(/--tx-0:\s*[^;]+;/g, '--tx-0: #1C1917;'); // Espresso black
content = content.replace(/--tx-1:\s*[^;]+;/g, '--tx-1: #44403C;');
content = content.replace(/--tx-2:\s*[^;]+;/g, '--tx-2: #78716C;');
content = content.replace(/--tx-3:\s*[^;]+;/g, '--tx-3: #A8A29E;');

// Map the old "blue" to the new primary Coral Pink
content = content.replace(/--blue:\s*[^;]+;/g, '--blue: #FF4D6D;'); 
content = content.replace(/--blue-dim:\s*[^;]+;/g, '--blue-dim: #FFE4E8;'); 

// Map the old "emerald" to Golden Amber
content = content.replace(/--emerald:\s*[^;]+;/g, '--emerald: #FFB703;'); 
content = content.replace(/--emerald-dim:\s*[^;]+;/g, '--emerald-dim: #FFF5D6;'); 

// Box shadow replacement to soft pink/warm shadow
content = content.replace(/box-shadow:\s*0\s*0\s*20px\s*rgba[^;]+;/g, 'box-shadow: 0 10px 40px -10px rgba(255, 77, 109, 0.1);');
content = content.replace(/box-shadow:\s*0\s*10px\s*40px\s*-10px\s*rgba[^;]+;/g, 'box-shadow: 0 10px 40px -10px rgba(255, 77, 109, 0.1);');

fs.writeFileSync(path, content);
