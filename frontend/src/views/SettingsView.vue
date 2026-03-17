<script setup lang="ts">
import { ref } from 'vue'
import { useToast } from '@/composables/useToast'
import PanelLayout from '@/components/PanelLayout.vue'
import AppCard from '@/components/ui/AppCard.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppInput from '@/components/ui/AppInput.vue'
import AppSelect from '@/components/ui/AppSelect.vue'
import AppSwitch from '@/components/ui/AppSwitch.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import AppSeparator from '@/components/ui/AppSeparator.vue'
import { Building2, Sparkles, Bell, Link } from 'lucide-vue-next'

const toast = useToast()
const clinicName = ref('청담피부과의원')
const email = ref('contact@cheongdam-derm.com')
const phone = ref('02-1234-5678')
const autoReply = ref(true)
const replyTone = ref('formal')
const notifyNewReview = ref(true)
const notifyLowRating = ref(true)

const toneOptions = [
  { label: '공손한 톤', value: 'formal' },
  { label: '친근한 톤', value: 'friendly' },
  { label: '전문적인 톤', value: 'professional' },
]

const handleSave = () => {
  toast.add({ title: '설정이 저장되었습니다', color: 'success' })
}
</script>

<template>
  <PanelLayout title="설정">
    <div class="mx-auto max-w-2xl p-6">
      <AppCard class="mb-6">
        <template #header>
          <div class="flex items-center gap-2">
            <Building2 class="size-5 text-blue-600" />
            <h3 class="font-semibold text-gray-900">병원 정보</h3>
          </div>
        </template>
        <div class="space-y-4">
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900">병원명</label>
            <AppInput v-model="clinicName" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900">이메일</label>
            <AppInput v-model="email" type="email" />
          </div>
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900">전화번호</label>
            <AppInput v-model="phone" type="tel" />
          </div>
        </div>
      </AppCard>
      <AppCard class="mb-6">
        <template #header>
          <div class="flex items-center gap-2">
            <Sparkles class="size-5 text-blue-600" />
            <h3 class="font-semibold text-gray-900">AI 답글 설정</h3>
          </div>
        </template>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-900">자동 답글 생성</p>
              <p class="text-sm text-gray-500">새 리뷰가 등록되면 자동으로 AI 답글을 생성합니다</p>
            </div>
            <AppSwitch v-model="autoReply" />
          </div>
          <AppSeparator />
          <div>
            <label class="mb-2 block text-sm font-medium text-gray-900">답글 톤</label>
            <AppSelect v-model="replyTone" :items="toneOptions" value-key="value" class="w-full" />
          </div>
        </div>
      </AppCard>
      <AppCard class="mb-6">
        <template #header>
          <div class="flex items-center gap-2">
            <Bell class="size-5 text-blue-600" />
            <h3 class="font-semibold text-gray-900">알림 설정</h3>
          </div>
        </template>
        <div class="space-y-4">
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-900">새 리뷰 알림</p>
              <p class="text-sm text-gray-500">새 리뷰가 등록되면 알림을 받습니다</p>
            </div>
            <AppSwitch v-model="notifyNewReview" />
          </div>
          <AppSeparator />
          <div class="flex items-center justify-between">
            <div>
              <p class="font-medium text-gray-900">낮은 별점 알림</p>
              <p class="text-sm text-gray-500">3점 이하 리뷰가 등록되면 즉시 알림을 받습니다</p>
            </div>
            <AppSwitch v-model="notifyLowRating" />
          </div>
        </div>
      </AppCard>
      <AppCard class="mb-6">
        <template #header>
          <div class="flex items-center gap-2">
            <Link class="size-5 text-blue-600" />
            <h3 class="font-semibold text-gray-900">Google 비즈니스 연동</h3>
          </div>
        </template>
        <div class="flex items-center justify-between">
          <div>
            <div class="flex items-center gap-2">
              <AppBadge color="success" variant="subtle">연동됨</AppBadge>
              <span class="text-sm text-gray-500">청담피부과의원</span>
            </div>
            <p class="mt-1 text-xs text-gray-500">마지막 동기화: 2026년 3월 14일 오전 10:30</p>
          </div>
          <AppButton label="재연동" color="neutral" variant="outline" size="sm" />
        </div>
      </AppCard>
      <div class="flex justify-end">
        <AppButton label="설정 저장" icon="i-lucide-save" @click="handleSave" />
      </div>
    </div>
  </PanelLayout>
</template>
