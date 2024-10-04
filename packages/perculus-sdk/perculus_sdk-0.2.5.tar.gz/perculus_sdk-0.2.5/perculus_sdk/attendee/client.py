import os
from dotenv import load_dotenv, find_dotenv
load_dotenv()

class AttendeeClient:
    def __init__(self, client):
        self.client = client
        self.base_url = None

    def _make_request(self, method, endpoint, data=None, params=None):
        env_path = find_dotenv()
        if env_path:
            load_dotenv(env_path)
            self.base_url = os.getenv("PERCULUS_XAPI_URL")

        self.base_url = f"https://{self.client.domain}/xapi" if self.client.domain is not None else self.base_url
        url = f'{self.base_url}/{endpoint}'
        return self.client._make_request(method, url, data=data, params=params)
    
    def add_by_user_id(self, session_id, user_id, role=None):
        if role is None:
            return self.add_attendee(session_id, {
                "user_id": user_id,
            })
        else:
            return self.add_attendee(session_id, {
                "user_id": user_id,
                "role": role
            })

    def add_multiple_by_user_id(self, session_id, attendees):
        return self.add_multiple(session_id, attendees)
    
    def add_attendee(self, session_id, attendee):
        return self.add_multiple(session_id, [attendee])
    
    def add_multiple(self, session_id, attendees):
        return self._make_request("POST", f'session/{session_id}/attendees', attendees)
    
    def update_by_attendance_code(self, session_id, attendance_code, attendee):
        return self._make_request("PUT", f'session/{session_id}/attendee/{attendance_code}', attendee)
    
    def update_by_email(self, session_id, email, attendee):
        return self._make_request("PUT", f'session/{session_id}/attendee/{email}', attendee)
    
    def get_by_attendance_code(self, session_id, attendance_code):
        return self._make_request("GET", f'session/{session_id}/attendee/{attendance_code}')
    
    def search_attendees(self, session_id, params):
        return self._make_request("GET", f'session/{session_id}/attendees', params=params)
    
    def get_by_email(self, session_id, email):
        return self._make_request("GET", f'session/{session_id}/attendee/{email}')

    def delete_by_attendance_code_or_user_id(self, session_id, attendance_code_or_user_id):
        return self._make_request("DELETE", f'session/{session_id}/attendee/{attendance_code_or_user_id}')

    def delete_by_email(self, session_id, email):
        return self._make_request("DELETE", f'session/{session_id}/attendee/{email}')

    
    