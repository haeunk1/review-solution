<script setup lang="ts">
import { ref } from 'vue'
import { useReviews } from '@/composables/useReviews'
import { useHospital } from '@/composables/useHospital'
import { useToast } from '@/composables/useToast'
import { reviewsApi } from '@/api/reviews'
import PanelLayout from '@/components/PanelLayout.vue'
import StatsCard from '@/components/StatsCard.vue'
import ReviewCard from '@/components/ReviewCard.vue'
import AIReplyPanel from '@/components/AIReplyPanel.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppEmpty from '@/components/ui/AppEmpty.vue'

const { reviews, selectedReview, stats, unrepliedReviews, selectReview, submitReply } = useReviews()
const { hospitalId } = useHospital()
const { add: addToast } = useToast()

const collecting = ref(false)

const handleClose = () => {
  selectedReview.value = null
}

async function fetchNewReviews() {
  collecting.value = true
  try {
    await reviewsApi.collect(hospitalId.value)
    addToast({ title: '리뷰 수집이 완료되었습니다.', color: 'success' })
  } catch {
    addToast({ title: '리뷰 수집에 실패했습니다.', color: 'error' })
  } finally {
    collecting.value = false
  }
}
</script>

<template>
  <div class="flex flex-1">
    <PanelLayout title="대시보드">
      <template #right>
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
      <div class="p-6">
        <div class="mb-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <StatsCard v-for="stat in stats" :key="stat.label" :stat="stat" />
        </div>
        <div class="mb-6">
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">
              답변 대기 리뷰
              <AppBadge color="warning" variant="subtle" size="sm" class="ml-2">
                {{ unrepliedReviews.length }}
              </AppBadge>
            </h2>
            <router-link to="/reviews">
              <AppButton label="전체 보기" variant="ghost" trailing-icon="i-lucide-arrow-right" size="sm" />
            </router-link>
          </div>
          <div class="grid gap-4 lg:grid-cols-2">
            <ReviewCard
              v-for="review in unrepliedReviews.slice(0, 4)"
              :key="review.id"
              :review="review"
              :selected="selectedReview?.id === review.id"
              @select="selectReview"
            />
          </div>
          <AppEmpty
            v-if="unrepliedReviews.length === 0"
            icon="i-lucide-check-circle"
            title="모든 리뷰에 답변 완료"
            description="현재 답변 대기 중인 리뷰가 없습니다."
          />
        </div>
        <div>
          <div class="mb-4 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">최근 리뷰</h2>
          </div>
          <div class="grid gap-4 lg:grid-cols-2">
            <ReviewCard
              v-for="review in reviews.slice(0, 4)"
              :key="review.id"
              :review="review"
              :selected="selectedReview?.id === review.id"
              @select="selectReview"
            />
          </div>
        </div>
      </div>
    </PanelLayout>
    <div
      v-if="selectedReview"
      class="w-[400px] shrink-0 border-l border-gray-200 bg-white"
    >
      <AIReplyPanel
        :review="selectedReview"
        @submit="submitReply"
        @close="handleClose"
      />
    </div>
  </div>
</template>
