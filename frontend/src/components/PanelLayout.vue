<template>
  <div class="flex flex-1 flex-col">
    <header v-if="title || $slots.right" class="flex h-14 shrink-0 items-center justify-between border-b border-gray-200 bg-white px-6">
      <h1 class="text-lg font-semibold text-gray-900">{{ title }}</h1>
      <div v-if="$slots.right" class="flex items-center gap-2">
        <slot name="right" />
      </div>
    </header>
    <div v-if="$slots.toolbar" class="border-b border-gray-200 bg-white px-6 py-2">
      <slot name="toolbar" />
    </div>
    <div class="flex-1 overflow-auto">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{ title?: string }>()
</script>
