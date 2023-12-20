import requests
from flight_data import FlightData
from flight_search import FlightSearch
from notification_manager import NotificationManager
from user_adder import UserSettings
from sensitive_data import SensitiveData


class DataManager:
    def __init__(self):

        self.user_settings = UserSettings()
        self.secret_data = SensitiveData()
        self.url = self.secret_data.sheety_link_prices
        self.headers = self.secret_data.sheety_auth
        response_get = requests.get(url=self.url, headers=self.headers)
        response_get.raise_for_status()
        self.data = response_get.json()
        self.city_list = []
        self.fares = []
        for i in self.data["prices"]:
            self.city_list.append(i["city"])
            self.fares.append(i["lowestPrice"])

        j = 2
        search = FlightData()
        iata_list = []
        for i in self.city_list:
            temp = search.get_id(i)
            iata_list.append(temp)
            sheets_input = {"price": {"iataCode": temp}}
            response_put = requests.put(url=f"{self.url}/{j}", headers=self.headers, json=sheets_input)
            response_put.raise_for_status()
            j += 1

        flight_finder = FlightSearch()
        j = 2
        for i in iata_list:
            temp = flight_finder.search_flight(i, 0)
            flag = 0
            print(temp["_results"])
            if int(temp["_results"]) == 0:
                temp = flight_finder.search_flight(i, 2)
                flag = 1
            if int(temp["data"][0]["price"]) < self.fares[j-2] and int(temp["_results"]) != 0:
                sheets_input = {"price": {"lowestPrice": int(temp["data"][0]["price"])}}
                response_put = requests.put(url=f"{self.url}/{j}", headers=self.headers, json=sheets_input)
                response_put.raise_for_status()
                send_notif = NotificationManager()

                #Uncomment if u want to send SMS also :)
                #send_notif.send_notification(price=temp["data"][0]["price"],departure="Sofia",codedep="SOF",arrival=temp["data"][0]["cityTo"],codearr=temp["data"][0]["cityCodeTo"],from_=temp["data"][0]["local_departure"][:10],to=temp["data"][0]["route"][1]["local_arrival"][:10],flag=flag)

                users_info = UserSettings()
                users_info.get_data()
                send_notif.send_email(users_info.first_names, users_info.last_names, users_info.emails, price=temp["data"][0]["price"], departure="Sofia", codedep="SOF", arrival=temp["data"][0]["cityTo"], codearr=temp["data"][0]["cityCodeTo"], from_=temp["data"][0]["local_departure"][:10], to=temp["data"][0]["route"][1]["local_arrival"][:10], flag=flag)
            j += 1
