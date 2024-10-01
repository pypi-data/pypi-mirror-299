from .api import make_request


def get_banks_and_mobile_money(country_id):
    """
        Fetch the list of financial institutions Settle is capable of transacting to in a specific country.

    Args:
        country_id (str): Id of the country.

    Returns:
        dict: A dictionary containing the list of financial institutions.

    Raises:
        Exception: If there is an error while fetching the financial institutions.
    """
    url = f"/fis/{country_id}"
    try:
        response = make_request(url, method="GET")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to fetch financial institutions: {str(e)}")


def get_countries():
    """
    Fetch the list of countries Settle is available for sending and receiving of transfers.
    Returns:
        dict: A dictionary containing the list of countries.
    Raises:
        Exception: If there is an error while fetching the countries.
    """
    url = "/countries"
    try:
        response = make_request(url, method="GET")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to fetch countries: {str(e)}")


def resolve_account_name(fi, account_number):
    """
    Fetch the receiver's account name by supplying their account number.
    Args:
        fi (str): The financial institution ID of the receiver.
        account_number (str): The account number/username of the receiver on the financial institution.
    Returns:
        dict: A dictionary containing the receiver's account name.
    Raises:
        Exception: If there is an error while fetching the account name.
    """
    url = f"/fisit/{fi}/{account_number}"
    try:
        response = make_request(url, method="GET")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to fetch account name: {str(e)}")


def get_exchange_rates(source, destination):
    """
    Get current exchange rates between two currencies of countries within Africa.

    Args:
        source (str): Id of the sending country.
        destination (str): Id of the receiver's country.

    Returns:
        dict: A dictionary containing the current exchange rates.

    Raises:
        Exception: If there is an error while fetching the exchange rates.
    """
    url = f"/rates/{source}/{destination}"
    try:
        response = make_request(url, method="GET")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to fetch exchange rates: {str(e)}")
