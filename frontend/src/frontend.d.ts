declare module "*.svg" {
    const content: string;
    export default content;
  };


  declare namespace NodeJS {
    interface ProcessEnv {
      GOOGLE_CLIENT_ID: string;
      GOOGLE_MANAGER_ID: string;
      ALL_GOOGLE_ADS_ACCOUNTS_API_PATH: string;
      ALL_GOOGLE_ADS_ACCOUNTS_SAVE_API_PATH: string;
      ALL_GOOGLE_ADS_FETCH_CAMPAIGNS_API_PATH: string;
      GOOGLE_ADS_AUTH_API_PATH: string;
      GOOGLE_ADS_AUTH_SAVE_CRED_API_PATH: string;
    }
  }
  


