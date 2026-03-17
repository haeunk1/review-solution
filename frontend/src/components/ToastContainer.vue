<template>
  <div class="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
    <div
      v-for="t in toasts"
      :key="t.id"
      class="rounded-lg border bg-white px-4 py-3 shadow-lg"
      :class="t.color === 'success' ? 'border-green-200 bg-green-50' : ''"
    >
      {{ t.title }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { getToasts } from '@/composables/useToast'

const toasts = getToasts()
</script>
