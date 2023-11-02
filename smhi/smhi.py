import argparse
import requests
import sys


class SmhiParser:
    """
    Class to handle communication with and extract data from the SMHI Open API.
    """

    BASE_URL = "https://opendata-download-metobs.smhi.se/api"

    def __init__(self, suffix=".json"):
        self.suffix = suffix

    def _make_request(self, session: requests.Session, path=""):
        r = session.get(self.BASE_URL + path + self.suffix)
        return r

    def check_connection(self, session: requests.Session, path=""):
        r = self._make_request(session, path)
        return r.status_code


def parse_args(args):
    parser = argparse.ArgumentParser(
        description="""Script to extract data from SMHI's Open API"""
    )
    parser.add_argument(
        "--parameters", action="store_true", help="List SMHI API parameters"
    )
    parser.add_argument(
        "--temperatures",
        action="store_true",
        help="List SMHI API temperatures for stations",
    )
    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])
    if args.parameters:
        parser = SmhiParser()
        for i in range(1, 41):
            param = str(i)
            with requests.Session() as session:
                response = parser._make_request(
                    session, f"/version/latest/parameter/{param}"
                )
            data = response.json()
            title = data["title"].split(":")[0]
            summary = "".join(["(", data["summary"], ")"])
            print(param + ",", title, summary)

    if args.temperatures:
        parser = SmhiParser()
        largest_temp = 0
        lowest_temp = 0
        largest_station = ""
        lowest_station = ""

        with requests.Session() as session:
            response = parser._make_request(session, "/version/latest/parameter/2")
        stations_dict = response.json()
        stations = [s["key"] for s in stations_dict["station"]]

        with requests.Session() as session:
            for i, s in enumerate(stations):
                response = parser._make_request(
                    session,
                    f"/version/latest/parameter/2/station/{s}/period/latest-day/data",
                )
                # 404 Client Error for stations without period=latest-day
                if response.status_code != 200:
                    continue
                data = response.json()
                if data["value"]:
                    temp = float(data["value"][0]["value"])
                    station = data["station"]["name"]
                    if temp > largest_temp:
                        largest_temp = temp
                        largest_station = station
                    if temp < lowest_temp:
                        lowest_temp = temp
                        lowest_station = station

        print("Highest temperature:", largest_station, largest_temp, "degrees")
        print("Lowest temperature:", lowest_station, lowest_temp, "degrees")


if __name__ == "__main__":
    main()
