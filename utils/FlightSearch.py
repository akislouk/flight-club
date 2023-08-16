import requests
from os import getenv as env
from datetime import datetime


class FlightData:
    """Represents an object with all the relevant information from the given data of a Tequila API response."""

    def __init__(self, data: dict[str,], stopover: bool = False):
        """Initializes a `FlightData` object with all the relevant information from the given data of the Tequila API response."""
        self.price: int = data["price"]
        self.link: str | None = data.get("deep_link")
        self.out_date = datetime.fromisoformat(data["route"][0]["local_departure"])
        self.return_date = datetime.fromisoformat(data["route"][-1]["local_departure"])
        self.origin_city: str = data["route"][0]["cityFrom"]
        self.origin_airport: str = data["route"][0]["flyFrom"]

        # Get the destination from the first return flight
        for flight in data["route"][1:]:
            if flight["return"] == 1:
                self.destination_city: str = flight["cityFrom"]
                self.destination_airport: str = flight["flyFrom"]
                break

        # Get the stopover city from the first destination that isn't the destination city
        self.via_city: str | None = None
        if stopover:
            for flight in data["route"]:
                if flight["cityTo"] != self.destination_city:
                    self.via_city: str = data["route"][0]["cityTo"]
                    break
        print(f"{self.destination_city}: {self.price}€")


class FlightSearch:
    """
    Class responsible for communicating with the Tequila API.

    Expects the following environment variables in order to work properly:
    - `TEQUILA_API`: Tequila API key
    - `TEQUILA_URL`: Tequila API endpoint, eg. https://api.tequila.kiwi.com/
    """

    def __init__(self) -> None:
        """Initializes a `FlightSearch` object."""
        self._headers = {"apikey": env("TEQUILA_API")}
        self._url = env("TEQUILA_URL") or "https://api.tequila.kiwi.com/"
        self._locations = self._url + "locations/query"
        self._search = self._url + "v2/search"

    def get_code(self, city: str) -> str | None:
        """Gets the IATA code of the given city from the Tequila API and returns it."""
        params = {"term": city, "location_types": "city", "limit": 1}
        res = requests.get(self._locations, params, headers=self._headers)
        if res.status_code != 200:
            return print("Something went wrong...\n", res.text)
        if len(res.json()["locations"]) == 0:
            return print(f"No airports found for {city}.")
        return res.json()["locations"][0]["code"]

    def get_flight(
        self,
        origin: str,
        destination: str,
        date_from: datetime,
        date_to: datetime,
        nights_min: int = 7,
        nights_max: int = 28,
        no_stops: bool = True,
    ) -> FlightData | None:
        """Gets the cheapest round-trip flight from the Tequila API based on the given parameters and returns it as a `FlightData` object."""
        params = {
            "fly_from": origin,
            "fly_to": destination,
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "nights_in_dst_from": nights_min,  # Minimum nights in destination
            "nights_in_dst_to": nights_max,  # Maximum nights in destination
            "one_for_city": 1,  # Returns only the cheapest flight for each city
            "max_stopovers": 0,  # Returns only direct flights
            "curr": "EUR",
        }
        res = requests.get(self._search, params, headers=self._headers)
        result = res.json()
        if res.status_code != 200:
            return print("Something went wrong...\n", result["message"])

        if len(result["data"]) > 0:
            return FlightData(result["data"][0])

        if no_stops:
            return print(f"No flights available for {destination}.")

        # Increase the maximum number of stopovers to 2 (1 for each way) and try again
        params["max_stopovers"] = 2
        res = requests.get(self._search, params, headers=self._headers)
        result = res.json()
        if res.status_code != 200:
            return print("Something went wrong...\n", result["message"])

        return (
            FlightData(result["data"][0], stopover=True)
            if len(result["data"]) > 0
            else print(f"No flights available for {destination}.")
        )
