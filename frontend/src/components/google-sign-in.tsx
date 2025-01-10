import React, { useState } from 'react';
import { GoogleOAuthProvider, useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';


interface AdAccount {
  account_id: string;
  name: string;
}

const GOOGLE_CLIENT_ID = process.env.REACT_APP_GOOGLE_CLIENT_ID as string;

if (!GOOGLE_CLIENT_ID) {
  throw new Error('REACT_APP_GOOGLE_CLIENT_ID must be defined in environment variables');
}

const GoogleAdsConnectWrapper: React.FC = () => {
  return (
    <GoogleOAuthProvider clientId={GOOGLE_CLIENT_ID}>
      <GoogleAdsConnect />
    </GoogleOAuthProvider>
  );
};

const GoogleAdsConnect: React.FC = () => {
  const [adAccounts, setAdAccounts] = useState<AdAccount[]>([]);
  const [selectedAccount, setSelectedAccount] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string>('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [token, setToken] = useState<string>('');
  const [refreshToken, setRefreshToken] = useState<string>('');

  // Google login with Auth Code Flow
  const googleLogin = useGoogleLogin({
    scope: 'https://www.googleapis.com/auth/adwords',
    flow: 'auth-code',
    onSuccess: async (response) => {
      console.log('Google login response:', response);
      try {
        setIsLoading(true);
        setError('');

        const { code } = response; // Yetkilendirme kodunu al
        console.log('Access Token:', code);
        // Yetkilendirme kodunu access token ve refresh token için backend'e gönder
        const tokenResponse = await axios.post('http://localhost:8000/api/v1/google/auth', {
          code: code || '',
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
          }
        }
        );
        console.log('tokenResponse  response:', tokenResponse);
       
        const { access_token, refresh_token } = tokenResponse.data;
        // Save Google credentials to the server
        const response_save = await axios.post('http://localhost:8000/api/v1/save-credentials', {
          access_token: access_token,  // Doğrudan token bilgilerini gönder
          refresh_token: refresh_token
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
            "Content-Type": "application/json",
          }
        });

        console.log('tokenResponse  response:', response_save);

        console.log('Access Token:', access_token);
        console.log('Refresh Token:', refresh_token);

        // Fetch Google Ads accounts
        const responseAdAccounts = await axios.post('http://localhost:8000/api/v1/google-ad-accounts', {
          access_token,
        });

        const accounts = responseAdAccounts.data.resourceNames.map((resourceName: string) => {
          const accountId = resourceName.split('/')[1];
          const accountName = resourceName.split('/')[0];
          return {
            account_id: accountId,
            name: `Account ${accountName}`,
          };
        });

        setAdAccounts(accounts);

      } catch (err) {
        setError('Failed to fetch Google Ads accounts');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    },
    onError: () => {
      setError('Google authorization failed');
    },
  });

  const handleSubmit = async () => {
    if (!selectedAccount) {
      setError('Please select an account');
      return;
    }

    try {
      setIsSubmitting(true);
      setError('');

      const response = await axios.post('http://localhost:8000/api/v1/save-ad-account', {
        account_id: selectedAccount,
        channel: "Google",
      }, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      });

      console.log('Account saved:', response.data);
      alert('Account saved successfully!');
    } catch (err) {
      setError('Failed to save the selected account');
      console.error(err);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="p-4">
      <button
        onClick={() => googleLogin()}
        disabled={isLoading}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        {isLoading ? 'Connecting...' : 'Connect Google Ads'}
      </button>

      {error && <div className="text-red-500 mt-2">{error}</div>}

      {adAccounts.length > 0 && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold">Select Google Ads Account:</h3>
          <div className="space-y-2 mt-2">
            {adAccounts.map((account) => (
              <div key={account.account_id} className="flex items-center">
                <input
                  type="radio"
                  id={account.account_id}
                  name="adAccount"
                  value={account.account_id}
                  checked={selectedAccount === account.account_id}
                  onChange={() => setSelectedAccount(account.account_id)}
                  className="mr-2"
                />
                <label htmlFor={account.account_id}>
                  {account.name} ({account.account_id})
                </label>
              </div>
            ))}
          </div>

          <button
            onClick={handleSubmit}
            disabled={isSubmitting || !selectedAccount}
            className="bg-green-500 text-white px-4 py-2 rounded mt-4"
          >
            {isSubmitting ? 'Submitting...' : 'Submit'}
          </button>
        </div>
      )}
    </div>
  );
};

export default GoogleAdsConnectWrapper;
