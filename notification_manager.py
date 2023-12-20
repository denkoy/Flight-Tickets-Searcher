from twilio.rest import Client
import smtplib
from sensitive_data import SensitiveData


class NotificationManager:
    def __init__(self):
        self.secret_data = SensitiveData()
        self.num = self.secret_data.twilio_num
        self.sid = self.secret_data.twilio_sid
        self.token = self.secret_data.twilio_token
    #This class is responsible for sending notifications with the deal flight details.

    def send_notification(self, price, departure, codedep, arrival, codearr, from_, to, flag):
        if flag == 0:
            y_or_n = "YES"
        else:
            y_or_n = "NO"
        self.client = Client(self.sid, self.token)
        self.message = self.client.messages \
            .create(body=f"Low price alert! Only GBP{price} to fly from {departure}-{codedep} to {arrival}-{codearr} from {from_} to {to}, direct flight: {y_or_n}.", from_=self.num, to="+359877272909")
        print(self.message.status)

    def send_email(self, first_names, surnames, emails, price, departure, codedep, arrival, codearr, from_, to, flag):
        if flag == 0:
            y_or_n = "YES"
        else:
            y_or_n = "NO"

        my_email = self.secret_data.gmail_username
        for i in range(0, len(emails)):
            with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=my_email, password=self.secret_data.gmail_password)
                connection.sendmail(from_addr=my_email, to_addrs=emails[i],
                                    msg=f"Subject:FLIGHT ALERT!\n\n Hey, {first_names[i]} {surnames[i]}!\n Low price alert! Only GBP{price} to fly from {departure}-{codedep} to {arrival}-{codearr} from {from_} to {to}, direct flight: {y_or_n}.")
