// pages/CampaignList.tsx
import React, { useState, useEffect } from 'react';
import Header from '../components/header/header';
import Sidebar from '../components/sidebar/sidebar';
import Footer from '../components/footer/footer';
import { fetchCampaigns } from '../utils/googleAdsApi';
import CampaignTable from '../components/campaignTable';
import { Campaign } from '../types/campaign';

const CampaignList: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true);       // loader
  const [error, setError] = useState<string | null>(null);      // error
  const [campaigns, setCampaigns] = useState<Campaign[]>([]);   // campaigns data
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  useEffect(() => {
    fetchCampaigns().then((data) => setCampaigns(data)).catch((error) => setError(error.message)).finally(() => setLoading(false));
  }, []); 

  if (loading) {
    return <div>Loading...</div>;  // Yükleniyor mesajı
  }

  if (error) {
    return <div>Error: {error}</div>;  // Hata mesajı
  }

  return (
    <div className="flex min-h-screen flex-col">
      {/* Header */}
      <Header toggleSidebar={toggleSidebar} /> 

      {/* Sidebar */}
      <Sidebar isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />

      {/* Overlay with fade effect */}
      <div
        onClick={toggleSidebar}
        className={`
          fixed inset-0 bg-black z-30
          transition-opacity duration-300 ease-in-out
          ${isSidebarOpen ? 'opacity-50' : 'opacity-0 pointer-events-none'}
        `}
      />

      {/* Main Content */}
      <main className="flex-1 p-6 pt-32">
    
        <CampaignTable campaigns={campaigns} />
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default CampaignList;
