import os
import subprocess
from io import BytesIO
import json
from vosk import Model, KaldiRecognizer, SetLogLevel
from .models import Language

MODELS_PATH = os.path.dirname(os.path.realpath(__file__)) + '/models/'

class Parser:
    def __init__(self, allowed_languages):
        # silence KaldiRecognizer
        SetLogLevel(-1)

        self.allowed_languages = allowed_languages
        self.languages = []
        # import language models
        # English
        if 'en' in allowed_languages:
            model_en = Model(MODELS_PATH + "model-en")
            self.rec_en = KaldiRecognizer(model_en, 16000)
            self.languages.append(Language.English)
        # Persian
        if 'fa' in allowed_languages:
            model_fa = Model(MODELS_PATH + "model-fa")
            self.rec_fa = KaldiRecognizer(model_fa, 16000)
            self.languages.append(Language.Farsi)
        # Arabic
        if 'ar' in allowed_languages:
            model_ar = Model(MODELS_PATH + "model-ar")
            self.rec_ar = KaldiRecognizer(model_ar, 16000)
            self.languages.append(Language.Arabic)


    # parse audio file from upload
    def parse_file(self, file_data, language):
        rec = self.get_recognizer(language)
        data_bytes = self.convert_audio(file_data)
        input_size = data_bytes.getbuffer().nbytes
        read_size = 0
        last_percentage = 0
        text_chunks = []

        # feed input to recognizer in increments
        while True:
            data = data_bytes.read(4000)
            read_size += 4000
            if len(data) == 0:
                break
            
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())['text']
                text_chunks.append(res)
            
#            # progressively return percentage
            completion = 100 * read_size / input_size
            if completion - last_percentage > 5:
                last_percentage = completion
                print(f'Progress: {completion}%')
                data = {'percentage' : completion}
#               io.emit('progress', data)
            
        res = json.loads(rec.FinalResult())['text']
        text_chunks.append(res)
        return ' '.join(text_chunks)

    # convert audio input to .wav format bytes
    def convert_audio(self, input):
        process = subprocess.Popen(['ffmpeg', 
                                    '-loglevel', 'quiet',
                                    '-i', '-',
                                    '-ar', "16000", 
                                    '-ac', '1', 
                                    '-f', 's16le', 
                                    '-'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        p_out, err = process.communicate(input=input, timeout=None)
        return BytesIO(p_out)
    
    def new_model(self, language):
        '''Take 2 letter language code and return a new recognizer model'''
        if type(language) != str:
            raise TypeError(f'Model path expected a string, instead got type {type(language)}')
        if len(language) != 2:
            raise ValueError(f'Cannot create model from invalid language code: {language}')
        path = MODELS_PATH + "model-" + language
        model = Model(path)
        rec = KaldiRecognizer(model, 16000)
        return rec

    def get_recognizer(self, language):
        '''Take 2 letter language code and return its corresponding model'''
        if language not in self.languages:
            raise ValueError('Language not supported or activated')
        rec = None
        if language == Language.English:
            rec = self.rec_en
        elif language == Language.Farsi:
            rec = self.rec_fa
        elif language == Language.Arabic:
            rec = self.rec_ar
        return rec
