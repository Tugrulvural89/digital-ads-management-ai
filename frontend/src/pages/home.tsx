// src/pages/Home.tsx
import React from 'react';
import LoginForm from '../components/login';

const Home: React.FC = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-purple-500">
      <h2 className="text-4xl font-extrabold text-white mb-6">Welcome to My Awesome App</h2>
      <div className="bg-white p-8 rounded-lg shadow-2xl w-full max-w-md">
        <LoginForm />
      </div>
      <p className="text-white mt-4">Navigate to the dashboard to see more features!</p>
    </div>
  );
};

export default Home;
