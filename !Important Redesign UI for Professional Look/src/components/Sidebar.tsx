import { Home, DollarSign, BarChart3, Users, ChevronDown, LogOut, User } from 'lucide-react';
import { useState } from 'react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const [financialOpen, setFinancialOpen] = useState(false);
  const [analyticsOpen, setAnalyticsOpen] = useState(true);

  return (
    <aside className={`
      fixed top-0 left-0 z-30 h-screen w-64 
      bg-gradient-to-b from-blue-600 via-blue-700 to-blue-800
      text-white transition-transform duration-300 ease-in-out
      ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
    `}>
      <div className="flex flex-col h-full">
        {/* Logo */}
        <div className="p-6 border-b border-blue-500/30">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-white rounded-lg flex items-center justify-center">
              <BarChart3 className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h1 className="font-semibold">IHC Data Analytics</h1>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto p-4 space-y-2">
          <div className="mb-6">
            <p className="text-blue-200 text-xs uppercase tracking-wider px-3 mb-3">E-Claim</p>
            
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-white/10 hover:bg-white/20 transition-colors">
              <Home className="w-5 h-5" />
              <span>Dashboard</span>
            </button>
          </div>

          <div className="mb-6">
            <button 
              onClick={() => setFinancialOpen(!financialOpen)}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition-colors"
            >
              <DollarSign className="w-5 h-5" />
              <span className="flex-1 text-left">Financial Data</span>
              <ChevronDown className={`w-4 h-4 transition-transform ${financialOpen ? 'rotate-180' : ''}`} />
            </button>
            
            {financialOpen && (
              <div className="ml-4 mt-2 space-y-1">
                <button className="w-full flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-white/10 transition-colors text-sm">
                  <div className="w-1.5 h-1.5 bg-blue-300 rounded-full" />
                  <span>Financial</span>
                </button>
                <button className="w-full flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-white/10 transition-colors text-sm">
                  <div className="w-1.5 h-1.5 bg-blue-300 rounded-full" />
                  <span>Patient</span>
                </button>
                <button className="w-full flex items-center gap-3 px-4 py-2 rounded-lg hover:bg-white/10 transition-colors text-sm">
                  <div className="w-1.5 h-1.5 bg-blue-300 rounded-full" />
                  <span>Upload File</span>
                </button>
              </div>
            )}
          </div>

          <div className="mb-6">
            <p className="text-blue-200 text-xs uppercase tracking-wider px-3 mb-3">Analytics</p>
            
            <button 
              onClick={() => setAnalyticsOpen(!analyticsOpen)}
              className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-cyan-500/30 hover:bg-cyan-500/40 transition-colors"
            >
              <BarChart3 className="w-5 h-5" />
              <span className="flex-1 text-left">Data Analysis</span>
              <ChevronDown className={`w-4 h-4 transition-transform ${analyticsOpen ? 'rotate-180' : ''}`} />
            </button>
          </div>

          <div>
            <p className="text-blue-200 text-xs uppercase tracking-wider px-3 mb-3">Administration</p>
            
            <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl hover:bg-white/10 transition-colors">
              <Users className="w-5 h-5" />
              <span>User Management</span>
            </button>
          </div>
        </nav>

        {/* User Info */}
        <div className="p-4 border-t border-blue-500/30">
          <div className="bg-white/10 rounded-xl p-4 mb-3">
            <div className="flex items-center gap-3 mb-3">
              <div className="w-10 h-10 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full flex items-center justify-center">
                <User className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">admin</p>
                <p className="text-xs text-blue-200">Online 29:50</p>
              </div>
            </div>
          </div>
          
          <button className="w-full flex items-center gap-3 px-4 py-3 rounded-xl bg-red-500/20 hover:bg-red-500/30 transition-colors text-red-200 hover:text-white">
            <LogOut className="w-5 h-5" />
            <span>2025 Selamete</span>
          </button>
        </div>
      </div>
    </aside>
  );
}
