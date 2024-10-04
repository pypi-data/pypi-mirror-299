import os
import requests
from urllib.parse import urlencode
from .auth import AuthClient
from .session.client import SessionClient
from .user.client import UserClient
from .attendee.client import AttendeeClient

def default_success_handler(response):
    return response

class APIClient:
    def __init__(self, success_handler=None):
        self.auth_client = AuthClient()
        self.sessions = SessionClient(self)
        self.users = UserClient(self)
        self.attendees = AttendeeClient(self)
        self.access_token = None
        self.domain = None
        self.success_handler = success_handler or default_success_handler

    def set_domain(self, domain):
        self.domain = domain

    def set_credentials(self, access_key, secret_key, account_id):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_id = account_id
        return self.authenticate()

    def authenticate(self):
        response = self.auth_client.authenticate(self.access_key, self.secret_key, self.account_id, self.domain)

        if 'error' in response:
            return response['error']
        else:
            self.access_token = f"Bearer {response['access_token']}"

    def _make_request(self, method, endpoint, data=None, params=None):
        headers = {"Authorization": f"{self.access_token}"}
        url = endpoint
        
        if params:
            query_string = urlencode(params)
            url = f"{url}?{query_string}"

        response = requests.request(method, url, headers=headers, json=data)
        if response.status_code == 401:
            # Token expired, re-authenticate
            self.authenticate()
            headers["Authorization"] = self.access_token
            response = requests.request(method, url, headers=headers, json=data)
        if response.status_code == 404:
            try:
                result = response.json()
            except ValueError as e:
                result = {
                    "details": "Not found."
                }
        
        elif response.status_code in {400, 422}:
            result = response.json()
        elif response.status_code == 204:
            result = None
        else:
            response.raise_for_status()  # Raise an error if status code is not handled
            result = response.json()        


        self.success_handler(result)
        return response
