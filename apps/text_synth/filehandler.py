'''File handling functionality'''
import queue
import time
from threading import Thread
from werkzeug.utils import secure_filename
from flask_login import current_user
from extensions import io
from extensions import q
from .models import load_file, save_file, update_text, File
from .parser import Parser

from rq import Queue
from rq.job import Job
from .worker import conn

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
        # save file to disk and acquire id
        file_id = save_file(user_id, file, language)
        
        # for redisqueue
        self.queue_task(file_id)

        # for fileprocessor
        # self.processor.queue.put(file_id)
    
    def queue_task(self, file_id):
        job = q.enqueue_call(
            func=background_process_file, args=(file_id,), result_ttl=5000
        )
        print(f'Job queued: {job.get_id()}')

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


def background_process_file(file_id):
    '''function enqueued in redisqueue to process files in the background'''
    # retrieve file data from disk
    file, filecontents = load_file(file_id)
    # transcribe file
    transcription = parser.parse_file(file, filecontents)
    # save transcription to database
    update_text(file_id, transcription)

def job_done(job_id):
    job = Job.fetch(job_id, connection=conn)
    return job.is_finished