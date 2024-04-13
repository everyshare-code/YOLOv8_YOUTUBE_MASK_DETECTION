<template>
  <div class="video-layout-container">
      <!-- video 태그에 ref 속성을 추가하여 비디오 요소의 참조를 얻습니다 -->
      <video ref="videoElement" controls></video>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineProps } from 'vue';
import Hls from 'hls.js';

const videoElement = ref(null);
const props = defineProps({
  videoPath: String,
});
const hls = new Hls();

onMounted(() => {
  if (Hls.isSupported()) {
    hls.loadSource(props.videoPath);
    hls.attachMedia(videoElement.value);
    hls.on(Hls.Events.MANIFEST_PARSED, () => {
      videoElement.value.play().catch(e => {
        console.error('Auto-play was prevented', e);
      });
    });
    hls.on(Hls.Events.ERROR, (event, data) => {
      if (data.fatal) {
        switch(data.type) {
          case Hls.ErrorTypes.NETWORK_ERROR:
            console.error('A network error occurred', data);
            // try to recover network error
            break;
          case Hls.ErrorTypes.MEDIA_ERROR:
            console.error('A media error occurred', data);
            // try to recover media error
            break;
          default:
            // cannot recover
            hls.destroy();
            break;
        }
      }
    });
  } else if (videoElement.value.canPlayType('application/vnd.apple.mpegurl')) {
    videoElement.value.src = props.videoPath;
    videoElement.value.addEventListener('loadedmetadata', () => {
      videoElement.value.play().catch(e => {
        console.error('Auto-play was prevented', e);
      });
    });
  }
});

onUnmounted(() => {
  if (Hls.isSupported()) {
    hls.destroy();
  }
});
</script>


<style scoped>
.video-layout-container {
max-width: 500px;
margin: auto; /* 가운데 정렬 */
aspect-ratio: 16 / 9;
}
.video-layout-container video {
width: 100%; /* 비디오 요소의 너비를 부모 요소의 너비에 맞춤 */
height: auto; /* 비디오 비율에 따라 높이 자동 조절 */
}
@media (max-width: 720px) {
.video-layout-container {
  max-width: 360px;
}
}
</style>
