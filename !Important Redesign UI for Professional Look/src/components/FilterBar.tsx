import { Calendar, ArrowUpDown, Filter, Search } from 'lucide-react';
import { useState } from 'react';

export function FilterBar() {
  const [dateFrom, setDateFrom] = useState('2025-12-01');
  const [dateTo, setDateTo] = useState('2025-12-17');
  const [sortColumn, setSortColumn] = useState('');
  const [selectColumn, setSelectColumn] = useState('');
  const [searchValue, setSearchValue] = useState('');

  const handleSearch = () => {
    console.log('Searching...');
  };

  const handleClear = () => {
    setDateFrom('');
    setDateTo('');
    setSortColumn('');
    setSelectColumn('');
    setSearchValue('');
  };

  return (
    <div className="p-6 lg:p-8 border-b border-gray-100 bg-gray-50/50">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {/* Date Range */}
        <div className="lg:col-span-2">
          <label className="block text-sm text-gray-700 mb-2">Date Range</label>
          <div className="flex gap-2 items-center">
            <div className="flex-1 relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="date"
                value={dateFrom}
                onChange={(e) => setDateFrom(e.target.value)}
                className="w-full pl-10 pr-3 py-2.5 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>
            <span className="text-gray-400">—</span>
            <div className="flex-1 relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input
                type="date"
                value={dateTo}
                onChange={(e) => setDateTo(e.target.value)}
                className="w-full pl-10 pr-3 py-2.5 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>
          </div>
        </div>

        {/* Sort By */}
        <div>
          <label className="block text-sm text-gray-700 mb-2">Sort By</label>
          <div className="relative">
            <ArrowUpDown className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <select
              value={sortColumn}
              onChange={(e) => setSortColumn(e.target.value)}
              className="w-full pl-10 pr-3 py-2.5 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all appearance-none cursor-pointer"
            >
              <option value="">Select Column</option>
              <option value="sep">SEP</option>
              <option value="mrn">MRN</option>
              <option value="nama_pasien">Nama Pasien</option>
              <option value="admission_date">Admission Date</option>
            </select>
          </div>
        </div>

        {/* Select Column */}
        <div>
          <label className="block text-sm text-gray-700 mb-2">Select Column</label>
          <div className="relative">
            <Filter className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <select
              value={selectColumn}
              onChange={(e) => setSelectColumn(e.target.value)}
              className="w-full pl-10 pr-3 py-2.5 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all appearance-none cursor-pointer"
            >
              <option value="">Select Column</option>
              <option value="sep">SEP</option>
              <option value="mrn">MRN</option>
              <option value="nama_pasien">Nama Pasien</option>
              <option value="los">LOS</option>
            </select>
          </div>
        </div>

        {/* Search Value */}
        <div>
          <label className="block text-sm text-gray-700 mb-2">Search Value</label>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              type="text"
              value={searchValue}
              onChange={(e) => setSearchValue(e.target.value)}
              placeholder="Search Value"
              className="w-full pl-10 pr-3 py-2.5 bg-white border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-wrap gap-3 mt-6">
        <button
          onClick={handleSearch}
          className="px-6 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 text-white rounded-xl hover:from-blue-700 hover:to-cyan-700 transition-all shadow-lg shadow-blue-500/30 flex items-center gap-2"
        >
          <Search className="w-4 h-4" />
          SEARCH
        </button>
        <button
          onClick={handleClear}
          className="px-6 py-2.5 bg-white text-gray-700 border border-gray-200 rounded-xl hover:bg-gray-50 transition-all flex items-center gap-2"
        >
          CLEAR
        </button>
      </div>
    </div>
  );
}
