<template>
  <div class="min-h-full">
    <!-- 헤더 -->
    <div class="border-b border-gray-200 bg-white px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="flex items-center gap-2 text-xl font-bold text-gray-900">
            <QrCode class="size-5 text-indigo-600" />
            리뷰 요청
          </h1>
          <p class="mt-0.5 text-sm text-gray-500">QR 코드와 단축 URL로 고객에게 리뷰를 요청하세요.</p>
        </div>
        <AppButton
          icon="i-lucide-plus"
          label="새 캠페인 만들기"
          @click="showCreateModal = true"
        />
      </div>
    </div>

    <div class="p-6 space-y-6">

      <!-- 가이드 배너 -->
      <div class="rounded-2xl bg-gradient-to-r from-indigo-600 to-violet-600 p-5 text-white">
        <div class="flex items-start gap-4">
          <div class="flex size-10 shrink-0 items-center justify-center rounded-xl bg-white/20">
            <Lightbulb class="size-5 text-yellow-300" />
          </div>
          <div>
            <h3 class="font-semibold">리뷰 요청으로 평점을 높이세요</h3>
            <p class="mt-1 text-sm text-indigo-100">만족한 고객에게 리뷰 작성을 요청하면 평균 평점이 0.3~0.5점 상승합니다. QR 코드를 영수증, 테이블, 명함에 인쇄해 보세요.</p>
          </div>
        </div>
        <div class="mt-4 grid grid-cols-3 gap-3 text-center">
          <div class="rounded-xl bg-white/10 p-3">
            <p class="text-2xl font-bold">QR</p>
            <p class="text-xs text-indigo-200">코드 인쇄</p>
          </div>
          <div class="rounded-xl bg-white/10 p-3">
            <p class="text-2xl font-bold">URL</p>
            <p class="text-xs text-indigo-200">단축 링크</p>
          </div>
          <div class="rounded-xl bg-white/10 p-3">
            <p class="text-2xl font-bold">SMS</p>
            <p class="text-xs text-indigo-200">문자 발송</p>
          </div>
        </div>
      </div>

      <!-- 전체 통계 -->
      <div class="grid gap-3 sm:grid-cols-3">
        <div class="rounded-xl border border-gray-200 bg-white p-4">
          <p class="text-xs font-medium text-gray-500">총 캠페인</p>
          <p class="mt-1 text-2xl font-bold text-gray-900">{{ campaigns.length }}</p>
        </div>
        <div class="rounded-xl border border-gray-200 bg-white p-4">
          <p class="text-xs font-medium text-gray-500">총 클릭</p>
          <p class="mt-1 text-2xl font-bold text-indigo-600">{{ totalClicks }}</p>
        </div>
        <div class="rounded-xl border border-gray-200 bg-white p-4">
          <p class="text-xs font-medium text-gray-500">리뷰 전환</p>
          <p class="mt-1 text-2xl font-bold text-green-600">{{ totalReviews }}</p>
          <p class="text-xs text-gray-400">전환율 {{ conversionRate }}%</p>
        </div>
      </div>

      <!-- 캠페인 목록 -->
      <div>
        <h2 class="mb-3 font-semibold text-gray-900">캠페인 목록</h2>
        <div v-if="campaigns.length === 0" class="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-200 py-16">
          <QrCode class="mb-3 size-10 text-gray-300" />
          <p class="font-medium text-gray-500">아직 캠페인이 없습니다</p>
          <p class="mt-1 text-sm text-gray-400">상단의 버튼을 눌러 첫 캠페인을 만들어보세요.</p>
          <AppButton label="캠페인 만들기" class="mt-4" @click="showCreateModal = true" />
        </div>
        <div v-else class="grid gap-4 lg:grid-cols-2">
          <article
            v-for="campaign in campaigns"
            :key="campaign.id"
            class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm"
          >
            <div class="flex items-start justify-between gap-3">
              <div class="flex-1 min-w-0">
                <div class="mb-1 flex items-center gap-2">
                  <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold', platformBadge(campaign.targetPlatform)]">
                    {{ platformLabel(campaign.targetPlatform) }}
                  </span>
                  <h3 class="truncate text-sm font-semibold text-gray-900">{{ campaign.title }}</h3>
                </div>
                <p class="text-xs text-gray-500 line-clamp-2">{{ campaign.message }}</p>
                <p class="mt-1 text-[10px] text-gray-400">생성일 {{ campaign.createdAt }}</p>
              </div>

              <!-- QR 코드 프리뷰 -->
              <div class="flex size-16 shrink-0 items-center justify-center rounded-xl bg-gray-50 border border-gray-200">
                <div class="grid grid-cols-5 gap-0.5 p-1">
                  <div v-for="i in 25" :key="i"
                    :class="['size-2 rounded-sm', Math.random() > 0.5 ? 'bg-gray-800' : 'bg-gray-100']"
                  />
                </div>
              </div>
            </div>

            <!-- 통계 -->
            <div class="mt-4 grid grid-cols-3 gap-2 rounded-xl bg-gray-50 p-3 text-center">
              <div>
                <p class="text-base font-bold text-gray-900">{{ campaign.clickCount }}</p>
                <p class="text-[10px] text-gray-500">클릭</p>
              </div>
              <div>
                <p class="text-base font-bold text-green-600">{{ campaign.reviewCount }}</p>
                <p class="text-[10px] text-gray-500">리뷰 작성</p>
              </div>
              <div>
                <p class="text-base font-bold text-indigo-600">
                  {{ campaign.clickCount ? Math.round((campaign.reviewCount / campaign.clickCount) * 100) : 0 }}%
                </p>
                <p class="text-[10px] text-gray-500">전환율</p>
              </div>
            </div>

            <!-- 단축 URL -->
            <div class="mt-3 flex items-center gap-2 rounded-lg bg-gray-50 px-3 py-2">
              <Link class="size-3.5 shrink-0 text-gray-400" />
              <span class="flex-1 truncate text-xs font-mono text-gray-600">{{ campaign.shortUrl || 'rvhub.kr/' + campaign.id }}</span>
              <button class="text-indigo-600 hover:text-indigo-800" @click="copyUrl(campaign)">
                <Copy class="size-3.5" />
              </button>
            </div>

            <!-- 액션 -->
            <div class="mt-3 flex gap-2">
              <AppButton
                icon="i-lucide-download"
                label="QR 다운로드"
                size="sm"
                color="neutral"
                variant="outline"
                class="flex-1"
                @click="downloadQr(campaign)"
              />
              <AppButton
                icon="i-lucide-send"
                label="SMS 발송"
                size="sm"
                color="neutral"
                variant="outline"
                class="flex-1"
                @click="openSmsModal(campaign)"
              />
              <button
                class="flex size-8 items-center justify-center rounded-lg border border-gray-200 text-gray-400 hover:bg-red-50 hover:border-red-200 hover:text-red-500 transition-colors"
                @click="deleteCampaign(campaign.id)"
              >
                <Trash2 class="size-3.5" />
              </button>
            </div>
          </article>
        </div>
      </div>
    </div>

    <!-- 새 캠페인 만들기 모달 -->
    <Teleport to="body">
      <div v-if="showCreateModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showCreateModal = false" />
        <div class="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
          <div class="mb-5 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">새 캠페인 만들기</h2>
            <button @click="showCreateModal = false" class="rounded-lg p-1 text-gray-400 hover:bg-gray-100">
              <X class="size-5" />
            </button>
          </div>

          <div class="space-y-4">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">캠페인 제목</label>
              <AppInput v-model="newCampaign.title" placeholder="예) 봄 시즌 리뷰 이벤트" />
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">대상 플랫폼</label>
              <AppSelect v-model="newCampaign.targetPlatform" :items="platformOptions" value-key="value" class="w-full" />
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">요청 메시지</label>
              <AppTextarea
                v-model="newCampaign.message"
                placeholder="고객에게 보낼 메시지를 입력하세요. 예) 저희 가게를 방문해 주셔서 감사합니다! 리뷰를 남겨주시면 다음 방문 시 10% 할인 쿠폰을 드립니다."
                :rows="3"
              />
            </div>
          </div>

          <div class="mt-6 flex gap-3">
            <AppButton label="취소" color="neutral" variant="outline" class="flex-1" @click="showCreateModal = false" />
            <AppButton label="캠페인 생성" class="flex-1" :loading="creating" @click="handleCreate" />
          </div>
        </div>
      </div>
    </Teleport>

    <!-- SMS 발송 모달 -->
    <Teleport to="body">
      <div v-if="showSmsModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showSmsModal = false" />
        <div class="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
          <div class="mb-5 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">SMS 발송</h2>
            <button @click="showSmsModal = false" class="rounded-lg p-1 text-gray-400 hover:bg-gray-100">
              <X class="size-5" />
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">전화번호 입력</label>
              <AppInput v-model="smsPhone" placeholder="010-1234-5678" />
              <p class="mt-1 text-xs text-gray-400">쉼표로 여러 번호를 구분할 수 있습니다</p>
            </div>
            <div class="rounded-xl bg-gray-50 p-3">
              <p class="text-xs font-semibold text-gray-600 mb-1">발송 메시지 미리보기</p>
              <p class="text-xs text-gray-700">{{ selectedCampaign?.message }}<br /><br />리뷰 남기기: rvhub.kr/{{ selectedCampaign?.id }}</p>
            </div>
          </div>
          <div class="mt-6 flex gap-3">
            <AppButton label="취소" color="neutral" variant="outline" class="flex-1" @click="showSmsModal = false" />
            <AppButton label="발송" icon="i-lucide-send" class="flex-1" :loading="sendingSms" @click="handleSendSms" />
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useHospital } from '@/composables/useHospital'
import { useToast } from '@/composables/useToast'
import { reviewRequestsApi } from '@/api/requests'
import type { ReviewRequest } from '@/types/review'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppSelect from '@/components/ui/AppSelect.vue'
import AppTextarea from '@/components/ui/AppTextarea.vue'
import { QrCode, Link, Copy, Trash2, X, Lightbulb, Send } from 'lucide-vue-next'

const { hospitalId } = useHospital()
const { add: addToast } = useToast()

const campaigns = ref<ReviewRequest[]>([])
const showCreateModal = ref(false)
const showSmsModal = ref(false)
const creating = ref(false)
const sendingSms = ref(false)
const smsPhone = ref('')
const selectedCampaign = ref<ReviewRequest | null>(null)

const newCampaign = ref({ title: '', message: '', targetPlatform: 'google' })

const platformOptions = [
  { label: 'Google Maps', value: 'google' },
  { label: '네이버 플레이스', value: 'naver' },
  { label: '카카오맵', value: 'kakao' },
]

const totalClicks = computed(() => campaigns.value.reduce((s, c) => s + c.clickCount, 0))
const totalReviews = computed(() => campaigns.value.reduce((s, c) => s + c.reviewCount, 0))
const conversionRate = computed(() =>
  totalClicks.value ? Math.round((totalReviews.value / totalClicks.value) * 100) : 0
)

function platformLabel(p: string) {
  return { google: 'Google', naver: '네이버', kakao: '카카오' }[p] ?? p
}
function platformBadge(p: string) {
  return {
    google: 'bg-blue-100 text-blue-700',
    naver: 'bg-green-100 text-green-700',
    kakao: 'bg-yellow-100 text-yellow-700',
  }[p] ?? 'bg-gray-100 text-gray-700'
}

function copyUrl(c: ReviewRequest) {
  const url = c.shortUrl || `rvhub.kr/${c.id}`
  navigator.clipboard.writeText(url).catch(() => {})
  addToast({ title: 'URL이 복사되었습니다.', color: 'success' })
}

function downloadQr(c: ReviewRequest) {
  addToast({ title: `"${c.title}" QR 코드 다운로드 준비 중...`, color: 'info' })
}

function openSmsModal(c: ReviewRequest) {
  selectedCampaign.value = c
  showSmsModal.value = true
}

async function handleCreate() {
  if (!newCampaign.value.title || !newCampaign.value.message) {
    addToast({ title: '제목과 메시지를 입력해주세요.', color: 'error' })
    return
  }
  creating.value = true
  try {
    const { data } = await reviewRequestsApi.create(hospitalId.value, {
      title: newCampaign.value.title,
      message: newCampaign.value.message,
      targetPlatform: newCampaign.value.targetPlatform as any,
    })
    campaigns.value.unshift(data)
    addToast({ title: '캠페인이 생성되었습니다.', color: 'success' })
  } catch {
    // 더미 추가
    campaigns.value.unshift({
      id: Date.now().toString(),
      storeId: hospitalId.value,
      title: newCampaign.value.title,
      message: newCampaign.value.message,
      targetPlatform: newCampaign.value.targetPlatform as any,
      shortUrl: `rvhub.kr/${Math.random().toString(36).slice(2, 7)}`,
      createdAt: new Date().toISOString().split('T')[0],
      clickCount: 0,
      reviewCount: 0,
    })
    addToast({ title: '캠페인이 생성되었습니다. (로컬)', color: 'success' })
  } finally {
    creating.value = false
    showCreateModal.value = false
    newCampaign.value = { title: '', message: '', targetPlatform: 'google' }
  }
}

async function handleSendSms() {
  if (!smsPhone.value || !selectedCampaign.value) return
  sendingSms.value = true
  try {
    await reviewRequestsApi.sendSms(selectedCampaign.value.id, smsPhone.value.split(',').map(s => s.trim()))
    addToast({ title: 'SMS가 발송되었습니다.', color: 'success' })
  } catch {
    addToast({ title: 'SMS 발송은 준비 중입니다.', color: 'info' })
  } finally {
    sendingSms.value = false
    showSmsModal.value = false
    smsPhone.value = ''
  }
}

function deleteCampaign(id: string) {
  campaigns.value = campaigns.value.filter(c => c.id !== id)
  addToast({ title: '캠페인이 삭제되었습니다.', color: 'neutral' })
}

onMounted(async () => {
  try {
    const { data } = await reviewRequestsApi.list(hospitalId.value)
    campaigns.value = data
  } catch {
    // 더미 데이터
    campaigns.value = [
      {
        id: 'c1', storeId: hospitalId.value, title: '봄 시즌 리뷰 이벤트',
        message: '안녕하세요! 저희 가게를 방문해 주셔서 감사합니다. 솔직한 리뷰를 남겨주시면 다음 방문 시 음료 1잔을 드립니다.',
        targetPlatform: 'google',
        shortUrl: 'rvhub.kr/spring24',
        createdAt: '2026-03-15',
        clickCount: 142, reviewCount: 38,
      },
      {
        id: 'c2', storeId: hospitalId.value, title: '네이버 리뷰 요청',
        message: '네이버 플레이스에 리뷰를 남겨주세요! 여러분의 소중한 의견이 저희 성장에 큰 힘이 됩니다.',
        targetPlatform: 'naver',
        shortUrl: 'rvhub.kr/naver01',
        createdAt: '2026-02-28',
        clickCount: 89, reviewCount: 21,
      },
    ]
  }
})
</script>
