<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useHospital } from '@/composables/useHospital'
import { useToast } from '@/composables/useToast'
import { useReviews } from '@/composables/useReviews'
import { analysisApi, type AnalysisSummary } from '@/api/analysis'
import { reviewsApi } from '@/api/reviews'
import PanelLayout from '@/components/PanelLayout.vue'
import ReviewCard from '@/components/ReviewCard.vue'
import AIReplyPanel from '@/components/AIReplyPanel.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppEmpty from '@/components/ui/AppEmpty.vue'
import {
  MessageSquareText, CheckCircle2, Clock, TrendingUp,
  Smile, Frown, Meh, Sparkles, RefreshCw
} from 'lucide-vue-next'

const { hospitalId } = useHospital()
const { add: addToast } = useToast()
const { reviews, selectedReview, unrepliedReviews, selectReview, submitReply, fetchReviews } = useReviews()

const summary = ref<AnalysisSummary | null>(null)
const loadingSummary = ref(false)
const collecting = ref(false)
const analyzing = ref(false)

async function loadSummary() {
  loadingSummary.value = true
  try {
    const { data } = await analysisApi.getSummary(hospitalId.value)
    summary.value = data
  } catch {
    // 분석 데이터 없어도 대시보드는 보여줌
  } finally {
    loadingSummary.value = false
  }
}

async function fetchNewReviews() {
  collecting.value = true
  try {
    await reviewsApi.collect(hospitalId.value)
    addToast({ title: '리뷰 수집 완료', color: 'success' })
    await Promise.all([loadSummary(), fetchReviews()])
  } catch {
    addToast({ title: '리뷰 수집에 실패했습니다.', color: 'error' })
  } finally {
    collecting.value = false
  }
}

async function runAnalysis() {
  analyzing.value = true
  try {
    const { data } = await analysisApi.runAnalysis(hospitalId.value)
    addToast({ title: `AI 분석 완료 (${data.analyzed_count}건)`, color: 'success' })
    await loadSummary()
  } catch {
    addToast({ title: 'AI 분석에 실패했습니다.', color: 'error' })
  } finally {
    analyzing.value = false
  }
}

const maxMonthlyCount = computed(() =>
  Math.max(...(summary.value?.monthly_trend.map(m => m.count) ?? [1]))
)

function formatMonth(m: string) {
  const [y, mo] = m.split('-')
  return `${y.slice(2)}년 ${parseInt(mo)}월`
}

onMounted(async () => { await Promise.all([loadSummary(), fetchReviews()]) })
</script>

<template>
  <div class="flex flex-1 overflow-hidden">
    <PanelLayout title="대시보드">
      <template #right>
        <AppButton
          icon="i-lucide-sparkles"
          label="AI 분석"
          size="sm"
          color="neutral"
          variant="outline"
          :loading="analyzing"
          @click="runAnalysis"
        />
        <AppButton
          icon="i-lucide-refresh-cw"
          label="새 리뷰 가져오기"
          size="sm"
          color="primary"
          variant="solid"
          :loading="collecting"
          @click="fetchNewReviews"
        />
      </template>

      <div class="overflow-auto p-6 space-y-6">

        <!-- 1. 핵심 지표 카드 4개 -->
        <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <div class="rounded-xl border border-gray-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-500">전체 리뷰</p>
              <div class="flex size-9 items-center justify-center rounded-lg bg-blue-50">
                <MessageSquareText class="size-4 text-blue-600" />
              </div>
            </div>
            <p class="mt-3 text-2xl font-bold text-gray-900">
              {{ summary?.total_reviews ?? '—' }}
            </p>
            <p class="mt-1 text-xs text-gray-400">
              분석 완료 {{ summary?.analyzed_count ?? 0 }}건
            </p>
          </div>

          <div class="rounded-xl border border-gray-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-500">긍정률</p>
              <div class="flex size-9 items-center justify-center rounded-lg bg-green-50">
                <Smile class="size-4 text-green-600" />
              </div>
            </div>
            <p class="mt-3 text-2xl font-bold text-gray-900">
              {{ summary?.sentiment.positive_pct ?? '—' }}
              <span v-if="summary" class="text-base font-normal text-gray-400">%</span>
            </p>
            <p class="mt-1 text-xs text-gray-400">
              긍정 {{ summary?.sentiment.positive ?? 0 }}건
            </p>
          </div>

          <div class="rounded-xl border border-gray-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-500">답변율</p>
              <div class="flex size-9 items-center justify-center rounded-lg bg-purple-50">
                <CheckCircle2 class="size-4 text-purple-600" />
              </div>
            </div>
            <p class="mt-3 text-2xl font-bold text-gray-900">
              {{ summary?.reply_rate ?? '—' }}
              <span v-if="summary" class="text-base font-normal text-gray-400">%</span>
            </p>
            <p class="mt-1 text-xs text-gray-400">답변 완료 기준</p>
          </div>

          <div class="rounded-xl border border-gray-200 bg-white p-5">
            <div class="flex items-center justify-between">
              <p class="text-sm font-medium text-gray-500">미답변</p>
              <div class="flex size-9 items-center justify-center rounded-lg bg-orange-50">
                <Clock class="size-4 text-orange-500" />
              </div>
            </div>
            <p class="mt-3 text-2xl font-bold text-gray-900">
              {{ summary?.pending_count ?? '—' }}
              <span v-if="summary" class="text-base font-normal text-gray-400">건</span>
            </p>
            <p class="mt-1 text-xs text-gray-400">답변 대기 중</p>
          </div>
        </div>

        <!-- 2. 감성 분석 + 키워드 -->
        <div class="grid gap-4 lg:grid-cols-2">
          <!-- 감성 분포 -->
          <div class="rounded-xl border border-gray-200 bg-white p-5">
            <h3 class="mb-4 text-sm font-semibold text-gray-900">감성 분포</h3>

            <div v-if="!summary || summary.analyzed_count === 0" class="flex h-28 items-center justify-center text-sm text-gray-400">
              AI 분석 실행 후 확인 가능합니다
            </div>
            <div v-else class="space-y-3">
              <!-- 세그먼트 바 -->
              <div class="flex h-3 w-full overflow-hidden rounded-full">
                <div
                  class="bg-green-400 transition-all"
                  :style="{ width: summary.sentiment.positive_pct + '%' }"
                />
                <div
                  class="bg-gray-300 transition-all"
                  :style="{ width: summary.sentiment.neutral_pct + '%' }"
                />
                <div
                  class="bg-red-400 transition-all"
                  :style="{ width: summary.sentiment.negative_pct + '%' }"
                />
              </div>
              <div class="grid grid-cols-3 gap-2 text-center">
                <div class="rounded-lg bg-green-50 p-3">
                  <Smile class="mx-auto mb-1 size-4 text-green-600" />
                  <p class="text-lg font-bold text-green-700">{{ summary.sentiment.positive_pct }}%</p>
                  <p class="text-xs text-green-600">긍정 {{ summary.sentiment.positive }}건</p>
                </div>
                <div class="rounded-lg bg-gray-50 p-3">
                  <Meh class="mx-auto mb-1 size-4 text-gray-500" />
                  <p class="text-lg font-bold text-gray-600">{{ summary.sentiment.neutral_pct }}%</p>
                  <p class="text-xs text-gray-500">중립 {{ summary.sentiment.neutral }}건</p>
                </div>
                <div class="rounded-lg bg-red-50 p-3">
                  <Frown class="mx-auto mb-1 size-4 text-red-500" />
                  <p class="text-lg font-bold text-red-600">{{ summary.sentiment.negative_pct }}%</p>
                  <p class="text-xs text-red-500">부정 {{ summary.sentiment.negative }}건</p>
                </div>
              </div>
            </div>
          </div>

          <!-- 주요 키워드 -->
          <div class="rounded-xl border border-gray-200 bg-white p-5">
            <h3 class="mb-4 text-sm font-semibold text-gray-900">주요 키워드</h3>

            <div v-if="!summary || (summary.top_positive_keywords.length === 0 && summary.top_negative_keywords.length === 0)"
              class="flex h-28 items-center justify-center text-sm text-gray-400">
              AI 분석 실행 후 확인 가능합니다
            </div>
            <div v-else class="space-y-4">
              <div v-if="summary.top_positive_keywords.length > 0">
                <p class="mb-2 flex items-center gap-1 text-xs font-medium text-green-700">
                  <Smile class="size-3.5" /> 긍정 키워드
                </p>
                <div class="flex flex-wrap gap-1.5">
                  <span
                    v-for="kw in summary.top_positive_keywords"
                    :key="kw"
                    class="rounded-full bg-green-50 px-2.5 py-1 text-xs font-medium text-green-700 ring-1 ring-green-200"
                  >
                    # {{ kw }}
                  </span>
                </div>
              </div>
              <div v-if="summary.top_negative_keywords.length > 0">
                <p class="mb-2 flex items-center gap-1 text-xs font-medium text-red-600">
                  <Frown class="size-3.5" /> 부정 키워드
                </p>
                <div class="flex flex-wrap gap-1.5">
                  <span
                    v-for="kw in summary.top_negative_keywords"
                    :key="kw"
                    class="rounded-full bg-red-50 px-2.5 py-1 text-xs font-medium text-red-600 ring-1 ring-red-200"
                  >
                    # {{ kw }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. 월별 트렌드 -->
        <div class="rounded-xl border border-gray-200 bg-white p-5">
          <h3 class="mb-4 text-sm font-semibold text-gray-900">월별 리뷰 트렌드</h3>

          <div v-if="!summary || summary.monthly_trend.length === 0"
            class="flex h-28 items-center justify-center text-sm text-gray-400">
            수집된 데이터가 없습니다
          </div>
          <div v-else class="flex items-end gap-2 h-32">
            <div
              v-for="item in summary.monthly_trend"
              :key="item.month"
              class="flex flex-1 flex-col items-center gap-1"
            >
              <span class="text-xs font-semibold text-gray-700">{{ item.count }}</span>
              <div class="w-full rounded-t-md bg-primary/80 transition-all"
                :style="{ height: Math.max((item.count / maxMonthlyCount) * 88, 4) + 'px' }"
              />
              <span class="text-[10px] text-gray-400 whitespace-nowrap">{{ formatMonth(item.month) }}</span>
            </div>
          </div>
        </div>

        <!-- 4. 답변 대기 리뷰 -->
        <div>
          <div class="mb-3 flex items-center justify-between">
            <h3 class="flex items-center gap-2 text-sm font-semibold text-gray-900">
              답변 대기
              <AppBadge color="warning" variant="subtle" size="sm">
                {{ unrepliedReviews.length }}
              </AppBadge>
            </h3>
            <router-link to="/reviews">
              <AppButton label="전체 보기" variant="ghost" trailing-icon="i-lucide-arrow-right" size="sm" />
            </router-link>
          </div>

          <div v-if="unrepliedReviews.length === 0">
            <AppEmpty
              icon="i-lucide-check-circle"
              title="모든 리뷰에 답변 완료"
              description="현재 답변 대기 중인 리뷰가 없습니다."
            />
          </div>
          <div v-else class="grid gap-3 lg:grid-cols-2">
            <ReviewCard
              v-for="review in unrepliedReviews.slice(0, 4)"
              :key="review.id"
              :review="review"
              :selected="selectedReview?.id === review.id"
              @select="selectReview"
            />
          </div>
        </div>

      </div>
    </PanelLayout>

    <!-- AI 답글 패널 -->
    <div v-if="selectedReview" class="w-[400px] shrink-0 border-l border-gray-200 bg-white">
      <AIReplyPanel
        :review="selectedReview"
        @submit="submitReply"
        @close="selectedReview = null"
      />
    </div>
  </div>
</template>
