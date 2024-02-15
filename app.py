from flask import Flask
from flask_socketio import SocketIO
from model.youtube_capture import YoutubeCap
from flask_cors import CORS

yc=YoutubeCap()
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,cors_allowed_origins=['http://localhost:8080'])
@socketio.on('stop_stream')
def handle_stop_stream(data):
    yc.stop_process(data['streaming'])

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('start_stream')
def handle_start_stream(data):
    yc.process_video_(data['url'],socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, allow_unsafe_werkzeug=True)
