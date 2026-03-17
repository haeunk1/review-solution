<script setup lang="ts">
import { computed } from 'vue'
import * as Lucide from 'lucide-vue-next'
import type { StatsData } from '@/types/review'
import AppCard from '@/components/ui/AppCard.vue'

const props = defineProps<{ stat: StatsData }>()

const iconComponent = computed(() => {
  const name = props.stat.icon.replace(/^i-lucide-/, '')
  const pascal = name.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')
  return (Lucide as Record<string, unknown>)[pascal] ?? Lucide.Star
})
</script>

<template>
  <AppCard>
    <div class="flex items-center justify-between">
      <div>
        <p class="text-sm text-gray-500">{{ stat.label }}</p>
        <p class="mt-1 text-2xl font-bold text-gray-900">{{ stat.value }}</p>
        <div v-if="stat.change !== undefined" class="mt-1 flex items-center gap-1 text-xs">
          <component
            :is="stat.change >= 0 ? Lucide.TrendingUp : Lucide.TrendingDown"
            :class="stat.change >= 0 ? 'text-green-500' : 'text-red-500'"
            class="size-3"
          />
          <span :class="stat.change >= 0 ? 'text-green-500' : 'text-red-500'">
            {{ stat.change >= 0 ? '+' : '' }}{{ stat.change }}
          </span>
          <span class="text-gray-500">지난 달 대비</span>
        </div>
      </div>
      <div class="flex size-12 items-center justify-center rounded-full bg-blue-100">
        <component :is="iconComponent" class="size-6 text-blue-600" />
      </div>
    </div>
  </AppCard>
</template>
