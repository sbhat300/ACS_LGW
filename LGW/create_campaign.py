from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from LGW_utils import handle_google_ads_exception
from dotenv import load_dotenv
import os
import uuid
from create_account import create_google_ads_account

def create_google_ads_campaign(customer_id: str, campaign_name: str = 'Campaign'):
    """
    Creates a new Google Ads campaign for the specified customer ID.

    Args:
        customer_id (str): The account id for which the campaign should be created
        campaign_name (str): The name of the campaign

    Returns:
        The resource name of the newly created campaign, or None if creation fails.
        
    Raises:
        Exception: If the Google Ads client could not be initialized (likely invalid credentials)
        Exception: If the campaign budget could not be created
        Exception: If the campaign could not be created
    """
    load_dotenv()
    
    try:
        client = GoogleAdsClient.load_from_storage(os.getenv('GOOGLE_ADS_YAML_LOCATION'))
    except Exception as e:
        raise Exception(f'Error initializing Google Ads client: {e}')
    
    # Get the services
    campaign_service = client.get_service("CampaignService")
    budget_service = client.get_service("CampaignBudgetService")

    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"{campaign_name} Budget {uuid.uuid4()}"
    campaign_budget.amount_micros = 1000000 # 1 USD (1 USD = 1,000,000 micros)
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )

    try:
        # Send the request to create the budget
        campaign_budget_response = budget_service.mutate_campaign_budgets(
            customer_id=customer_id,
            operations=[campaign_budget_operation]
        )
        budget_resource_name = campaign_budget_response.results[0].resource_name
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)

    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = campaign_name
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    
    campaign.status = client.enums.CampaignStatusEnum.PAUSED # Start as paused
    
    campaign.manual_cpc.enhanced_cpc_enabled = False
    campaign.campaign_budget = budget_resource_name # Link to the created budget

    # Set network settings
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_content_network = False # Exclude Display Network
    campaign.network_settings.target_partner_search_network = False

    try:
        # Send the request to create the campaign
        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id,
            operations=[campaign_operation]
        )
        campaign_resource_name = campaign_response.results[0].resource_name
        return campaign_resource_name
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)
    
if __name__ == '__main__':
    new_account_id = create_google_ads_account()
    print(f"\nAttempting to create a campaign in account: {new_account_id}...")
    campaign_resource = create_google_ads_campaign(new_account_id, "Test Campaign")

    if campaign_resource:
        print(f"\nCampaign created successfully: {campaign_resource}")
    else:
        print("\nFailed to create campaign.")