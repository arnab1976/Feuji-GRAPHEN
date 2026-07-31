import React, { useState } from 'react';
import { Send, CornerDownLeft } from 'lucide-react';

export default function Ask() {
  const [activeTab, setActiveTab] = useState('graph');
  const [showAnswer, setShowAnswer] = useState(true); // Default to true to match demo state
  const [inputValue, setInputValue] = useState('');

  return (
    <div className="max-w-7xl mx-auto pb-12 animate-fade-in flex flex-col gap-6 h-[calc(100vh-100px)]">
      
      <div className="mb-2 shrink-0">
        <div className="inline-flex items-center gap-2 bg-[#7252A4]/10 text-[#a085d3] px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider mb-4 border border-[#7252A4]/20">
          <span className="w-1.5 h-1.5 rounded-full bg-[#7252A4]"></span>
          Graph-RAG Q&A
        </div>
        <h1 className="text-3xl font-bold text-text-primary mb-2">Ask Questions — Answers Grounded in the Graph</h1>
        <p className="text-[#588BFA] text-lg max-w-3xl leading-relaxed">
          Every answer is generated from a structured Cypher query against Neo4j, not from re-reading PDF text. 
          Click a graph node on the right to see exactly what was retrieved.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-0 flex-1">
        
        {/* Left Column: Chat Area */}
        <div className="flex flex-col gap-4">
          <div className="glass-panel flex-1 p-6 flex flex-col gap-6 overflow-y-auto min-h-0 custom-scrollbar">
            
            {/* System Greeting */}
            <div className="bg-[rgba(0,0,0,0.03)] border border-border-primary rounded-xl rounded-tl-none p-5 text-text-secondary self-start max-w-[90%] text-sm leading-relaxed">
              Hi — I'm grounded in your live lease knowledge graph (18 leases, 14 properties, 17 tenants). Ask me anything, or try a suggestion below.
            </div>

            {/* User Input Mock */}
            <div className="bg-[#588BFA] text-text-primary rounded-xl rounded-tr-none p-4 self-end max-w-[80%] text-sm font-medium shadow-[0_0_15px_rgba(88,139,250,0.15)]">
              Which leases expire in the next 90 days?
            </div>

            {/* System Answer Mock */}
            {showAnswer && (
              <div className="bg-[rgba(0,0,0,0.03)] border border-border-primary rounded-xl rounded-tl-none p-6 text-text-secondary self-start w-full text-sm leading-relaxed">
                <p className="text-text-primary font-bold mb-4 text-base">3 leases expire in the next 90 days:</p>
                <ul className="flex flex-col gap-3 mb-6">
                  <li><span className="text-text-primary font-bold">• Vantage Analytics</span> — 456 Commerce Blvd — expires 2026-08-11 (42 days) — 18,000 sqft</li>
                  <li><span className="text-text-primary font-bold">• Coastal Retail Group</span> — 456 Commerce Blvd — expires 2026-08-27 (58 days) — 6,500 sqft</li>
                  <li><span className="text-text-primary font-bold">• Brightline Legal</span> — 875 Riverfront Dr — expires 2026-09-14 (76 days) — 14,200 sqft</li>
                </ul>
                <p className="text-text-muted italic text-xs border-t border-border-primary pt-3">
                  Source: Neo4j Lease nodes, filtered by end_date.
                </p>
              </div>
            )}
          </div>

          {/* Input Box */}
          <div className="glass-panel p-2 flex items-center shrink-0">
            <input 
              type="text" 
              placeholder="Ask about properties, leases, or clauses..." 
              className="flex-1 bg-transparent border-none text-text-primary px-4 py-3 outline-none text-sm placeholder:text-text-muted"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
            />
            <button className="bg-[rgba(0,0,0,0.05)] hover:bg-[rgba(0,0,0,0.1)] text-text-secondary hover:text-text-primary p-3 rounded-lg transition-colors flex items-center gap-2 text-sm font-medium">
              <CornerDownLeft size={16} />
            </button>
          </div>
        </div>

        {/* Right Column: Context Tabs */}
        <div className="glass-panel flex flex-col min-h-0">
          <div className="flex items-center p-2 border-b border-border-primary shrink-0 gap-2">
            <button 
              className={`flex-1 py-2 text-sm font-medium rounded-lg transition-colors ${activeTab === 'graph' ? 'bg-[rgba(0,0,0,0.05)] text-text-primary' : 'text-text-secondary hover:text-text-primary'}`}
              onClick={() => setActiveTab('graph')}
            >
              Graph Context
            </button>
            <button 
              className={`flex-1 py-2 text-sm font-medium rounded-lg transition-colors ${activeTab === 'cypher' ? 'bg-[rgba(0,0,0,0.05)] text-text-primary' : 'text-text-secondary hover:text-text-primary'}`}
              onClick={() => setActiveTab('cypher')}
            >
              Raw Cypher Result
            </button>
          </div>

          <div className="flex-1 p-6 overflow-hidden relative">
            {activeTab === 'graph' ? (
              <div className="w-full h-full bg-[#0B0E14] rounded-lg border border-border-primary flex items-center justify-center relative overflow-hidden">
                {/* SVG Mockup of the local subgraph */}
                <svg viewBox="0 0 300 400" className="w-full h-full max-w-sm">
                  <g stroke="rgba(0,0,0,0.1)" strokeWidth="1">
                    <line x1="150" y1="50" x2="150" y2="100" />
                    <line x1="150" y1="100" x2="150" y2="150" />
                    <line x1="150" y1="150" x2="150" y2="200" />
                    <line x1="150" y1="200" x2="150" y2="250" />
                    <line x1="150" y1="250" x2="150" y2="300" />
                    <line x1="150" y1="300" x2="150" y2="350" />
                  </g>
                  
                  {/* Nodes */}
                  <circle cx="150" cy="50" r="12" fill="#588BFA" />
                  <text x="150" y="70" fill="white" fontSize="8" textAnchor="middle" className="font-mono opacity-70">875 Riverfron...</text>
                  
                  <circle cx="150" cy="100" r="12" fill="#7252A4" />
                  <text x="150" y="120" fill="white" fontSize="8" textAnchor="middle" className="font-mono opacity-70">LG-C317</text>
                  
                  <circle cx="150" cy="150" r="12" fill="#1FB16D" />
                  <text x="150" y="170" fill="white" fontSize="8" textAnchor="middle" className="font-mono opacity-70">Brightline Le...</text>
                  
                  <circle cx="150" cy="200" r="12" fill="#1FB16D" />
                  <text x="150" y="220" fill="white" fontSize="8" textAnchor="middle" className="font-mono opacity-70">Vantage Analy...</text>
                  
                  <circle cx="150" cy="250" r="12" fill="#7252A4" />
                  <text x="150" y="270" fill="white" fontSize="8" textAnchor="middle" className="font-mono opacity-70">LG-A192</text>
                  
                  <circle cx="150" cy="300" r="12" fill="#588BFA" />
                  <text x="150" y="320" fill="white" fontSize="8" textAnchor="middle" className="font-mono opacity-70">456 Commerce ...</text>
                </svg>
              </div>
            ) : (
              <div className="w-full h-full bg-[#0B0E14] rounded-lg border border-border-primary p-4 overflow-auto custom-scrollbar">
                <pre className="text-xs font-mono text-[#a085d3]">
                  <code dangerouslySetInnerHTML={{ __html: `[
  {
    "lease_id": "LG-C317",
    "property_name": "875 Riverfront Dr",
    "tenant_name": "Brightline Legal",
    "end_date": "2026-09-14",
    "sqft": 14200
  },
  {
    "lease_id": "LG-A192",
    "property_name": "456 Commerce Blvd",
    "tenant_name": "Vantage Analytics",
    "end_date": "2026-08-11",
    "sqft": 18000
  },
  {
    "lease_id": "LG-B841",
    "property_name": "456 Commerce Blvd",
    "tenant_name": "Coastal Retail Group",
    "end_date": "2026-08-27",
    "sqft": 6500
  }
]` }}>
                  </code>
                </pre>
              </div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}
