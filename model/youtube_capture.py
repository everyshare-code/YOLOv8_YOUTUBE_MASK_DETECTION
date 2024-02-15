import cv2
import base64
from ultralytics import YOLO
import yt_dlp
import os
from threading import Event
from io import BytesIO
from pytube import YouTube

class YoutubeCap():
    def __init__(self):
        weights_filename = os.path.join('model', 'best.pt')
        self.model = YOLO(weights_filename)
        self.stop_event = Event()
        self.streaming=True

    def process_video_(self, url, socketio):
        yt = YouTube(url)
        video_stream = (yt.streams.filter(progressive=True, file_extension='mp4')
                        .order_by('resolution').desc().first())
        if video_stream is None:
            print("유튜브 스트리밍 연결 실패")
            return
        video_url = video_stream.url
        cap = cv2.VideoCapture(video_url)
        while cap.isOpened():
            ret, frame = cap.read()
            print(ret)
            if ret:
                results = self.model.predict([frame], save=False)
                narr = results[0].plot()
                # 메모리에 이미지를 임시 저장하기 위한 BytesIO 객체 생성
                _, buffer = cv2.imencode('.jpg', narr)
                io_buf = BytesIO(buffer)
                # Base64 문자열로 인코딩
                base64_string = base64.b64encode(io_buf.getvalue()).decode('utf-8')
                socketio.emit('frame', {'image': base64_string})
            else:
                break
        cap.release()
    def process_video(self,url,socketio):
        with yt_dlp.YoutubeDL({'format': 'best'}) as ydl:
            self.result = ydl.extract_info(url, download=False)
            video_url = self.result['url']
            cap = cv2.VideoCapture(video_url)
            while cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    results=self.model.predict([frame],save=False)
                    narr=results[0].plot()
                    # 메모리에 이미지를 임시 저장하기 위한 BytesIO 객체 생성
                    _, buffer = cv2.imencode('.jpg', narr)
                    io_buf = BytesIO(buffer)
                    # Base64 문자열로 인코딩
                    base64_string = base64.b64encode(io_buf.getvalue()).decode('utf-8')
                    socketio.emit('frame', {'image': base64_string})
                else:
                    break
            cap.release()
    def stop_process(self,streaming):
        self.stop_event.set()
        self.streaming=streaming


    def restart_process(self):
        self.stop_event.clear()


