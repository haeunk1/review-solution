import apiClient from './client'
import type { ReviewAlert } from '@/types/review'

export const alertsApi = {
  /** 미해결 위기 알림 목록 */
  list: (storeId: string, params?: { severity?: string; isResolved?: boolean }) =>
    apiClient.get<ReviewAlert[]>('/alerts/', { params: { store_id: storeId, ...params } }),

  /** 알림 읽음 처리 */
  markRead: (alertId: string) =>
    apiClient.patch(`/alerts/${alertId}/read`),

  /** 알림 해결 처리 */
  resolve: (alertId: string) =>
    apiClient.patch(`/alerts/${alertId}/resolve`),

  /** AI 위기 대응 답글 생성 */
  generateCrisisReply: (alertId: string, style?: 'formal' | 'apologetic' | 'compensation') =>
    apiClient.post<{ reply_text: string }>(`/alerts/${alertId}/generate-reply`, { style }),

  /** 블랙컨슈머 의심 신고 */
  reportBlacklist: (alertId: string, reason: string) =>
    apiClient.post(`/alerts/${alertId}/blacklist`, { reason }),

  /** 알림 통계 (심각도별 카운트) */
  getStats: (storeId: string) =>
    apiClient.get<{ critical: number; warning: number; info: number; unread: number }>(
      `/alerts/stats/${storeId}`
    ),
}
