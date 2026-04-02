import apiClient from './client'
import type { MonthlyReport } from '@/types/review'

export const reportsApi = {
  /** 월간 리포트 목록 (최근 12개월) */
  list: (storeId: string) =>
    apiClient.get<MonthlyReport[]>('/reports/', { params: { store_id: storeId } }),

  /** 특정 월 리포트 조회 (period: '2026-03') */
  getByPeriod: (storeId: string, period: string) =>
    apiClient.get<MonthlyReport>(`/reports/${storeId}/${period}`),

  /** 리포트 수동 생성 (AI 분석) */
  generate: (storeId: string, period: string) =>
    apiClient.post<MonthlyReport>(`/reports/generate`, { store_id: storeId, period }),

  /** PDF 다운로드 URL 발급 */
  getPdfUrl: (reportId: string) =>
    apiClient.get<{ pdf_url: string; expires_at: string }>(`/reports/${reportId}/pdf`),

  /** 최신 리포트 1개 */
  getLatest: (storeId: string) =>
    apiClient.get<MonthlyReport>(`/reports/latest/${storeId}`),
}
