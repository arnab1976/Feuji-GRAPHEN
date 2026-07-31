import React from 'react';

export default function Sidebar() {
  return (
    <aside className="sidebar flex flex-col gap-8 text-sm">
      
      {/* Portfolio Snapshot */}
      <div>
        <h3 className="text-xs font-bold text-text-muted tracking-wider mb-4 uppercase">Portfolio Snapshot</h3>
        <ul className="flex flex-col gap-3">
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>Leases</span>
            <span className="font-bold text-text-primary">18</span>
          </li>
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>Properties</span>
            <span className="font-bold text-text-primary">14</span>
          </li>
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>Tenants</span>
            <span className="font-bold text-text-primary">17</span>
          </li>
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>Total Sqft</span>
            <span className="font-bold text-text-primary">412,800</span>
          </li>
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>Avg Rent PSF</span>
            <span className="font-bold text-text-primary">$38.40</span>
          </li>
        </ul>
      </div>

      {/* Risk Signals */}
      <div>
        <h3 className="text-xs font-bold text-text-muted tracking-wider mb-4 uppercase">Risk Signals</h3>
        <ul className="flex flex-col gap-3">
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>Expiring ≤90d</span>
            <span className="font-bold text-accent-warning">3</span>
          </li>
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>High-risk clauses</span>
            <span className="font-bold text-accent-warning">5</span>
          </li>
          <li className="flex justify-between items-center text-text-secondary hover:text-text-primary transition-colors cursor-default">
            <span>Concentration flag</span>
            <span className="font-bold text-accent-warning">1</span>
          </li>
        </ul>
        {/* Decorative bar */}
        <div className="h-1 w-full bg-black/ rounded mt-4 overflow-hidden flex">
          <div className="h-full bg-accent-secondary w-1/3"></div>
        </div>
      </div>

      {/* Free Stack */}
      <div>
        <h3 className="text-xs font-bold text-text-muted tracking-wider mb-4 uppercase">Free Stack</h3>
        <div className="flex flex-wrap gap-2">
          <span className="px-2 py-1 bg-[#151923] border border-white/5 rounded text-xs text-text-secondary flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-[#588BFA]"></div>Neo4j</span>
          <span className="px-2 py-1 bg-[#151923] border border-white/5 rounded text-xs text-text-secondary flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-[#1FB16D]"></div>ChromaDB</span>
          <span className="px-2 py-1 bg-[#151923] border border-white/5 rounded text-xs text-text-secondary flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-[#7252A4]"></div>spaCy</span>
          <span className="px-2 py-1 bg-[#151923] border border-white/5 rounded text-xs text-text-secondary flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-[#FFB020]"></div>Groq</span>
          <span className="px-2 py-1 bg-[#151923] border border-white/5 rounded text-xs text-text-secondary flex items-center gap-1.5"><div className="w-1.5 h-1.5 rounded-full bg-[#00E5FF]"></div>Ollama</span>
        </div>
      </div>

      {/* Session */}
      <div className="mt-auto">
        <h3 className="text-xs font-bold text-text-muted tracking-wider mb-4 uppercase">Session</h3>
        <ul className="flex flex-col gap-3">
          <li className="flex justify-between items-center text-text-secondary">
            <span>LLM calls</span>
            <span className="font-bold text-text-primary">1</span>
          </li>
          <li className="flex justify-between items-center text-text-secondary">
            <span>Est. cost</span>
            <span className="font-bold text-accent-success">$0.00</span>
          </li>
        </ul>
      </div>

    </aside>
  );
}
