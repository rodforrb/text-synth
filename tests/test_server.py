'''Tests for server connectivity and responses'''
import pytest
from .conftest import testserver

def test_url_upload_get(testserver):
    '''check for OK from server'''
    testserver.request('GET', '/upload')
    response = testserver.getresponse()
    
    assert response.status == 200

def test_url_upload_post(testserver):
    '''check for redirect on empty upload from server'''
    testserver.request('POST', '/upload')
    response = testserver.getresponse()
    
    assert response.status == 302
