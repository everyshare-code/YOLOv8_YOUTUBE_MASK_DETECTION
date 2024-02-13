from flask import Flask
from flask_socketio import SocketIO
from model.youtube_capture import process_video,stop_process,restart_process
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
socketio = SocketIO(app,cors_allowed_origins=['http://localhost:8080'])

# 클라이언트로부터의 중지 및 재시작 요청 처리
@socketio.on('stop_stream')
def handle_stop_stream():
    stop_process()

@socketio.on('restart_stream')
def handle_restart_stream():
    restart_process()

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('start_stream')
def handle_start_stream(data):
    process_video(data['url'],socketio)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, allow_unsafe_werkzeug=True)
