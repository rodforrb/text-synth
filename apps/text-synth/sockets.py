from flask import render_template, flash, redirect, url_for, request
from flask_socketio import SocketIO, emit
from extensions import io

@io.on('connect')
def test_connect():
    print('Connected!')

def emit_progress():
    pass

def emit_complete():
    pass