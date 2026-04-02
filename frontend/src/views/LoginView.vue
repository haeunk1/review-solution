<template>
  <div class="flex min-h-screen bg-gradient-to-br from-indigo-950 via-indigo-900 to-violet-900">
    <!-- 배경 장식 -->
    <div class="pointer-events-none absolute inset-0 overflow-hidden">
      <div class="absolute -left-32 -top-32 size-96 rounded-full bg-indigo-500/10 blur-3xl" />
      <div class="absolute -bottom-32 -right-32 size-96 rounded-full bg-violet-500/10 blur-3xl" />
    </div>

    <div class="relative flex flex-1 flex-col items-center justify-center px-6 py-12">
      <!-- 헤드 -->
      <div class="mb-8 text-center">
        <div class="mx-auto mb-4 flex size-16 items-center justify-center rounded-2xl bg-white/10 backdrop-blur ring-1 ring-white/20">
          <Star class="size-8 text-white" />
        </div>
        <h1 class="text-3xl font-bold tracking-tight text-white">ReviewHub</h1>
        <p class="mt-2 text-sm text-indigo-300">AI 리뷰 통합 관리 플랫폼</p>
      </div>

      <!-- 카드 -->
      <div class="w-full max-w-sm rounded-2xl bg-white/10 p-8 shadow-2xl backdrop-blur ring-1 ring-white/20">
        <div class="mb-6">
          <h2 class="text-lg font-semibold text-white">대시보드 접속</h2>
          <p class="mt-1 text-sm text-indigo-300">업장 ID를 입력하여 접속하세요.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-indigo-200">업장 ID</label>
            <input
              v-model="inputId"
              type="text"
              placeholder="예) my_store_001"
              autocomplete="off"
              :class="[
                'w-full rounded-xl border px-4 py-2.5 text-sm outline-none transition-all',
                'bg-white/10 placeholder:text-indigo-400 text-white',
                error
                  ? 'border-red-400 focus:border-red-300 focus:ring-2 focus:ring-red-400/20'
                  : 'border-white/20 focus:border-indigo-300 focus:ring-2 focus:ring-indigo-400/20',
              ]"
              @input="error = ''"
            />
            <p v-if="error" class="mt-1.5 flex items-center gap-1 text-xs text-red-400">
              <AlertCircle class="size-3.5 shrink-0" />
              {{ error }}
            </p>
          </div>

          <button
            type="submit"
            :disabled="loading || !inputId.trim()"
            class="flex w-full items-center justify-center gap-2 rounded-xl bg-indigo-500 px-4 py-2.5 text-sm font-semibold text-white shadow-lg shadow-indigo-500/30 transition-all hover:bg-indigo-400 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-300 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <span v-if="loading" class="size-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
            <LogIn v-else class="size-4" />
            {{ loading ? '확인 중...' : '대시보드 접속' }}
          </button>
        </form>
      </div>

      <!-- 하단 안내 -->
      <p class="mt-6 text-center text-xs text-indigo-400">
        테스트 ID:
        <button class="font-mono font-medium text-indigo-200 underline-offset-2 hover:underline" @click="inputId = 'test_clinic_001'">
          test_clinic_001
        </button>
      </p>

      <!-- 기능 소개 -->
      <div class="mt-10 grid grid-cols-3 gap-4 text-center">
        <div v-for="feat in features" :key="feat.label" class="rounded-xl bg-white/5 p-3">
          <component :is="feat.icon" class="mx-auto mb-1.5 size-5 text-indigo-300" />
          <p class="text-xs text-indigo-200">{{ feat.label }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Star, LogIn, AlertCircle, MessageSquareText, BarChart3, Sparkles } from 'lucide-vue-next'
import { useHospital } from '@/composables/useHospital'
import { hospitalsApi } from '@/api/hospitals'
import axios from 'axios'

const router = useRouter()
const { login } = useHospital()

const inputId = ref('')
const loading = ref(false)
const error = ref('')

const features = [
  { icon: MessageSquareText, label: '리뷰 통합 수집' },
  { icon: Sparkles, label: 'AI 답글 생성' },
  { icon: BarChart3, label: '경쟁사 분석' },
]

async function handleLogin() {
  const id = inputId.value.trim()
  if (!id) return

  loading.value = true
  error.value = ''

  try {
    const { data } = await hospitalsApi.getById(id)
    login(data.hospital_id ?? data.store_id ?? id, data.name)
    router.push('/')
  } catch (err) {
    if (axios.isAxiosError(err) && err.response?.status === 404) {
      error.value = '등록되지 않은 업장 ID입니다.'
    } else {
      error.value = '서버에 연결할 수 없습니다. 백엔드를 확인해주세요.'
    }
  } finally {
    loading.value = false
  }
}
</script>
