import axios from 'axios';
import { AdAccount } from '../types/adAccount';



const ALL_GOOGLE_ADS_ACCOUNTS_API_PATH = process.env.REACT_APP_ALL_GOOGLE_ADS_ACCOUNTS_API_PATH as string;

if (!ALL_GOOGLE_ADS_ACCOUNTS_API_PATH) {
  throw new Error('ALL_GOOGLE_ADS_ACCOUNTS_API_PATH must be defined in environment variables');
}

const ALL_GOOGLE_ADS_ACCOUNTS_SAVE_API_PATH = process.env.REACT_APP_ALL_GOOGLE_ADS_ACCOUNTS_SAVE_API_PATH as string;

if (!ALL_GOOGLE_ADS_ACCOUNTS_SAVE_API_PATH) {
  throw new Error('ALL_GOOGLE_ADS_ACCOUNTS_SAVE_API_PATH must be defined in environment variables');
}


export const fetchGoogleAdsAccounts = async (accessToken: string): Promise<AdAccount[]> => {
  const response = await axios.post(ALL_GOOGLE_ADS_ACCOUNTS_API_PATH, {
    access_token: accessToken,
  });

  return response.data.resourceNames.map((resourceName: string) => {
    const accountId = resourceName.split('/')[1];
    const accountName = resourceName.split('/')[0];
    return {
      account_id: accountId,
      name: `Account ${accountName}`,
    };
  });
};

export const saveAdAccount = async (accountId: string) => {
  const response = await axios.post(ALL_GOOGLE_ADS_ACCOUNTS_SAVE_API_PATH, {
    account_id: accountId,
    channel: 'Google',
  }, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
    },
  });

  return response.data;
};
