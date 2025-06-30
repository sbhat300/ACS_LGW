# Import necessary modules from the Google Ads API client library
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from LGW_utils import handle_google_ads_exception
from dotenv import load_dotenv
import os
import uuid

def create_google_ads_account() -> str:
    """
    Creates a new Google Ads client account under the specified manager account.

    Returns:
        new_customer_id (str): The resource name of the newly created customer account
        
    Raises:
        Exception: If the Google Ads client could not be initialized (likely invalid credentials)
        Exception: If the Google Ads customer account could not be created
    """
    load_dotenv()
    
    try:
        client = GoogleAdsClient.load_from_storage(os.getenv('GOOGLE_ADS_YAML_LOCATION'))
    except Exception as e:
        raise Exception(f'Error initializing Google Ads client: {e}')
        
    manager_customer_id = os.getenv('GOOGLE_ADS_LOGIN_CUSTOMER_ID')
    
    customer_service = client.get_service("CustomerService")

    # Create a new customer (account)
    customer = client.get_type("Customer")
    customer.descriptive_name = f"Account {uuid.uuid4()}" # Unique name
    customer.currency_code = "USD"
    customer.time_zone = "America/New_York"

    try:
        # Send the request to create the customer
        response = customer_service.create_customer_client(
            customer_id=manager_customer_id,
            customer_client=customer,
        )
        new_customer_resource_name = response.resource_name

        # Extract the new customer ID from the resource name
        new_customer_id = new_customer_resource_name.split('/')[-1]
        return new_customer_id
    except GoogleAdsException as ex:
        handle_google_ads_exception(ex)


if __name__ == "__main__":

    new_account_id = create_google_ads_account()

    if new_account_id:
        print(f"\nNew account created successfully. Customer ID: {new_account_id}")
    else:
        print("\nFailed to create new Google Ads account.")
