import os
#import pandas as pd
from sodapy import Socrata

nasa_dns = "data.nasa.gov"
nasa_meteorite_data_set = "y77d-th95"

def main():
    app_token = os.environ["NASA_APP_TOKEN"]

    client = None
    if app_token != None:
        print("Using credentials")
        client = Socrata(nasa_dns, app_token)
    else:
        print("Incomplete credentials detected, using unauthorized API calls")
        client = Socrata(nasa_dns, None)

    results = client.get(nasa_meteorite_data_set, limit=2000)
    print(str(results))

    client.close()

if __name__ == '__main__':
    main()
