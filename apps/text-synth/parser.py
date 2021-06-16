import os
import subprocess
from io import BytesIO
#from extensions import io
import json
from vosk import Model, KaldiRecognizer, SetLogLevel


class Parser:
    def __init__(self, allowed_languages):
        SetLogLevel(-1)
        APP_ROOT = os.path.dirname(os.path.realpath(__file__))
        self.languages = []
        # language models
        # English
        if 'en' in allowed_languages:
            model_en = Model(APP_ROOT + "/models/model-en")
            self.rec_en = KaldiRecognizer(model_en, 16000)
            self.languages.append('en')
        # Persian
        if 'fa' in allowed_languages:
            model_fa = Model(APP_ROOT + "/models/model-fa")
            self.rec_fa = KaldiRecognizer(model_fa, 16000)
            self.languages.append('fa')

    # parse audio file from upload
    def parse_file(self, file_in, language):
        rec = self.get_recognizer(language)
        file_data = file_in.read()
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
#            completion = 100 * read_size / input_size
#            if completion - last_percentage > 5:
#                last_percentage = completion
#                print(completion)
#                data = {'percentage' : completion}
#                io.emit('progress', data)
            
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
    
    def get_recognizer(self, language):
        if language not in self.languages:
            raise ValueError('Language not supported or activated')
        rec = None
        if language == 'en':
            rec = self.rec_en
        elif language == 'fa':
            rec = self.rec_fa
        return rec
