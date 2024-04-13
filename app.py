from flask import Flask, request, send_from_directory, jsonify
from model.youtube_capture import YoutubeCap
from flask_cors import CORS
import os
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)
yc = YoutubeCap()

# 비디오 처리 상태를 추적하는 딕셔너리
video_processing = {}

def check_segments_ready(video_id):
    # 해당 비디오 ID에 대한 세그먼트 파일 수를 확인
    directory = os.path.join(app.root_path, 'data/videos')
    segment_files = [f for f in os.listdir(directory) if f.startswith(video_id) and f.endswith('.ts')]
    return len(segment_files) >= 3

@app.post('/prepare_video')
def prepare_video():
    video_id = request.json.get('videoId')
    if video_id not in video_processing or not video_processing[video_id]:
        # 비디오 처리를 시작
        video_processing[video_id] = True
        playlist_path = yc.stream_video(video_id)
    else:
        # 이미 처리 중인 경우 경로만 반환
        playlist_path = os.path.join('videos', f'{video_id}.m3u8')

    if check_segments_ready(video_id):
        return jsonify({"video_path": playlist_path})
    else:
        # 처리 중이지만 세그먼트가 아직 준비되지 않은 경우
        return jsonify({"error": "비디오가 아직 준비되지 않았습니다."}), 202

@app.route('/videos/<path:filename>')
def serve_video(filename):
    safe_filename = unquote(filename)
    directory = os.path.join(app.root_path, 'data/videos')
    if safe_filename.endswith('.m3u8'):
        mimetype = 'application/x-mpegURL'
    elif safe_filename.endswith('.ts'):
        mimetype = 'video/MP2T'
    else:
        mimetype = None
    return send_from_directory(directory, safe_filename, mimetype=mimetype)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
