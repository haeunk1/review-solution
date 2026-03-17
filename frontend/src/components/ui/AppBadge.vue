<template>
  <span :class="badgeClass">
    <slot />
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(
  defineProps<{
    color?: 'success' | 'warning' | 'primary' | 'error'
    variant?: 'subtle' | 'solid'
    size?: 'xs' | 'sm' | 'lg'
  }>(),
  { color: 'primary', variant: 'subtle', size: 'sm' }
)

const badgeClass = computed(() => {
  const sizeClass = props.size === 'xs' ? 'px-1.5 py-0 text-xs' : props.size === 'lg' ? 'px-3 py-1 text-sm' : 'px-2 py-0.5 text-xs'
  const colorClass =
    props.color === 'success'
      ? 'bg-green-100 text-green-800'
      : props.color === 'warning'
        ? 'bg-amber-100 text-amber-800'
        : props.color === 'error'
          ? 'bg-red-100 text-red-800'
          : 'bg-blue-100 text-blue-800'
  return `inline-flex items-center rounded-full font-medium ${sizeClass} ${colorClass}`
})
</script>
