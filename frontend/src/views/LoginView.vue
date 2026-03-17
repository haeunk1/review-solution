<template>
  <div class="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-50 via-white to-blue-50 px-4">
    <div class="w-full max-w-md">
      <!-- 로고 영역 -->
      <div class="mb-8 flex flex-col items-center gap-3 text-center">
        <div class="flex size-14 items-center justify-center rounded-2xl bg-primary shadow-lg">
          <HeartPulse class="size-7 text-primary-foreground" />
        </div>
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-gray-900">CareReply AI</h1>
          <p class="mt-1 text-sm text-gray-500">의료기관 리뷰 통합 관리 플랫폼</p>
        </div>
      </div>

      <!-- 카드 -->
      <div class="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl shadow-gray-100">
        <div class="mb-6">
          <h2 class="text-lg font-semibold text-gray-900">대시보드 접속</h2>
          <p class="mt-1 text-sm text-gray-500">병원 ID를 입력하여 접속하세요.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700">병원 ID</label>
            <input
              v-model="inputId"
              type="text"
              placeholder="예) test_clinic_001"
              autocomplete="off"
              :class="[
                'w-full rounded-lg border px-3.5 py-2.5 text-sm outline-none transition-all',
                'placeholder:text-gray-400',
                error
                  ? 'border-red-300 bg-red-50 focus:border-red-400 focus:ring-2 focus:ring-red-100'
                  : 'border-gray-300 bg-white focus:border-primary focus:ring-2 focus:ring-primary/10',
              ]"
              @input="error = ''"
            />
            <p v-if="error" class="mt-1.5 flex items-center gap-1 text-xs text-red-500">
              <AlertCircle class="size-3.5 shrink-0" />
              {{ error }}
            </p>
          </div>

          <button
            type="submit"
            :disabled="loading || !inputId.trim()"
            class="flex w-full items-center justify-center gap-2 rounded-lg bg-primary px-4 py-2.5 text-sm font-semibold text-primary-foreground shadow-sm transition-all hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/50 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <span v-if="loading" class="size-4 animate-spin rounded-full border-2 border-primary-foreground border-t-transparent" />
            <LogIn v-else class="size-4" />
            {{ loading ? '확인 중...' : '대시보드 접속' }}
          </button>
        </form>
      </div>

      <!-- 하단 안내 -->
      <p class="mt-6 text-center text-xs text-gray-400">
        테스트 ID:
        <button class="font-mono font-medium text-gray-600 underline-offset-2 hover:underline" @click="inputId = 'test_clinic_001'">
          test_clinic_001
        </button>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { HeartPulse, LogIn, AlertCircle } from 'lucide-vue-next'
import { useHospital } from '@/composables/useHospital'
import { hospitalsApi } from '@/api/hospitals'
import axios from 'axios'

const router = useRouter()
const { login } = useHospital()

const inputId = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  const id = inputId.value.trim()
  if (!id) return

  loading.value = true
  error.value = ''

  try {
    const { data } = await hospitalsApi.getById(id)
    login(data.hospital_id, data.name)
    router.push('/')
  } catch (err) {
    if (axios.isAxiosError(err) && err.response?.status === 404) {
      error.value = '등록되지 않은 병원 ID입니다.'
    } else {
      error.value = '서버에 연결할 수 없습니다. 백엔드 서버 상태를 확인해주세요.'
    }
  } finally {
    loading.value = false
  }
}
</script>
