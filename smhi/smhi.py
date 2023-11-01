import argparse
import requests
import json
from datetime import date
from datetime import timedelta

class SmhiParser:
    """
    Class to handle communication with and extract data from the SMHI Open API.
    """
    BASE_URL = "https://opendata-download-metobs.smhi.se/api"

    def __init__(self, suffix=".json"):
        self.suffix = suffix

    def _make_request(self, session: requests.Session,  path=""):
        r = session.get(self.BASE_URL+path+self.suffix)
        return r

    def check_connection(self, session: requests.Session, path=""):
        r = self._make_request(session, path)
        return r.status_code


# def parse_args(args):
#     parser = argparse.ArgumentParser(...)
#     parser.add_argument...
#     # ...Create your parser as you like...
#     return parser.parse_args(args)

def main():
    parser = argparse.ArgumentParser(
        description="""Script to extract data from SMHI's Open API"""
    )
    parser.add_argument("--parameters", action="store_true", help="List SMHI API parameters")
    parser.add_argument("--temperatures", action="store_true", help="List SMHI API temperatures for stations")

    args = parser.parse_args()
    if args.parameters:
        parser = SmhiParser()
        for i in range(1,41):
            param = str(i)
            with requests.Session() as session:
               response = parser._make_request(session, f"/version/latest/parameter/{param}")
            data = response.json()
    
            title = data["title"].split(":")[0]
            summary = "".join(["(", data["summary"], ")"])
            print(param+",", title, summary)

    if args.temperatures:
        parser = SmhiParser()
        largest_temp = 0
        lowest_temp = 0
        larg_station = ""
        low_station = ""
        # missing_stations = []
        with requests.Session() as session:
            response = parser._make_request(session, "/version/latest/parameter/2")
        stations_dict = response.json()
        stations = [s["key"] for s in stations_dict["station"]]

        with requests.Session() as session:
            for i, s in enumerate(stations):
                response =  parser._make_request(session,f"/version/latest/parameter/2/station/{s}/period/latest-day/data")
                # throws 404 Client Error for stations that do not have data for period=latest-day)
                if response.status_code != 200:
                    # missing_stations.append(s)
                    continue
                data = response.json()
                if data["value"]:
                    temp = float(data["value"][0]["value"])
                    station = data["station"]["name"]
                    if temp > largest_temp:
                        largest_temp = temp
                        larg_station =  station
                    if temp < lowest_temp:
                        lowest_temp = temp
                        low_station =  station
        
        print("Highest temperature:", larg_station, largest_temp, "degrees")
        print("Lowest temperature:", low_station, lowest_temp, "degrees")
        # print("The number of stations missing", len(missing_stations))




if __name__ == "__main__":
    main()
