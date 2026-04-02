<template>
  <div class="flex min-h-screen bg-slate-50">
    <!-- Sidebar -->
    <aside class="sidebar-gradient flex w-60 shrink-0 flex-col">
      <!-- 로고 -->
      <div class="flex items-center gap-3 px-5 py-5">
        <div class="flex size-9 items-center justify-center rounded-xl bg-white/15">
          <Star class="size-5 text-white" />
        </div>
        <div>
          <span class="text-base font-bold tracking-tight text-white">ReviewHub</span>
          <p class="text-[10px] leading-none text-indigo-300">AI 리뷰 통합 관리</p>
        </div>
      </div>

      <!-- 구분선 -->
      <div class="mx-4 border-t border-white/10" />

      <!-- 네비게이션 -->
      <nav class="flex-1 space-y-0.5 px-3 py-3">
        <p class="mb-1 px-3 text-[10px] font-semibold uppercase tracking-wider text-indigo-400">메인</p>
        <router-link
          v-for="item in mainNavItems"
          :key="item.to"
          :to="item.to"
          class="group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all"
          :class="isActive(item.to) ? 'bg-white/15 text-white' : 'text-indigo-200 hover:bg-white/10 hover:text-white'"
        >
          <component :is="item.icon" class="size-4 shrink-0" />
          {{ item.label }}
          <!-- 부정 리뷰 알림 뱃지 -->
          <span
            v-if="item.badge && item.badge > 0"
            class="ml-auto flex size-5 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white alert-pulse"
          >
            {{ item.badge > 9 ? '9+' : item.badge }}
          </span>
        </router-link>

        <p class="mb-1 mt-4 px-3 text-[10px] font-semibold uppercase tracking-wider text-indigo-400">분석 & 성장</p>
        <router-link
          v-for="item in analyticsNavItems"
          :key="item.to"
          :to="item.to"
          class="group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all"
          :class="isActive(item.to) ? 'bg-white/15 text-white' : 'text-indigo-200 hover:bg-white/10 hover:text-white'"
        >
          <component :is="item.icon" class="size-4 shrink-0" />
          {{ item.label }}
        </router-link>

        <p class="mb-1 mt-4 px-3 text-[10px] font-semibold uppercase tracking-wider text-indigo-400">시스템</p>
        <router-link
          v-for="item in systemNavItems"
          :key="item.to"
          :to="item.to"
          class="group flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all"
          :class="isActive(item.to) ? 'bg-white/15 text-white' : 'text-indigo-200 hover:bg-white/10 hover:text-white'"
        >
          <component :is="item.icon" class="size-4 shrink-0" />
          {{ item.label }}
        </router-link>
      </nav>

      <!-- 하단 업장 정보 -->
      <div class="border-t border-white/10 p-3">
        <button
          class="flex w-full items-center gap-3 rounded-lg px-3 py-2 text-left transition-all hover:bg-white/10"
          @click="logout"
        >
          <div class="flex size-8 shrink-0 items-center justify-center rounded-full bg-indigo-400/30 text-xs font-bold text-white">
            {{ storeName.charAt(0) }}
          </div>
          <div class="min-w-0 flex-1">
            <p class="truncate text-xs font-semibold text-white">{{ storeName }}</p>
            <p class="truncate text-[10px] text-indigo-300">로그아웃</p>
          </div>
          <LogOut class="size-3.5 shrink-0 text-indigo-300" />
        </button>
      </div>
    </aside>

    <!-- Main -->
    <main class="min-w-0 flex-1 overflow-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  LayoutDashboard, MessageSquareText, BarChart3, Settings,
  Star, LogOut, AlertTriangle, QrCode, Users, FileText
} from 'lucide-vue-next'
import { useHospital } from '@/composables/useHospital'
import { alertsApi } from '@/api/alerts'

const { hospitalId, hospitalName, logout } = useHospital()
const storeName = hospitalName
const route = useRoute()

const urgentAlertCount = ref(0)

function isActive(path: string) {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}

const mainNavItems = [
  { label: '대시보드', to: '/', icon: LayoutDashboard },
  { label: '리뷰 목록', to: '/reviews', icon: MessageSquareText },
  { label: '부정 리뷰 관리', to: '/alerts', icon: AlertTriangle, get badge() { return urgentAlertCount.value } },
]

const analyticsNavItems = [
  { label: '통계 · 분석', to: '/statistics', icon: BarChart3 },
  { label: '경쟁사 모니터링', to: '/competitors', icon: Users },
  { label: '월간 리포트', to: '/reports', icon: FileText },
  { label: '리뷰 요청', to: '/requests', icon: QrCode },
]

const systemNavItems = [
  { label: '설정', to: '/settings', icon: Settings },
]

onMounted(async () => {
  try {
    const { data } = await alertsApi.getStats(hospitalId.value)
    urgentAlertCount.value = data.critical + data.unread
  } catch {
    // 알림 통계 실패해도 무시
  }
})
</script>
