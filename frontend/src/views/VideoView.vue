<template>
    <div class="container">
      <h1>Mask Detection(YOLOv8)</h1>
      <div class="input-group">
          <input type="text" class="form-control" v-model="url" 
          placeholder="YouTube URL을 입력하세요">
          <a class="btn btn-primary" role="button" @click.prevent="searchVideos">검색</a>
      </div>
      <LoadingModal v-if="modal"/>
      <div v-if="selectVideo" class="video-layout-container">
        <VideoLayout :videoPath="videoPath" @stop="stop"/>
      </div>
      <VideoList v-if="videoList" :videoList="videoList" @selectVideo="setVideoId"/>
    </div>
</template>
<script setup>
import { ref } from 'vue'
import axios from 'axios'
import VideoLayout from '@/components/VideoLayout.vue'
import VideoList from '@/components/VideoList.vue'
import LoadingModal from '@/components/LoadingModal.vue'
const url = ref('')
const selectVideo = ref(false)
const videoPath = ref('')
const videoList = ref([])

function stop(){
    url.value=''
}

const searchVideos = async()=>{
  selectVideo.value=false
  const searchQuery=url.value
  const YOUTUBE_API_KEY=process.env.VUE_APP_YOUTUBE_API_KEY
  const baseURL='https://www.googleapis.com/youtube/v3/search'
  const params=`?part=snippet&maxResults=25&q=${encodeURIComponent(searchQuery)}&key=${YOUTUBE_API_KEY}`
  const response= await axios.get(baseURL+params)
  const data = response.data
  videoList.value=data.items
  console.log(videoList.value)
}
const RETRY_INTERVAL=2000
const videoId=ref('')
const setVideoId= (videoId_)=>{
  videoId.value=videoId_
  sendToURL()
}

const modal=ref(false)
const sendToURL= async()=>{
  modal.value=true
  const response= await axios.post('http://localhost:5001/prepare_video',{videoId:videoId.value})
  if (response.status==200){
    const data=response.data
    if(data) {
      modal.value=false
      selectVideo.value=true
      videoList.value=[]
      videoPath.value=`http://localhost:5001/${data['video_path']}`
    }
  }else if(response.status==202){
    setTimeout(sendToURL,RETRY_INTERVAL)
  }
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