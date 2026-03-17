<template>
  <router-view v-slot="{ Component }">
    <component :is="Component" />
  </router-view>
  <ToastContainer />
</template>

<script setup lang="ts">
import ToastContainer from '@/components/ToastContainer.vue'
</script>
