from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class GoogleAdsService:
    def __init__(self, credentials: Dict[str, str], developer_token: str, login_customer_id: Optional[str] = None):
        self.credentials = Credentials(
            token=credentials.get('token'),
            refresh_token=credentials.get('refresh_token'),
            token_uri=credentials.get('token_uri'),
            client_id=credentials.get('client_id'),
            client_secret=credentials.get('client_secret'),
            scopes=credentials.get('scopes')
        )
        self.developer_token = developer_token
        self.login_customer_id = login_customer_id

    def _get_client(self) -> GoogleAdsClient:
        return GoogleAdsClient(
            credentials=self.credentials,
            developer_token=self.developer_token,
            login_customer_id=self.login_customer_id
        )

    def fetch_campaigns(self, customer_id: str) -> List[Dict]:
        """
        Fetch campaigns and metrics from Google Ads API.

        Args:
            customer_id (str): Customer ID of the Google Ads account.

        Returns:
            List[Dict]: List of campaign data.
        """
        try:
            client = self._get_client()
            ga_service = client.get_service("GoogleAdsService")
            query = """
                SELECT 
                    campaign.id, 
                    campaign.name, 
                    campaign.status, 
                    metrics.clicks, 
                    metrics.ctr, 
                    metrics.cost_micros,
                    metrics.all_conversions_value
                FROM 
                    campaign
                WHERE 
                    segments.date DURING LAST_7_DAYS
                ORDER BY 
                    campaign.id
            """
            response = ga_service.search(customer_id=customer_id, query=query)

            # Enum eşlemesi
            CAMPAIGN_STATUS_MAP = {
                0: "UNSPECIFIED",
                1: "UNKNOWN",
                2: "ENABLED",
                3: "PAUSED",
                4: "REMOVED",
            }

            # Process the response
            campaigns = []
            for row in response:
                campaigns.append({
                    "campaign_id": row.campaign.id,
                    "name": row.campaign.name,
                    "status": CAMPAIGN_STATUS_MAP.get(row.campaign.status, "UNKNOWN"), 
                    "clicks": row.metrics.clicks,
                    "ctr": row.metrics.ctr,
                    "cost": row.metrics.cost_micros / 1_000_000,  # Convert micros to standard currency
                    "conversion_value": row.metrics.all_conversions_value
                })
            return campaigns

        except GoogleAdsException as ex:
            logging.error(f"Google Ads API error: {ex}")
            raise
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            raise
