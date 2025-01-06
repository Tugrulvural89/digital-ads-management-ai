// App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/dashboard';
import Home from './pages/home';

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        {/* Başlık */}
        <header className="bg-blue-600 text-white p-4">
          <h1 className="text-2xl font-bold">My Awesome App</h1>
        </header>

        {/* Ana İçerik */}
        <main className="p-4">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-blue-600 text-white p-4 mt-auto">
          <p>© 2023 My Awesome App. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
};

export default App;