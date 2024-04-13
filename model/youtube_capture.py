import cv2
from ultralytics import YOLO
from pytube import YouTube
from dotenv import load_dotenv
import subprocess
from threading import Thread
from urllib.parse import quote
load_dotenv()
import os
class YoutubeCap():
    def __init__(self):
        weights_filename = os.path.join('model_train', 'runs', 'detect', 'train', 'weights', 'best.pt')
        self.model = YOLO(weights_filename)
        root_path = os.getenv('ROOT_PATH')
        self.videos_path = os.path.join(root_path, 'data', 'videos')

    def download_video(self, videoId):
        url=f'https://www.youtube.com/watch?v={videoId}'
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        # title = stream.title
        # safe_title = re.sub(r'[^a-zA-Z0-9가-힣]', '', title)  # a-z, A-Z, 0-9, 그리고 한글을 제외한 모든 문자를 제거
        filename = f'{videoId}.mp4'
        output_path = self.videos_path  # 저장될 경로 설정
        stream.download(output_path=output_path, filename=filename)  # 파일 저장
        full_path = os.path.join(output_path, filename)  # 전체 경로 반환
        return full_path

    def process_and_stream(self, video_path, playlist_path, videoId):
        cap = cv2.VideoCapture(video_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        segment_duration = 3  # seconds per segment
        frames_per_segment = segment_duration * fps

        with open(playlist_path, 'w') as playlist:
            playlist.write('#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:3\n')

        segment_count = 0

        while True:
            segment_filename = f"{videoId}_{segment_count}.ts"
            segment_path = os.path.join(self.videos_path, segment_filename)
            command = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-pix_fmt', 'bgr24',
                       '-s', f"{int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))}x{int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))}",
                       '-r', str(fps), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-preset', 'fast', '-f',
                       'mpegts', segment_path]
            proc = subprocess.Popen(command, stdin=subprocess.PIPE)

            frames_collected = 0
            while frames_collected < frames_per_segment:
                ret, frame = cap.read()
                if not ret:
                    break
                frame = self.model.predict([frame], save=False)[0].plot()
                proc.stdin.write(frame.tobytes())
                frames_collected += 1

            proc.stdin.close()
            proc.wait()

            if not ret:  # If no more frames, exit loop
                break

            with open(playlist_path, 'a') as playlist:
                playlist.write(f'#EXTINF:3,\n{segment_filename}\n')
            segment_count += 1

        with open(playlist_path, 'a') as playlist:
            playlist.write('#EXT-X-ENDLIST\n')
        cap.release()

    def stream_video(self, videoId):
        video_path = self.download_video(videoId)
        playlist_path = os.path.splitext(video_path)[0] + ".m3u8"
        Thread(target=self.process_and_stream, args=(video_path, playlist_path, videoId)).start()
        return quote(os.path.join('videos', os.path.basename(playlist_path)))



