<template>
  <div class="min-h-full">
    <!-- 헤더 -->
    <div class="border-b border-gray-200 bg-white px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="flex items-center gap-2 text-xl font-bold text-gray-900">
            <FileText class="size-5 text-indigo-600" />
            월간 인사이트 리포트
          </h1>
          <p class="mt-0.5 text-sm text-gray-500">월별 리뷰 현황과 AI 분석 결과를 한눈에 확인하세요.</p>
        </div>
        <AppButton
          icon="i-lucide-sparkles"
          label="이번 달 리포트 생성"
          :loading="generating"
          @click="generateReport"
        />
      </div>

      <!-- 기간 선택 -->
      <div class="mt-4 flex gap-2 overflow-x-auto pb-1">
        <button
          v-for="p in availablePeriods"
          :key="p.value"
          :class="[
            'shrink-0 rounded-lg px-3 py-1.5 text-sm font-medium transition-all',
            selectedPeriod === p.value ? 'bg-gray-900 text-white' : 'text-gray-500 hover:bg-gray-100'
          ]"
          @click="selectPeriod(p.value)"
        >{{ p.label }}</button>
      </div>
    </div>

    <div class="p-6 space-y-5">

      <div v-if="!currentReport && !loading" class="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-200 py-16">
        <FileText class="mb-3 size-10 text-gray-300" />
        <p class="font-medium text-gray-500">선택한 기간의 리포트가 없습니다</p>
        <p class="mt-1 text-sm text-gray-400">상단 버튼을 눌러 AI 리포트를 생성하세요.</p>
        <AppButton label="리포트 생성" class="mt-4" :loading="generating" @click="generateReport" />
      </div>

      <div v-if="loading" class="space-y-4">
        <div v-for="i in 3" :key="i" class="h-40 animate-pulse rounded-2xl bg-gray-100" />
      </div>

      <template v-if="currentReport && !loading">

        <!-- 리포트 타이틀 + 다운로드 -->
        <div class="flex items-center justify-between rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 p-5 text-white">
          <div>
            <p class="text-sm font-medium text-indigo-200">{{ formatPeriod(currentReport.period) }} 리뷰 인사이트 리포트</p>
            <h2 class="mt-0.5 text-xl font-bold">{{ storeName }}</h2>
            <p class="mt-2 text-xs text-indigo-300">생성일 {{ currentReport.generatedAt }}</p>
          </div>
          <AppButton
            icon="i-lucide-download"
            label="PDF 다운로드"
            color="neutral"
            variant="outline"
            class="!bg-white/10 !border-white/30 !text-white hover:!bg-white/20"
            @click="downloadPdf"
          />
        </div>

        <!-- KPI 카드 -->
        <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
          <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
            <div class="flex items-center justify-between">
              <p class="text-xs font-medium text-gray-500">신규 리뷰</p>
              <MessageSquare class="size-4 text-indigo-500" />
            </div>
            <p class="mt-2 text-2xl font-bold text-gray-900">{{ currentReport.newReviews }}</p>
            <div class="mt-1 flex items-center gap-1">
              <TrendingUp v-if="currentReport.newReviews >= 0" class="size-3 text-green-500" />
              <TrendingDown v-else class="size-3 text-red-500" />
              <p class="text-xs text-gray-400">전월 대비</p>
            </div>
          </div>

          <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
            <div class="flex items-center justify-between">
              <p class="text-xs font-medium text-gray-500">평균 평점</p>
              <Star class="size-4 text-yellow-500" />
            </div>
            <p class="mt-2 text-2xl font-bold text-gray-900">{{ currentReport.avgRating.toFixed(1) }}</p>
            <div class="mt-1 flex items-center gap-1">
              <span :class="['text-xs font-medium', currentReport.ratingChange >= 0 ? 'text-green-600' : 'text-red-500']">
                {{ currentReport.ratingChange >= 0 ? '+' : '' }}{{ currentReport.ratingChange.toFixed(1) }}
              </span>
              <p class="text-xs text-gray-400">전월 대비</p>
            </div>
          </div>

          <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
            <div class="flex items-center justify-between">
              <p class="text-xs font-medium text-gray-500">긍정률</p>
              <Smile class="size-4 text-green-500" />
            </div>
            <p class="mt-2 text-2xl font-bold text-gray-900">{{ currentReport.positiveRate }}%</p>
            <div class="mt-1 h-1.5 w-full rounded-full bg-gray-100">
              <div class="h-full rounded-full bg-green-400 transition-all" :style="{ width: currentReport.positiveRate + '%' }" />
            </div>
          </div>

          <div class="rounded-2xl border border-gray-200 bg-white p-4 shadow-sm">
            <div class="flex items-center justify-between">
              <p class="text-xs font-medium text-gray-500">답변율</p>
              <CheckCircle class="size-4 text-purple-500" />
            </div>
            <p class="mt-2 text-2xl font-bold text-gray-900">{{ currentReport.replyRate }}%</p>
            <div class="mt-1 h-1.5 w-full rounded-full bg-gray-100">
              <div class="h-full rounded-full bg-purple-400 transition-all" :style="{ width: currentReport.replyRate + '%' }" />
            </div>
          </div>
        </div>

        <!-- 감성 분포 -->
        <div class="grid gap-4 lg:grid-cols-2">
          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <h3 class="mb-4 font-semibold text-gray-900">감성 분포</h3>
            <div class="mb-3 flex h-4 w-full overflow-hidden rounded-full">
              <div class="bg-green-400 transition-all" :style="{ width: currentReport.positiveRate + '%' }" />
              <div class="bg-gray-300 transition-all" :style="{ width: currentReport.neutralRate + '%' }" />
              <div class="bg-red-400 transition-all" :style="{ width: currentReport.negativeRate + '%' }" />
            </div>
            <div class="grid grid-cols-3 gap-2 text-center">
              <div class="rounded-xl bg-green-50 p-3">
                <Smile class="mx-auto mb-1 size-4 text-green-600" />
                <p class="text-base font-bold text-green-700">{{ currentReport.positiveRate }}%</p>
                <p class="text-[10px] text-green-600">긍정</p>
              </div>
              <div class="rounded-xl bg-gray-50 p-3">
                <Meh class="mx-auto mb-1 size-4 text-gray-500" />
                <p class="text-base font-bold text-gray-600">{{ currentReport.neutralRate }}%</p>
                <p class="text-[10px] text-gray-500">중립</p>
              </div>
              <div class="rounded-xl bg-red-50 p-3">
                <Frown class="mx-auto mb-1 size-4 text-red-500" />
                <p class="text-base font-bold text-red-600">{{ currentReport.negativeRate }}%</p>
                <p class="text-[10px] text-red-500">부정</p>
              </div>
            </div>
          </div>

          <!-- 플랫폼별 분포 -->
          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <h3 class="mb-4 font-semibold text-gray-900">플랫폼별 분포</h3>
            <div class="space-y-3">
              <div
                v-for="stat in currentReport.platformBreakdown"
                :key="stat.platform"
                class="flex items-center gap-3"
              >
                <div class="w-20 shrink-0">
                  <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold', platformBadge(stat.platform)]">
                    {{ platformLabel(stat.platform) }}
                  </span>
                </div>
                <div class="flex-1">
                  <div class="h-5 overflow-hidden rounded-full bg-gray-100">
                    <div
                      class="flex h-full items-center pl-2 text-[10px] font-bold text-white transition-all rounded-full"
                      :class="stat.platform === 'google' ? 'bg-blue-500' : 'bg-green-500'"
                      :style="{ width: Math.max(stat.percentage, 15) + '%' }"
                    >
                      {{ stat.count }}개
                    </div>
                  </div>
                </div>
                <div class="flex items-center gap-0.5 shrink-0">
                  <span class="text-xs text-gray-700">{{ stat.avgRating.toFixed(1) }}</span>
                  <Star class="size-3 fill-yellow-400 text-yellow-400" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 키워드 분석 -->
        <div class="grid gap-4 lg:grid-cols-2">
          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <h3 class="mb-3 font-semibold text-gray-900">이번 달 긍정 키워드 TOP 10</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(kw, i) in currentReport.topPositiveKeywords"
                :key="kw"
                class="flex items-center gap-1 rounded-full bg-green-50 px-3 py-1 text-xs font-medium text-green-700 ring-1 ring-green-200"
              >
                <span class="text-green-400">{{ i + 1 }}</span>
                {{ kw }}
              </span>
            </div>
          </div>
          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <h3 class="mb-3 font-semibold text-gray-900">개선 필요 키워드</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="kw in currentReport.topNegativeKeywords"
                :key="kw"
                class="rounded-full bg-red-50 px-3 py-1 text-xs font-medium text-red-600 ring-1 ring-red-200"
              >
                {{ kw }}
              </span>
            </div>
            <div class="mt-4 rounded-xl bg-orange-50 p-3">
              <p class="text-xs font-semibold text-orange-700 mb-1">AI 개선 제안</p>
              <p class="text-xs text-orange-600">{{ aiSuggestion }}</p>
            </div>
          </div>
        </div>

        <!-- 월별 트렌드 미니 차트 -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <h3 class="mb-4 font-semibold text-gray-900">6개월 리뷰 트렌드</h3>
          <div class="flex items-end gap-2 h-32">
            <div
              v-for="item in currentReport.monthlyTrend"
              :key="item.month"
              class="flex flex-1 flex-col items-center gap-1"
            >
              <span class="text-[10px] font-semibold text-gray-600">{{ item.count }}</span>
              <div
                class="w-full rounded-t-lg transition-all"
                :class="item.month === currentReport.period ? 'bg-indigo-500' : 'bg-indigo-200'"
                :style="{ height: Math.max((item.count / Math.max(...currentReport.monthlyTrend.map(t => t.count))) * 88, 4) + 'px' }"
              />
              <span class="text-[9px] text-gray-400 whitespace-nowrap">{{ formatMonth(item.month) }}</span>
            </div>
          </div>
        </div>

        <!-- 리포트 히스토리 -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <h3 class="mb-3 font-semibold text-gray-900">리포트 히스토리</h3>
          <div class="divide-y divide-gray-100">
            <div
              v-for="report in reportHistory"
              :key="report.id"
              class="flex items-center justify-between py-3"
            >
              <div class="flex items-center gap-3">
                <div class="flex size-8 items-center justify-center rounded-lg bg-indigo-50">
                  <FileText class="size-4 text-indigo-600" />
                </div>
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ formatPeriod(report.period) }} 리포트</p>
                  <p class="text-xs text-gray-400">평균 {{ report.avgRating.toFixed(1) }}점 · {{ report.newReviews }}건</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                <button
                  class="rounded-lg px-3 py-1.5 text-xs font-medium text-indigo-600 hover:bg-indigo-50 transition-colors"
                  @click="selectPeriod(report.period)"
                >
                  보기
                </button>
                <button class="rounded-lg px-3 py-1.5 text-xs font-medium text-gray-500 hover:bg-gray-100 transition-colors">
                  PDF
                </button>
              </div>
            </div>
          </div>
        </div>

      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHospital } from '@/composables/useHospital'
import { useToast } from '@/composables/useToast'
import { reportsApi } from '@/api/reports'
import type { MonthlyReport, Platform } from '@/types/review'
import AppButton from '@/components/ui/AppButton.vue'
import {
  FileText, MessageSquare, Star, Smile, Meh, Frown,
  CheckCircle, TrendingUp, TrendingDown
} from 'lucide-vue-next'

const { hospitalId, hospitalName } = useHospital()
const { add: addToast } = useToast()
const storeName = hospitalName

const loading = ref(false)
const generating = ref(false)
const currentReport = ref<MonthlyReport | null>(null)
const reportHistory = ref<MonthlyReport[]>([])
const selectedPeriod = ref('2026-04')

const availablePeriods = [
  { label: '2026년 4월', value: '2026-04' },
  { label: '2026년 3월', value: '2026-03' },
  { label: '2026년 2월', value: '2026-02' },
  { label: '2026년 1월', value: '2026-01' },
  { label: '2025년 12월', value: '2025-12' },
]

const aiSuggestion = computed(() => {
  if (!currentReport.value) return ''
  const kws = currentReport.value.topNegativeKeywords
  if (kws.includes('주차')) return '주차 공간 안내 개선이 필요합니다. 근처 주차장 정보를 리뷰 답글에 적극 안내하세요.'
  if (kws.includes('대기')) return '대기 시간 단축을 위한 예약 시스템 도입 또는 피크 타임 인력 보충을 고려해보세요.'
  if (kws.includes('가격')) return '가격 대비 가치 전달을 위해 재료/서비스 품질을 답글에 더 자세히 설명해보세요.'
  return '고객 의견을 꾸준히 반영하면 부정 키워드를 줄일 수 있습니다.'
})

function formatPeriod(p: string) {
  const [y, m] = p.split('-')
  return `${y}년 ${parseInt(m)}월`
}
function formatMonth(m: string) {
  return parseInt(m.split('-')[1]) + '월'
}

function platformLabel(p: Platform) {
  return { naver: '네이버', google: '구글', kakao: '카카오' }[p]
}
function platformBadge(p: Platform) {
  return {
    google: 'bg-blue-100 text-blue-700',
    naver: 'bg-green-100 text-green-700',
    kakao: 'bg-yellow-100 text-yellow-700',
  }[p]
}

function makeDummyReport(period: string): MonthlyReport {
  const isRecent = period >= '2026-03'
  return {
    id: period,
    storeId: hospitalId.value,
    period,
    totalReviews: Math.floor(Math.random() * 100) + 150,
    newReviews: Math.floor(Math.random() * 40) + 20,
    avgRating: 3.9 + Math.random() * 0.8,
    ratingChange: (Math.random() - 0.3) * 0.4,
    positiveRate: 60 + Math.floor(Math.random() * 20),
    negativeRate: 5 + Math.floor(Math.random() * 10),
    neutralRate: 0,
    replyRate: 70 + Math.floor(Math.random() * 25),
    topPositiveKeywords: ['친절', '맛있음', '분위기', '청결', '빠른 응대', '재방문', '추천', '합리적', '세심함', '전문적'],
    topNegativeKeywords: ['주차', '대기시간', '가격'],
    platformBreakdown: [
      { platform: 'google', count: 28, avgRating: 4.2, percentage: 55 },
      { platform: 'naver', count: 23, avgRating: 4.4, percentage: 45 },
    ],
    monthlyTrend: [
      { month: '2025-11', count: 22, avgRating: 4.0 },
      { month: '2025-12', count: 31, avgRating: 4.1 },
      { month: '2026-01', count: 28, avgRating: 4.3 },
      { month: '2026-02', count: 35, avgRating: 4.3 },
      { month: '2026-03', count: 42, avgRating: 4.4 },
      { month: '2026-04', count: isRecent ? 19 : 38, avgRating: 4.5 },
    ],
    generatedAt: new Date().toISOString().split('T')[0],
  }
}

async function selectPeriod(period: string) {
  selectedPeriod.value = period
  loading.value = true
  try {
    const { data } = await reportsApi.getByPeriod(hospitalId.value, period)
    currentReport.value = data
    if (data.neutralRate === 0) {
      data.neutralRate = 100 - data.positiveRate - data.negativeRate
    }
  } catch {
    const dummy = makeDummyReport(period)
    dummy.neutralRate = 100 - dummy.positiveRate - dummy.negativeRate
    currentReport.value = dummy
  } finally {
    loading.value = false
  }
}

async function generateReport() {
  generating.value = true
  try {
    const { data } = await reportsApi.generate(hospitalId.value, selectedPeriod.value)
    currentReport.value = data
    addToast({ title: '리포트가 생성되었습니다.', color: 'success' })
  } catch {
    const dummy = makeDummyReport(selectedPeriod.value)
    dummy.neutralRate = 100 - dummy.positiveRate - dummy.negativeRate
    currentReport.value = dummy
    addToast({ title: '(더미) 리포트가 생성되었습니다.', color: 'success' })
  } finally {
    generating.value = false
  }
}

function downloadPdf() {
  addToast({ title: 'PDF 다운로드는 준비 중입니다.', color: 'info' })
}

onMounted(async () => {
  try {
    const { data } = await reportsApi.list(hospitalId.value)
    reportHistory.value = data
    if (data.length > 0) {
      currentReport.value = data[0]
      if (currentReport.value.neutralRate === 0) {
        currentReport.value.neutralRate = 100 - currentReport.value.positiveRate - currentReport.value.negativeRate
      }
      selectedPeriod.value = data[0].period
    }
  } catch {
    reportHistory.value = availablePeriods.map(p => makeDummyReport(p.value))
    const dummy = makeDummyReport('2026-04')
    dummy.neutralRate = 100 - dummy.positiveRate - dummy.negativeRate
    currentReport.value = dummy
  }
})
</script>
