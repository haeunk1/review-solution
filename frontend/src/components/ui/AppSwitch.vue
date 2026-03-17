<template>
  <button
    type="button"
    role="switch"
    :aria-checked="modelValue"
    class="inline-flex h-6 w-11 shrink-0 cursor-pointer items-center rounded-full border-0 transition-colors focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
    :class="modelValue ? 'bg-primary' : 'bg-gray-200'"
    @click="$emit('update:modelValue', !modelValue)"
  >
    <span
      class="pointer-events-none inline-block size-5 rounded-full bg-white shadow ring-0 transition"
      :class="modelValue ? 'translate-x-5' : 'translate-x-0.5'"
    />
  </button>
</template>

<script setup lang="ts">
defineProps<{ modelValue: boolean }>()
defineEmits<{ 'update:modelValue': [value: boolean] }>()
</script>
