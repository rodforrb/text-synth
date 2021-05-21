import os
import subprocess
from io import BytesIO
import json
from vosk import Model, KaldiRecognizer

APP_ROOT = os.path.dirname(os.path.realpath(__file__))

class Parser:
    def __init__(self):
        # language models
        model_fa = Model(APP_ROOT + "/models/model-fa")
        self.rec = KaldiRecognizer(model_fa, 16000)

    # parse microphone audio from input stream
    def parse_audio(self, stream):
        stream.seek(0)
        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet',
                                    '-i', '-',
                                    '-ar', "16000", '-ac', '1', '-f', 's16le', '-'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)

        p_out, err = process.communicate(input=stream.getvalue(), timeout=None)

        data_bytes = BytesIO(p_out)

        while True:
            data = data_bytes.read(4000)
            if len(data) == 0:
                break
            if self.rec.AcceptWaveform(data):
                print(self.rec.Result())
            else:
                print(self.rec.PartialResult())
            # emit('Text received', res['text'])

        res = json.loads(self.rec.FinalResult())


        # emit('Text received', res['text']) # for live feedback

        stream.flush()

        return res['text']

    # parse audio file from upload
    def parse_file(self, file_in):
        file_data = file_in.read()

        process = subprocess.Popen(['ffmpeg', '-loglevel', 'quiet',
                                    '-i', '-',
                                    '-ar', "16000", '-ac', '1', '-f', 's16le', '-'],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE)

        p_out, err = process.communicate(input=file_data, timeout=None)

        data_bytes = BytesIO(p_out)

        while True:
            data = data_bytes.read(4000)
            if len(data) == 0:
                break
            self.rec.AcceptWaveform(data)

        res = json.loads(self.rec.FinalResult())

        return res['text']
