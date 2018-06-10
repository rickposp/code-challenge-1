import os
import pandas as pd
from sodapy import Socrata
from datetime import datetime
import math

pd.set_option('display.max_columns', None)

nasa_dns = "data.nasa.gov"
nasa_meteorite_data_set = "y77d-th95"

def convert_string_to_datetime(input_series):
    retval = None
    try:
        retval = datetime.strptime(input_series['year'], '%Y-%m-%dT%H:%M:%S.%f')
    except Exception as e:
        print(e)
        raise e
    return retval

def strip_nan(input_series):
    year = input_series['year']
    if type(year) == float:
        if math.isnan(year):
            return False
    return True

def filter_by_year(input_series, year):
    date = input_series['year']
    return date.year == year

def main():
    app_token = os.environ.get("NASA_APP_TOKEN")

    client = None
    if app_token != None:
        print("Using credentials")
        client = Socrata(nasa_dns, app_token)
    else:
        print("Incomplete credentials detected, using unauthorized API calls")
        client = Socrata(nasa_dns, None)

    results = client.get(nasa_meteorite_data_set, limit=1000000)

    df = pd.DataFrame.from_records(results)

    series = df.apply(strip_nan, axis=1)
    df = df.loc[series]
    series = df.apply(convert_string_to_datetime, axis=1)
    df = df.drop("year", axis=1)
    df = df.assign(year=series)

    series = df.apply(filter_by_year, axis=1, args=(2008,))
    df = df.loc[series]
    client.close()

    print("Meteor Strikes in 2008: " + str(df.shape[0]))

if __name__ == '__main__':
    main()
