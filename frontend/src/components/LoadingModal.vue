<template>
    <div v-if="visible" class="modal-backdrop">
        <div class="modal-content">
            <div class="d-flex justify-content-center"> <!-- 중앙 정렬을 위한 추가적인 div -->
            <div class="spinner-border text-light" role="status">
            <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    </div>
    </div>
</template>
  
<script setup>
  import { defineProps } from 'vue'
  
  // eslint-disable-next-line no-unused-vars
  const props = defineProps({
    visible: Boolean
  })
  </script>
  
  <style scoped>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1050;
  }
  
  .modal-content {
    text-align: center;
  }
  </style>
  