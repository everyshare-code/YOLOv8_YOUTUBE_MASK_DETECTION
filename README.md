# 프로젝트 개요
![마스크 감지(메인 화면)](https://github.com/everyshare-code/YOLOv8_YOUTUBE_MASK_DETECTION/blob/main/main.png)

이 프로젝트는 YOLOv8 모델을 사용하여 마스크 착용 여부를 감지하는 시스템을 구축하는 것을 목표로 합니다. Python을 사용하여 데이터 전처리, 모델 학습, 예측 및 결과 시각화를 수행합니다. 또한, 비디오 스트리밍 기능을 포함하여 실시간으로 마스크 착용 여부를 감지할 수 있습니다.

## 파일 구조

- `youtube_capture.py`: 유튜브 영상을 다운 받고 마스크 감지를 통해 세그먼트를 생성하는 서비스 로직.
- `app.py`: Flask를 통해서 클라이언트의 요청을 받고 응답을 해주는 파일.
- `main.py`: Flask 앱을 ASGI 앱으로 변환하고 실행하는 파일.
- `model_train/YOLOv8_MASK_DETECT.ipynb`: 데이터 전처리, 모델 학습 및 예측을 수행하는 Jupyter 노트북.

## 주요 기능

### 데이터 전처리

1. **데이터 분할**:
    ```python
    X_train, X_test = train_test_split(df_data.filename.unique(), test_size=0.1, random_state=42)
    X_train, valid = train_test_split(X_train, test_size=0.2, random_state=42)
    ```

2. **디렉토리 생성**:
    ```python
    if not os.path.exists(train_images_dir):
        os.makedirs(train_images_dir)
    if not os.path.exists(train_labels_dir):
        os.makedirs(train_labels_dir)
    if not os.path.exists(test_images_dir):
        os.makedirs(test_images_dir)
    if not os.path.exists(test_labels_dir):
        os.makedirs(test_labels_dir)
    if not os.path.exists(valid_images_dir):
        os.makedirs(valid_images_dir)
    if not os.path.exists(valid_labels_dir):
        os.makedirs(valid_labels_dir)
    ```

3. **이미지 복사**:
    ```python
    def copy_images(images, folder_name):
        for image in images:
            image_path = image_directory + "/" + image
            new_image_path = os.path.join(folder_name, image)
            shutil.copy(image_path, new_image_path)
    ```

4. **YOLO 레이블 파일 생성**:
    ```python
    def create_yolo_label_file(images, folder_name):
        for image in images:
            filename = image.split('.')[0]
            df = df_data[df_data['filename'] == image]
            with open(folder_name + "/" + filename + '.txt', 'w') as f:
                for i in range(0, len(df)):
                    bbox = pascal_to_yolo_bbox(df.iloc[i]['bboxes'], df.iloc[i]['width'], df.iloc[i]['height'])
                    bbox_text = " ".join(map(str, bbox))
                    txt = str(df.iloc[i]['class_id']) + " " + bbox_text
                    f.write(txt)
    ```

### 모델 학습

1. **YOLO 모델 다운로드**:
    ```python
    model = YOLO('yolov8s.pt')
    ```

2. **학습 설정 파일 생성**:
    ```python
    config_yaml = f'''
        train: train
        val: valid
        test: test
        nc: {df_data.label.unique().size}
        names:
            0: with_mask
            1: mask_weared_incorrect
            2: without_mask
    '''
    with open('mask_config.yaml', 'w', encoding='utf8') as f:
        f.write(config_yaml)
    ```

### 예측 및 시각화

1. **예측 수행**:
    ```python
    results = mask_model.predict(source=images, save=True, conf=0.5)
    ```

2. **결과 시각화**:
    ```python
    for index in range(len(images)):
        pred_image = Image.open(os.path.join(results[index].save_dir, f'image{str(index)}.jpg'))
        plt.figure(figsize=(10, 10))
        plt.imshow(pred_image)
        plt.title("Object Detection")
        plt.axis(False)
    plt.show()
    ```

### 비디오 스트리밍
![마스크 감지(마스크 착용)](https://github.com/everyshare-code/YOLOv8_YOUTUBE_MASK_DETECTION/blob/main/temp2.png)

1. **비디오 세그먼트 준비 상태 확인**:
    ```python
    def check_segments_ready(video_id):
        directory = os.path.join(app.root_path, 'data/videos')
        segment_files = [f for f in os.listdir(directory) if f.startswith(video_id) and f.endswith('.ts')]
        return len(segment_files) >= 3
    ```

2. **비디오 준비 및 스트리밍 파일 경로 전달**:
    ```python
    def prepare_video():
        video_id = request.json.get('videoId')
        if video_id not in video_processing or not video_processing[video_id]:
            video_processing[video_id] = True
            playlist_path = yc.stream_video(video_id)
        else:
            playlist_path = os.path.join('videos', f'{video_id}.m3u8')

        if check_segments_ready(video_id):
            return jsonify({"video_path": playlist_path})
        else:
            return jsonify({"error": "비디오가 아직 준비되지 않았습니다."}), 202
    ```

3. **캡처 및 세그먼트 생성**:
    ```python
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
    ```

## 실행 방법

1. **환경 설정**:
    - 필요한 라이브러리를 설치합니다.
    ```bash
    pip install -r requirements.txt
    ```

2. **앱 실행**:
    - `main.py` 파일을 실행하여 서버를 시작합니다.
    ```bash
    python main.py
    ```

3. **모델 학습 및 예측**:
    - `model_train/YOLOv8_MASK_DETECT.ipynb` 노트북을 열어 각 셀을 실행합니다.

## 참고 자료

- [YOLOv8 GitHub Repository](https://github.com/ultralytics/ultralytics.git)
- [Face Mask Detection Dataset](https://www.kaggle.com/datasets/andrewmvd/face-mask-detection)
