import apiClient from './client'
import type { ReviewRequest, ReviewRequestCreate } from '@/types/review'

export const reviewRequestsApi = {
  /** 리뷰 요청 캠페인 목록 */
  list: (storeId: string) =>
    apiClient.get<ReviewRequest[]>('/review-requests/', { params: { store_id: storeId } }),

  /** 새 캠페인 생성 (QR + 단축 URL 자동 발급) */
  create: (storeId: string, data: ReviewRequestCreate) =>
    apiClient.post<ReviewRequest>('/review-requests/', { store_id: storeId, ...data }),

  /** 캠페인 삭제 */
  remove: (requestId: string) =>
    apiClient.delete(`/review-requests/${requestId}`),

  /** QR 코드 이미지 URL */
  getQrImage: (requestId: string) =>
    apiClient.get<{ qr_url: string }>(`/review-requests/${requestId}/qr`),

  /** 단축 URL 재발급 */
  regenerateUrl: (requestId: string) =>
    apiClient.post<{ short_url: string }>(`/review-requests/${requestId}/regenerate-url`),

  /** SMS/카카오 알림톡 발송 */
  sendSms: (requestId: string, phones: string[]) =>
    apiClient.post(`/review-requests/${requestId}/send-sms`, { phones }),

  /** 클릭/전환 통계 */
  getStats: (requestId: string) =>
    apiClient.get<{ clicks: number; reviews: number; conversion_rate: number }>(
      `/review-requests/${requestId}/stats`
    ),
}
