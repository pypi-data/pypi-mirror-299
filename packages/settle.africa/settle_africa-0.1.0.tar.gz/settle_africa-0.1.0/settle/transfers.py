from .api import make_request


def send_transfer(data):
    """
    Sends a transfer using the API.
    Parameters:
    - data: A dictionary containing the transfer data.
    Returns:
    - A JSON response containing the result of the transfer.
    Raises:
    - Exception: If there is an error while sending the transfer.

    Handle sending of transfers.
    """
    url = "/transfer"
    try:
        response = make_request(url, data=data, method="POST")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to send transfer: {str(e)}")


def verify_transfer(transfer_id):
    """
    Fetches a transaction to validate/verify its status or recall its details.
    Args:
        transfer_id (str): The ID of the transfer to be verified.
    Returns:
        dict: A dictionary containing the response from the API call.
    Raises:
        Exception: If the verification of the transfer fails.

    """
    url = f"/transaction/{transfer_id}"
    try:
        response = make_request(url, method="GET")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to verify transfer: {str(e)}")


def get_transaction_history(transaction_id):
    """
    Fetches a transaction to validate/verify its status or recall its details.
    Args:
        transfer_id (str): The ID of the transfer to be verified.
    Returns:
        dict: A dictionary containing the response from the API call.
    Raises:
        Exception: If the verification of the transfer fails.

    """
    url = f"/transaction/{transaction_id}"
    try:
        response = make_request(url, method="GET")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to fetch transaction: {str(e)}")


def estimate_fees_and_speed(source, destination, amount):
    """
    Args:
        source (str): Id of the sending country.
        destination (str): Id of the receiver's country.
        amount (float): The amount to be sent.
    Returns:
        dict: A dictionary containing the estimated fees and speed of the transfer.
    Raises:
        Exception: If there is an error while estimating fees and speed.

    """
    url = f"/rates/{source}/{destination}/{amount}"
    try:
        response = make_request(url, method="GET")
        return response.json()
    except Exception as e:
        raise Exception(f"Failed to estimate fees and speed: {str(e)}")
