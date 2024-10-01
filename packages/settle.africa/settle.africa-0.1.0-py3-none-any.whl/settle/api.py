import requests
from .auth import get_auth_headers
from .settings import get_env_var

def make_request(endpoint: str, data: dict = None):
    base_url = get_env_var('BASE_URL')
    headers = get_auth_headers()
    response = requests.post(f"{base_url}/{endpoint}", json=data, headers=headers)
    response.raise_for_status()
    return response.json()
