export type Platform = 'naver' | 'google' | 'gangnamunni'
export type Sentiment = 'positive' | 'negative' | 'neutral'
export type ReplyStatus = 'pending' | 'approved' | 'posted'
export type ReplyStyle = 'formal' | 'friendly' | 'positive'

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
}

export interface ReplyOption {
  id: string
  type: 'formal' | 'friendly' | 'positive'
  label: string
}

export interface StatsData {
  label: string
  value: string | number
  change?: number
  icon: string
}
