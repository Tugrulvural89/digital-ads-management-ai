from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.auth.exceptions import RefreshError
from google.oauth2.credentials import Credentials
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class GoogleAdsService:
    def __init__(self, credentials: Dict[str, str], developer_token: str, login_customer_id: Optional[str] = None):
        """
        Initialize the Google Ads service.

        Args:
            credentials (Dict[str, str]): Google OAuth2 credentials (token, refresh_token, etc.).
            developer_token (str): Google Ads developer token.
            login_customer_id (Optional[str]): Login customer ID for managing accounts.
        """
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
        """
        Create and return a Google Ads client.

        Returns:
            GoogleAdsClient: Authenticated Google Ads client.
        """
        return GoogleAdsClient(
            credentials=self.credentials,
            developer_token=self.developer_token,
            login_customer_id=self.login_customer_id
        )

    def get_reports(self, customer_id: str, query: str) -> List[Dict]:
        """
        Fetch reports from Google Ads API.

        Args:
            customer_id (str): Google Ads customer ID.
            query (str): GAQL (Google Ads Query Language) query.

        Returns:
            List[Dict]: List of report data.
        """
        try:
            client = self._get_client()
            google_ads_service = client.get_service("GoogleAdsService")
            response = google_ads_service.search(customer_id=customer_id, query=query)
            results = []
            for row in response:
                campaign = row.campaign
                metrics = row.metrics
                results.append({
                    'campaign_id': campaign.id,
                    'campaign_name': campaign.name,
                    'impressions': metrics.impressions,
                    'clicks': metrics.clicks,
                    'cost': metrics.cost_micros / 1e6  # Convert micros to currency
                })
            return results
        except GoogleAdsException as e:
            logger.error(f"Google Ads API error: {e}")
            raise
        except RefreshError as e:
            logger.error(f"Token refresh error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def get_ad_accounts(self, customer_id: str) -> List[Dict]:
        try:
            client = self._get_client()
            google_ads_service = client.get_service("GoogleAdsService")
            query = """
                SELECT customer_client.client_customer, customer_client.descriptive_name
                FROM customer_client
                WHERE customer_client.level = 1
            """
            response = google_ads_service.search(customer_id=customer_id, query=query)
            results = []
            for row in response:
                results.append({
                    'account_id': row.customer_client.client_customer,
                    'name': row.customer_client.descriptive_name
                })
            return results
        except GoogleAdsException as e:
            logger.error(f"Google Ads API error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

        