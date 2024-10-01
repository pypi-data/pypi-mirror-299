import requests
from .settings import get_base_url
import datetime
from decouple import config

auth_token = None
expiry_time = None
user_id = config.get("SETTLE_ID")
password = config.get("SETTLE_PASSWORD")
settle_mode = config.get("SETTLE_MODE", default="live")
base_url = get_base_url()


def is_token_expired(expiry):
    expiry_date = datetime.strptime(expiry, "%d/%m/%Y")
    return datetime.now() >= expiry_date


def set_credentials(user_id, password):
    global auth_token, expiry_time
    # Simulate an API call to get new credentials
    response = requests.post(base_url, data={"user_id": user_id, "password": password})
    if response.status_code == 200:
        auth_token = response.json()
        expiry_time = auth_token["expiry"]
    else:
        raise Exception("Authentication failed")


def get_headers():
    global auth_token, expiry_time
    if not auth_token:
        raise Exception(
            "You need to authenticate first or Authentication credentials invalid"
        )

    if is_token_expired(expiry_time):
        set_credentials(user_id, password)

    return {
        "Content-Type": "application/json",
        "id": auth_token["id"],
        "token": auth_token["token"],
        "expiry": auth_token["expiry"],
        "mode": settle_mode,
    }
