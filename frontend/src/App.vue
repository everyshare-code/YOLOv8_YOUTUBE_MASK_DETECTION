<template>
  <div class="container">
    <div class="row g-3">
      <div class="col-auto">
        <input type="text" class="form-control" v-model="url" placeholder="YouTube URL을 입력하세요">
      </div>
      <div class="col-auto">
        <button class="btn btn-primary mb-3" @click="toggleStreaming">{{ streaming ? '스트리밍 중지' : '스트리밍 시작' }}</button>
        
      </div>
    </div>
    <div class="video-layout-container">
      <VideoLayout :url="url" :streaming="streaming"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import VideoLayout from '@/components/VideoLayout.vue'

const url = ref('')
const streaming = ref(false)

const toggleStreaming = () => {
  console.log(streaming.value)
  streaming.value = !streaming.value
}

</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.video-layout-container {
  margin-top: 20px;
}
</style>
