import React from 'react';
import { NavLink } from 'react-router-dom';
import { Database } from 'lucide-react';

export default function TopNav() {
  const links = [
    { name: 'Overview', path: '/' },
    { name: 'Ingest', path: '/ingest' },
    { name: 'Ask AI', path: '/ask' },
    { name: 'Risk Dashboard', path: '/risk' },
    { name: 'Knowledge Graph', path: '/graph' },
    { name: 'Architecture', path: '/architecture' },
  ];

  return (
    <header className="top-nav flex justify-between items-center w-full">
      {/* Logo & Branding */}
      <div className="flex items-center gap-4">
        <div className="w-8 h-8 rounded bg-gradient-to-br from-accent-primary to-accent-secondary flex items-center justify-center text-white font-bold text-sm">
          G
        </div>
        <div className="flex items-center gap-3">
          <span className="text-accent-primary font-bold text-xl tracking-wide">GRAPHEN</span>
          <div className="h-4 w-px bg-border-light"></div>
          <span className="text-text-secondary text-xs font-medium">Graph-powered Reasoning Agentic Platform</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex items-center gap-6">
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            end={link.path === '/'}
            className={({ isActive }) => 
              `text-sm font-medium transition-colors px-3 py-1.5 rounded-lg ${
                isActive ? 'text-accent-primary bg-accent-primary/10' : 'text-text-secondary hover:text-text-primary'
              }`
            }
          >
            {({ isActive }) => (
              <div className="flex items-center gap-2">
                {isActive && <div className="w-1.5 h-1.5 rounded-full bg-accent-primary"></div>}
                {link.name}
              </div>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Neo4j Status Badge */}
      <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-accent-success/10 border border-accent-success/20 text-accent-success text-xs font-medium">
        <Database size={12} />
        Neo4j - 142 nodes
      </div>
    </header>
  );
}
