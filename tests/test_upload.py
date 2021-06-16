import pytest
from .conftest import testserver
import requests

def test_file_upload(testserver):
    with open('tests/audio/farsi_test.wav', 'rb') as file_in:
        filename = 'farsi_test.wav'
        data = {'language': 'fa'}
        files = {'file': file_in}

        r = requests.post('http://127.0.0.1:5000/upload', files=files, data=data)
        print(r.status_code, r.reason)
        print(r.text)
        assert False # check filecontents from output page
