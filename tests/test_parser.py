import pytest
from .fileimport import _import
from .testdata import fa_text

Parser = _import('parser').Parser

def test_parse_wav_file():
    '''Parse sample wav'''
    languages = ['fa']
    parser = Parser(languages)

    with open('tests/audio/farsi_test.wav', 'rb') as filein:
        text = parser.parse_file(filein, 'fa')
        assert text == fa_text

def test_invalid_lang_config():
    parser = Parser(['invalid'])

    with open('tests/audio/farsi_test.wav', 'rb') as filein:
        with pytest.raises(ValueError):
            parser.parse_file(filein, 'fa')
        
def test_invalid_lang_provided(): 
    parser = Parser(['fa'])

    with open('tests/audio/farsi_test.wav', 'rb') as filein:
        with pytest.raises(ValueError):
            parser.parse_file(filein, 'invalid')

