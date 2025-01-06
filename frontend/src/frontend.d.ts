declare module "*.svg" {
    const content: string;
    export default content;
  };


  declare namespace NodeJS {
    interface ProcessEnv {
      GOOGLE_CLIENT_ID: string;
    }
  }
  


