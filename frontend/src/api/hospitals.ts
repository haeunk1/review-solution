import apiClient from './client'

export interface HospitalInfo {
  hospital_id: string
  name: string
  category: string | null
  naver_place_id: string | null
  google_place_id: string | null
  gangnamunni_id: string | null
  crawl_interval_hours: number
  is_active: boolean
}

export const hospitalsApi = {
  getById: (hospitalId: string) =>
    apiClient.get<HospitalInfo>(`/hospitals/info/${hospitalId}`),
}
