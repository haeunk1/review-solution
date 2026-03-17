<template>
  <div
    class="inline-flex shrink-0 items-center justify-center overflow-hidden rounded-full bg-gray-200 text-gray-600"
    :class="sizeClass"
  >
    <img v-if="src" :src="src" :alt="alt" class="h-full w-full object-cover" />
    <span v-else class="text-sm font-medium">{{ alt?.charAt(0) ?? '?' }}</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    src?: string
    alt?: string
    size?: 'sm' | 'md'
  }>(),
  { size: 'md' }
)

const sizeClass = computed(() =>
  props.size === 'sm' ? 'size-8' : 'size-10'
)
</script>
