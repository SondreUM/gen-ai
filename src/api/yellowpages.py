
import requests
import json
from pathlib import Path
import os


API_KEY = None
PARENT_PATH = Path(__file__).parent
DATA_PATH = PARENT_PATH.joinpath("yellowpages_data")

""" Search for a company name in the 1881 API, and write the results to disk"""
def get_yellowpages_data(company_name: str):

    # clean up data directory
    json_files = os.listdir(f"{DATA_PATH}")
    for file in json_files:
        print(f"Removing {file}")
        os.remove(f"{DATA_PATH}/{file}")

    with open(PARENT_PATH / "1881_key.txt") as file:
        API_KEY = file.read().strip()

    headers = {'Cache-Control': 'no-cache',
               'Ocp-Apim-Subscription-Key': API_KEY}
    

    # Company name needs to have "%20" instead of spaces
    company_name = company_name.replace(" ", "%20")
    URL = f"https://services.api1881.no/search/company?query={company_name}"

    # Make a request for the company name
    response = requests.get(URL, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    # Write the response to a file
    data = response.json()
    string_data = json.dumps(data, indent=4)
    with open(DATA_PATH / f"{company_name}_search_result.json", "w") as file:
        file.write(string_data)


    # REMOVE THIS AND REPLACE WITH THE BELOW CODE ONCE 1881 SUBSCRIPTION IS FIXED
    # Get the organization number from the first result
    first = data['contacts'][0]
    orgnum = first['organizationNumber']

    # Make a request to the organization number API
    URL2 = f"https://services.api1881.no/lookup/organizationnumber/{orgnum}"
    response = requests.get(URL2, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return None
    
    data2 = response.json()
    string_data2 = json.dumps(data2, indent=4)

    with open(DATA_PATH / f"{first['name']}.json", "w") as file:
        file.write(string_data2)

    
    # # Request info for each contact and write to file
    # for contact in data['contacts']:
    #     orgnum = contact['organizationNumber']
    #     URL2 = f"https://services.api1881.no/lookup/organizationnumber/{orgnum}"
    #     response = requests.get(URL2, headers=headers)
    #     if response.status_code != 200:
    #         print(f"Error: {response.status_code}")
            
    #     contact_data = response.json()
    #     string_contact = json.dumps(contact_data, indent=4)

    #     with open(DATA_PATH / f"{contact['name']}.json", "w") as file:
    #         file.write(string_contact)

    

    return True