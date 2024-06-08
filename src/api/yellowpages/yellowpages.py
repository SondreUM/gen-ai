import requests
import json
from pathlib import Path
from config import DATA_PATH, KEY_PATH
from api.api import APIinterface

API_KEY = None

""" Class for interacting with the 1881 API"""
class YellowpagesAPI(APIinterface):

    def __init__(self):

        path: Path = DATA_PATH.joinpath("yellowpages_data")
        path.mkdir(parents=True, exist_ok=True)

        for file in path.iterdir():
            file.unlink()

        try:
            with open(KEY_PATH / "1881_key.txt") as file:
                self.API_KEY = file.read().strip()
                if self.API_KEY == "":
                    raise FileNotFoundError
        except FileNotFoundError:
            print("1881 API key not provided. Please add it to keys/1881_key.txt")
            self.API_KEY = None
            return

        self.headers = {"Cache-Control": "no-cache", "Ocp-Apim-Subscription-Key": self.API_KEY}
        self.path = path

    """ Search for a company name in the 1881 API, and write the results to disk"""
    def search(self, query: str) -> list[dict]:

        if self.API_KEY is None:
            return []

        # Company name needs to have "%20" instead of spaces
        query = query.replace(" ", "%20")
        URL = f"https://services.api1881.no/search/company?query={query}"

        # Make a request for the company name
        response = requests.get(URL, headers=self.headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return []

        data = response.json()

        # Write the response to a file
        string_data = json.dumps(data, indent=4)
        resultpath = self.path / f"{query}_search_result.json"
        with resultpath.open("w") as file:
            file.write(string_data)

        return data["contacts"]

    """ Get the details of a company from the 1881 API, and write the results to disk"""
    def get(self, id: int, name: str) -> dict:

        if self.API_KEY is None:
            return {}

        URL = f"https://services.api1881.no/lookup/organizationnumber/{id}"
        response = requests.get(URL, headers=self.headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            return {}

        contact_data = response.json()

        # Write the response to a file
        string_contact = json.dumps(contact_data, indent=4)
        filepath = self.path / f"{name}.json"
        with filepath.open("w") as file:
            file.write(string_contact)

        return contact_data
