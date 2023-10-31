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

    def _make_request(self, path=""):
        r = requests.get(self.BASE_URL+path+self.suffix)
        return r

    def check_connection(self, path=""):
        r = self._make_request(path)
        return r.status_code


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
            path = f"/version/latest/parameter/{param}"
            response = parser._make_request(path)
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
        response = parser._make_request("/version/latest/parameter/2")
        stations_dict = response.json()
        stations = [s["key"] for s in stations_dict["station"]]

        for s in stations:
            response =  parser._make_request(f"/version/latest/parameter/2/station/{s}/period/latest-day/data")
            # throws 404 Client Error for stations that do not have data for period=latest-day
            if response.status_code != 200:
                continue
            data = response.json()
            if data["value"]:
                # temp = float(data["value"][0]["value"])
                # station = data["station"]["name"]
                if float(data["value"][0]["value"]) > largest_temp:
                    largest_temp = float(data["value"][0]["value"])
                    larg_station =  data["station"]["name"]
                if float(data["value"][0]["value"]) < lowest_temp:
                    lowest_temp = float(data["value"][0]["value"])
                    low_station =  data["station"]["name"]
        
        print("Highest temperature:", larg_station, largest_temp, "degrees")
        print("Lowest temperature:", low_station, lowest_temp, "degrees")
        # print("Station", data["station"]["name"], "Temperature", data["value"][0]["value"], "degrees", "Quality", data["value"][0]["quality"])

        # for debugging
        # obj = json.dumps(data, indent=2, ensure_ascii=False)
        # outfile.write(obj)



if __name__ == "__main__":
    main()
