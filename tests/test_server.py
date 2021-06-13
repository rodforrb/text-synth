import pytest
from .conftest import testserver
from http import client

def test_url_upload_get(testserver):
    testserver.request('GET', '/upload')
    response = testserver.getresponse()
    
    assert response.status == 200

def test_url_upload_post(testserver):
    testserver.request('POST', '/upload')
    response = testserver.getresponse()
    
    assert response.status == 302
