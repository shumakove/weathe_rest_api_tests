from jsonschema.validators import validate
from conftest import *
import json
import jsonschema
import pytest
import requests
import re


class TestBase:

    def test_base_response(self):
        assert requests.get(base_url + '/current.json?key=' + api_key + '&q=50.50').status_code == 200

    def test_response_not_null(self):
        assert requests.get(base_url + '/current.json?key=' + api_key + '&q=50.50').json() is not ''

    def test_weather_by_city(self):
        assert requests.get(base_url + '/current.json?key=' + api_key + '&q=Barcelona').json()['location']['name'] \
               == 'Barcelona'

    def test_weather_by_zip(self):
        assert requests.get(base_url + '/current.json?key=' + api_key + '&q=10001').json()['location']['name'] \
               == 'New York'

    def test_language_parameter(self):
        assert re.search('[а-яА-Я]', requests.get(base_url + '/current.json?key=' + api_key + '&q=10001&lang=ru').json()['current']['condition']['text'])

    def test_validate_schema(self):
        response = requests.get(base_url + '/current.json' + '?key=' + api_key + '&q=45.50')
        weather_object = response.json()
        try:
            validate(instance=weather_object, schema=schema)
        except jsonschema.exceptions.ValidationError or jsonschema.exceptions.SchemaError as exc:
            assert False, f' raised an exception {exc}'
