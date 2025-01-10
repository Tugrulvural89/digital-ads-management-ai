// pages/CampaignList.tsx
import React, { useState, useEffect } from 'react';
import Header from '../components/header/header';
import Sidebar from '../components/sidebar/sidebar';
import Footer from '../components/footer/footer';
import { fetchCampaigns } from '../services/googleAdsApi';
import CampaignTable from '../components/campaignTable';
import { Campaign } from '../types/campaign';
import Loading from '../components/loading';

const CampaignList: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(true); // Loader
  const [error, setError] = useState<string | null>(null); // Error
  const [campaigns, setCampaigns] = useState<Campaign[]>([]); // Campaigns data
  const [isSidebarOpen, setIsSidebarOpen] = useState<boolean>(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  useEffect(() => {
    fetchCampaigns()
      .then((data) => setCampaigns(data))
      .catch((error) => setError(error.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <Loading />; // Loading bileşenini kullanın
  }

  if (error) {
    return <div>Error: {error}</div>; // Error message
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
