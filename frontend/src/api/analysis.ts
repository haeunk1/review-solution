import apiClient from './client'

export interface SentimentDist {
  positive: number
  negative: number
  neutral: number
  positive_pct: number
  negative_pct: number
  neutral_pct: number
}

export interface MonthlyTrend {
  month: string
  count: number
}

export interface AnalysisSummary {
  total_reviews: number
  analyzed_count: number
  reply_rate: number
  pending_count: number
  sentiment: SentimentDist
  top_positive_keywords: string[]
  top_negative_keywords: string[]
  monthly_trend: MonthlyTrend[]
}

export const analysisApi = {
  getSummary: (hospitalId: string) =>
    apiClient.get<AnalysisSummary>(`/analysis/summary/${hospitalId}`),

  runAnalysis: (hospitalId: string) =>
    apiClient.post<{ analyzed_count: number; message: string }>(`/analysis/run/${hospitalId}`),
}
