import requests


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def set_token(self, token):
        self.session.headers.update({
            "x-auth-token": token
        })

    def get(self, endpoint):
        return self.session.get(
            f"{self.base_url}{endpoint}"
        )

    def post(self, endpoint, payload=None):

        return self.session.post(
            f"{self.base_url}{endpoint}",
            data=payload
        )

    def put(self, endpoint, payload=None):
        return self.session.put(
            f"{self.base_url}{endpoint}",
            json=payload
        )

    def patch(self, endpoint, payload=None):
        return self.session.patch(
            f"{self.base_url}{endpoint}",
            json=payload
        )

    def delete(self, endpoint):
        return self.session.delete(
            f"{self.base_url}{endpoint}"
        )