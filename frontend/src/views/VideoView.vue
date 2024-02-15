<template>
    <div class="container">
    <h1>Mask Detection(YOLOv8)</h1>
      <input type="text" class="form-control" v-model="url" 
      placeholder="YouTube URL을 입력하세요">
      <div class="video-layout-container">
      <VideoLayout :url="url" @stop="stop"/>
    </div>
  </div>
</template>
<script setup>
import { ref } from 'vue'
import VideoLayout from '@/components/VideoLayout.vue'
const url = ref('')
function stop(){
    url.value=''
}
</script>
<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: fit-content;
}

.video-layout-container {
  margin-top: 20px;
}    
</style>