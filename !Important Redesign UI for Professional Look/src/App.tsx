import { useState } from 'react';
import { Sidebar } from './components/Sidebar';
import { Header } from './components/Header';
import { FilterBar } from './components/FilterBar';
import { PatientTable } from './components/PatientTable';

export default function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-sky-50 to-cyan-50">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      
      {/* Main Content */}
      <div className="lg:pl-64">
        <Header onMenuClick={() => setSidebarOpen(true)} />
        
        <main className="p-4 lg:p-8">
          {/* Dashboard Title */}
          <div className="mb-8">
            <h1 className="text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">IHC Data Analytics Dashboard</p>
          </div>

          {/* Analysis Patient Section */}
          <div className="bg-white rounded-2xl shadow-lg border border-blue-100 overflow-hidden">
            <div className="p-6 lg:p-8 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-cyan-50">
              <h2 className="text-gray-900 mb-2">Analisis Patient</h2>
              <p className="text-gray-600">Menampilkan analisis data patient with complete medical information</p>
            </div>

            {/* Filters */}
            <FilterBar />

            {/* Table */}
            <PatientTable />
          </div>
        </main>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
    </div>
  );
}
