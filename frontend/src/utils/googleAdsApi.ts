import axios from "axios";
import { Campaign } from "../types/campaign";

export const fetchCampaigns = async (): Promise<Campaign[]> => {
  try {
    const response = await axios.post(
      "http://localhost:8000/api/v1/google/fetch-campaigns",
      {}, // Request body burada boş olabilir, çünkü API sadece başlık bilgisi (Authorization) istiyor
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`, // Token'ı doğru şekilde alıyoruz
        },
      }
    );

    if (!response.data) {
      return [];
    }
    const campaigns = response.data.campaigns.map((campaign: any) => ({
          campaign_id: campaign.campaign_id,
          name: campaign.name,
          status: campaign.status,
          cost: campaign.cost || 0, // Provide default values if necessary
          ctr: campaign.ctr || 0,
          clicks: campaign.clicks || 0,
          conversion_value: campaign.conversion_value || 0,
      }));
    return campaigns;
  } catch (error: unknown) {
    // Error tipi 'unknown' olduğu için, 'error'ı doğru şekilde kontrol etmeliyiz
    if (error instanceof Error) {
      // Error nesnesi 'instanceof Error' ile kontrol ediliyor
      throw new Error(`Failed to fetch campaigns: ${error.message}`);
    } else {
      throw new Error("An unknown error occurred");
    }
  }
};
