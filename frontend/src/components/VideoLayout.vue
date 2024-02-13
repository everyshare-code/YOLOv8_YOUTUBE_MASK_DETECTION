<template>
    <div class="video-container">
      <img v-if="streaming" class="video-frame" :src="currentFrame"/>
    </div>
  </template>
  
  <script setup>
  import { ref, onBeforeUnmount, defineProps, watchEffect } from 'vue';
  import io from 'socket.io-client';
  
  const props = defineProps({
    url: String,
    streaming: Boolean
  });
  
  const currentFrame = ref('');
  const socket = io('http://localhost:5001');
  
  let lastFrame = ''; // 마지막 프레임 상태를 저장하기 위한 변수
  socket.on('connect', () => {
    
  });
  
  socket.on('frame', data => {
    currentFrame.value = data.image;
    lastFrame = data.image; // 마지막 프레임 상태 업데이트
  });
  
  onBeforeUnmount(() => {
    socket.disconnect();
  });
  
  watchEffect(() => {
  if (props.streaming) {
    socket.emit('start_stream', { url: props.url });
  } else {
    socket.emit('stop_stream');
    currentFrame.value = lastFrame; // 스트리밍 중지 시 마지막 프레임 유지
  }
});

  </script>
  
  <style scoped>
  .video-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100%; /* 부모 컨테이너의 높이를 100%로 설정하여 화면 전체를 차지하도록 함 */
  }
  
  .video-frame {
    max-width: 100%; /* 최대 너비를 100%로 설정하여 이미지가 컨테이너 내에 적절하게 맞게 함 */
    max-height: 100%; /* 최대 높이를 100%로 설정하여 이미지가 컨테이너 내에 적절하게 맞게 함 */
    height: auto; /* 높이를 자동으로 조정하여 가로세로 비율 유지 */
    border-radius: 8px; /* 이미지를 라운드 처리 */
    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* 그림자 효과 추가 */
  }
  </style>
  