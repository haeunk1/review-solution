export type Platform = 'naver' | 'google' | 'kakao'
export type Sentiment = 'positive' | 'negative' | 'neutral'
export type ReplyStatus = 'pending' | 'approved' | 'posted'
export type ReplyStyle = 'formal' | 'friendly' | 'positive'
export type AlertSeverity = 'critical' | 'warning' | 'info'
export type ReportPeriod = '1m' | '3m' | '6m' | '1y'

// ────────── Review ──────────
export interface Review {
  id: string
  author: string
  rating: number
  content: string
  date: string
  replied: boolean
  replyContent?: string
  avatarUrl?: string
  platform?: Platform
  sentiment?: Sentiment
  keywords?: string[]
  isNegative?: boolean   // rating <= 2
  language?: string      // 'ko' | 'en' | 'zh' | 'ja' 등
}

export interface ReplyOption {
  id: string
  type: ReplyStyle
  label: string
}

export interface StatsData {
  label: string
  value: string | number
  change?: number
  icon: string
}

// ────────── Alert (부정 리뷰 위기 관리) ──────────
export interface ReviewAlert {
  id: string
  reviewId: string
  storeId: string
  severity: AlertSeverity
  platform: Platform
  author: string
  rating: number
  content: string
  date: string
  isRead: boolean
  isResolved: boolean
  suggestedReply?: string
  isBlacklist?: boolean   // 반복/악성 의심
  language?: string
}

// ────────── Competitor (경쟁사 모니터링) ──────────
export interface Competitor {
  id: string
  storeId: string
  name: string
  platform: Platform
  platformPlaceId: string
  address?: string
  avgRating?: number
  totalReviews?: number
  recentReviews?: CompetitorReview[]
  positiveKeywords?: string[]
  negativeKeywords?: string[]
  createdAt: string
}

export interface CompetitorReview {
  id: string
  competitorId: string
  platform: Platform
  author: string
  rating: number
  content: string
  date: string
  sentiment?: Sentiment
}

export interface CompetitorComparison {
  myStore: {
    name: string
    avgRating: number
    totalReviews: number
    positiveRate: number
    topKeywords: string[]
  }
  competitors: Array<{
    name: string
    avgRating: number
    totalReviews: number
    positiveRate: number
    topKeywords: string[]
  }>
}

// ────────── ReviewRequest (리뷰 요청) ──────────
export interface ReviewRequest {
  id: string
  storeId: string
  title: string
  message: string
  targetPlatform: Platform
  qrCodeUrl?: string
  shortUrl?: string
  createdAt: string
  clickCount: number
  reviewCount: number
}

export interface ReviewRequestCreate {
  title: string
  message: string
  targetPlatform: Platform
}

// ────────── Report (월간 리포트) ──────────
export interface MonthlyReport {
  id: string
  storeId: string
  period: string          // '2026-03' 형식
  totalReviews: number
  newReviews: number
  avgRating: number
  ratingChange: number    // 전월 대비
  positiveRate: number
  negativeRate: number
  neutralRate: number
  replyRate: number
  topPositiveKeywords: string[]
  topNegativeKeywords: string[]
  platformBreakdown: PlatformStat[]
  monthlyTrend: MonthlyTrendItem[]
  generatedAt: string
  pdfUrl?: string
}

export interface PlatformStat {
  platform: Platform
  count: number
  avgRating: number
  percentage: number
}

export interface MonthlyTrendItem {
  month: string
  count: number
  avgRating: number
}
