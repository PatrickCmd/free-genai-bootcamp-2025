import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header: React.FC = () => {
  const location = useLocation();
  const path = location.pathname.split('/').filter(Boolean);
  
  return (
    <header className="border-b border-gray-800 mb-6">
      <div className="flex items-center gap-2 py-4">
        {path.map((segment, index) => (
          <React.Fragment key={index}>
            <span className="text-gray-400 capitalize">
              {segment.replace(/_/g, ' ')}
            </span>
            {index < path.length - 1 && (
              <span className="text-gray-600">/</span>
            )}
          </React.Fragment>
        ))}
      </div>
    </header>
  );
};

export default Header; 