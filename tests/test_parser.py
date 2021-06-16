import pytest
from .fileimport import _import

Parser = _import('parser').Parser

def test_parse_wav_file():
    '''Parse sample wav'''
    languages = ['fa']
    parser = Parser(languages)

    with open('tests/audio/farsi_test.wav', 'rb') as filein:
        text = parser.parse_file(filein, 'fa')
        assert text == 'من عرضه این کار را ندارم'

def test_invalid_lang_config():
    parser = Parser(['invalid'])

    with open('tests/audio/farsi_test.wav', 'rb') as filein:
        with pytest.raises(ValueError):
            text = parser.parse_file(filein, 'fa')
        
def test_invalid_lang_provided(): 
    parser = Parser(['fa'])

    with open('tests/audio/farsi_test.wav', 'rb') as filein:
        with pytest.raises(ValueError):
            text = parser.parse_file(filein, 'invalid')

