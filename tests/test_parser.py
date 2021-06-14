from .rootdir.parser import Parser
from .conftest import testserver

def test_wav(testserver):
    languages = ['fa']
    parser = Parser(languages)

    with open('audio/farsi_test.wav') as filein:
        text = parser.parse_file(filein, 'fa')
        print(text)
        assert False

