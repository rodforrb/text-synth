import pytest
from .conftest import myserver


def test_connection(myserver):
    myserver.send(b"GET / HTTP/1.1\r\n\r\n")