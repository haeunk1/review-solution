<script setup lang="ts">
import { ref, computed } from 'vue'
import { useReviews } from '@/composables/useReviews'
import PanelLayout from '@/components/PanelLayout.vue'
import StatsCard from '@/components/StatsCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppSelect from '@/components/ui/AppSelect.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppProgress from '@/components/ui/AppProgress.vue'
import { Star, TrendingUp, TrendingDown, Minus } from 'lucide-vue-next'

const { reviews, stats } = useReviews()

const periodOptions = [
  { label: '최근 7일', value: '7d' },
  { label: '최근 30일', value: '30d' },
  { label: '최근 90일', value: '90d' },
  { label: '최근 1년', value: '1y' },
]

const selectedPeriod = ref('30d')

const ratingDistribution = computed(() => {
  const distribution = [0, 0, 0, 0, 0]
  reviews.value.forEach((review) => {
    distribution[review.rating - 1]++
  })
  return distribution.reverse()
})

const totalReviews = computed(() => reviews.value.length)

const monthlyTrend = [
  { month: '10월', reviews: 18, avgRating: 4.2 },
  { month: '11월', reviews: 24, avgRating: 4.3 },
  { month: '12월', reviews: 31, avgRating: 4.4 },
  { month: '1월', reviews: 28, avgRating: 4.5 },
  { month: '2월', reviews: 35, avgRating: 4.4 },
  { month: '3월', reviews: 42, avgRating: 4.6 },
]

const responseTimeData = [
  { range: '1시간 이내', count: 45, percentage: 45 },
  { range: '1-3시간', count: 30, percentage: 30 },
  { range: '3-6시간', count: 15, percentage: 15 },
  { range: '6-24시간', count: 8, percentage: 8 },
  { range: '24시간 이상', count: 2, percentage: 2 },
]
</script>

<template>
  <PanelLayout title="통계">
    <template #right>
      <AppSelect v-model="selectedPeriod" :items="periodOptions" value-key="value" class="w-36" />
      <AppButton icon="i-lucide-download" label="리포트 다운로드" color="neutral" variant="outline" size="sm" />
    </template>
    <div class="p-6">
      <div class="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatsCard v-for="stat in stats" :key="stat.label" :stat="stat" />
      </div>
      <div class="grid gap-6 lg:grid-cols-2">
        <AppCard>
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold text-gray-900">별점 분포</h3>
              <AppBadge color="primary" variant="subtle">총 {{ totalReviews }}개</AppBadge>
            </div>
          </template>
          <div class="space-y-3">
            <div
              v-for="(count, index) in ratingDistribution"
              :key="index"
              class="flex items-center gap-3"
            >
              <div class="flex w-16 items-center gap-1">
                <span class="text-sm font-medium">{{ 5 - index }}점</span>
                <Star class="size-4 text-yellow-400" />
              </div>
              <div class="flex-1">
                <AppProgress :value="totalReviews > 0 ? (count / totalReviews) * 100 : 0" />
              </div>
              <span class="w-12 text-right text-sm text-gray-500">{{ count }}개</span>
            </div>
          </div>
        </AppCard>
        <AppCard>
          <template #header>
            <h3 class="font-semibold text-gray-900">답변 시간 분포</h3>
          </template>
          <div class="space-y-3">
            <div
              v-for="item in responseTimeData"
              :key="item.range"
              class="flex items-center gap-3"
            >
              <span class="w-24 text-sm">{{ item.range }}</span>
              <div class="flex-1">
                <AppProgress
                  :value="item.percentage"
                  :color="item.percentage > 30 ? 'success' : 'primary'"
                />
              </div>
              <span class="w-12 text-right text-sm text-gray-500">{{ item.percentage }}%</span>
            </div>
          </div>
        </AppCard>
        <AppCard class="lg:col-span-2">
          <template #header>
            <h3 class="font-semibold text-gray-900">월별 리뷰 추이</h3>
          </template>
          <div class="overflow-x-auto">
            <table class="w-full">
              <thead>
                <tr class="border-b border-gray-200">
                  <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">월</th>
                  <th class="px-4 py-3 text-right text-sm font-medium text-gray-500">리뷰 수</th>
                  <th class="px-4 py-3 text-right text-sm font-medium text-gray-500">평균 별점</th>
                  <th class="px-4 py-3 text-left text-sm font-medium text-gray-500">추이</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="(item, index) in monthlyTrend"
                  :key="item.month"
                  class="border-b border-gray-200 last:border-0"
                >
                  <td class="px-4 py-3 text-sm font-medium text-gray-900">{{ item.month }}</td>
                  <td class="px-4 py-3 text-right text-sm">{{ item.reviews }}개</td>
                  <td class="px-4 py-3 text-right">
                    <div class="flex items-center justify-end gap-1">
                      <span class="text-sm">{{ item.avgRating }}</span>
                      <Star class="size-4 text-yellow-400" />
                    </div>
                  </td>
                  <td class="px-4 py-3">
                    <div class="flex items-center gap-1">
                      <TrendingUp
                        v-if="index > 0 && item.reviews > monthlyTrend[index - 1].reviews"
                        class="size-4 text-green-500"
                      />
                      <TrendingDown
                        v-else-if="index > 0 && item.reviews < monthlyTrend[index - 1].reviews"
                        class="size-4 text-red-500"
                      />
                      <Minus v-else class="size-4 text-gray-400" />
                      <span
                        v-if="index > 0"
                        class="text-xs"
                        :class="
                          item.reviews > monthlyTrend[index - 1].reviews
                            ? 'text-green-500'
                            : item.reviews < monthlyTrend[index - 1].reviews
                              ? 'text-red-500'
                              : 'text-gray-500'
                        "
                      >
                        {{ item.reviews > monthlyTrend[index - 1].reviews ? '+' : '' }}{{ item.reviews - monthlyTrend[index - 1].reviews }}
                      </span>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </AppCard>
        <AppCard>
          <template #header>
            <h3 class="font-semibold text-gray-900">긍정 키워드</h3>
          </template>
          <div class="flex flex-wrap gap-2">
            <AppBadge
              v-for="keyword in ['친절', '전문적', '깔끔', '효과 좋음', '만족', '추천', '세심함', '상담', '자연스러움']"
              :key="keyword"
              color="success"
              variant="subtle"
              size="lg"
            >
              {{ keyword }}
            </AppBadge>
          </div>
        </AppCard>
        <AppCard>
          <template #header>
            <h3 class="font-semibold text-gray-900">개선 필요 키워드</h3>
          </template>
          <div class="flex flex-wrap gap-2">
            <AppBadge
              v-for="keyword in ['대기 시간', '가격', '주차', '예약']"
              :key="keyword"
              color="warning"
              variant="subtle"
              size="lg"
            >
              {{ keyword }}
            </AppBadge>
          </div>
        </AppCard>
      </div>
    </div>
  </PanelLayout>
</template>
