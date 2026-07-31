import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import TopNav from './components/TopNav';
import Sidebar from './components/Sidebar';
import Overview from './pages/Overview';
import Ingest from './pages/Ingest';
import Ask from './pages/Ask';
import Risk from './pages/Risk';
import KnowledgeGraph from './pages/KnowledgeGraph';
import Architecture from './pages/Architecture';
import Dashboard from './pages/Dashboard';
import Admin from './pages/Admin';
import './index.css';

function App() {
  return (
    <div className="app-container">
      <TopNav />
      <div className="main-wrapper">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Overview />} />
            <Route path="/ingest" element={<Ingest />} />
            <Route path="/ask" element={<Ask />} />
            <Route path="/risk" element={<Risk />} />
            <Route path="/graph" element={<KnowledgeGraph />} />
            <Route path="/architecture" element={<Architecture />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/admin" element={<Admin />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
