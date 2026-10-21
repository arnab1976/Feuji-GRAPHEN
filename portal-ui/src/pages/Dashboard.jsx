import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Building2, Users, AlertTriangle, FileCheck, TrendingUp, RefreshCcw } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8004';

export default function Dashboard() {
  const [stats, setStats] = useState({ leases: 0, tenants: 0, criticalClauses: 0, totalSqft: 0 });
  const [loading, setLoading] = useState(false);

  // Mock fetching for now, eventually this will call /api/summary
  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    setLoading(true);
    try {
      // If backend is running, this would fetch real data
      // const res = await axios.get(`${API_BASE}/api/summary`);
      // setStats(res.data);
      
      // Mock data for UI visual check
      setTimeout(() => {
        setStats({
          leases: 25,
          tenants: 18,
          criticalClauses: 4,
          totalSqft: '145,000'
        });
        setLoading(false);
      }, 800);
    } catch (error) {
      console.error("Failed to fetch stats", error);
      setLoading(false);
    }
  };

  const statCards = [
    { title: 'Total Leases', value: stats.leases, icon: <FileCheck className="text-accent-primary" size={24} /> },
    { title: 'Unique Tenants', value: stats.tenants, icon: <Users className="text-accent-secondary" size={24} /> },
    { title: 'Total SqFt', value: stats.totalSqft, icon: <Building2 className="text-accent-success" size={24} /> },
    { title: 'High-Risk Clauses', value: stats.criticalClauses, icon: <AlertTriangle className="text-accent-danger" size={24} /> },
  ];

  return (
    <div className="animate-fade-in">
      <header className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold m-0 text-text-primary">Portfolio Overview</h1>
          <p className="text-text-secondary mt-1">Real-time intelligence from your Neo4j Knowledge Graph</p>
        </div>
        <button className="btn btn-outline" onClick={fetchStats} disabled={loading}>
          <RefreshCcw size={16} className={loading ? "animate-spin" : ""} />
          Refresh Data
        </button>
      </header>

      <div className="grid grid-cols-4 mb-8">
        {statCards.map((stat, idx) => (
          <div key={idx} className="glass-panel stat-card" style={{ animationDelay: `${idx * 0.1}s` }}>
            <div className="flex justify-between items-start">
              <span className="stat-title">{stat.title}</span>
              <div className="p-2 rounded-lg bg-[rgba(0,0,0,0.03)] border border-white/5">
                {stat.icon}
              </div>
            </div>
            <div className="mt-2">
              <span className="stat-value">{loading ? '...' : stat.value}</span>
              {!loading && (
                <div className="flex items-center gap-1 mt-2 text-xs text-accent-success">
                  <TrendingUp size={12} />
                  <span>Updated just now</span>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="glass-panel p-6 col-span-2">
          <h3 className="text-xl font-bold mb-4">Portfolio Risk Narrative</h3>
          <div className="p-4 rounded-xl bg-[rgba(0,0,0,0.2)] border border-[rgba(0,0,0,0.05)]">
            <p className="text-text-primary leading-relaxed">
              <span className="text-accent-primary font-semibold">AI Summary:</span> The current portfolio exhibits stable occupancy with <span className="text-text-primary font-medium">18 unique tenants</span> across <span className="text-text-primary font-medium">25 active leases</span>. However, attention is required for <span className="text-accent-danger font-medium">4 high-risk clauses</span> primarily involving uncapped CAM expenses and unfavorable early termination conditions in the Chicago properties.
            </p>
          </div>
        </div>

        <div className="glass-panel p-6 col-span-1">
          <h3 className="text-xl font-bold mb-4">Recent Ingestions</h3>
          <ul className="flex flex-col gap-3">
            {[1, 2, 3].map((_, i) => (
              <li key={i} className="flex items-center gap-3 p-3 rounded-lg hover:bg-[rgba(0,0,0,0.03)] transition-colors border border-transparent hover:border-[rgba(0,0,0,0.05)] cursor-pointer">
                <div className="w-10 h-10 rounded-lg bg-accent-primary/10 flex items-center justify-center text-accent-primary">
                  <Building2 size={18} />
                </div>
                <div>
                  <p className="text-sm font-medium text-text-primary m-0">LG-A3F9B{i}</p>
                  <p className="text-xs text-text-secondary m-0">Processed 2h ago</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
