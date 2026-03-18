import { ref, computed, onMounted } from 'vue'
import type { Review } from '@/types/review'
import { reviewsApi } from '@/api/reviews'
import { useHospital } from '@/composables/useHospital'

const reviews = ref<Review[]>([])
const selectedReview = ref<Review | null>(null)
const loading = ref(false)

export function useReviews() {
  const { hospitalId } = useHospital()

  async function fetchReviews() {
    if (!hospitalId.value) return
    loading.value = true
    try {
      const { data } = await reviewsApi.list(hospitalId.value)
      reviews.value = data
    } finally {
      loading.value = false
    }
  }

  const unrepliedReviews = computed(() => reviews.value.filter(r => !r.replied))
  const repliedReviews = computed(() => reviews.value.filter(r => r.replied))

  const selectReview = (review: Review) => {
    selectedReview.value = review
  }

  const submitReply = async (reviewId: string, replyContent: string) => {
    await reviewsApi.submitReply(reviewId, replyContent)
    const review = reviews.value.find(r => r.id === reviewId)
    if (review) {
      review.replied = true
      review.replyContent = replyContent
    }
    selectedReview.value = null
  }

  return {
    reviews,
    selectedReview,
    loading,
    unrepliedReviews,
    repliedReviews,
    selectReview,
    submitReply,
    fetchReviews,
  }
}
