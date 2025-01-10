export interface Campaign {
    campaign_id: string;
    name: string;
    status: string;
    cost: number; // in USD
    ctr: number; // as a decimal (e.g., 0.05 for 5%)
    clicks: number;
    conversion_value: number;
}
