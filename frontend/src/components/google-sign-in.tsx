import React, { useState } from 'react';
import { GoogleOAuthProvider, useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';


interface AdAccount {
  account_id: string;
  name: string;
}

const GoogleAdsConnectWrapper: React.FC = () => {
  const apiKey = process.env.GOOGLE_CLIENT_ID;

  // Eğer apiKey yoksa hata veririz ya da kullanıcıya mesaj gösteririz
  if (!apiKey) {
    console.error("Google Client ID is missing!");
    return <div>Error: Google Client ID is missing.</div>;
  }
  
  return (
    <GoogleOAuthProvider clientId={apiKey}>
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


  const googleLogin = useGoogleLogin({
    scope: 'https://www.googleapis.com/auth/adwords',
    onSuccess: async (tokenResponse) => {
      try {
        setIsLoading(true);
        setError('');


        // Save Google credentials to the server
        await axios.post('http://localhost:8000/api/v1/save-credentials', {
          credentials: {
            access_token: tokenResponse.access_token,
            scope: 'https://www.googleapis.com/auth/adwords',
            expires_in: tokenResponse.expires_in,
            token_type: tokenResponse.token_type,
          },
          user_email: "admin@admin.com", 
        });

        console.log(tokenResponse.access_token);
        // Fetch Google Ads accounts using the Google token
        const response = await axios.post('http://localhost:8000/api/v1/google-ad-accounts', {
          access_token: tokenResponse.access_token.toString(),
        });
        console.log(response.data)

         // Parse the resourceNames and map them to AdAccount objects
         const accounts = response.data.resourceNames.map((resourceName: string) => {
          const accountId = resourceName.split('/')[1];
          return {
            account_id: accountId,
            name: `Account ${accountId}`,
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

      // Send the selected account to the backend
      const response = await axios.post('http://localhost:8000/api/v1/save-ad-account', {
        account_id: selectedAccount,
        user_email: "admin@admin.com", // Replace with the actual user email
        channel: "Google"
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