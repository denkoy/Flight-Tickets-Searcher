import requests
from sensitive_data import SensitiveData


class UserSettings:
    def __init__(self):
        self.secret_data = SensitiveData()
        self.url = self.secret_data.sheety_link_users
        self.auth = self.secret_data.sheety_auth

    def add_row(self, first_name, last_name, email):

        json_to_add = {"user": {"firstName": first_name,
                                "surname": last_name,
                                "email": email}}
        self.response = requests.post(url=f"{self.url}", headers=self.auth, json=json_to_add)
        self.response.raise_for_status()

    def get_data(self):
        response_get = requests.get(url=self.url, headers=self.auth)
        response_get.raise_for_status()
        self.data = response_get.json()
        self.emails = []
        self.first_names = []
        self.last_names = []
        for i in self.data["users"]:
            self.first_names.append(i["firstName"])
            self.last_names.append(i["surname"])
            self.emails.append(i["email"])
