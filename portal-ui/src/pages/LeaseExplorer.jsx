import React, { useState, useEffect } from 'react';
import { Search, Filter, ArrowUpDown } from 'lucide-react';

export default function LeaseExplorer() {
  const [leases, setLeases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Mock data for UI
    setTimeout(() => {
      setLeases([
        { id: 'LG-A3F9B1', property: 'One World Trade Center', tenant: 'TechCorp LLC', sqft: '45,000', expires: '2028-12-31', status: 'Active' },
        { id: 'LG-A3F9B2', property: 'Salesforce Tower', tenant: 'Global Finance', sqft: '22,500', expires: '2026-06-30', status: 'Expiring Soon' },
        { id: 'LG-A3F9B3', property: 'Willis Tower', tenant: 'Innovate Inc', sqft: '18,200', expires: '2029-01-15', status: 'Active' },
        { id: 'LG-A3F9B4', property: 'Transamerica Pyramid', tenant: 'Design Studio', sqft: '8,400', expires: '2025-10-31', status: 'Expiring Soon' },
        { id: 'LG-A3F9B5', property: 'Empire State Building', tenant: 'Media Group', sqft: '31,000', expires: '2030-05-01', status: 'Active' },
      ]);
      setLoading(false);
    }, 800);
  }, []);

  const filteredLeases = leases.filter(l => 
    l.property.toLowerCase().includes(searchTerm.toLowerCase()) || 
    l.tenant.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="animate-fade-in">
      <header className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold m-0 text-text-primary">Lease Explorer</h1>
          <p className="text-text-secondary mt-1">View and filter extracted lease entities</p>
        </div>
      </header>

      <div className="glass-panel p-6">
        <div className="flex gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-text-muted" size={18} />
            <input 
              type="text" 
              placeholder="Search by property or tenant..." 
              className="w-full bg-[rgba(0,0,0,0.03)] border border-black/ rounded-lg py-2 pl-10 pr-4 text-text-primary focus:outline-none focus:border-accent-primary transition-colors"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <button className="btn btn-outline">
            <Filter size={16} /> Filter
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-black/ text-text-secondary text-sm">
                <th className="py-3 px-4 font-medium"><div className="flex items-center gap-1 cursor-pointer hover:text-text-primary transition-colors">Lease ID <ArrowUpDown size={14} /></div></th>
                <th className="py-3 px-4 font-medium"><div className="flex items-center gap-1 cursor-pointer hover:text-text-primary transition-colors">Property <ArrowUpDown size={14} /></div></th>
                <th className="py-3 px-4 font-medium"><div className="flex items-center gap-1 cursor-pointer hover:text-text-primary transition-colors">Tenant <ArrowUpDown size={14} /></div></th>
                <th className="py-3 px-4 font-medium">SqFt</th>
                <th className="py-3 px-4 font-medium"><div className="flex items-center gap-1 cursor-pointer hover:text-text-primary transition-colors">Expiration <ArrowUpDown size={14} /></div></th>
                <th className="py-3 px-4 font-medium">Status</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-text-muted">Loading lease data...</td>
                </tr>
              ) : filteredLeases.length === 0 ? (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-text-muted">No leases found.</td>
                </tr>
              ) : (
                filteredLeases.map((lease, idx) => (
                  <tr key={lease.id} className="border-b border-white/5 hover:bg-[rgba(0,0,0,0.02)] transition-colors">
                    <td className="py-3 px-4 text-accent-primary font-medium cursor-pointer hover:underline">{lease.id}</td>
                    <td className="py-3 px-4 text-text-primary">{lease.property}</td>
                    <td className="py-3 px-4 text-text-secondary">{lease.tenant}</td>
                    <td className="py-3 px-4 text-text-secondary">{lease.sqft}</td>
                    <td className="py-3 px-4 text-text-secondary">{lease.expires}</td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-1 rounded-md text-xs font-medium ${
                        lease.status === 'Active' ? 'bg-accent-success/10 text-accent-success border border-accent-success/20' : 
                        'bg-accent-warning/10 text-accent-warning border border-accent-warning/20'
                      }`}>
                        {lease.status}
                      </span>
                    </td>
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
