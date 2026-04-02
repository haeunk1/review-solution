<template>
  <div class="min-h-full p-6">
    <!-- 헤더 -->
    <div class="mb-6">
      <h1 class="text-xl font-bold text-gray-900">설정</h1>
      <p class="mt-1 text-sm text-gray-500">업장 정보, AI 설정, 플랫폼 연동을 관리하세요.</p>
    </div>

    <div class="mx-auto max-w-3xl space-y-6">

      <!-- ① 업장 기본 정보 -->
      <section class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-center gap-3">
          <div class="flex size-9 items-center justify-center rounded-xl bg-indigo-50">
            <Building2 class="size-4 text-indigo-600" />
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">업장 정보</h3>
            <p class="text-xs text-gray-400">기본 업장 프로필을 설정합니다</p>
          </div>
        </div>
        <div class="grid gap-4 sm:grid-cols-2">
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700">업장명</label>
            <AppInput v-model="form.name" placeholder="예) 맛있는 카페" />
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700">업종</label>
            <AppSelect v-model="form.businessType" :items="businessTypeOptions" value-key="value" class="w-full" />
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700">이메일</label>
            <AppInput v-model="form.email" type="email" placeholder="contact@example.com" />
          </div>
          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700">전화번호</label>
            <AppInput v-model="form.phone" type="tel" placeholder="02-1234-5678" />
          </div>
          <div class="sm:col-span-2">
            <label class="mb-1.5 block text-sm font-medium text-gray-700">업장 주소</label>
            <AppInput v-model="form.address" placeholder="서울시 강남구..." />
          </div>
        </div>
      </section>

      <!-- ② 리뷰 수집 설정 -->
      <section class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-center gap-3">
          <div class="flex size-9 items-center justify-center rounded-xl bg-green-50">
            <RefreshCw class="size-4 text-green-600" />
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">리뷰 수집 설정</h3>
            <p class="text-xs text-gray-400">자동 수집 주기 및 플랫폼을 설정합니다</p>
          </div>
        </div>
        <div class="space-y-4">
          <div class="grid gap-4 sm:grid-cols-2">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">수집 주기</label>
              <AppSelect v-model="form.crawlInterval" :items="crawlIntervalOptions" value-key="value" class="w-full" />
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">중복 감지 임계값</label>
              <AppSelect v-model="form.duplicateThreshold" :items="duplicateOptions" value-key="value" class="w-full" />
              <p class="mt-1 text-xs text-gray-400">연속 N개 중복 감지 시 수집 조기 종료</p>
            </div>
          </div>

          <!-- 플랫폼별 토글 -->
          <div class="rounded-xl border border-gray-100 bg-gray-50 divide-y divide-gray-100">
            <div v-for="platform in platforms" :key="platform.key" class="flex items-center justify-between px-4 py-3">
              <div class="flex items-center gap-3">
                <img :src="platform.logo" :alt="platform.name" class="size-5 rounded" />
                <div>
                  <p class="text-sm font-medium text-gray-900">{{ platform.name }}</p>
                  <p class="text-xs text-gray-400">{{ platform.idLabel }}: {{ form[platform.idField] || '미등록' }}</p>
                </div>
              </div>
              <AppSwitch v-model="form[platform.activeField]" />
            </div>
          </div>
        </div>
      </section>

      <!-- ③ 플랫폼 연동 -->
      <section class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-center gap-3">
          <div class="flex size-9 items-center justify-center rounded-xl bg-blue-50">
            <Link class="size-4 text-blue-600" />
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">플랫폼 연동</h3>
            <p class="text-xs text-gray-400">리뷰를 수집할 플랫폼 정보를 등록합니다</p>
          </div>
        </div>
        <div class="space-y-4">
          <!-- 구글 -->
          <div class="rounded-xl border border-gray-200 p-4">
            <div class="mb-3 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="flex size-8 items-center justify-center rounded-lg bg-white shadow-sm ring-1 ring-gray-200">
                  <span class="text-sm font-bold text-blue-500">G</span>
                </div>
                <div>
                  <p class="text-sm font-semibold text-gray-900">Google Maps</p>
                  <AppBadge :color="form.googlePlaceId ? 'success' : 'warning'" variant="subtle" size="sm">
                    {{ form.googlePlaceId ? '연동됨' : '미연동' }}
                  </AppBadge>
                </div>
              </div>
              <AppButton
                :label="form.googlePlaceId ? '재연동' : 'OAuth 연동'"
                color="neutral"
                variant="outline"
                size="sm"
                @click="connectGoogle"
              />
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium text-gray-600">Google Place ID</label>
              <AppInput v-model="form.googlePlaceId" placeholder="ChIJ..." size="sm" />
            </div>
          </div>

          <!-- 네이버 -->
          <div class="rounded-xl border border-gray-200 p-4">
            <div class="mb-3 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <div class="flex size-8 items-center justify-center rounded-lg bg-green-500 shadow-sm">
                  <span class="text-xs font-bold text-white">N</span>
                </div>
                <div>
                  <p class="text-sm font-semibold text-gray-900">네이버 플레이스</p>
                  <AppBadge :color="form.naverPlaceId ? 'success' : 'warning'" variant="subtle" size="sm">
                    {{ form.naverPlaceId ? '연동됨' : '미연동' }}
                  </AppBadge>
                </div>
              </div>
            </div>
            <div>
              <label class="mb-1 block text-xs font-medium text-gray-600">네이버 플레이스 ID</label>
              <AppInput v-model="form.naverPlaceId" placeholder="1234567890" size="sm" />
            </div>
          </div>
        </div>
      </section>

      <!-- ④ AI 답글 설정 -->
      <section class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-center gap-3">
          <div class="flex size-9 items-center justify-center rounded-xl bg-violet-50">
            <Sparkles class="size-4 text-violet-600" />
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">AI 답글 설정</h3>
            <p class="text-xs text-gray-400">답글 스타일 및 자동화 옵션을 설정합니다</p>
          </div>
        </div>
        <div class="space-y-5">
          <div class="flex items-center justify-between rounded-xl bg-gray-50 p-4">
            <div>
              <p class="text-sm font-semibold text-gray-900">자동 답글 초안 생성</p>
              <p class="text-xs text-gray-500">새 리뷰 수집 시 자동으로 AI 답글 초안을 생성합니다</p>
            </div>
            <AppSwitch v-model="form.autoReplyDraft" />
          </div>

          <div class="flex items-center justify-between rounded-xl bg-gray-50 p-4">
            <div>
              <p class="text-sm font-semibold text-gray-900">자동 게시 (별점 4~5점)</p>
              <p class="text-xs text-gray-500">긍정 리뷰는 AI 답글을 자동으로 게시합니다</p>
            </div>
            <AppSwitch v-model="form.autoPostPositive" />
          </div>

          <!-- 무드 & 컨셉 -->
          <div>
            <label class="mb-2 block text-sm font-semibold text-gray-900">답글 무드 & 컨셉</label>
            <p class="mb-3 text-xs text-gray-500">업장 이미지에 맞는 답글 톤을 선택하세요</p>
            <div class="grid grid-cols-2 gap-2 sm:grid-cols-3">
              <button
                v-for="mood in moodOptions"
                :key="mood.value"
                :class="[
                  'flex flex-col items-start gap-1 rounded-xl border p-3 text-left transition-all',
                  form.replyMood === mood.value
                    ? 'border-indigo-400 bg-indigo-50 ring-1 ring-indigo-400'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                ]"
                @click="form.replyMood = mood.value"
              >
                <span class="text-lg">{{ mood.emoji }}</span>
                <p class="text-xs font-semibold text-gray-800">{{ mood.label }}</p>
                <p class="text-[10px] text-gray-400 leading-tight">{{ mood.desc }}</p>
              </button>
            </div>
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700">답글 길이 제한</label>
            <AppSelect v-model="form.replyLength" :items="replyLengthOptions" value-key="value" class="w-full sm:w-64" />
          </div>

          <div>
            <label class="mb-1.5 block text-sm font-medium text-gray-700">업장 소개 (AI 프롬프트에 활용)</label>
            <AppTextarea v-model="form.storeDescription" placeholder="우리 업장의 특징, 강점, 고객에게 전하고 싶은 메시지를 입력하세요..." rows="3" />
          </div>
        </div>
      </section>

      <!-- ⑤ 알림 설정 -->
      <section class="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-center gap-3">
          <div class="flex size-9 items-center justify-center rounded-xl bg-orange-50">
            <Bell class="size-4 text-orange-600" />
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">알림 설정</h3>
            <p class="text-xs text-gray-400">중요 이벤트 알림을 설정합니다</p>
          </div>
        </div>
        <div class="divide-y divide-gray-100">
          <div v-for="notif in notifications" :key="notif.key" class="flex items-center justify-between py-3.5">
            <div>
              <p class="text-sm font-medium text-gray-900">{{ notif.label }}</p>
              <p class="text-xs text-gray-400">{{ notif.desc }}</p>
            </div>
            <AppSwitch v-model="form[notif.key]" />
          </div>
        </div>
      </section>

      <!-- 저장 버튼 -->
      <div class="flex justify-end gap-3 pb-8">
        <AppButton label="취소" color="neutral" variant="outline" @click="resetForm" />
        <AppButton label="변경사항 저장" icon="i-lucide-save" :loading="saving" @click="handleSave" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from '@/composables/useToast'
import { useHospital } from '@/composables/useHospital'
import AppInput from '@/components/ui/AppInput.vue'
import AppSelect from '@/components/ui/AppSelect.vue'
import AppSwitch from '@/components/ui/AppSwitch.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppTextarea from '@/components/ui/AppTextarea.vue'
import { Building2, RefreshCw, Link, Sparkles, Bell } from 'lucide-vue-next'

const toast = useToast()
const { hospitalName } = useHospital()
const saving = ref(false)

const form = ref({
  name: hospitalName.value,
  businessType: 'cafe',
  email: '',
  phone: '',
  address: '',
  crawlInterval: '6',
  duplicateThreshold: '5',
  googlePlaceId: '',
  naverPlaceId: '',
  naverActive: true,
  googleActive: true,
  autoReplyDraft: true,
  autoPostPositive: false,
  replyMood: 'friendly',
  replyLength: '100-200',
  storeDescription: '',
  notifyNewReview: true,
  notifyLowRating: true,
  notifyUnreplied: true,
  notifyCompetitor: false,
})

const businessTypeOptions = [
  { label: '카페', value: 'cafe' },
  { label: '음식점', value: 'restaurant' },
  { label: '피부과/성형외과', value: 'clinic_beauty' },
  { label: '치과', value: 'clinic_dental' },
  { label: '한의원', value: 'clinic_korean' },
  { label: '뷰티샵 (네일/헤어)', value: 'beauty' },
  { label: '숙박업체', value: 'accommodation' },
  { label: '기타', value: 'other' },
]

const crawlIntervalOptions = [
  { label: '1시간마다', value: '1' },
  { label: '3시간마다', value: '3' },
  { label: '6시간마다 (권장)', value: '6' },
  { label: '12시간마다', value: '12' },
  { label: '24시간마다', value: '24' },
]

const duplicateOptions = [
  { label: '3개 연속 중복', value: '3' },
  { label: '5개 연속 중복 (권장)', value: '5' },
  { label: '10개 연속 중복', value: '10' },
]

const replyLengthOptions = [
  { label: '짧게 (50~100자)', value: '50-100' },
  { label: '보통 (100~200자)', value: '100-200' },
  { label: '길게 (200~300자)', value: '200-300' },
]

const platforms = [
  { key: 'naver', name: '네이버 플레이스', logo: 'https://placehold.co/20x20/03c75a/ffffff?text=N', idLabel: 'Place ID', idField: 'naverPlaceId', activeField: 'naverActive' },
  { key: 'google', name: 'Google Maps', logo: 'https://placehold.co/20x20/4285f4/ffffff?text=G', idLabel: 'Place ID', idField: 'googlePlaceId', activeField: 'googleActive' },
]

const moodOptions = [
  { value: 'friendly', emoji: '😊', label: '친근한', desc: '따뜻하고 친근한 어조' },
  { value: 'professional', emoji: '💼', label: '전문적인', desc: '신뢰감 있는 전문 어조' },
  { value: 'luxury', emoji: '✨', label: '고급스러운', desc: '품위 있고 격조 있는 어조' },
  { value: 'cute', emoji: '🐾', label: '귀여운', desc: '발랄하고 밝은 어조' },
  { value: 'formal', emoji: '📋', label: '정중한', desc: '공손하고 격식 있는 어조' },
  { value: 'thankful', emoji: '🙏', label: '감사 중심', desc: '감사함을 강조하는 어조' },
]

const notifications = [
  { key: 'notifyNewReview', label: '새 리뷰 알림', desc: '새 리뷰가 등록되면 알림을 받습니다' },
  { key: 'notifyLowRating', label: '낮은 별점 즉시 알림', desc: '별점 2점 이하 리뷰 즉시 알림' },
  { key: 'notifyUnreplied', label: '미답변 리마인더', desc: '24시간 이상 미답변 리뷰 알림' },
  { key: 'notifyCompetitor', label: '경쟁사 신규 리뷰', desc: '등록된 경쟁사에 새 리뷰가 달리면 알림' },
]

function connectGoogle() {
  toast.add({ title: 'Google OAuth 연동은 준비 중입니다.', color: 'info' })
}

function resetForm() {
  toast.add({ title: '변경사항이 취소되었습니다.', color: 'neutral' })
}

async function handleSave() {
  saving.value = true
  try {
    await new Promise(r => setTimeout(r, 800)) // API 연동 예정
    toast.add({ title: '설정이 저장되었습니다.', color: 'success' })
  } finally {
    saving.value = false
  }
}
</script>
