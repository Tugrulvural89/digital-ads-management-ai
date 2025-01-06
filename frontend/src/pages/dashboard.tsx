// src/pages/Dashboard.tsx
import React, { useEffect } from 'react';
import GoogleAdsConnectWrapper from '../components/google-sign-in';

const Dashboard: React.FC = () => {
  return (
    <div>
      <h1>Dashboard</h1>
      <p>Welcome to the dashboard!</p>
      <GoogleAdsConnectWrapper />
    </div>
  );
};

export default Dashboard;