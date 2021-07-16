from flask import request
from flask_login import current_user, login_required
from flask_socketio import SocketIO, emit, join_room
from extensions import io
from .models import get_active_files
import json

@io.on('connect')
def test_connect():
    if current_user.is_authenticated:
        print(f'Connected\n\tuser: {current_user.name}\n\tid: {current_user.id}')
        join_room(current_user.id)

def emit_progress(user_id, file_id, percent):
    data = {'file_id' : file_id,
            'percent' : percent
    }
    io.emit('progress', data, room=user_id)

    print(f'emit progress, uid:{user_id}, room:{user_id}')

def emit_complete(user_id, file_id):
    data = {'file_id' : file_id}
    io.emit('complete', data, room=user_id)

@io.on('update')
@login_required
def request_update():
    '''Process the request to update file completions'''
    files = get_active_files(current_user.id)
    updates = []
    for f in files:
        completion = str(f.completion)
        text = None
        if completion == '100':
            completion = 'Complete'
            text = f.text
        elif completion == '0':
            completion = 'Parsing'
        else:
            completion += '%'
        updates.append({'file_id':f.file_id, 'percent':completion, 'text':text})
    
    output = {'size':len(files), 'updates':updates}
    print(json.dumps(output))
    io.emit('progress', data=(json.dumps(output)), room=current_user.id)