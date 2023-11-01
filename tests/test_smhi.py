from smhi.smhi import SmhiParser
import requests
import json

def test_check_connection():
    parser = SmhiParser()
    with requests.Session() as session:
        assert 200 == parser.check_connection(session)

def test_make_request():
    parser = SmhiParser()
    with requests.Session() as session:
        response = parser._make_request(session)
        data = response.json()
        assert True == isinstance(data, dict)

