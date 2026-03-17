<template>
  <div class="flex flex-col items-center justify-center rounded-lg border border-dashed border-gray-300 py-12 text-center">
    <component :is="iconComponent" class="mb-3 size-12 text-gray-400" />
    <p class="font-medium text-gray-900">{{ title }}</p>
    <p v-if="description" class="mt-1 text-sm text-gray-500">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as Lucide from 'lucide-vue-next'

const props = withDefaults(
  defineProps<{
    icon?: string
    title: string
    description?: string
  }>(),
  { icon: 'inbox' }
)

const iconComponent = computed(() =>
  (Lucide as Record<string, unknown>)[toPascal(props.icon)] ?? Lucide.Inbox
)
function toPascal(name: string) {
  const base = name.replace(/^i-lucide-/, '')
  return base.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')
}
</script>
