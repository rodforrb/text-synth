'''File handling functionality'''
import queue
import time
from threading import Thread
from werkzeug.utils import secure_filename
from flask_login import current_user
from extensions import io
from .models import load_file, save_file, update_text, File
from .parser import Parser

parser = Parser(['en','fa'])

class FileHandler:
    '''Handler to save and enqueue files'''
    appcontext = None
    def __init__(self):
        self.processor = FileProcessor()

    def set_app_context(self, context):
        '''The app context needs to be supplied at runtime before use, because this module exists outside of the context'''
        self.appcontext = context
        self.processor.appcontext = context

    def put(self, file, language):
        file.filename = secure_filename(file.filename)
        user_id = current_user.id
        file_id = save_file(user_id, file, language)
        self.processor.queue.put(file_id)
    

class FileProcessor(object):
    '''Processor to retrieve and process files asynchronously'''
    queue = queue.Queue()
    ready = True
    appcontext = None

    def __init__(self):
        thread = Thread(target=self.run)
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            time.sleep(1)
            if self.ready and not self.queue.empty():
                if self.appcontext is None:
                    raise RuntimeError('App context is missing from fileprocessor')
                with self.appcontext:
                    self.ready = False
                    file_id = self.queue.get()
                    file, filecontents = load_file(file_id)
                    transcription = parser.parse_file(file, filecontents)
                    update_text(file_id, transcription)
                    self.ready = True
