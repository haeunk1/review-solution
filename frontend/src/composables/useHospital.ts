import { ref } from 'vue'
import router from '@/router'

const hospitalId = ref<string>(localStorage.getItem('hospital_id') ?? '')
const hospitalName = ref<string>(localStorage.getItem('hospital_name') ?? '')

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

export function useHospital() {
  const isLoggedIn = () => !!hospitalId.value

  const login = (id: string, name: string) => {
    hospitalId.value = id
    hospitalName.value = name
    localStorage.setItem('hospital_id', id)
    localStorage.setItem('hospital_name', name)
  }

  const logout = () => {
    hospitalId.value = ''
    hospitalName.value = ''
    localStorage.removeItem('hospital_id')
    localStorage.removeItem('hospital_name')
    router.push('/login')
  }

  return { hospitalId, hospitalName, isLoggedIn, login, logout }
}
