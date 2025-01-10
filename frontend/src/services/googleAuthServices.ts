import axios from 'axios';



const GOOGLE_ADS_AUTH_API_PATH = process.env.REACT_APP_GOOGLE_ADS_AUTH_API_PATH as string;

if (!GOOGLE_ADS_AUTH_API_PATH) {
  throw new Error('GOOGLE_ADS_AUTH_API_PATH must be defined in environment variables');
}

const GOOGLE_ADS_AUTH_SAVE_CRED_API_PATH = process.env.REACT_APP_GOOGLE_ADS_AUTH_SAVE_CRED_API_PATH as string;

if (!GOOGLE_ADS_AUTH_SAVE_CRED_API_PATH) {
  throw new Error('GOOGLE_ADS_AUTH_SAVE_CRED_API_PATH must be defined in environment variables');
}


export const exchangeAuthCodeForTokens = async (authCode: string) => {
  const response = await axios.post(GOOGLE_ADS_AUTH_API_PATH, {
    code: authCode,
  }, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
    },
  });

  return response.data;
};

export const saveGoogleCredentials = async (accessToken: string, refreshToken: string) => {
  const response = await axios.post(GOOGLE_ADS_AUTH_SAVE_CRED_API_PATH, {
    access_token: accessToken,
    refresh_token: refreshToken,
  }, {
    headers: {
      Authorization: `Bearer ${localStorage.getItem('accessToken')}`,
      'Content-Type': 'application/json',
    },
  });

  return response.data;
};
