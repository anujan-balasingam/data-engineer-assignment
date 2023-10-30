import argparse
import requests
import json

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
            path = f"/version/latest/parameter/{i}"
            response = p._make_request(path)
            data = response.json()
    
            title = data["title"].split(":")[0]
            summary = "(" + data["summary"] + ")"
            print(str(i)+",", title, summary)

    if args.temperatures:
        path = ""
        p = SmhiParser()
        # response = p.check_connection()
        # print(response)
        response = p._make_request(path)
        data = response.json()
        # Writing to sample.json
        with open("sample.json", "w") as outfile:
            obj = json.dumps(data, indent=2, ensure_ascii=False)
            outfile.write(obj)


if __name__ == "__main__":
    main()
