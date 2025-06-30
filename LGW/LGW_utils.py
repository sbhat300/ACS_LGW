
from google.ads.googleads.errors import GoogleAdsException

def handle_google_ads_exception(ex: GoogleAdsException):
    """
    Reports a GoogleAdsException in an easy to read way

    Args:
        customer_id (GoogleAdsException): The exception

    Raises:
        Exception: The formatted exception
    """
    
    exception = f"Request with ID '{ex.request_id}' failed with status '{ex.error.code().name}'\n"
    for error in ex.failure.errors:
        exception += "\tError: {error.message}\n"
        if error.location:
            for field_path_element in error.location.field_path_elements:
                exception += f"\t\tField: {field_path_element.field_name}\n"
    raise Exception(exception)