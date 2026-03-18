import apiClient from './client'
import type { Review } from '@/types/review'

// 백엔드 응답 원본 타입 (snake_case)
interface ReviewRaw {
  id: number
  hospital_id: string
  platform: string
  review_text: string
  rating: string | null
  visitor_name: string | null
  visited_date: string | null
  sentiment: string | null
  keywords: string | null  // JSON 문자열
  reply_text: string | null
  reply_status: string | null
  created_at: string
}

export function mapReview(r: ReviewRaw): Review {
  let keywords: string[] = []
  if (r.keywords) {
    try { keywords = JSON.parse(r.keywords) } catch { /* ignore */ }
  }
  return {
    id: String(r.id),
    author: r.visitor_name ?? '익명',
    rating: r.rating ? parseFloat(r.rating) : 0,
    content: r.review_text,
    date: r.created_at.split('T')[0],
    replied: r.reply_text !== null && r.reply_status !== 'pending',
    replyContent: r.reply_text ?? undefined,
    platform: r.platform as Review['platform'],
    sentiment: r.sentiment as Review['sentiment'],
    keywords,
  }
}

export const reviewsApi = {
  list: (hospitalId: string, params?: { platform?: string; reply_status?: string }) =>
    apiClient.get<ReviewRaw[]>('/reviews/', { params: { hospital_id: hospitalId, ...params } })
      .then(res => ({ ...res, data: res.data.map(mapReview) })),

  collect: (hospitalId: string) =>
    apiClient.post(`/reviews/collect/${hospitalId}`),

  generateReply: (reviewId: string, style?: string) =>
    apiClient.post<{ reply_text: string }>(`/replies/generate/${reviewId}`, { style }),

  submitReply: (reviewId: string, replyText: string) =>
    apiClient.post(`/replies/submit/${reviewId}`, { reply_text: replyText }),
}
