import argparse
import requests
import json

class SmhiParser:
    """
    Class to handle communication with and extract data from the SMHI Open API.
    """
    BASE_URL = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/{}/station/97280/period/latest-day/data"
    def __init__(self, suffix=".json"):
        self.suffix = suffix

    def _make_request(self, param="2", path=""):
        r = requests.get(self.BASE_URL.format(param)+self.suffix)
        return r

    def check_connection(self):
        r = self._make_request()
        return r.status_code


def main():
    parser = argparse.ArgumentParser(
        description="""Script to extract data from SMHI's Open API"""
    )
    parser.add_argument("--parameters", action="store_true", help="List SMHI API parameters")
    parser.add_argument("--temperatures", action="store_true", help="List SMHI API temperatures for stations")

    args = parser.parse_args()
    if args.parameters:
        p = SmhiParser()
        for i in range(1,41):
            param = str(i)
            response = p._make_request(param)
            data = response.json()
    
            title = data["title"].split(":")[0]
            summary = "(" + data["summary"] + ")"
            print(param+",", title, summary)

    if args.temperatures:
        url = "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/{}/period/latest-day/data"
        print("hämta temps")
        p = SmhiParser()
        param = "2"
        response = p.check_connection()
        print(response)
        # response = p._make_request(param)
        # data = response.json()
        # # Writing to sample.json
        # with open("sample.json", "w") as outfile:
        #     obj = json.dumps(data, indent=2, ensure_ascii=False)
        #     outfile.write(obj)


if __name__ == "__main__":
    main()
