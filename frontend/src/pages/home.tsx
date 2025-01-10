// src/pages/Home.tsx
import React from 'react';
import { Navigate, useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  
  const navigate = useNavigate();
  return (
    <div className="flex flex-col min-h-screen">
      {/* Header */}
      <header className="bg-gray-900 text-white w-full">
        <div className="container mx-auto px-6 py-4 flex items-center justify-between">
          <div className="text-2xl font-bold">AdsGenAi</div>
          <nav className="flex space-x-4">
            <a href="/" className="hover:text-gray-300">Home</a>
            <a href="/about" className="hover:text-gray-300">About</a>
            <a href="/features" className="hover:text-gray-300">Features</a>
            <a href="/contact" className="hover:text-gray-300">Contact</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <div className="w-full h-[400px] bg-cover bg-center" style={{ backgroundImage: "url('https://via.placeholder.com/1920x400')" }}></div>

      {/* Introduction Section */}
      <section className="container mx-auto px-6 py-12 text-center">
        <h2 className="text-3xl font-bold mb-4">Revolutionize Your Ads with AI</h2>
        <p className="text-lg text-gray-700 mb-6">
          AdsGenAi helps you create effective, high-conversion advertisements in minutes. Leverage our powerful AI to enhance your marketing campaigns.
        </p>
        <button className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-500" onClick={() => navigate('/login')}>
          Get Started
        </button>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white w-full mt-auto">
        <div className="container mx-auto px-6 py-4 text-center">
          <p className="text-sm">&copy; 2025 AdsGenAi. All rights reserved.</p>
          <p className="text-sm">Privacy Policy | Terms of Service</p>
        </div>
      </footer>
    </div>
  );
};

export default Home;
