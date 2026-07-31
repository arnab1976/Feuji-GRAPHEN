const fs = require('fs');
const path = 'c:/CBRE_Ontology/index.html';
let content = fs.readFileSync(path, 'utf8');

// Material Theme CSS Variables
content = content.replace(/--bg-0:\s*[^;]+;/g, '--bg-0: #FAFAFA;');
content = content.replace(/--bg-1:\s*[^;]+;/g, '--bg-1: #FFFFFF;');
content = content.replace(/--bg-2:\s*[^;]+;/g, '--bg-2: #F5F5F5;');
content = content.replace(/--bg-3:\s*[^;]+;/g, '--bg-3: #E0E0E0;');

content = content.replace(/--line:\s*[^;]+;/g, '--line: rgba(0, 0, 0, 0.12);');
content = content.replace(/--line-soft:\s*[^;]+;/g, '--line-soft: rgba(0, 0, 0, 0.06);');

content = content.replace(/--tx-0:\s*[^;]+;/g, '--tx-0: #212121;');
content = content.replace(/--tx-1:\s*[^;]+;/g, '--tx-1: #424242;');
content = content.replace(/--tx-2:\s*[^;]+;/g, '--tx-2: #757575;');
content = content.replace(/--tx-3:\s*[^;]+;/g, '--tx-3: #9E9E9E;');

content = content.replace(/--blue:\s*[^;]+;/g, '--blue: #1976D2;');
content = content.replace(/--blue-dim:\s*[^;]+;/g, '--blue-dim: #BBDEFB;');

content = content.replace(/--emerald:\s*[^;]+;/g, '--emerald: #388E3C;');
content = content.replace(/--emerald-dim:\s*[^;]+;/g, '--emerald-dim: #C8E6C9;');

content = content.replace(/box-shadow:\s*0\s*0\s*20px\s*rgba[^;]+;/g, 'box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);');
content = content.replace(/box-shadow:\s*0\s*10px\s*40px\s*-10px\s*rgba[^;]+;/g, 'box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);');
content = content.replace(/box-shadow:\s*0\s*2px\s*8px\s*rgba[^;]+;/g, 'box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);');

fs.writeFileSync(path, content);
