import { ChevronRight } from "lucide-react";
import dashboardImage from "figma:asset/98e6c69740e0bb2a0ab23ca4d11b217e045a432e.png";

export function DashboardHeader() {
  return (
    <div className="mb-8">
      {/* Cards section */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {/* Financial Data Card */}
        <div className="bg-blue-600 rounded-xl p-6 text-white relative overflow-hidden group hover:shadow-xl transition-shadow cursor-pointer">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm opacity-90">B.Clear</p>
              <h3>Financial Data</h3>
            </div>
            <div className="bg-white/20 p-2 rounded-lg">
              <div className="w-6 h-6 bg-white/30 rounded"></div>
            </div>
          </div>
          <button className="flex items-center gap-2 text-sm bg-blue-700 px-4 py-2 rounded-lg hover:bg-blue-800 transition-colors">
            View Details
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {/* Patient Data Card */}
        <div className="bg-green-500 rounded-xl p-6 text-white relative overflow-hidden group hover:shadow-xl transition-shadow cursor-pointer">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm opacity-90">Report</p>
              <h3>Patient Data</h3>
            </div>
            <div className="bg-white/20 p-2 rounded-lg">
              <div className="w-6 h-6 bg-white/30 rounded"></div>
            </div>
          </div>
          <button className="flex items-center gap-2 text-sm bg-green-600 px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
            View Details
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {/* Site Analysis Card */}
        <div className="bg-orange-500 rounded-xl p-6 text-white relative overflow-hidden group hover:shadow-xl transition-shadow cursor-pointer">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm opacity-90">Statistics</p>
              <h3>Site Analysis</h3>
            </div>
            <div className="bg-white/20 p-2 rounded-lg">
              <div className="w-6 h-6 bg-white/30 rounded"></div>
            </div>
          </div>
          <button className="flex items-center gap-2 text-sm bg-orange-600 px-4 py-2 rounded-lg hover:bg-orange-700 transition-colors">
            View Details
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        {/* File Upload Card */}
        <div className="bg-red-500 rounded-xl p-6 text-white relative overflow-hidden group hover:shadow-xl transition-shadow cursor-pointer">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm opacity-90">Upload</p>
              <h3>File Upload</h3>
            </div>
            <div className="bg-white/20 p-2 rounded-lg">
              <div className="w-6 h-6 bg-white/30 rounded"></div>
            </div>
          </div>
          <button className="flex items-center gap-2 text-sm bg-red-600 px-4 py-2 rounded-lg hover:bg-red-700 transition-colors">
            View Details
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Welcome Section */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h2 className="mb-4">Welcome to IHC Data Analytics Dashboard</h2>
        
        <p className="text-gray-600 mb-4">This dashboard provides various data analysis for:</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
          <div className="flex gap-2">
            <span className="text-green-600">✓</span>
            <span>Financial and patient data analysis with accurate profit and loss calculation</span>
          </div>
          <div className="flex gap-2">
            <span className="text-green-600">✓</span>
            <span>Rate difference, LOS, and NACCR5 with interactive data visualization</span>
          </div>
          <div className="flex gap-2">
            <span className="text-green-600">✓</span>
            <span>Patient data management with complete and structured medical information</span>
          </div>
          <div className="flex gap-2">
            <span className="text-green-600">✓</span>
            <span>Ventilator usage monitoring with detailed analysis and reports</span>
          </div>
        </div>

        <div className="mt-4 bg-blue-50 border-l-4 border-blue-600 p-4 rounded">
          <p className="text-sm text-blue-900">
            <span className="inline-block mr-2">💡</span>
            <strong>Getting Started:</strong> To get started, please upload .txt, .xlsx, or .xls file using the Upload File menu in the sidebar.
          </p>
        </div>
      </div>
    </div>
  );
}
