export interface Review {
  id: string
  author: string
  rating: number
  content: string
  date: string
  replied: boolean
  replyContent?: string
  avatarUrl?: string
}

export interface ReplyOption {
  id: string
  type: 'thank' | 'inform' | 'inquiry'
  label: string
  content: string
}

export interface StatsData {
  label: string
  value: string | number
  change?: number
  icon: string
}
