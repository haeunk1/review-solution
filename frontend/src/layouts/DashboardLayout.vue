<template>
  <div class="flex min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="flex w-56 shrink-0 flex-col border-r border-gray-200 bg-white">
      <div class="flex items-center gap-2 px-4 py-4">
        <div class="flex size-10 items-center justify-center rounded-lg bg-primary text-primary-foreground">
          <HeartPulse class="size-5" />
        </div>
        <span class="text-lg font-bold text-gray-900">CareReply AI</span>
      </div>
      <nav class="flex-1 space-y-0.5 px-2 py-2">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors"
          :class="$route.path === item.to ? 'bg-gray-100 text-gray-900' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
        >
          <component :is="item.icon" class="size-5 shrink-0" />
          {{ item.label }}
        </router-link>
      </nav>
      <div class="border-t border-gray-200 p-2">
        <button
          class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left transition-colors hover:bg-gray-50"
          @click="logout"
        >
          <AppAvatar :src="`https://api.dicebear.com/7.x/initials/svg?seed=${hospitalName}`" :alt="hospitalName" size="sm" />
          <div class="min-w-0 flex-1">
            <p class="truncate text-sm font-medium text-gray-900">{{ hospitalName }}</p>
            <p class="truncate text-xs text-gray-400">{{ hospitalId }}</p>
          </div>
          <LogOut class="size-4 shrink-0 text-gray-400" />
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="min-w-0 flex-1">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { LayoutDashboard, MessageSquareText, BarChart3, Settings, HeartPulse, LogOut } from 'lucide-vue-next'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import { useHospital } from '@/composables/useHospital'

const { hospitalId, hospitalName, logout } = useHospital()

const navItems = [
  { label: '대시보드', to: '/', icon: LayoutDashboard },
  { label: '리뷰 목록', to: '/reviews', icon: MessageSquareText },
  { label: '통계', to: '/statistics', icon: BarChart3 },
  { label: '설정', to: '/settings', icon: Settings },
]
</script>
