<template>
  <div class="h-2 w-full overflow-hidden rounded-full bg-gray-200">
    <div
      class="h-full rounded-full transition-all"
      :class="colorClass"
      :style="{ width: `${Math.min(100, Math.max(0, value))}%` }"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    value: number
    color?: 'primary' | 'success'
  }>(),
  { color: 'primary' }
)

const colorClass = computed(() =>
  props.color === 'success' ? 'bg-green-500' : 'bg-primary'
)
</script>
