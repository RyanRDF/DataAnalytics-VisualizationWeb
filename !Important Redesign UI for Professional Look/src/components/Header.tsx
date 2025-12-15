import { Menu, Bell, Moon, Search } from 'lucide-react';

interface HeaderProps {
  onMenuClick: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="bg-white/80 backdrop-blur-lg border-b border-blue-100 sticky top-0 z-10">
      <div className="flex items-center justify-between px-4 lg:px-8 py-4">
        <button
          onClick={onMenuClick}
          className="lg:hidden p-2 hover:bg-blue-50 rounded-lg transition-colors"
        >
          <Menu className="w-6 h-6 text-gray-700" />
        </button>

        <div className="flex-1 max-w-xl mx-4 hidden md:block">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search patients, data..."
              className="w-full pl-10 pr-4 py-2.5 bg-blue-50/50 border border-blue-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            />
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button className="p-2.5 hover:bg-blue-50 rounded-xl transition-colors relative">
            <Bell className="w-5 h-5 text-gray-700" />
            <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-cyan-500 rounded-full border-2 border-white"></span>
          </button>
          
          <button className="p-2.5 hover:bg-blue-50 rounded-xl transition-colors">
            <Moon className="w-5 h-5 text-gray-700" />
          </button>

          <div className="hidden sm:flex items-center gap-3 ml-2 px-3 py-2 bg-gradient-to-r from-blue-50 to-cyan-50 rounded-xl border border-blue-100">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center text-white text-sm">
              A
            </div>
            <span className="text-gray-700">Admin</span>
          </div>
        </div>
      </div>
    </header>
  );
}
