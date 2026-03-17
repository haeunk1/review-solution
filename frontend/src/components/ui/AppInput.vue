<template>
  <div class="relative">
    <component
      v-if="icon"
      :is="iconComponent"
      class="absolute left-3 top-1/2 size-4 -translate-y-1/2 text-gray-400"
    />
    <input
      :value="modelValue"
      :type="type"
      :placeholder="placeholder"
      class="w-full rounded-md border border-gray-300 bg-white py-2 pr-3 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
      :class="icon ? 'pl-9' : 'pl-3'"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as Lucide from 'lucide-vue-next'

const props = withDefaults(
  defineProps<{
    modelValue: string
    icon?: string
    placeholder?: string
    type?: string
  }>(),
  { type: 'text' }
)

const iconComponent = computed(() =>
  props.icon ? (Lucide as Record<string, unknown>)[toPascal(props.icon)] : null
)
function toPascal(name: string) {
  const base = name.replace(/^i-lucide-/, '')
  return base.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')
}

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
