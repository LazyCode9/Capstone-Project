from api.api_client import APIClient
from config.environment import config


class NotesAPI:

    def __init__(self):

        self.client = APIClient(
            config.get("api_base_url")
        )

    def login(self, email, password):

        payload = {
            "email": email,
            "password": password
        }

        response = self.client.post(
            "/users/login",
            payload
        )

        if response.status_code == 200:

            token = response.json()["data"]["token"]

            self.client.set_token(token)

        return response
         

    def create_note(self, payload):

        return self.client.post(
            "/notes",
            payload
        )

    def get_all_notes(self):

        return self.client.get("/notes")

    def get_note(self, note_id):

        return self.client.get(
            f"/notes/{note_id}"
        )

    def update_note(self, note_id, payload):

        return self.client.put(
            f"/notes/{note_id}",
            payload
        )

    def delete_note(self, note_id):

        return self.client.delete(
            f"/notes/{note_id}"
        )
    def create_note(self, title, description, category):

        payload = {
            "title": title,
            "description": description,
            "category": category
        }

        return self.client.post(
            "/notes",
            payload
        )
    
    def health_check(self):

        return self.client.get(
            "/health-check"
        )
    
    def register_user(self, name, email, password):

        payload = {
            "name": name,
            "email": email,
            "password": password
        }

        return self.client.post(
            "/users/register",
            payload
        )