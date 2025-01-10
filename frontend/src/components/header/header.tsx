import React from 'react';

const Header: React.FC<{ toggleSidebar: () => void }> = ({ toggleSidebar }) => {
  return (
    <header className="bg-blue-600 text-white p-4 shadow-md flex items-center justify-between fixed top-0 w-full z-50">
      <h1 className="text-2xl">Dashboard</h1>
      {/* Burger Menu Button */}
      <button
        onClick={toggleSidebar}
        className="text-white p-2 hover:bg-blue-700 rounded-lg transition-colors"
        aria-label="Toggle Sidebar"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
          className="w-6 h-6"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 6h16M4 12h16M4 18h16"
          />
        </svg>
      </button>
    </header>
  );
};

export default Header;
