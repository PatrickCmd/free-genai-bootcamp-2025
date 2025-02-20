import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  HomeIcon,
  BookOpenIcon,
  DocumentTextIcon,
  UserGroupIcon,
  ClockIcon,
  Cog6ToothIcon,
} from '@heroicons/react/24/outline';

const Sidebar: React.FC = () => {
  const location = useLocation();
  
  const navItems = [
    { path: '/dashboard', name: 'Dashboard', icon: HomeIcon },
    { path: '/study_activities', name: 'Study Activities', icon: BookOpenIcon },
    { path: '/words', name: 'Words', icon: DocumentTextIcon },
    { path: '/groups', name: 'Word Groups', icon: UserGroupIcon },
    { path: '/study_sessions', name: 'Sessions', icon: ClockIcon },
    { path: '/settings', name: 'Settings', icon: Cog6ToothIcon },
  ];

  return (
    <aside className="bg-[#1e293b] text-white w-64 min-h-screen flex flex-col">
      <div className="p-4">
        <Link to="/" className="text-xl font-bold text-blue-400">LangPortal</Link>
      </div>
      <nav className="flex-1 px-2 py-4">
        {navItems.map(({ path, name, icon: Icon }) => (
          <Link
            key={path}
            to={path}
            className={`flex items-center gap-4 px-4 py-3 rounded-lg mb-1 transition-colors ${
              location.pathname === path 
                ? 'bg-blue-900 text-blue-400' 
                : 'text-gray-300 hover:bg-blue-900/50 hover:text-blue-400'
            }`}
          >
            <Icon className="w-6 h-6" />
            <span>{name}</span>
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar; 