import React from 'react';
import { LayoutDashboard, Settings } from 'lucide-react';
import { Link } from 'react-router-dom';

/**
 * GRAPHEN home page.
 * The hero is a single relevant "context image" (public/graphen-overview.svg)
 * that communicates the whole application end-to-end:
 *   Lease PDFs -> NER + LLM extraction -> Neo4j Knowledge Graph
 *   -> Graph-RAG grounded reasoning -> Ask AI / Risk / Graph Explorer
 * It fills ~70% of the page, leaving ~30% breathing room.
 *
 * NOTE: this project has no Tailwind build, so everything here uses inline
 * styles to guarantee the layout and image actually render.
 */
export default function Overview() {
  return (
    <div style={{ maxWidth: 1440, margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

      {/* Title strip — part of the ~30% breathing room */}
      <div style={{ display: 'flex', alignItems: 'flex-end', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8, marginBottom: 8,
            padding: '4px 10px', borderRadius: 999, background: 'rgba(88,139,250,0.10)',
            color: '#588BFA', fontSize: 11, fontWeight: 600, letterSpacing: '0.04em', textTransform: 'uppercase',
          }}>
            <span style={{ width: 6, height: 6, borderRadius: '50%', background: '#1FB16D' }} />
            Live knowledge-graph intelligence
          </div>
          <h1 style={{
            fontSize: '2.15rem', lineHeight: 1.15, fontWeight: 800, margin: 0, letterSpacing: '-0.01em',
            background: 'linear-gradient(90deg,#588BFA,#7252A4)', WebkitBackgroundClip: 'text',
            backgroundClip: 'text', color: 'transparent',
          }}>
            Experience GRAPHEN
          </h1>
          <p style={{ color: '#475569', fontSize: 14, marginTop: 4 }}>
            Graph-powered Reasoning Agentic Platform for Hierarchical Enterprise Networks
          </p>
        </div>
        <div style={{ display: 'flex', gap: 12 }}>
          <Link to="/dashboard" style={btn('#588BFA')}>
            <LayoutDashboard size={18} /> Launch
          </Link>
          <Link to="/admin" style={btn('#7252A4')}>
            <Settings size={18} /> Admin
          </Link>
        </div>
      </div>

      {/* HERO CONTEXT IMAGE — fills ~70% of the home page */}
      <div style={{
        height: '72vh', borderRadius: 16, overflow: 'hidden',
        border: '1px solid rgba(0,0,0,0.08)', background: '#f8fbff',
        boxShadow: '0 12px 40px rgba(88,139,250,0.10), 0 2px 8px rgba(0,0,0,0.04)',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
      }}>
        <img
          src="/graphen-overview.svg"
          alt="GRAPHEN application context: lease PDFs are extracted with NER and LLMs into a Neo4j knowledge graph, then grounded Graph-RAG reasoning powers Ask AI, the Risk Dashboard and the Graph Explorer."
          style={{ width: '100%', height: '100%', objectFit: 'contain', display: 'block' }}
        />
      </div>

    </div>
  );
}

function btn(color) {
  return {
    display: 'inline-flex', alignItems: 'center', gap: 8, color: '#fff',
    padding: '10px 22px', borderRadius: 10, fontWeight: 700, textDecoration: 'none',
    background: color, boxShadow: `0 4px 15px ${color}59`,
  };
}
