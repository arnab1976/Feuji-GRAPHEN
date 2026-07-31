import React from 'react';
import { Settings, Shield } from 'lucide-react';

export default function Admin() {
  return (
    <div className="animate-fade-in flex flex-col items-center justify-center min-h-[60vh]">
      <div className="glass-panel p-12 flex flex-col items-center max-w-xl text-center">
        <div className="w-20 h-20 rounded-full bg-[#7252A4]/10 border border-[#7252A4]/30 flex items-center justify-center text-[#7252A4] mb-6 shadow-[0_0_20px_rgba(114,82,164,0.2)]">
          <Shield size={40} />
        </div>
        <h1 className="text-3xl font-bold text-text-primary mb-4">Admin Portal</h1>
        <p className="text-text-secondary text-lg mb-8 leading-relaxed">
          Welcome to the administrative control center. System configuration, user management, and advanced tuning parameters will be available here.
        </p>
        <button className="bg-[#7252A4] hover:bg-[#5b4183] text-white px-6 py-3 rounded-lg font-bold transition-colors shadow-[0_4px_15px_rgba(114,82,164,0.3)] flex items-center gap-2">
          <Settings size={18} />
          System Settings
        </button>
      </div>
    </div>
  );
}
