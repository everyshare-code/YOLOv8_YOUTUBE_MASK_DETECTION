<template>
    <div class="video-layout-container">
        <LoadingModal :visible="isLoading" />
        <div class="video-container d-flex justify-content-center align-items-center" @click.prevent="play">
        <img class="video-frame" :src="currentFrame" />
        <button v-if="!streaming" @click.prevent.stop="play" class="btn btn-primary btn-play" ref="buttonRef">
        <i class="bi bi-play-fill"></i>
        </button>
      </div>
    </div>
</template>
  
  
<script setup>
import { ref, onBeforeUnmount, defineProps, defineEmits, watch } from 'vue';
import io from 'socket.io-client';
import LoadingModal from './LoadingModal.vue'
import { gsap } from 'gsap'  
const streaming=ref(false);
const isLoading=ref(false);
const buttonRef = ref(null);

function play(){
    streaming.value=!streaming.value
}

const emits=defineEmits(['stop'])

const props = defineProps({
    url: String,
});
  
const currentFrame = ref('');
const socket = io('http://localhost:5001');
  
let lastFrame = ''; // 마지막 프레임 상태를 저장하기 위한 변수
socket.on('connect', () => {
    console.log('socket연결')
});
  
socket.on('frame', data => {
    if(isLoading.value) isLoading.value=false;
    currentFrame.value = 'data:image/jpeg;base64,' + data.image;
    lastFrame = data.image; // 마지막 프레임 상태 업데이트
});
  
onBeforeUnmount(() => {
    socket.disconnect();
});

watch(streaming, (newVal) => {
  if (newVal) {
    isLoading.value = true;
    socket.emit('start_stream', { url: props.url });
  } else {
    socket.emit('stop_stream');
    emits('stop')
    currentFrame.value = lastFrame; // 스트리밍 중지 시 마지막 프레임 유지
  }
});


/*
watchEffect(() => {
  if (streaming.value) {
    isLoading.value=true;
    socket.emit('start_stream', { url: props.url });
  } else {
    socket.disconnect();
  }
});
*/


// URL이 변경될 때마다 버튼에 깜빡임 효과를 적용
watch(() => props.url, (newVal, oldVal) => {
  if (newVal !== oldVal) {
    console.log('props:',props.url)
    blinkButton()
  }
}, { immediate: true })

// 버튼 깜빡임 효과 함수
function blinkButton() {
    if(buttonRef.value){
        gsap.to(buttonRef.value, {
        opacity: 0,
        duration: 0.5,
        repeat: 5,
        yoyo: true,
        ease: "power1.inOut"
        })
    }
}
</script>
  
<style scoped>
.video-container {
  position: relative; /* 컨테이너를 상대 위치로 설정 */
  background-color: black;
  min-height: 360px; /* 최소 높이 설정 */
  min-width: 360px;
  max-width: 100%; /* 최대 너비를 100%로 설정 */
  height: auto; /* 비디오 비율에 따라 자동으로 높이 조절 */
  aspect-ratio: 16 / 9; /* 비디오 비율 설정 */
  display: flex; /* Flexbox를 사용하여 내용을 중앙에 정렬 */
  justify-content: center; /* 가로 방향 중앙 정렬 */
  align-items: center; /* 세로 방향 중앙 정렬 */
}

.btn-play {
  position: absolute; /* 버튼을 절대 위치로 설정 */
  top: 50%; /* 상단으로부터 50% 위치 */
  left: 50%; /* 왼쪽으로부터 50% 위치 */
  transform: translate(-50%, -50%); /* 정확한 중앙 정렬을 위한 조정 */
  opacity: 0.75; /* 버튼의 불투명도 설정 */
}


.video-layout-container {
  max-width: 500px; /* 최대 너비 설정 */
  height: auto; /* 비디오 비율에 따라 자동으로 높이 조절 */
  aspect-ratio: 16 / 9; /* 비디오 비율 설정 */
}

@media (max-width: 720px) {
  .video-layout-container {
    max-width: 360px; 
  }
}

.video-frame {
  max-width: 100%; /* 최대 너비를 100%로 설정하여 이미지가 컨테이너를 넘지 않도록 함 */
  max-height: 100%; /* 최대 높이를 100%로 설정하여 이미지가 컨테이너를 넘지 않도록 함 */
  object-fit: contain; /* 이미지의 비율을 유지하면서, 가능한 경우 컨테이너 내에 꽉 차게 함 */
}


  </style>
  