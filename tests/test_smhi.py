from smhi.smhi import SmhiParser
from smhi.smhi import parse_args
import requests
import json


def test_check_connection():
    """
    Test the connection to SMHI Open API function.
    """
    parser = SmhiParser()
    with requests.Session() as session:
        assert 200 == parser.check_connection(session)


def test_make_request():
    """
    Test the make_request function to ensure it returns a json and subsequently a dictionary for the BASE url.
    """
    parser = SmhiParser()
    with requests.Session() as session:
        response = parser._make_request(session)
        data = response.json()
        assert True == isinstance(data, dict)


def test_parse_args():
    """
    Test the parse_args function to ensure it returns the expected dictionary.
    """
    args = parse_args(["--temperatures"])
    assert True == args.temperatures
