import requests
from sensitive_data import SensitiveData

class FlightData:
    def get_id(self, name_of_city):
        self.secret_data=SensitiveData()
        self.teq_url = "https://tequila-api.kiwi.com/locations/query"
        self.apikey = self.secret_data.kiwi_apikey
        self.teq_headers = {"apikey": self.apikey}
        self.params = {"term": name_of_city}
        teq_response = requests.get(url=self.teq_url, headers=self.teq_headers, params=self.params)
        teq_response.raise_for_status()
        teq_data = teq_response.json()["locations"][0]["code"]
        return teq_data
