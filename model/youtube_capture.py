import cv2
import base64
from ultralytics import YOLO
import yt_dlp
import os
import shutil
from threading import Event

weights_filename = os.path.join('model', 'best.pt')
model = YOLO(weights_filename)

stop_event = Event()  # 중지 이벤트


def process_video(url, socketio):
    with yt_dlp.YoutubeDL({'format': 'best'}) as ydl:
        result = ydl.extract_info(url, download=False)
        video_url = result['url']
        cap = cv2.VideoCapture(video_url)
        while True:
            ret, frame = cap.read()
            if not ret or stop_event.is_set():
                break

            results = model.predict([frame], save=True)

            file_path = os.path.join('runs', 'detect', 'predict', results[0].path)
            with open(file_path, 'rb') as f:
                base64Predicted = base64.b64encode(f.read()).decode('utf-8')
                socketio.emit('frame', {'image': 'data:image/jpeg;base64,' + base64Predicted})

            # 삭제할 폴더 경로
            folder_path = os.path.dirname(file_path)
            # 폴더가 실제로 존재하는지 확인
            if os.path.exists(folder_path):
                # 폴더와 그 안의 모든 내용 삭제
                shutil.rmtree(folder_path)
        cap.release()

# 중지 기능 추가
def stop_process():
    stop_event.set()


# 재시작 기능 추가
def restart_process():
    stop_event.clear()