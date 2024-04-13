<template>
    <div id="carouselExample" class="carousel slide">
        <div class="carousel-inner">
            <div v-for="video,index in videoList" :key="video.id.videoId" 
            class="carousel-item" 
            :class="[index==0?'active':'']"
            @click="selectVideo(video.id.videoId)">
                <div class="card text-bg-dark">
                    <img :src="video.snippet.thumbnails.high.url" class="card-img" alt="...">
                    <div class="card-img-overlay">
                        <h5 class="card-title">{{ video.snippet.title }}</h5>
                    </div>
                    <div class="p-3">
                        <p class="card-text"><small>{{timeSince(video.snippet.publishedAt)}}</small></p>
                        <p class="card-text">{{video.snippet.description}}</p>
                    </div>
                    
                </div>
            </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
        </button>
    </div>
</template>
<script setup>
import { defineProps, defineEmits} from 'vue';
import {timeSince} from '@/composable/calculatetime'
// eslint-disable-next-line no-unused-vars
const props = defineProps({
    videoList:Array
})

// eslint-disable-next-line no-unused-vars
const emits = defineEmits(['selectVideo'])
const selectVideo=(videoId)=>{
    emits('selectVideo',videoId)
}
</script>
<style scoped>
.card-img-overlay {
    padding: 7px 16px 16px 32px
}
.carousel {
    width: 40em;
    height: auto;
}    
</style>