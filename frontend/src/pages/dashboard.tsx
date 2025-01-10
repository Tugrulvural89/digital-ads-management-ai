import React, { useState } from 'react';
import GoogleAdsConnectWrapper from '../components/google-sign-in';
import Header from '../components/header/header';
import Sidebar from '../components/sidebar/sidebar';
import Footer from '../components/footer/footer';

const Dashboard: React.FC = () => {
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <Header toggleSidebar={toggleSidebar} />

      {/* Main Layout */}
      <div className="flex flex-1 pt-16">
        {/* Sidebar */}
        <Sidebar isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />

        {/* Sidebar Overlay */}
        <div
          onClick={toggleSidebar}
          className={`
            fixed inset-0 bg-black z-30
            transition-opacity duration-300 ease-in-out
            ${isSidebarOpen ? 'opacity-50' : 'opacity-0 pointer-events-none'}
          `}
        />

        {/* Main Content */}
        <main className="flex-1 p-6">
          <h2 className="text-xl font-semibold">Welcome to the Dashboard!</h2>
          <p className="mt-2">Here is your dashboard content.</p>

          {/* Google Ads Integration */}
          
          <GoogleAdsConnectWrapper />
        </main>
      </div>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Dashboard;
