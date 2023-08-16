from smtplib import SMTP
from os import getenv as env
from utils.FlightSearch import FlightData


class NotificationManager:
    """
    A class with utilities for sending alerts to users via SMS or email.

    Expects the following environment variables in order to work properly:
    - `EMAIL`: Gmail address
    - `PASSWORD`: Gmail app password
    - `TWILIO_SID`: Twilio account SID
    - `TWILIO_TOKEN`: Twilio account token
    - `TWILIO_NUMBER`: Twilio phone number
    - `OWNER_NUMBER`: Phone number used to sign up for Twilio
    """

    def __init__(self) -> None:
        """Initializes a `NotificationManager` object."""
        self._email = env("EMAIL")
        self._password = env("PASSWORD")
        self._sid = env("TWILIO_SID")
        self._token = env("TWILIO_TOKEN")
        self._number = env("TWILIO_NUMBER")
        self._owner_number = env("OWNER_NUMBER")

    def send_email(
        self, flight: FlightData, users: list[dict[str, str]] = None
    ) -> None:
        """Sends an email with the given flight information. If no recipient is provided, the email is sent to the owner of the app."""
        email = self._email
        users = users or [{"firstName": "Flight Club", "email": email}]
        with SMTP("smtp.gmail.com", 587) as conn:
            conn.starttls()
            conn.login(email, self._password)
            for user in users:
                conn.sendmail(email, user["email"], self.msg_formatter(flight, user))

    def send_sms(self, flight: FlightData, numbers: list[str] = None) -> None:
        """Utilizes the Twilio API to send an SMS with the given flight information. If no recipient is provided, the SMS is sent to the owner of the app."""
        from twilio.rest import Client
        from twilio.base.exceptions import TwilioRestException

        client = Client(self._sid, self._token)
        numbers = numbers or [self._owner_number]
        for number in numbers:
            try:
                message = client.messages.create(
                    body=self.msg_formatter(flight), from_=self._number, to=number
                )
                print("SMS status: ", message.status)
            except TwilioRestException as e:
                print("Error sending SMS:\n", e)

    def msg_formatter(self, flight: FlightData, user: dict[str, str] = None) -> str:
        """Uses the given flight data to create and return a message. If a user is provided, the message is formatted as an email."""
        msg = (
            f"Low price alert! Only {flight.price}€ to fly from {flight.origin_city}-"
            f"{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, "
            f"from {flight.out_date.strftime('%Y-%m-%d')} to {flight.return_date.strftime('%Y-%m-%d')}."
        )
        if flight.via_city:
            msg += f"\nThe flight has 1 stop at {flight.via_city}."
        if user:
            msg = f"From: Flight Club <{self._email}>\r\nTo: {user['firstName']} <{user['email']}> \r\nSubject:Cheap Tickets Detected!\r\n\r\n{msg}"
        return msg.encode("utf8")
