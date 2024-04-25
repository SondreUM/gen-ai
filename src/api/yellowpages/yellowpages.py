import requests
import json
from pathlib import Path
from config import DATA_PATH, KEY_PATH

API_KEY = None

""" Search for a company name in the 1881 API, and write the results to disk"""
def get_yellowpages_data(company_name: str):

    path: Path = DATA_PATH.joinpath("yellowpages_data")
    path.mkdir(parents=True, exist_ok=True)

    for file in path.iterdir():
        file.unlink()

    try:
        with open(KEY_PATH / "1881_key.txt") as file:
            API_KEY = file.read().strip()
    except FileNotFoundError:
        print("1881 API key not provided. Please add it to keys/1881_key.txt")
        return False

    headers = {'Cache-Control': 'no-cache',
               'Ocp-Apim-Subscription-Key': API_KEY}

    # Company name needs to have "%20" instead of spaces
    company_name = company_name.replace(" ", "%20")
    URL = f"https://services.api1881.no/search/company?query={company_name}"

    # Make a request for the company name
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return False

    # Write the response to a file
    data = response.json()
    string_data = json.dumps(data, indent=4)
    resultpath = path / f"{company_name}_search_result.json"
    with resultpath.open("w") as file:
        file.write(string_data)

    # Request info for top 3 results and write to file
    first_3 = data['contacts'][:3]
    for contact in first_3:
        orgnum = contact['organizationNumber']
        URL2 = f"https://services.api1881.no/lookup/organizationnumber/{orgnum}"
        response = requests.get(URL2, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")

        contact_data = response.json()
        string_contact = json.dumps(contact_data, indent=4)

        filepath = path / f"{contact['name']}.json"
        with filepath.open("w") as file:
            file.write(string_contact)

    return True
