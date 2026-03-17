<template>
  <div class="shrink-0 bg-gray-200" :class="vertical ? 'w-px self-stretch' : 'h-px w-full'" />
</template>

<script setup lang="ts">
defineProps<{ vertical?: boolean }>()
</script>
