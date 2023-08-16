import requests
from os import getenv as env


class DataManager:
    """
    Class responsible for communicating with the Sheety API.

    Expects the following environment variables in order to work properly:
    - `SHEETY_AUTH`: Sheety authorization, eg. "Basic cGFzc3dvcmQ"
    - `SHEETY_URL`: Sheety API endpoint, eg. https://api.sheety.co/:api_key/:filename
    """

    def __init__(self) -> None:
        """Initializes a `DataManager` object."""
        self.data: list[dict[str, str | int]] = []
        self._init_data: list[dict[str, str | int]] = []
        self._headers = {"Authorization": env("SHEETY_AUTH")}
        self._url = env("SHEETY_URL")

    def get_data(self) -> None:
        """
        Fetches the flight prices data from the Google sheet. If everything went well,
        stores the data in the `data` attribute and returns it, otherwise returns `None`.
        """
        res = requests.get(self._url + "/prices", headers=self._headers)
        if res.status_code != 200:
            return print("Something went wrong...\n", res.text)
        self.data = res.json()["prices"]
        self._init_data = res.json()["prices"]

    def get_users(self) -> list[dict[str, str]] | None:
        """Fetches the users from the Google sheet. Returns the users if everything went well, `None` otherwise."""
        res = requests.get(self._url + "/users", headers=self._headers)
        return print(res.text) if res.status_code != 200 else res.json()["users"]

    def add_user(self, user: dict[str, str]) -> None:
        """Adds a user's info to the Google sheet."""
        body = {"user": user}
        res = requests.post(self._url + "/users", headers=self._headers, json=body)
        print(res.text if res.status_code != 200 else "You are in the Flight Club!")

    def update(self) -> None:
        """Updates the Google sheet with the new flight data."""
        for i in range(len(self.data)):
            if self.data[i] == self._init_data[i]:
                continue
            url = f"{self._url}/prices/{self.data[i]['id']}"
            body = {"price": self.data[i]}
            res = requests.put(url, headers=self._headers, json=body)
            res.status_code != 200 and print("Something went wrong...\n", res.text)
        print("Update completed.")
