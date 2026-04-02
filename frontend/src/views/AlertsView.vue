<template>
  <div class="min-h-full">
    <!-- 상단 헤더 -->
    <div class="border-b border-gray-200 bg-white px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="flex items-center gap-2 text-xl font-bold text-gray-900">
            <AlertTriangle class="size-5 text-red-500" />
            부정 리뷰 관리
          </h1>
          <p class="mt-0.5 text-sm text-gray-500">낮은 별점 리뷰를 신속하게 파악하고 위기 대응을 진행하세요.</p>
        </div>
        <div class="flex items-center gap-2">
          <AppButton
            icon="i-lucide-check-check"
            label="모두 읽음"
            color="neutral"
            variant="outline"
            size="sm"
            @click="markAllRead"
          />
          <AppButton
            icon="i-lucide-refresh-cw"
            label="새로고침"
            size="sm"
            :loading="loading"
            @click="loadAlerts"
          />
        </div>
      </div>

      <!-- 심각도 탭 -->
      <div class="mt-4 flex gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          :class="[
            'flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-sm font-medium transition-all',
            activeTab === tab.value
              ? 'bg-gray-900 text-white'
              : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900'
          ]"
          @click="activeTab = tab.value"
        >
          {{ tab.label }}
          <span
            :class="[
              'flex h-5 min-w-5 items-center justify-center rounded-full px-1 text-[10px] font-bold',
              activeTab === tab.value ? 'bg-white/20 text-white' : 'bg-gray-200 text-gray-600'
            ]"
          >
            {{ getTabCount(tab.value) }}
          </span>
        </button>
      </div>
    </div>

    <div class="p-6">
      <!-- 통계 카드 -->
      <div class="mb-6 grid gap-3 sm:grid-cols-4">
        <div class="rounded-xl border border-red-200 bg-red-50 p-4">
          <div class="flex items-center justify-between">
            <p class="text-xs font-medium text-red-600">긴급</p>
            <AlertOctagon class="size-4 text-red-500" />
          </div>
          <p class="mt-2 text-2xl font-bold text-red-700">{{ stats.critical }}</p>
          <p class="text-xs text-red-500">별점 1점</p>
        </div>
        <div class="rounded-xl border border-orange-200 bg-orange-50 p-4">
          <div class="flex items-center justify-between">
            <p class="text-xs font-medium text-orange-600">주의</p>
            <AlertTriangle class="size-4 text-orange-500" />
          </div>
          <p class="mt-2 text-2xl font-bold text-orange-700">{{ stats.warning }}</p>
          <p class="text-xs text-orange-500">별점 2점</p>
        </div>
        <div class="rounded-xl border border-yellow-200 bg-yellow-50 p-4">
          <div class="flex items-center justify-between">
            <p class="text-xs font-medium text-yellow-600">확인 필요</p>
            <MessageSquareWarning class="size-4 text-yellow-600" />
          </div>
          <p class="mt-2 text-2xl font-bold text-yellow-700">{{ stats.info }}</p>
          <p class="text-xs text-yellow-600">별점 3점</p>
        </div>
        <div class="rounded-xl border border-gray-200 bg-gray-50 p-4">
          <div class="flex items-center justify-between">
            <p class="text-xs font-medium text-gray-600">미읽음</p>
            <BellRing class="size-4 text-gray-500" />
          </div>
          <p class="mt-2 text-2xl font-bold text-gray-700">{{ stats.unread }}</p>
          <p class="text-xs text-gray-500">전체 미읽음</p>
        </div>
      </div>

      <!-- 리스트 -->
      <div v-if="loading" class="space-y-3">
        <div v-for="i in 3" :key="i" class="h-40 animate-pulse rounded-2xl bg-gray-100" />
      </div>

      <div v-else-if="filteredAlerts.length === 0" class="flex flex-col items-center justify-center py-16 text-gray-400">
        <CheckCircle2 class="mb-3 size-12 text-green-300" />
        <p class="font-medium text-gray-600">모든 위기 알림이 해결되었습니다</p>
        <p class="mt-1 text-sm">새로운 부정 리뷰가 없습니다.</p>
      </div>

      <div v-else class="space-y-3">
        <article
          v-for="alert in filteredAlerts"
          :key="alert.id"
          :class="[
            'rounded-2xl border bg-white p-5 shadow-sm transition-all',
            !alert.isRead ? 'border-l-4 shadow-md' : 'border-gray-200',
            alert.severity === 'critical' && !alert.isRead ? 'border-l-red-500' : '',
            alert.severity === 'warning' && !alert.isRead ? 'border-l-orange-400' : '',
            alert.severity === 'info' && !alert.isRead ? 'border-l-yellow-400' : '',
          ]"
        >
          <div class="flex items-start gap-4">
            <!-- 심각도 아이콘 -->
            <div :class="['mt-0.5 flex size-9 shrink-0 items-center justify-center rounded-xl', severityBg(alert.severity)]">
              <component :is="severityIcon(alert.severity)" :class="['size-4', severityColor(alert.severity)]" />
            </div>

            <div class="flex-1 min-w-0">
              <!-- 메타 -->
              <div class="mb-2 flex flex-wrap items-center gap-2">
                <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold uppercase', severityBadge(alert.severity)]">
                  {{ severityLabel(alert.severity) }}
                </span>
                <span class="flex items-center gap-1 text-xs text-gray-500">
                  <component :is="platformIcon(alert.platform)" class="size-3" />
                  {{ platformLabel(alert.platform) }}
                </span>
                <div class="flex items-center gap-0.5">
                  <Star v-for="i in alert.rating" :key="i" class="size-3 fill-yellow-400 text-yellow-400" />
                  <Star v-for="i in (5 - alert.rating)" :key="'e'+i" class="size-3 text-gray-200" />
                </div>
                <span class="text-xs text-gray-400">{{ alert.date }}</span>
                <span v-if="!alert.isRead" class="rounded-full bg-indigo-100 px-2 py-0.5 text-[10px] font-bold text-indigo-700">NEW</span>
                <span v-if="alert.isBlacklist" class="flex items-center gap-0.5 rounded-full bg-red-100 px-2 py-0.5 text-[10px] font-bold text-red-700">
                  <ShieldAlert class="size-2.5" /> 블랙컨슈머 의심
                </span>
              </div>

              <!-- 리뷰 내용 -->
              <p class="mb-1 text-xs font-semibold text-gray-700">{{ alert.author }}</p>
              <p class="text-sm text-gray-800 line-clamp-3">{{ alert.content }}</p>

              <!-- AI 답글 제안 -->
              <div v-if="alert.suggestedReply" class="mt-3 rounded-xl bg-indigo-50 p-3">
                <div class="mb-1 flex items-center gap-1.5">
                  <Sparkles class="size-3 text-indigo-500" />
                  <p class="text-[11px] font-semibold text-indigo-700">AI 답글 제안</p>
                </div>
                <p class="text-xs text-indigo-800">{{ alert.suggestedReply }}</p>
              </div>

              <!-- 액션 버튼 -->
              <div class="mt-3 flex flex-wrap gap-2">
                <button
                  v-if="!alert.isRead"
                  class="flex items-center gap-1 rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-200 transition-colors"
                  @click="handleMarkRead(alert.id)"
                >
                  <Eye class="size-3" /> 읽음 처리
                </button>
                <button
                  v-if="!alert.suggestedReply"
                  class="flex items-center gap-1 rounded-lg bg-indigo-100 px-3 py-1.5 text-xs font-medium text-indigo-700 hover:bg-indigo-200 transition-colors"
                  @click="handleGenerateReply(alert)"
                >
                  <Sparkles class="size-3" /> AI 답글 생성
                </button>
                <button
                  v-if="alert.suggestedReply"
                  class="flex items-center gap-1 rounded-lg bg-green-100 px-3 py-1.5 text-xs font-medium text-green-700 hover:bg-green-200 transition-colors"
                  @click="handleApproveReply(alert)"
                >
                  <CheckCircle2 class="size-3" /> 답글 승인
                </button>
                <button
                  v-if="!alert.isResolved"
                  class="flex items-center gap-1 rounded-lg bg-gray-100 px-3 py-1.5 text-xs font-medium text-gray-600 hover:bg-gray-200 transition-colors"
                  @click="handleResolve(alert.id)"
                >
                  <CheckCheck class="size-3" /> 해결 완료
                </button>
                <button
                  v-if="!alert.isBlacklist"
                  class="flex items-center gap-1 rounded-lg bg-red-50 px-3 py-1.5 text-xs font-medium text-red-600 hover:bg-red-100 transition-colors"
                  @click="handleBlacklist(alert.id)"
                >
                  <ShieldAlert class="size-3" /> 블랙컨슈머 신고
                </button>
              </div>
            </div>
          </div>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHospital } from '@/composables/useHospital'
import { useToast } from '@/composables/useToast'
import { alertsApi } from '@/api/alerts'
import type { ReviewAlert, AlertSeverity, Platform } from '@/types/review'
import AppButton from '@/components/ui/AppButton.vue'
import {
  AlertTriangle, AlertOctagon, MessageSquareWarning, BellRing,
  CheckCircle2, Star, Sparkles, Eye, CheckCheck, ShieldAlert, Globe, Map
} from 'lucide-vue-next'

const { hospitalId } = useHospital()
const { add: addToast } = useToast()

const loading = ref(false)
const activeTab = ref('all')
const alerts = ref<ReviewAlert[]>([])
const stats = ref({ critical: 0, warning: 0, info: 0, unread: 0 })

const tabs = [
  { label: '전체', value: 'all' },
  { label: '긴급 (1점)', value: 'critical' },
  { label: '주의 (2점)', value: 'warning' },
  { label: '확인 필요 (3점)', value: 'info' },
  { label: '해결 완료', value: 'resolved' },
]

const filteredAlerts = computed(() => {
  if (activeTab.value === 'all') return alerts.value.filter(a => !a.isResolved)
  if (activeTab.value === 'resolved') return alerts.value.filter(a => a.isResolved)
  return alerts.value.filter(a => a.severity === activeTab.value && !a.isResolved)
})

function getTabCount(tab: string) {
  if (tab === 'all') return alerts.value.filter(a => !a.isResolved).length
  if (tab === 'resolved') return alerts.value.filter(a => a.isResolved).length
  return alerts.value.filter(a => a.severity === tab && !a.isResolved).length
}

function severityBg(s: AlertSeverity) {
  return { critical: 'bg-red-100', warning: 'bg-orange-100', info: 'bg-yellow-100' }[s]
}
function severityColor(s: AlertSeverity) {
  return { critical: 'text-red-600', warning: 'text-orange-500', info: 'text-yellow-600' }[s]
}
function severityBadge(s: AlertSeverity) {
  return {
    critical: 'bg-red-100 text-red-700',
    warning: 'bg-orange-100 text-orange-700',
    info: 'bg-yellow-100 text-yellow-700',
  }[s]
}
function severityLabel(s: AlertSeverity) {
  return { critical: '긴급', warning: '주의', info: '확인 필요' }[s]
}
function severityIcon(s: AlertSeverity) {
  return { critical: AlertOctagon, warning: AlertTriangle, info: MessageSquareWarning }[s]
}
function platformLabel(p: Platform) {
  return { naver: '네이버', google: '구글', kakao: '카카오' }[p]
}
function platformIcon(_p: Platform) {
  return Globe
}

// ── 더미 데이터 (API 연동 전) ──────────────────────────────────────────────
function generateDummyAlerts(): ReviewAlert[] {
  return [
    {
      id: '1', reviewId: 'r1', storeId: hospitalId.value,
      severity: 'critical', platform: 'naver', author: '이*수',
      rating: 1, date: '2026-04-01',
      content: '음식이 너무 짜고 서비스도 불친절했습니다. 다시는 안 올 것 같아요. 위생 상태도 불안했고 가격 대비 최악이었습니다.',
      isRead: false, isResolved: false, isBlacklist: false,
      suggestedReply: undefined,
    },
    {
      id: '2', reviewId: 'r2', storeId: hospitalId.value,
      severity: 'critical', platform: 'google', author: 'Kim J.',
      rating: 1, date: '2026-03-30',
      content: 'Terrible experience. Waited over 1 hour and the food was cold. Staff was rude. Would not recommend.',
      isRead: false, isResolved: false, isBlacklist: true,
      suggestedReply: '안녕하세요, Kim님. 불편을 드려 진심으로 사과드립니다. 저희의 서비스 수준이 기대에 미치지 못했던 점 매우 유감스럽게 생각합니다. 말씀해 주신 사항을 바탕으로 즉시 개선하겠습니다.',
      language: 'en',
    },
    {
      id: '3', reviewId: 'r3', storeId: hospitalId.value,
      severity: 'warning', platform: 'naver', author: '박*민',
      rating: 2, date: '2026-03-29',
      content: '기대가 컸는데 실망스러웠어요. 예약 시간보다 30분이나 늦게 입장했고 안내도 없었습니다.',
      isRead: false, isResolved: false, isBlacklist: false,
      suggestedReply: undefined,
    },
    {
      id: '4', reviewId: 'r4', storeId: hospitalId.value,
      severity: 'warning', platform: 'google', author: '최*영',
      rating: 2, date: '2026-03-28',
      content: '주차 공간이 너무 좁아서 불편했습니다. 직원분들은 친절하셨는데 시설이 아쉬웠어요.',
      isRead: true, isResolved: false, isBlacklist: false,
      suggestedReply: '안녕하세요, 최님. 방문해 주셔서 감사합니다. 주차 공간 불편에 대해 깊이 사과드립니다. 주차 환경 개선을 위해 노력하겠습니다.',
    },
    {
      id: '5', reviewId: 'r5', storeId: hospitalId.value,
      severity: 'info', platform: 'naver', author: '정*아',
      rating: 3, date: '2026-03-27',
      content: '보통이에요. 나쁘지는 않았지만 특별히 좋지도 않았습니다. 가격이 조금 비싼 것 같아요.',
      isRead: true, isResolved: false, isBlacklist: false,
      suggestedReply: undefined,
    },
    {
      id: '6', reviewId: 'r6', storeId: hospitalId.value,
      severity: 'critical', platform: 'naver', author: '한*준',
      rating: 1, date: '2026-03-25',
      content: '환불 요청을 해도 처리해주지 않네요. 고객 센터에도 연락이 안 되고 정말 화가 납니다.',
      isRead: false, isResolved: true, isBlacklist: false,
      suggestedReply: undefined,
    },
  ]
}

async function loadAlerts() {
  loading.value = true
  try {
    const { data } = await alertsApi.list(hospitalId.value)
    alerts.value = data
    const statsRes = await alertsApi.getStats(hospitalId.value)
    stats.value = statsRes.data
  } catch {
    // API 미연동 시 더미 데이터 사용
    alerts.value = generateDummyAlerts()
    stats.value = {
      critical: alerts.value.filter(a => a.severity === 'critical' && !a.isResolved).length,
      warning: alerts.value.filter(a => a.severity === 'warning' && !a.isResolved).length,
      info: alerts.value.filter(a => a.severity === 'info' && !a.isResolved).length,
      unread: alerts.value.filter(a => !a.isRead).length,
    }
  } finally {
    loading.value = false
  }
}

async function handleMarkRead(id: string) {
  try {
    await alertsApi.markRead(id)
  } catch { /* ignore */ }
  const a = alerts.value.find(x => x.id === id)
  if (a) { a.isRead = true; stats.value.unread = Math.max(0, stats.value.unread - 1) }
}

async function handleGenerateReply(alert: ReviewAlert) {
  addToast({ title: 'AI 답글을 생성하는 중...', color: 'info' })
  try {
    const { data } = await alertsApi.generateCrisisReply(alert.id, 'formal')
    alert.suggestedReply = data.reply_text
    addToast({ title: 'AI 답글이 생성되었습니다.', color: 'success' })
  } catch {
    alert.suggestedReply = '안녕하세요, 소중한 의견을 남겨주셔서 감사합니다. 불편을 드린 점 진심으로 사과드리며, 빠른 시일 내에 개선하겠습니다. 더 나은 서비스로 보답할 것을 약속드립니다.'
    addToast({ title: '(더미) AI 답글이 생성되었습니다.', color: 'success' })
  }
}

async function handleApproveReply(alert: ReviewAlert) {
  addToast({ title: '답글이 승인되었습니다. 게시 준비 완료.', color: 'success' })
  alert.isResolved = true
}

async function handleResolve(id: string) {
  try {
    await alertsApi.resolve(id)
  } catch { /* ignore */ }
  const a = alerts.value.find(x => x.id === id)
  if (a) a.isResolved = true
  addToast({ title: '알림이 해결 처리되었습니다.', color: 'success' })
}

async function handleBlacklist(id: string) {
  try {
    await alertsApi.reportBlacklist(id, '반복 악성 리뷰 의심')
  } catch { /* ignore */ }
  const a = alerts.value.find(x => x.id === id)
  if (a) a.isBlacklist = true
  addToast({ title: '블랙컨슈머로 신고되었습니다.', color: 'warning' })
}

async function markAllRead() {
  alerts.value.filter(a => !a.isRead).forEach(a => { a.isRead = true })
  stats.value.unread = 0
  addToast({ title: '모든 알림을 읽음 처리했습니다.', color: 'success' })
}

onMounted(loadAlerts)
</script>
