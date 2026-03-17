import { ref, computed } from 'vue'
import type { Review, StatsData } from '@/types/review'

export const useReviews = () => {
  const reviews = ref<Review[]>([
    {
      id: '1',
      author: '김**',
      rating: 5,
      content: '원장님이 정말 친절하시고 시술도 꼼꼼하게 해주셨어요. 피부 고민 상담도 자세히 해주셔서 너무 좋았습니다. 다음에 또 방문할 예정이에요!',
      date: '2026-03-12',
      replied: false,
      avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=kim',
    },
    {
      id: '2',
      author: '이**',
      rating: 4,
      content: '전반적으로 만족스러웠습니다. 대기 시간이 조금 길었지만 시술 결과는 좋았어요.',
      date: '2026-03-11',
      replied: true,
      replyContent: '소중한 리뷰 감사합니다. 대기 시간 개선을 위해 노력하겠습니다.',
      avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=lee',
    },
    {
      id: '3',
      author: '박**',
      rating: 5,
      content: '여드름 치료 받으러 왔는데 정말 효과가 좋아요! 직원분들도 친절하시고 청결해서 좋았습니다.',
      date: '2026-03-10',
      replied: false,
      avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=park',
    },
    {
      id: '4',
      author: '최**',
      rating: 3,
      content: '시술은 괜찮았는데 가격이 좀 비싼 것 같아요. 할인 이벤트가 있으면 좋겠습니다.',
      date: '2026-03-09',
      replied: false,
      avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=choi',
    },
    {
      id: '5',
      author: '정**',
      rating: 5,
      content: '리프팅 시술 받았는데 자연스럽고 만족스러워요. 상담부터 시술까지 전문적이었습니다.',
      date: '2026-03-08',
      replied: true,
      replyContent: '만족스러운 결과를 얻으셔서 기쁩니다. 앞으로도 최선을 다하겠습니다.',
      avatarUrl: 'https://api.dicebear.com/7.x/avataaars/svg?seed=jung',
    },
  ])

  const selectedReview = ref<Review | null>(null)

  const stats = computed<StatsData[]>(() => [
    { label: '평균 별점', value: '4.4', change: 0.2, icon: 'star' },
    { label: '총 리뷰 수', value: reviews.value.length, change: 12, icon: 'message-square' },
    {
      label: '답변율',
      value: `${Math.round((reviews.value.filter(r => r.replied).length / reviews.value.length) * 100)}%`,
      change: 5,
      icon: 'check-circle',
    },
    { label: '평균 답변 시간', value: '2.3시간', change: -0.5, icon: 'clock' },
  ])

  const unrepliedReviews = computed(() => reviews.value.filter(r => !r.replied))
  const repliedReviews = computed(() => reviews.value.filter(r => r.replied))

  const selectReview = (review: Review) => {
    selectedReview.value = review
  }

  const submitReply = (reviewId: string, replyContent: string) => {
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
    stats,
    unrepliedReviews,
    repliedReviews,
    selectReview,
    submitReply,
  }
}
