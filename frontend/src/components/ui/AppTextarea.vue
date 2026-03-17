<template>
  <textarea
    :value="modelValue"
    :rows="rows"
    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
    @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
  />
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string
    rows?: number
  }>(),
  { rows: 4 }
)

defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
