<template>
  <div class="min-h-full">
    <!-- 헤더 -->
    <div class="border-b border-gray-200 bg-white px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="flex items-center gap-2 text-xl font-bold text-gray-900">
            <Users class="size-5 text-indigo-600" />
            경쟁사 모니터링
          </h1>
          <p class="mt-0.5 text-sm text-gray-500">근처 경쟁 업체의 리뷰를 분석하고 우위를 파악하세요.</p>
        </div>
        <div class="flex items-center gap-2">
          <AppButton
            icon="i-lucide-refresh-cw"
            label="전체 수집"
            color="neutral"
            variant="outline"
            size="sm"
            :loading="collecting"
            @click="collectAll"
          />
          <AppButton
            icon="i-lucide-plus"
            label="경쟁사 추가"
            @click="showAddModal = true"
          />
        </div>
      </div>

      <!-- 탭 -->
      <div class="mt-4 flex gap-1">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          :class="[
            'rounded-lg px-3 py-1.5 text-sm font-medium transition-all',
            activeTab === tab.value ? 'bg-gray-900 text-white' : 'text-gray-500 hover:bg-gray-100'
          ]"
          @click="activeTab = tab.value"
        >{{ tab.label }}</button>
      </div>
    </div>

    <div class="p-6 space-y-6">

      <!-- 내 업장 vs 경쟁사 비교 요약 -->
      <div v-if="activeTab === 'overview'" class="space-y-5">

        <!-- 평점 비교 바 차트 -->
        <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
          <h3 class="mb-4 font-semibold text-gray-900">평균 평점 비교</h3>
          <div class="space-y-3">
            <!-- 내 업장 -->
            <div class="flex items-center gap-3">
              <div class="w-28 shrink-0 text-right">
                <span class="text-xs font-semibold text-indigo-700">내 업장</span>
              </div>
              <div class="flex-1">
                <div class="h-7 overflow-hidden rounded-lg bg-gray-100">
                  <div
                    class="flex h-full items-center justify-end rounded-lg bg-indigo-500 pr-2 text-xs font-bold text-white transition-all"
                    :style="{ width: (myStore.avgRating / 5 * 100) + '%' }"
                  >
                    {{ myStore.avgRating.toFixed(1) }} ★
                  </div>
                </div>
              </div>
              <span class="w-16 text-right text-xs text-gray-500">{{ myStore.totalReviews }}개 리뷰</span>
            </div>

            <!-- 경쟁사들 -->
            <div v-for="comp in competitors" :key="comp.id" class="flex items-center gap-3">
              <div class="w-28 shrink-0 text-right">
                <span class="text-xs font-medium text-gray-600 truncate block">{{ comp.name }}</span>
              </div>
              <div class="flex-1">
                <div class="h-7 overflow-hidden rounded-lg bg-gray-100">
                  <div
                    class="flex h-full items-center justify-end rounded-lg pr-2 text-xs font-bold text-white transition-all"
                    :class="(comp.avgRating ?? 0) >= myStore.avgRating ? 'bg-red-400' : 'bg-green-400'"
                    :style="{ width: ((comp.avgRating ?? 0) / 5 * 100) + '%' }"
                  >
                    {{ (comp.avgRating ?? 0).toFixed(1) }} ★
                  </div>
                </div>
              </div>
              <span class="w-16 text-right text-xs text-gray-500">{{ comp.totalReviews ?? 0 }}개</span>
            </div>
          </div>
        </div>

        <!-- 키워드 비교 -->
        <div class="grid gap-4 lg:grid-cols-2">
          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <h3 class="mb-3 font-semibold text-gray-900">내 업장 긍정 키워드</h3>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="kw in myStore.topKeywords"
                :key="kw"
                class="rounded-full bg-indigo-50 px-3 py-1 text-xs font-medium text-indigo-700 ring-1 ring-indigo-200"
              ># {{ kw }}</span>
            </div>
          </div>
          <div class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
            <h3 class="mb-3 font-semibold text-gray-900">경쟁사 주요 키워드</h3>
            <div class="space-y-2">
              <div v-for="comp in competitors.slice(0, 3)" :key="comp.id">
                <p class="mb-1 text-xs font-medium text-gray-600">{{ comp.name }}</p>
                <div class="flex flex-wrap gap-1">
                  <span
                    v-for="kw in (comp.positiveKeywords ?? []).slice(0, 4)"
                    :key="kw"
                    class="rounded-full bg-gray-100 px-2 py-0.5 text-[10px] font-medium text-gray-600"
                  ># {{ kw }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 인사이트 카드 -->
        <div class="grid gap-3 sm:grid-cols-3">
          <div
            v-for="insight in insights"
            :key="insight.title"
            :class="['rounded-2xl p-4 shadow-sm', insight.bg]"
          >
            <div class="mb-2 flex items-center gap-2">
              <component :is="insight.icon" :class="['size-4', insight.iconColor]" />
              <p :class="['text-xs font-semibold', insight.labelColor]">{{ insight.label }}</p>
            </div>
            <p :class="['text-sm font-semibold', insight.textColor]">{{ insight.title }}</p>
            <p :class="['mt-1 text-xs', insight.subColor]">{{ insight.desc }}</p>
          </div>
        </div>
      </div>

      <!-- 경쟁사 카드 목록 -->
      <div v-if="activeTab === 'list'" class="space-y-4">
        <div v-if="competitors.length === 0" class="flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-gray-200 py-16">
          <Users class="mb-3 size-10 text-gray-300" />
          <p class="font-medium text-gray-500">등록된 경쟁사가 없습니다</p>
          <AppButton label="경쟁사 추가" class="mt-4" @click="showAddModal = true" />
        </div>
        <div v-else class="grid gap-4 lg:grid-cols-2">
          <article
            v-for="comp in competitors"
            :key="comp.id"
            class="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm card-hover"
          >
            <div class="flex items-start justify-between">
              <div>
                <div class="mb-1 flex items-center gap-2">
                  <span :class="['rounded-full px-2 py-0.5 text-[10px] font-bold', platformBadge(comp.platform)]">
                    {{ platformLabel(comp.platform) }}
                  </span>
                  <h3 class="font-semibold text-gray-900">{{ comp.name }}</h3>
                </div>
                <p v-if="comp.address" class="text-xs text-gray-400">{{ comp.address }}</p>
              </div>
              <button
                class="rounded-lg p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-500 transition-colors"
                @click="removeCompetitor(comp.id)"
              >
                <Trash2 class="size-4" />
              </button>
            </div>

            <div class="mt-4 grid grid-cols-3 gap-2 rounded-xl bg-gray-50 p-3 text-center">
              <div>
                <div class="flex items-center justify-center gap-0.5">
                  <span class="text-base font-bold text-gray-900">{{ (comp.avgRating ?? 0).toFixed(1) }}</span>
                  <Star class="size-3 fill-yellow-400 text-yellow-400" />
                </div>
                <p class="text-[10px] text-gray-500">평균 평점</p>
              </div>
              <div>
                <p class="text-base font-bold text-gray-900">{{ comp.totalReviews ?? 0 }}</p>
                <p class="text-[10px] text-gray-500">총 리뷰</p>
              </div>
              <div>
                <p class="text-base font-bold"
                  :class="(comp.avgRating ?? 0) >= myStore.avgRating ? 'text-red-500' : 'text-green-500'"
                >
                  {{ (comp.avgRating ?? 0) >= myStore.avgRating ? '▲ 우위' : '▼ 열세' }}
                </p>
                <p class="text-[10px] text-gray-500">내 업장 대비</p>
              </div>
            </div>

            <!-- 최근 리뷰 -->
            <div v-if="(comp.recentReviews ?? []).length > 0" class="mt-3">
              <p class="mb-2 text-xs font-semibold text-gray-600">최근 리뷰</p>
              <div class="space-y-1.5">
                <div
                  v-for="rev in (comp.recentReviews ?? []).slice(0, 2)"
                  :key="rev.id"
                  class="rounded-lg bg-gray-50 px-3 py-2"
                >
                  <div class="flex items-center gap-2 mb-0.5">
                    <div class="flex gap-0.5">
                      <Star v-for="i in rev.rating" :key="i" class="size-2.5 fill-yellow-400 text-yellow-400" />
                    </div>
                    <span class="text-[10px] text-gray-400">{{ rev.date }}</span>
                  </div>
                  <p class="text-xs text-gray-600 line-clamp-2">{{ rev.content }}</p>
                </div>
              </div>
            </div>

            <AppButton
              icon="i-lucide-refresh-cw"
              label="리뷰 수집"
              size="sm"
              color="neutral"
              variant="outline"
              class="mt-3 w-full"
              @click="collectOne(comp.id)"
            />
          </article>
        </div>
      </div>
    </div>

    <!-- 경쟁사 추가 모달 -->
    <Teleport to="body">
      <div v-if="showAddModal" class="fixed inset-0 z-50 flex items-center justify-center p-4">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="showAddModal = false" />
        <div class="relative w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
          <div class="mb-5 flex items-center justify-between">
            <h2 class="text-lg font-semibold text-gray-900">경쟁사 추가</h2>
            <button @click="showAddModal = false" class="rounded-lg p-1 text-gray-400 hover:bg-gray-100">
              <X class="size-5" />
            </button>
          </div>
          <div class="space-y-4">
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">업체명</label>
              <AppInput v-model="newComp.name" placeholder="예) 옆집 카페" />
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">플랫폼</label>
              <AppSelect v-model="newComp.platform" :items="platformOptions" value-key="value" class="w-full" />
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">Place ID</label>
              <AppInput v-model="newComp.platformPlaceId" placeholder="플랫폼 Place ID 입력" />
              <p class="mt-1 text-xs text-gray-400">구글: ChIJ..., 네이버: 숫자로 된 플레이스 ID</p>
            </div>
            <div>
              <label class="mb-1.5 block text-sm font-medium text-gray-700">주소 (선택)</label>
              <AppInput v-model="newComp.address" placeholder="서울시 강남구..." />
            </div>
          </div>
          <div class="mt-6 flex gap-3">
            <AppButton label="취소" color="neutral" variant="outline" class="flex-1" @click="showAddModal = false" />
            <AppButton label="추가" class="flex-1" :loading="adding" @click="handleAdd" />
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
import { competitorsApi } from '@/api/competitors'
import type { Competitor, Platform } from '@/types/review'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppSelect from '@/components/ui/AppSelect.vue'
import { Users, Star, Trash2, X, TrendingUp, TrendingDown, Target } from 'lucide-vue-next'

const { hospitalId } = useHospital()
const { add: addToast } = useToast()

const competitors = ref<Competitor[]>([])
const activeTab = ref('overview')
const showAddModal = ref(false)
const collecting = ref(false)
const adding = ref(false)

const tabs = [
  { label: '비교 개요', value: 'overview' },
  { label: '경쟁사 목록', value: 'list' },
]

const platformOptions = [
  { label: 'Google Maps', value: 'google' },
  { label: '네이버 플레이스', value: 'naver' },
]

const newComp = ref({ name: '', platform: 'google', platformPlaceId: '', address: '' })

const myStore = ref({
  name: '내 업장',
  avgRating: 4.4,
  totalReviews: 215,
  positiveRate: 78,
  topKeywords: ['친절', '맛있음', '분위기', '청결', '재방문'],
})

const insights = computed(() => {
  const higher = competitors.value.filter(c => (c.avgRating ?? 0) > myStore.value.avgRating)
  const lower = competitors.value.filter(c => (c.avgRating ?? 0) < myStore.value.avgRating)
  return [
    {
      icon: TrendingUp, label: '강점',
      title: `경쟁사 ${lower.length}곳 대비 우위`,
      desc: '평균 평점이 더 높습니다',
      bg: 'bg-green-50 border border-green-200',
      iconColor: 'text-green-600', labelColor: 'text-green-700',
      textColor: 'text-green-800', subColor: 'text-green-600',
    },
    {
      icon: TrendingDown, label: '개선 필요',
      title: `경쟁사 ${higher.length}곳에 뒤처짐`,
      desc: '집중 개선이 필요합니다',
      bg: 'bg-red-50 border border-red-200',
      iconColor: 'text-red-500', labelColor: 'text-red-600',
      textColor: 'text-red-700', subColor: 'text-red-500',
    },
    {
      icon: Target, label: '목표',
      title: `리뷰 ${myStore.value.totalReviews + 50}개 달성`,
      desc: '리뷰 요청으로 수를 늘리세요',
      bg: 'bg-indigo-50 border border-indigo-200',
      iconColor: 'text-indigo-600', labelColor: 'text-indigo-700',
      textColor: 'text-indigo-800', subColor: 'text-indigo-600',
    },
  ]
})

function platformLabel(p: Platform) {
  return { naver: '네이버', google: '구글', kakao: '카카오' }[p]
}
function platformBadge(p: Platform) {
  return {
    google: 'bg-blue-100 text-blue-700',
    naver: 'bg-green-100 text-green-700',
    kakao: 'bg-yellow-100 text-yellow-700',
  }[p]
}

async function collectAll() {
  collecting.value = true
  try {
    await competitorsApi.collectAll(hospitalId.value)
    addToast({ title: '경쟁사 리뷰 수집 완료', color: 'success' })
  } catch {
    addToast({ title: '수집 완료 (더미)', color: 'info' })
  } finally {
    collecting.value = false
  }
}

async function collectOne(id: string) {
  try {
    await competitorsApi.collect(id)
    addToast({ title: '리뷰 수집 완료', color: 'success' })
  } catch {
    addToast({ title: '수집 완료 (더미)', color: 'info' })
  }
}

async function removeCompetitor(id: string) {
  try {
    await competitorsApi.remove(id)
  } catch { /* ignore */ }
  competitors.value = competitors.value.filter(c => c.id !== id)
  addToast({ title: '경쟁사가 삭제되었습니다.', color: 'neutral' })
}

async function handleAdd() {
  if (!newComp.value.name || !newComp.value.platformPlaceId) {
    addToast({ title: '업체명과 Place ID를 입력해주세요.', color: 'error' })
    return
  }
  adding.value = true
  try {
    const { data } = await competitorsApi.create(hospitalId.value, {
      name: newComp.value.name,
      platform: newComp.value.platform,
      platform_place_id: newComp.value.platformPlaceId,
      address: newComp.value.address,
    })
    competitors.value.push(data)
    addToast({ title: '경쟁사가 추가되었습니다.', color: 'success' })
  } catch {
    competitors.value.push({
      id: Date.now().toString(),
      storeId: hospitalId.value,
      name: newComp.value.name,
      platform: newComp.value.platform as Platform,
      platformPlaceId: newComp.value.platformPlaceId,
      address: newComp.value.address,
      avgRating: 3.5 + Math.random() * 1.5,
      totalReviews: Math.floor(Math.random() * 200) + 50,
      positiveKeywords: ['친절', '맛있음', '분위기'],
      negativeKeywords: ['주차', '가격'],
      recentReviews: [],
      createdAt: new Date().toISOString().split('T')[0],
    })
    addToast({ title: '경쟁사가 추가되었습니다. (로컬)', color: 'success' })
  } finally {
    adding.value = false
    showAddModal.value = false
    newComp.value = { name: '', platform: 'google', platformPlaceId: '', address: '' }
  }
}

onMounted(async () => {
  try {
    const { data } = await competitorsApi.list(hospitalId.value)
    competitors.value = data
  } catch {
    // 더미 데이터
    competitors.value = [
      {
        id: '1', storeId: hospitalId.value, name: '근처 카페 A',
        platform: 'google', platformPlaceId: 'ChIJabc',
        address: '서울시 강남구 역삼동',
        avgRating: 4.6, totalReviews: 312,
        positiveKeywords: ['커피', '분위기', '인테리어', '직원', '빠름'],
        negativeKeywords: ['가격', '소음'],
        recentReviews: [
          { id: 'r1', competitorId: '1', platform: 'google', author: '김*수', rating: 5, content: '분위기 너무 좋아요! 커피도 맛있고 직원분들도 친절합니다.', date: '2026-04-01' },
          { id: 'r2', competitorId: '1', platform: 'google', author: '이*진', rating: 4, content: '인테리어가 예뻐서 자주 오게 됩니다.', date: '2026-03-30' },
        ],
        createdAt: '2026-03-01',
      },
      {
        id: '2', storeId: hospitalId.value, name: '스타벅스 역삼점',
        platform: 'naver', platformPlaceId: '1234567',
        address: '서울시 강남구 역삼동 825',
        avgRating: 4.2, totalReviews: 1240,
        positiveKeywords: ['편의성', '와이파이', '브랜드', '다양한 메뉴'],
        negativeKeywords: ['가격', '줄', '자리'],
        recentReviews: [],
        createdAt: '2026-03-01',
      },
      {
        id: '3', storeId: hospitalId.value, name: '카페 블루밍',
        platform: 'naver', platformPlaceId: '7654321',
        address: '서울시 강남구 테헤란로',
        avgRating: 3.9, totalReviews: 87,
        positiveKeywords: ['조용함', '뷰'],
        negativeKeywords: ['서비스', '가격', '느림'],
        recentReviews: [],
        createdAt: '2026-03-01',
      },
    ]
  }
})
</script>
