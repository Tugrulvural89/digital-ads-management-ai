import React from 'react';

const Sidebar: React.FC<{ isSidebarOpen: boolean; toggleSidebar: () => void }> = ({
  isSidebarOpen,
  toggleSidebar,
}) => {
  return (
    <aside
      className={`
        fixed top-16 left-0 w-64 h-[calc(100vh-4rem)]
        bg-gray-800 text-white z-40
        transform transition-transform duration-300 ease-in-out
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}
    >
      <nav className="p-4">
        <ul className="space-y-2">
          <li>
            <a
              href="#"
              className="block p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              Home
            </a>
          </li>
          <li>
            <a
              href="/campaigns"
              className="block p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              Campaigns
            </a>
          </li>
          <li>
            <a
              href="#"
              className="block p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              Settings
            </a>
          </li>
          <li>
            <a
              href="#"
              className="block p-2 hover:bg-gray-700 rounded-lg transition-colors"
            >
              Logout
            </a>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
