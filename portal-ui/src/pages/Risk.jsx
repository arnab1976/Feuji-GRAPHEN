import React, { useState } from 'react';
import { Calendar, Users, AlertTriangle, ChevronDown } from 'lucide-react';

export default function Risk() {
  const [filter, setFilter] = useState('Next 90 days');

  return (
    <div className="max-w-7xl mx-auto pb-12 animate-fade-in flex flex-col gap-6">
      <div className="mb-2">
        <h1 className="text-3xl font-bold text-text-primary mb-2">Risk Dashboard</h1>
        <p className="text-text-secondary text-lg">
          Computed live from graph traversals — expiration exposure, tenant concentration, and AI-flagged high-risk clauses.
        </p>
      </div>

      {/* Top Row: Tables */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        
        {/* Lease Expiration Risk */}
        <div className="lg:col-span-3 glass-panel p-6">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Calendar size={20} className="text-[#588BFA]" />
              <h2 className="text-lg font-bold text-text-primary">Lease Expiration Risk</h2>
            </div>
            <div className="relative">
              <select 
                className="appearance-none bg-[rgba(0,0,0,0.05)] border border-border-primary rounded-lg px-4 py-2 pr-10 text-sm text-text-primary focus:outline-none focus:border-[#588BFA] cursor-pointer"
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
              >
                <option value="Next 90 days">Next 90 days</option>
                <option value="Next 180 days">Next 180 days</option>
                <option value="Next 365 days">Next 365 days</option>
              </select>
              <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-text-muted pointer-events-none" />
            </div>
          </div>

          <div className="w-full overflow-x-auto">
            <table className="w-full text-left text-sm text-text-secondary">
              <thead>
                <tr className="border-b border-border-primary/50 text-xs uppercase tracking-wider text-text-muted">
                  <th className="pb-3 font-medium">Property</th>
                  <th className="pb-3 font-medium">Tenant</th>
                  <th className="pb-3 font-medium">Expires</th>
                  <th className="pb-3 font-medium text-right">Sqft</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-border-primary/30 hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 font-medium text-text-primary">456 Commerce Blvd</td>
                  <td className="py-4">Vantage Analytics</td>
                  <td className="py-4">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-[#f7768e]/10 text-[#f7768e]">
                      2026-08-11 • 42d
                    </span>
                  </td>
                  <td className="py-4 text-right font-mono text-text-primary">18,000</td>
                </tr>
                <tr className="border-b border-border-primary/30 hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 font-medium text-text-primary">456 Commerce Blvd</td>
                  <td className="py-4">Coastal Retail Group</td>
                  <td className="py-4">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-[#e0af68]/10 text-[#e0af68]">
                      2026-08-27 • 58d
                    </span>
                  </td>
                  <td className="py-4 text-right font-mono text-text-primary">6,500</td>
                </tr>
                <tr className="hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 font-medium text-text-primary">875 Riverfront Dr</td>
                  <td className="py-4">Brightline Legal</td>
                  <td className="py-4">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-[#e0af68]/10 text-[#e0af68]">
                      2026-09-14 • 76d
                    </span>
                  </td>
                  <td className="py-4 text-right font-mono text-text-primary">14,200</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        {/* Tenant Concentration */}
        <div className="lg:col-span-2 glass-panel p-6">
          <div className="flex items-center gap-2 mb-6">
            <Users size={20} className="text-[#7252A4]" />
            <h2 className="text-lg font-bold text-text-primary">Tenant Concentration</h2>
          </div>

          <div className="w-full overflow-x-auto">
            <table className="w-full text-left text-sm text-text-secondary">
              <thead>
                <tr className="border-b border-border-primary/50 text-xs uppercase tracking-wider text-text-muted">
                  <th className="pb-3 font-medium">Tenant</th>
                  <th className="pb-3 font-medium text-right">Leases</th>
                  <th className="pb-3 font-medium text-right">Total Sqft</th>
                  <th className="pb-3 font-medium pl-4">Share</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-border-primary/30 hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 text-text-primary font-medium">Vantage Analytics</td>
                  <td className="py-4 text-right">3</td>
                  <td className="py-4 text-right font-mono">50,800</td>
                  <td className="py-4 pl-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 rounded-full bg-[rgba(0,0,0,0.1)] w-16">
                        <div className="h-full rounded-full bg-[#f7768e]" style={{ width: '45%' }}></div>
                      </div>
                      <span className="text-xs font-mono w-8 text-right">45%</span>
                    </div>
                  </td>
                </tr>
                <tr className="border-b border-border-primary/30 hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 text-text-primary font-medium">Northgate Financial</td>
                  <td className="py-4 text-right">2</td>
                  <td className="py-4 text-right font-mono">32,000</td>
                  <td className="py-4 pl-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 rounded-full bg-[rgba(0,0,0,0.1)] w-16">
                        <div className="h-full rounded-full bg-[#f7768e]" style={{ width: '28.3%' }}></div>
                      </div>
                      <span className="text-xs font-mono w-8 text-right">28.3%</span>
                    </div>
                  </td>
                </tr>
                <tr className="border-b border-border-primary/30 hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 text-text-primary font-medium">Brightline Legal</td>
                  <td className="py-4 text-right">1</td>
                  <td className="py-4 text-right font-mono">14,200</td>
                  <td className="py-4 pl-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 rounded-full bg-[rgba(0,0,0,0.1)] w-16">
                        <div className="h-full rounded-full bg-[#588BFA]" style={{ width: '12.6%' }}></div>
                      </div>
                      <span className="text-xs font-mono w-8 text-right">12.6%</span>
                    </div>
                  </td>
                </tr>
                <tr className="border-b border-border-primary/30 hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 text-text-primary font-medium">Meridian Health Group</td>
                  <td className="py-4 text-right">1</td>
                  <td className="py-4 text-right font-mono">9,500</td>
                  <td className="py-4 pl-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 rounded-full bg-[rgba(0,0,0,0.1)] w-16">
                        <div className="h-full rounded-full bg-[#588BFA]" style={{ width: '8.4%' }}></div>
                      </div>
                      <span className="text-xs font-mono w-8 text-right">8.4%</span>
                    </div>
                  </td>
                </tr>
                <tr className="hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                  <td className="py-4 text-text-primary font-medium">Coastal Retail Group</td>
                  <td className="py-4 text-right">1</td>
                  <td className="py-4 text-right font-mono">6,500</td>
                  <td className="py-4 pl-4">
                    <div className="flex items-center gap-2">
                      <div className="flex-1 h-1.5 rounded-full bg-[rgba(0,0,0,0.1)] w-16">
                        <div className="h-full rounded-full bg-[#588BFA]" style={{ width: '5.8%' }}></div>
                      </div>
                      <span className="text-xs font-mono w-8 text-right">5.8%</span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      {/* Bottom Row: AI Flags */}
      <div className="glass-panel p-6">
        <div className="flex items-center gap-2 mb-6">
          <AlertTriangle size={20} className="text-[#f7768e]" />
          <h2 className="text-lg font-bold text-text-primary">AI-Flagged High-Risk Clauses</h2>
        </div>

        <div className="flex flex-col gap-4">
          <div className="p-5 rounded-lg bg-[rgba(0,0,0,0.02)] border border-border-primary border-l-4 border-l-[#f7768e] relative overflow-hidden group">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-bold text-text-primary">
                Termination Right <span className="text-text-muted font-normal mx-2">—</span> <span className="text-[#f7768e] font-mono text-sm">LG-A192</span>
              </h3>
              <span className="text-[10px] font-bold uppercase tracking-wider bg-[#f7768e]/10 text-[#f7768e] px-2 py-1 rounded">High Risk</span>
            </div>
            <p className="text-sm text-text-secondary mb-3">
              Tenant may terminate this Lease effective the last day of Year 3 with 12 months prior written notice.
            </p>
            <div className="text-xs text-text-muted font-mono bg-bg-darkest p-2 rounded inline-block">
              ↳ 456 Commerce Blvd (Vantage Analytics)
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
