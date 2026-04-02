import apiClient from './client'
import type { Competitor, CompetitorComparison, CompetitorReview } from '@/types/review'

export const competitorsApi = {
  /** 등록된 경쟁사 목록 */
  list: (storeId: string) =>
    apiClient.get<Competitor[]>('/competitors/', { params: { store_id: storeId } }),

  /** 경쟁사 등록 */
  create: (storeId: string, data: { name: string; platform: string; platform_place_id: string; address?: string }) =>
    apiClient.post<Competitor>('/competitors/', { store_id: storeId, ...data }),

  /** 경쟁사 삭제 */
  remove: (competitorId: string) =>
    apiClient.delete(`/competitors/${competitorId}`),

  /** 경쟁사 리뷰 수집 (수동 트리거) */
  collect: (competitorId: string) =>
    apiClient.post(`/competitors/${competitorId}/collect`),

  /** 경쟁사 최근 리뷰 */
  getReviews: (competitorId: string, limit = 10) =>
    apiClient.get<CompetitorReview[]>(`/competitors/${competitorId}/reviews`, { params: { limit } }),

  /** 내 업장 vs 경쟁사 비교 분석 */
  getComparison: (storeId: string) =>
    apiClient.get<CompetitorComparison>(`/competitors/comparison/${storeId}`),

  /** 모든 경쟁사 일괄 수집 */
  collectAll: (storeId: string) =>
    apiClient.post(`/competitors/collect-all/${storeId}`),
}
