import React, { useMemo, useState, useRef, useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { RefreshCw, Zap, Download, Search } from 'lucide-react';

// Full demo graph matching the Live Graph Explorer visualization
const gData = {
  nodes: [
    // Properties
    { id: 'P1', label: '120 Innovation Drive', type: 'Property', group: 5, properties: { ID: 'P1', NAME: '120 Innovation Drive', CITY: 'Atlanta', TYPE: 'Office' } },
    { id: 'P2', label: '33 Peachtree Center', type: 'Property', group: 5, properties: { ID: 'P2', NAME: '33 Peachtree Center', CITY: 'Atlanta', TYPE: 'Office' } },
    { id: 'P3', label: '875 Riverfront Dr', type: 'Property', group: 5, properties: { ID: 'P3', NAME: '875 Riverfront Dr', CITY: 'Austin', TYPE: 'Office' } },
    { id: 'P4', label: '901 Lakeside Plaza', type: 'Property', group: 5, properties: { ID: 'P4', NAME: '901 Lakeside Plaza', CITY: 'Chicago', TYPE: 'Office' } },
    { id: 'P5', label: '1500 Tech Park Blvd', type: 'Property', group: 5, properties: { ID: 'P5', NAME: '1500 Tech Park Blvd', CITY: 'San Jose', TYPE: 'Office' } },
    { id: 'P6', label: '456 Commerce Blvd', type: 'Property', group: 5, properties: { ID: 'P6', NAME: '456 Commerce Blvd', CITY: 'Dallas', TYPE: 'Office' } },

    // Tenants
    { id: 'T1', label: 'Northgate Financial', type: 'Tenant', group: 2, properties: { ID: 'T1', NAME: 'Northgate Financial', INDUSTRY: 'Finance' } },
    { id: 'T2', label: 'Brightline Legal', type: 'Tenant', group: 2, properties: { ID: 'T2', NAME: 'Brightline Legal', INDUSTRY: 'Legal' } },
    { id: 'T3', label: 'Vantage Analytics', type: 'Tenant', group: 2, properties: { ID: 'T3', NAME: 'Vantage Analytics', INDUSTRY: 'Technology' } },
    { id: 'T4', label: 'Coastal Retail Group', type: 'Tenant', group: 2, properties: { ID: 'T4', NAME: 'Coastal Retail Group', INDUSTRY: 'Retail' } },

    // Leases
    { id: 'L1', label: 'LG-H845', type: 'Lease', group: 1, properties: { ID: 'LG-H845', PROP: 'P1', TENANT: 'T1', START: '2019-03-01', END: '2027-02-28', RENT: 28.5, SQFT: 11000 } },
    { id: 'L2', label: 'LG-D488', type: 'Lease', group: 1, properties: { ID: 'LG-D488', PROP: 'P2', TENANT: 'T1', START: '2020-09-01', END: '2028-09-27', RENT: 33.5, SQFT: 21000 } },
    { id: 'L3', label: 'LG-C317', type: 'Lease', group: 1, properties: { ID: 'LG-C317', PROP: 'P3', TENANT: 'T2', START: '2021-01-15', END: '2026-09-14', RENT: 41.0, SQFT: 14200 } },
    { id: 'L4', label: 'LG-E519', type: 'Lease', group: 1, properties: { ID: 'LG-E519', PROP: 'P4', TENANT: 'T3', START: '2018-06-01', END: '2029-05-31', RENT: 29.0, SQFT: 16800 } },
    { id: 'L5', label: 'LG-A192', type: 'Lease', group: 1, properties: { ID: 'LG-A192', PROP: 'P6', TENANT: 'T3', START: '2022-08-12', END: '2026-08-11', RENT: 36.25, SQFT: 18000 } },
    { id: 'L6', label: 'LG-F626', type: 'Lease', group: 1, properties: { ID: 'LG-F626', PROP: 'P5', TENANT: 'T3', START: '2020-04-01', END: '2028-03-31', RENT: 44.0, SQFT: 16000 } },
    { id: 'L7', label: 'LG-G731', type: 'Lease', group: 1, properties: { ID: 'LG-G731', PROP: 'P6', TENANT: 'T4', START: '2023-09-01', END: '2026-08-27', RENT: 31.0, SQFT: 6500 } },

    // Options (Renewal)
    { id: 'O1', label: '5yr option', type: 'Option', group: 3, properties: { TYPE: 'RenewalOption', TERM: '5 years', LEASE: 'LG-D488' } },
    { id: 'O2', label: '5yr option', type: 'Option', group: 3, properties: { TYPE: 'RenewalOption', TERM: '5 years', LEASE: 'LG-A192' } },
    { id: 'O3', label: '5yr option', type: 'Option', group: 3, properties: { TYPE: 'RenewalOption', TERM: '5 years', LEASE: 'LG-F626' } },

    // Clauses / Rights
    { id: 'C1', label: 'Exclusivity', type: 'Clause', group: 4, properties: { TYPE: 'Exclusivity', LEASE: 'LG-D488' } },
    { id: 'C2', label: 'Co-Tenancy', type: 'Clause', group: 4, properties: { TYPE: 'Co-Tenancy', LEASE: 'LG-C317' } },
    { id: 'C3', label: 'ROFR', type: 'Clause', group: 4, properties: { TYPE: 'Right of First Refusal', LEASE: 'LG-F626' } },
    { id: 'C4', label: 'Termination Right', type: 'Clause', group: 4, properties: { TYPE: 'TerminationRight', LEASE: 'LG-A192' } },
    { id: 'C5', label: 'Termination Right', type: 'Clause', group: 4, properties: { TYPE: 'TerminationRight', LEASE: 'LG-G731' } },
  ],
  links: [
    // Cluster 1 — Northgate
    { source: 'P1', target: 'L1', relationship: 'HAS_LEASE' },
    { source: 'L1', target: 'T1', relationship: 'SIGNED_BY' },
    { source: 'L2', target: 'T1', relationship: 'SIGNED_BY' },
    { source: 'P2', target: 'L2', relationship: 'HAS_LEASE' },
    { source: 'L2', target: 'O1', relationship: 'HAS_OPTION' },
    { source: 'L2', target: 'C1', relationship: 'HAS_CLAUSE' },

    // Cluster 2 — Brightline
    { source: 'P3', target: 'L3', relationship: 'HAS_LEASE' },
    { source: 'L3', target: 'T2', relationship: 'SIGNED_BY' },
    { source: 'L3', target: 'C2', relationship: 'HAS_CLAUSE' },

    // Cluster 3 — Vantage / Coastal
    { source: 'P4', target: 'L4', relationship: 'HAS_LEASE' },
    { source: 'L4', target: 'T3', relationship: 'SIGNED_BY' },
    { source: 'L5', target: 'T3', relationship: 'SIGNED_BY' },
    { source: 'L6', target: 'T3', relationship: 'SIGNED_BY' },
    { source: 'P6', target: 'L5', relationship: 'HAS_LEASE' },
    { source: 'L5', target: 'O2', relationship: 'HAS_OPTION' },
    { source: 'L5', target: 'C4', relationship: 'HAS_TERM_RIGHT' },
    { source: 'P5', target: 'L6', relationship: 'HAS_LEASE' },
    { source: 'L6', target: 'O3', relationship: 'HAS_OPTION' },
    { source: 'L6', target: 'C3', relationship: 'HAS_CLAUSE' },
    { source: 'P6', target: 'L7', relationship: 'HAS_LEASE' },
    { source: 'L7', target: 'T4', relationship: 'SIGNED_BY' },
    { source: 'L7', target: 'C5', relationship: 'HAS_TERM_RIGHT' },
  ],
};

const nodeColors = {
  1: '#7252A4', // Lease
  2: '#1FB16D', // Tenant
  3: '#FFB020', // Option
  4: '#f7768e', // Clause / Risk
  5: '#588BFA', // Property
};

const typeColors = {
  Property: '#588BFA',
  Tenant: '#1FB16D',
  Lease: '#7252A4',
  Option: '#FFB020',
  Clause: '#f7768e',
};

function resolveNodeId(ref) {
  return typeof ref === 'object' && ref !== null ? ref.id : ref;
}

function buildRelationshipRows(nodes, links) {
  const byId = Object.fromEntries(nodes.map((n) => [n.id, n]));
  return links.map((link, index) => {
    const sourceId = resolveNodeId(link.source);
    const targetId = resolveNodeId(link.target);
    const source = byId[sourceId];
    const target = byId[targetId];
    return {
      id: index + 1,
      sourceId,
      sourceLabel: source?.label ?? sourceId,
      sourceType: source?.type ?? '',
      relationship: link.relationship || 'RELATED_TO',
      targetId,
      targetLabel: target?.label ?? targetId,
      targetType: target?.type ?? '',
    };
  });
}

function toCsv(rows) {
  if (!rows.length) return '';
  const cols = [
    'id',
    'sourceId',
    'sourceLabel',
    'sourceType',
    'relationship',
    'targetId',
    'targetLabel',
    'targetType',
  ];
  const headers = [
    'ID',
    'Source ID',
    'Source',
    'Source Type',
    'Relationship',
    'Target ID',
    'Target',
    'Target Type',
  ];
  const esc = (v) => {
    const s = v == null ? '' : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [headers.join(','), ...rows.map((r) => cols.map((c) => esc(r[c])).join(','))].join('\n');
}

function downloadFile(filename, text, mime) {
  const blob = new Blob([text], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function TypeBadge({ type }) {
  const color = typeColors[type] || '#8B949E';
  return (
    <span
      className="inline-block px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider"
      style={{ backgroundColor: `${color}20`, color }}
    >
      {type}
    </span>
  );
}

export default function KnowledgeGraph() {
  const fgRef = useRef();
  const [selectedNode, setSelectedNode] = useState(gData.nodes.find((n) => n.id === 'L2') || gData.nodes[0]);
  const [searchTerm, setSearchTerm] = useState('');

  const relationshipRows = useMemo(
    () => buildRelationshipRows(gData.nodes, gData.links),
    []
  );

  const filteredRows = useMemo(() => {
    const q = searchTerm.trim().toLowerCase();
    if (!q) return relationshipRows;
    return relationshipRows.filter((r) =>
      [r.sourceLabel, r.sourceType, r.relationship, r.targetLabel, r.targetType]
        .join(' ')
        .toLowerCase()
        .includes(q)
    );
  }, [relationshipRows, searchTerm]);

  const handleNodeClick = useCallback((node) => {
    setSelectedNode(node);
    if (fgRef.current) {
      fgRef.current.centerAt(node.x, node.y, 1000);
      fgRef.current.zoom(8, 2000);
    }
  }, []);

  const handleReset = () => {
    if (fgRef.current) fgRef.current.zoomToFit(400, 50);
  };

  const handleRelayout = () => {
    if (fgRef.current) fgRef.current.d3ReheatSimulation();
  };

  const handleDownloadCsv = () => {
    downloadFile('knowledge_graph_relationships.csv', toCsv(relationshipRows), 'text/csv;charset=utf-8');
  };

  const handleDownloadJson = () => {
    downloadFile(
      'knowledge_graph_relationships.json',
      JSON.stringify(relationshipRows, null, 2),
      'application/json'
    );
  };

  return (
    <div className="max-w-7xl mx-auto pb-12 animate-fade-in flex flex-col gap-6">
      <div className="mb-2 shrink-0">
        <div className="inline-flex items-center gap-2 bg-[#7252A4]/10 text-[#a085d3] px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider mb-4 border border-[#7252A4]/20">
          <span className="w-1.5 h-1.5 rounded-full bg-[#7252A4]"></span>
          Ontology-Driven Knowledge Graph
        </div>
        <h1 className="text-3xl font-bold text-text-primary mb-2">Live Graph Explorer</h1>
        <p className="text-text-secondary text-lg max-w-4xl">
          The actual Neo4j graph, rendered live. Drag nodes, click to inspect properties — this is the structured foundation every AI answer is grounded in.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 min-h-[520px] h-[calc(100vh-220px)]">
        {/* Graph Canvas */}
        <div className="lg:col-span-3 glass-panel relative overflow-hidden flex flex-col">
          <div className="absolute top-4 left-4 z-10 flex gap-2">
            <button
              onClick={handleReset}
              className="flex items-center gap-2 px-4 py-2 bg-[rgba(0,0,0,0.05)] hover:bg-[rgba(0,0,0,0.1)] border border-border-primary rounded-lg text-sm text-text-primary transition-colors"
            >
              <RefreshCw size={14} /> Reset View
            </button>
            <button
              onClick={handleRelayout}
              className="flex items-center gap-2 px-4 py-2 bg-[rgba(0,0,0,0.05)] hover:bg-[rgba(0,0,0,0.1)] border border-border-primary rounded-lg text-sm text-text-primary transition-colors"
            >
              <Zap size={14} className="text-[#FFB020]" /> Re-layout
            </button>
          </div>

          <div className="absolute bottom-4 left-4 z-10 flex flex-wrap gap-3 text-xs text-text-secondary bg-[rgba(11,14,20,0.85)] border border-black/ rounded-lg px-3 py-2">
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full" style={{ background: nodeColors[5] }} /> Property</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full" style={{ background: nodeColors[2] }} /> Tenant</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full" style={{ background: nodeColors[1] }} /> Lease</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full" style={{ background: nodeColors[3] }} /> Option</span>
            <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full" style={{ background: nodeColors[4] }} /> Clause</span>
          </div>

          <div className="flex-1 w-full bg-[#0B0E14] cursor-crosshair">
            <ForceGraph2D
              ref={fgRef}
              graphData={gData}
              nodeLabel="label"
              nodeColor={(node) => nodeColors[node.group]}
              nodeRelSize={6}
              linkColor={() => 'rgba(0,0,0,0.2)'}
              linkWidth={1}
              onNodeClick={handleNodeClick}
              cooldownTicks={100}
              onEngineStop={() => fgRef.current && fgRef.current.zoomToFit(400, 50)}
              nodeCanvasObject={(node, ctx, globalScale) => {
                const label = node.label;
                const fontSize = 12 / globalScale;
                ctx.font = `${fontSize}px "IBM Plex Mono", monospace`;

                ctx.fillStyle = nodeColors[node.group];
                ctx.beginPath();
                ctx.arc(node.x, node.y, node.group === 5 ? 8 : 6, 0, 2 * Math.PI, false);
                ctx.fill();

                if (selectedNode && selectedNode.id === node.id) {
                  ctx.lineWidth = 2;
                  ctx.strokeStyle = 'white';
                  ctx.stroke();
                }

                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillStyle = 'rgba(0,0,0,0.7)';
                ctx.fillText(label, node.x, node.y + 12);
              }}
            />
          </div>
        </div>

        {/* Node Inspector */}
        <div className="glass-panel p-6 flex flex-col overflow-y-auto custom-scrollbar">
          {selectedNode ? (
            <div className="animate-fade-in">
              <div className="mb-6">
                <span
                  className="inline-block px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider mb-3"
                  style={{
                    backgroundColor: `${nodeColors[selectedNode.group]}20`,
                    color: nodeColors[selectedNode.group],
                  }}
                >
                  {selectedNode.type}
                </span>
                <h2 className="text-xl font-bold text-text-primary">{selectedNode.label}</h2>
              </div>

              <div className="flex flex-col gap-4">
                {selectedNode.properties ? (
                  Object.entries(selectedNode.properties).map(([key, value]) => (
                    <div key={key} className="border-b border-border-primary/50 pb-3 last:border-0">
                      <div className="text-[10px] uppercase tracking-wider text-text-muted mb-1 font-bold">{key}</div>
                      <div className="text-sm text-text-primary font-mono">{value}</div>
                    </div>
                  ))
                ) : (
                  <div className="text-sm text-text-muted italic">No properties available for this node.</div>
                )}
              </div>
            </div>
          ) : (
            <div className="flex-1 flex items-center justify-center text-text-muted text-sm italic text-center">
              Click a node in the graph to inspect its properties.
            </div>
          )}
        </div>
      </div>

      {/* Full Relationship Table */}
      <div className="glass-panel p-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <div>
            <h2 className="text-xl font-bold text-text-primary m-0">Relationship Table</h2>
            <p className="text-text-secondary text-sm mt-1">
              Complete edge list from the knowledge graph ({relationshipRows.length} relationships)
            </p>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              onClick={handleDownloadCsv}
              className="flex items-center gap-2 px-4 py-2 bg-[#588BFA] hover:bg-[#4a7ae8] rounded-lg text-sm text-text-primary font-medium transition-colors"
            >
              <Download size={14} /> Download CSV
            </button>
            <button
              onClick={handleDownloadJson}
              className="flex items-center gap-2 px-4 py-2 bg-[rgba(0,0,0,0.05)] hover:bg-[rgba(0,0,0,0.1)] border border-black/ rounded-lg text-sm text-text-primary transition-colors"
            >
              <Download size={14} /> Download JSON
            </button>
          </div>
        </div>

        <div className="relative mb-4 max-w-md">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" size={16} />
          <input
            type="text"
            placeholder="Filter by source, target, type, or relationship..."
            className="w-full bg-[rgba(0,0,0,0.03)] border border-black/ rounded-lg py-2 pl-10 pr-4 text-text-primary text-sm focus:outline-none focus:border-[#588BFA] transition-colors"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        <div className="overflow-x-auto max-h-[420px] overflow-y-auto custom-scrollbar">
          <table className="w-full text-left text-sm text-text-secondary border-collapse">
            <thead className="sticky top-0 bg-[#11141D] z-10">
              <tr className="border-b border-black/ text-xs uppercase tracking-wider text-text-muted">
                <th className="py-3 px-3 font-medium">#</th>
                <th className="py-3 px-3 font-medium">Source</th>
                <th className="py-3 px-3 font-medium">Source Type</th>
                <th className="py-3 px-3 font-medium">Relationship</th>
                <th className="py-3 px-3 font-medium">Target</th>
                <th className="py-3 px-3 font-medium">Target Type</th>
              </tr>
            </thead>
            <tbody>
              {filteredRows.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-text-muted">
                    No relationships match your filter.
                  </td>
                </tr>
              ) : (
                filteredRows.map((row) => (
                  <tr
                    key={row.id}
                    className="border-b border-white/5 hover:bg-[rgba(0,0,0,0.02)] transition-colors"
                  >
                    <td className="py-3 px-3 font-mono text-text-muted">{row.id}</td>
                    <td className="py-3 px-3 text-text-primary font-medium">{row.sourceLabel}</td>
                    <td className="py-3 px-3"><TypeBadge type={row.sourceType} /></td>
                    <td className="py-3 px-3">
                      <span className="inline-block px-2 py-0.5 rounded text-[11px] font-mono bg-[#7252A4]/15 text-[#a085d3] border border-[#7252A4]/25">
                        {row.relationship}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-text-primary font-medium">{row.targetLabel}</td>
                    <td className="py-3 px-3"><TypeBadge type={row.targetType} /></td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
