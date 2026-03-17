<template>
  <select
    :value="modelValue"
    class="w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-primary focus:outline-none focus:ring-1 focus:ring-primary"
    @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
  >
    <option
      v-for="item in items"
      :key="String(item[valueKey])"
      :value="item[valueKey]"
    >
      {{ item.label }}
    </option>
  </select>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    modelValue: string
    items: { label: string; value: string }[]
    valueKey?: string
  }>(),
  { valueKey: 'value' }
)
defineEmits<{ 'update:modelValue': [value: string] }>()
</script>
