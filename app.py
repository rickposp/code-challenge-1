import os
import pandas as pd
from sodapy import Socrata
import requests
from xml.etree import ElementTree

nasa_dns = "data.nasa.gov"
nasa_meteorite_data_set = "y77d-th95"

world_bank_dns="api.worldbank.org"
world_bank_journal_data_set = "IP.JRN.ARTC.SC"

def main():
    app_token = os.environ["NASA_APP_TOKEN"]

    client = None
    if app_token != None:
        print("Using credentials")
        client = Socrata(nasa_dns, app_token)
    else:
        print("Incomplete credentials detected, using unauthorized API calls")
        client = Socrata(nasa_dns, None)

    results = client.get(nasa_meteorite_data_set)
    print(str(results))

    client.close()

    request = requests.get("http://api.worldbank.org/countries/aw/indicators/IP.JRN.ARTC.SC")
    parsed_response = ElementTree.fromstring(request.content)
    print(str(parsed_response))

if __name__ == '__main__':
    main()
