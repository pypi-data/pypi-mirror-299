import os
import requests
from dotenv import load_dotenv, find_dotenv
load_dotenv()

class AuthClient:
    def __init__(self):
        self.base_url = None

    def authenticate(self, access_key, secret_key, account_id, domain=None):

        env_path = find_dotenv()
        if env_path:
            load_dotenv(env_path)
            self.base_url = os.getenv("PERCULUS_AUTH_URL")
        
        if domain is None and self.base_url is None:
            return {
                "error": "You should set your domain or you should add auth url and xapi url to your .env file as 'PERCULUS_AUTH_URL' with 'PERCULUS_XAPI_URL'"
            }
        self.base_url = f"https://{domain}/auth" if domain is not None else self.base_url
        url = f"{self.base_url}/connect/token"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            "username": access_key, 
            "password": secret_key, 
            "account_id": account_id, 
            "client_id": "api", 
            "grant_type": "password"
        }
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        return response.json()