'''
Tests for responses to uploading files to the server.
This represents user-facing functionality.
'''
import pytest
from .testdata import fa_text
from .conftest import testserver
import requests
from bs4 import BeautifulSoup

def test_file_upload(testserver):
    with open('tests/audio/farsi_test.wav', 'rb') as file_in:
        filename = 'farsi_test.wav'
        data = {'language': 'fa'}
        files = {'file': file_in}
        address = f'http://{testserver.host}:{str(testserver.port)}/upload'
        r = requests.post(address, files=files, data=data)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        text_output = soup.find('textarea').string
        assert text_output == fa_text