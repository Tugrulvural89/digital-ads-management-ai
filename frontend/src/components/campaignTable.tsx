import React from "react";
import { Campaign } from "../types/campaign";

interface CampaignTableProps {
    campaigns: Campaign[];
}

const CampaignTable: React.FC<CampaignTableProps> = ({ campaigns }) => {
    const getStatusColor = (status: string) => {
        switch (status.toLowerCase()) {
            case 'active':
                return 'bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium';
            case 'paused':
                return 'bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium';
            case 'ended':
                return 'bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-medium';
            default:
                return 'bg-gray-100 text-gray-800 px-2 py-1 rounded-full text-xs font-medium';
        }
    };

    return (
        <div className="w-full bg-white rounded-xl shadow-md p-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-6">
                Campaign Performance
                <span className="text-sm font-normal text-gray-500 ml-2">(Last 7 Days)</span>
            </h1>
            
            <div className="overflow-x-auto rounded-lg border border-gray-200">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Campaign ID
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Name
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Status
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Cost
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                CTR
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Clicks
                            </th>
                            <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                                Conversion Value
                            </th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {campaigns.map((campaign) => (
                            <tr 
                                key={campaign.campaign_id}
                                className="hover:bg-gray-50 transition-colors duration-200"
                            >
                                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-600">
                                    #{campaign.campaign_id}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    {campaign.name}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap">
                                    <span className={getStatusColor(campaign.status)}>
                                        {campaign.status}
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    ${campaign.cost.toFixed(2)}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    <span className="font-medium">
                                        {(campaign.ctr * 100).toFixed(2)}%
                                    </span>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                                    {campaign.clicks.toLocaleString()}
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-green-600 font-medium">
                                    ${campaign.conversion_value.toFixed(2)}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default CampaignTable;