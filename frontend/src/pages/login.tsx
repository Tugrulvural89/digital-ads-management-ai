import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const navigate = useNavigate();
  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setIsLoading(true);
      setError('');

      // Authenticate user and get custom token
      const response = await axios.post('http://localhost:8000/api/v1/token', {
        user_email: email,
        password: password,
      });

      const accessToken = response.data.access_token;
      localStorage.setItem('accessToken', accessToken); // Store the token
      navigate('/dashboard');
    } catch (err) {
      setError('Login failed');
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-purple-500">
          <h2 className="text-4xl font-extrabold text-white mb-6">Welcome to AdsGenAi</h2>
          <div className="bg-white p-8 rounded-lg shadow-2xl w-full max-w-md">
          <form onSubmit={handleLogin} className="p-4">
            <div className="mb-4">
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">Email</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="mt-1 p-2 w-full border rounded"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">Password</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="mt-1 p-2 w-full border rounded"
                required
              />
            </div>
            {error && <div className="text-red-500 mb-4">{error}</div>}
            <button
              type="submit"
              disabled={isLoading}
              className="bg-green-500 text-white px-4 py-2 rounded"
            >
              {isLoading ? 'Logging in...' : 'Login'}
            </button>
          </form>
          </div>
          <p className="text-white mt-4">Navigate to the dashboard to see more features!</p>
        </div>

    
  );
};

export default LoginForm;