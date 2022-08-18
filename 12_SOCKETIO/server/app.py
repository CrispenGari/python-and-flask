
from socket import socket
from flask import Flask
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfghjkl'
io = SocketIO(app,  cors_allowed_origins='*')

@io.on('message', namespace='/chat')
def new_message(message):
    emit('new-message', message, broadcast=True)
 
    
if __name__ == "__main__":
    io.run(app, '127.0.0.1', port=3001, debug=True)