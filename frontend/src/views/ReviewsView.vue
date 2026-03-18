<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useReviews } from '@/composables/useReviews'
import PanelLayout from '@/components/PanelLayout.vue'
import ReviewCard from '@/components/ReviewCard.vue'
import AIReplyPanel from '@/components/AIReplyPanel.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppSelect from '@/components/ui/AppSelect.vue'
import AppEmpty from '@/components/ui/AppEmpty.vue'

const { reviews, selectedReview, selectReview, submitReply, fetchReviews } = useReviews()
onMounted(fetchReviews)
const searchQuery = ref('')
const filterStatus = ref('all')
const filterRating = ref('all')
const sortOrder = ref('newest')

const statusOptions = [
  { label: '전체', value: 'all' },
  { label: '답변 대기', value: 'pending' },
  { label: '답변 완료', value: 'replied' },
]

const ratingOptions = [
  { label: '전체 별점', value: 'all' },
  { label: '5점', value: '5' },
  { label: '4점', value: '4' },
  { label: '3점', value: '3' },
  { label: '2점 이하', value: '2' },
]

const filteredReviews = computed(() => {
  return reviews.value.filter((review) => {
    const matchesSearch =
      review.content.includes(searchQuery.value) || review.author.includes(searchQuery.value)
    const matchesStatus =
      filterStatus.value === 'all' ||
      (filterStatus.value === 'pending' && !review.replied) ||
      (filterStatus.value === 'replied' && review.replied)
    const matchesRating =
      filterRating.value === 'all' ||
      (filterRating.value === '2' && review.rating <= 2) ||
      review.rating === Number(filterRating.value)
    return matchesSearch && matchesStatus && matchesRating
  })
})

const handleClose = () => {
  selectedReview.value = null
}
</script>

<template>
  <div class="flex flex-1">
    <PanelLayout title="리뷰 목록">
      <template #right>
        <AppButton icon="i-lucide-download" label="내보내기" color="neutral" variant="outline" size="sm" />
      </template>
      <template #toolbar>
        <div class="flex flex-wrap items-center gap-4">
          <AppInput v-model="searchQuery" icon="i-lucide-search" placeholder="리뷰 검색..." class="w-64" />
          <AppSelect v-model="filterStatus" :items="statusOptions" value-key="value" class="w-32" />
          <AppSelect v-model="filterRating" :items="ratingOptions" value-key="value" class="w-32" />
        </div>
      </template>
      <div class="p-6">
        <div class="mb-4 flex items-center justify-between">
          <p class="text-sm text-gray-500">총 {{ filteredReviews.length }}개의 리뷰</p>
          <AppSelect
            v-model="sortOrder"
            :items="[
              { label: '최신순', value: 'newest' },
              { label: '별점 높은순', value: 'rating-high' },
              { label: '별점 낮은순', value: 'rating-low' },
            ]"
            value-key="value"
            class="w-32"
          />
        </div>
        <div class="space-y-4">
          <ReviewCard
            v-for="review in filteredReviews"
            :key="review.id"
            :review="review"
            :selected="selectedReview?.id === review.id"
            @select="selectReview"
          />
        </div>
        <AppEmpty
          v-if="filteredReviews.length === 0"
          icon="i-lucide-search-x"
          title="검색 결과가 없습니다"
          description="다른 검색어나 필터를 시도해 보세요."
        />
      </div>
    </PanelLayout>
    <div v-if="selectedReview" class="w-[400px] shrink-0 border-l border-gray-200 bg-white">
      <AIReplyPanel :review="selectedReview" @submit="submitReply" @close="handleClose" />
    </div>
  </div>
</template>
