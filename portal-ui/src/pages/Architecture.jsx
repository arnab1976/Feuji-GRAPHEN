import React from 'react';
import { Layers, Database, Cpu, Search, Layout } from 'lucide-react';

export default function Architecture() {
  return (
    <div className="max-w-7xl mx-auto pb-12 animate-fade-in flex flex-col gap-6">
      
      <div className="mb-4">
        <div className="inline-flex items-center gap-2 bg-[#7252A4]/10 text-[#a085d3] px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider mb-4 border border-[#7252A4]/20">
          <Layers size={14} />
          System Architecture
        </div>
        <h1 className="text-3xl font-bold text-text-primary mb-2">Open-Source Knowledge Graph Stack</h1>
        <p className="text-text-secondary text-lg">
          End-to-end pipeline from PDF ingestion to graph-grounded LLM answers.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Column: Stack Layers */}
        <div className="lg:col-span-1 flex flex-col gap-3">
          <div className="glass-panel p-4 flex items-center gap-4 relative overflow-hidden group">
            <div className="w-12 h-12 rounded bg-[rgba(0,0,0,0.05)] flex items-center justify-center text-text-muted group-hover:text-text-primary transition-colors">
              <Layout size={24} />
            </div>
            <div>
              <h3 className="font-bold text-text-primary text-sm">5. Application</h3>
              <p className="text-xs text-text-secondary">React / Vite UI</p>
            </div>
            <div className="absolute left-0 top-0 w-1 h-full bg-[#588BFA]"></div>
          </div>

          <div className="flex justify-center -my-2 relative z-10 text-text-muted">
            <div className="w-px h-6 bg-border-primary"></div>
          </div>

          <div className="glass-panel p-4 flex items-center gap-4 relative overflow-hidden group">
            <div className="w-12 h-12 rounded bg-[rgba(0,0,0,0.05)] flex items-center justify-center text-text-muted group-hover:text-[#FFB020] transition-colors">
              <Search size={24} />
            </div>
            <div>
              <h3 className="font-bold text-text-primary text-sm">4. Intelligence</h3>
              <p className="text-xs text-text-secondary">Agents & GraphRAG</p>
            </div>
            <div className="absolute left-0 top-0 w-1 h-full bg-[#FFB020]"></div>
          </div>

          <div className="flex justify-center -my-2 relative z-10 text-text-muted">
            <div className="w-px h-6 bg-border-primary"></div>
          </div>

          <div className="glass-panel p-4 flex items-center gap-4 relative overflow-hidden group">
            <div className="w-12 h-12 rounded bg-[rgba(0,0,0,0.05)] flex items-center justify-center text-text-muted group-hover:text-[#1FB16D] transition-colors">
              <Database size={24} />
            </div>
            <div>
              <h3 className="font-bold text-text-primary text-sm">3. Knowledge Graph</h3>
              <p className="text-xs text-text-secondary">Neo4j Database</p>
            </div>
            <div className="absolute left-0 top-0 w-1 h-full bg-[#1FB16D]"></div>
          </div>

          <div className="flex justify-center -my-2 relative z-10 text-text-muted">
            <div className="w-px h-6 bg-border-primary"></div>
          </div>

          <div className="glass-panel p-4 flex items-center gap-4 relative overflow-hidden group">
            <div className="w-12 h-12 rounded bg-[rgba(0,0,0,0.05)] flex items-center justify-center text-text-muted group-hover:text-[#00E5FF] transition-colors">
              <Cpu size={24} />
            </div>
            <div>
              <h3 className="font-bold text-text-primary text-sm">2. Processing</h3>
              <p className="text-xs text-text-secondary">FastAPI + NLP Models</p>
            </div>
            <div className="absolute left-0 top-0 w-1 h-full bg-[#00E5FF]"></div>
          </div>
          
          <div className="flex justify-center -my-2 relative z-10 text-text-muted">
            <div className="w-px h-6 bg-border-primary"></div>
          </div>

          <div className="glass-panel p-4 flex items-center gap-4 relative overflow-hidden group">
            <div className="w-12 h-12 rounded bg-[rgba(0,0,0,0.05)] flex items-center justify-center text-text-muted group-hover:text-[#7252A4] transition-colors">
              <Layers size={24} />
            </div>
            <div>
              <h3 className="font-bold text-text-primary text-sm">1. Ingestion</h3>
              <p className="text-xs text-text-secondary">PDF Parsing Pipeline</p>
            </div>
            <div className="absolute left-0 top-0 w-1 h-full bg-[#7252A4]"></div>
          </div>
        </div>

        {/* Right Column: Stack Details */}
        <div className="lg:col-span-2">
          <div className="glass-panel p-8 h-full">
            <h3 className="text-xl font-bold text-text-primary mb-6">Core Technologies</h3>
            
            <div className="grid grid-cols-2 gap-6">
              
              <div className="p-4 rounded-lg bg-[rgba(0,0,0,0.02)] border border-border-primary">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 rounded-full bg-[#1FB16D]"></div>
                  <h4 className="font-bold text-text-primary">Neo4j</h4>
                </div>
                <p className="text-sm text-text-secondary">
                  The primary data store. Represents leases, properties, tenants, and clauses as interconnected nodes and relationships for highly traversable data retrieval.
                </p>
              </div>

              <div className="p-4 rounded-lg bg-[rgba(0,0,0,0.02)] border border-border-primary">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 rounded-full bg-[#FFB020]"></div>
                  <h4 className="font-bold text-text-primary">Groq / Llama-3</h4>
                </div>
                <p className="text-sm text-text-secondary">
                  Ultra-fast LLM inference. Used for parsing unstructured PDF text into structured JSON, and generating natural language answers from graph context.
                </p>
              </div>

              <div className="p-4 rounded-lg bg-[rgba(0,0,0,0.02)] border border-border-primary">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 rounded-full bg-[#00E5FF]"></div>
                  <h4 className="font-bold text-text-primary">FastAPI</h4>
                </div>
                <p className="text-sm text-text-secondary">
                  The Python backend framework orchestrating the ingestion pipeline, graph queries (Cypher), and LLM agent chains.
                </p>
              </div>

              <div className="p-4 rounded-lg bg-[rgba(0,0,0,0.02)] border border-border-primary">
                <div className="flex items-center gap-2 mb-3">
                  <div className="w-2 h-2 rounded-full bg-[#588BFA]"></div>
                  <h4 className="font-bold text-text-primary">React + Vite</h4>
                </div>
                <p className="text-sm text-text-secondary">
                  The high-fidelity frontend portal. Uses modern glassmorphism UI, interactive force-directed graphs, and real-time state management.
                </p>
              </div>

            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
