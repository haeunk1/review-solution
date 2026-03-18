<script setup lang="ts">
import { ref, watch } from 'vue'
import type { Review, ReplyOption } from '@/types/review'
import AppButton from '@/components/ui/AppButton.vue'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import AppTextarea from '@/components/ui/AppTextarea.vue'
import { Star } from 'lucide-vue-next'
import { useToast } from '@/composables/useToast'
import { reviewsApi } from '@/api/reviews'

const props = defineProps<{ review: Review }>()
const emit = defineEmits<{ submit: [reviewId: string, content: string]; close: [] }>()
const toast = useToast()

const styleOptions: ReplyOption[] = [
  { id: 'friendly', type: 'friendly', label: '친근한' },
  { id: 'formal', type: 'formal', label: '정중한' },
  { id: 'positive', type: 'positive', label: '긍정적' },
]

function defaultStyle(sentiment?: string): ReplyOption {
  if (sentiment === 'negative') return styleOptions[1]  // formal
  if (sentiment === 'positive') return styleOptions[2]  // positive
  return styleOptions[0]  // friendly
}

const selectedStyle = ref<ReplyOption>(defaultStyle(props.review.sentiment))
const editedContent = ref('')
const isGenerating = ref(false)

watch(
  () => props.review,
  () => {
    selectedStyle.value = defaultStyle(props.review.sentiment)
    editedContent.value = ''
  },
  { immediate: false },
)

async function generate() {
  isGenerating.value = true
  try {
    const { data } = await reviewsApi.generateReply(props.review.id, selectedStyle.value.type)
    editedContent.value = data.reply_text
  } catch {
    toast.add({ title: 'AI 답글 생성에 실패했습니다.', color: 'error' })
  } finally {
    isGenerating.value = false
  }
}

// 패널이 열릴 때 자동으로 AI 답글 생성
if (!props.review.replied) {
  generate()
}

const handleSubmit = async () => {
  emit('submit', props.review.id, editedContent.value)
  toast.add({ title: '답글이 등록되었습니다', color: 'success' })
  emit('close')
}
</script>

<template>
  <div class="flex h-full flex-col">
    <div class="flex items-center justify-between border-b border-gray-200 p-4">
      <h3 class="text-lg font-semibold text-gray-900">AI 답글 추천</h3>
      <AppButton icon="i-lucide-x" color="neutral" variant="ghost" size="sm" @click="emit('close')" />
    </div>
    <div class="flex-1 overflow-auto p-4">
      <!-- 원본 리뷰 -->
      <div class="mb-6 rounded-lg bg-gray-100 p-4">
        <div class="mb-2 flex items-center gap-3">
          <AppAvatar :src="review.avatarUrl" :alt="review.author" size="sm" />
          <div>
            <span class="font-medium text-gray-900">{{ review.author }}</span>
            <div v-if="review.platform" class="text-xs text-gray-400">{{ review.platform }}</div>
            <div class="flex items-center gap-1">
              <Star
                v-for="i in 5"
                :key="i"
                class="size-3"
                :class="i <= review.rating ? 'text-yellow-400' : 'text-gray-300'"
              />
            </div>
          </div>
        </div>
        <p class="text-sm text-gray-700">{{ review.content }}</p>
        <!-- 감성 태그 -->
        <div v-if="review.sentiment" class="mt-2">
          <span
            class="inline-block rounded-full px-2 py-0.5 text-xs font-medium"
            :class="{
              'bg-green-100 text-green-700': review.sentiment === 'positive',
              'bg-red-100 text-red-600': review.sentiment === 'negative',
              'bg-gray-100 text-gray-500': review.sentiment === 'neutral',
            }"
          >
            {{ review.sentiment === 'positive' ? '긍정' : review.sentiment === 'negative' ? '부정' : '중립' }}
          </span>
        </div>
      </div>

      <!-- 답글 스타일 선택 -->
      <div class="mb-4">
        <label class="mb-2 block text-sm font-medium text-gray-900">답글 스타일</label>
        <div class="flex gap-2">
          <AppButton
            v-for="opt in styleOptions"
            :key="opt.id"
            :label="opt.label"
            :color="selectedStyle.id === opt.id ? 'primary' : 'neutral'"
            :variant="selectedStyle.id === opt.id ? 'solid' : 'outline'"
            size="sm"
            @click="selectedStyle = opt; generate()"
          />
        </div>
      </div>

      <!-- AI 생성 답글 -->
      <div class="mb-4">
        <div class="mb-2 flex items-center justify-between">
          <label class="text-sm font-medium text-gray-900">AI 생성 답글</label>
          <AppButton
            icon="i-lucide-refresh-cw"
            label="재생성"
            color="neutral"
            variant="ghost"
            size="xs"
            :loading="isGenerating"
            @click="generate"
          />
        </div>
        <div v-if="isGenerating" class="flex h-32 items-center justify-center rounded-lg border border-gray-200 bg-gray-50 text-sm text-gray-400">
          AI가 답글을 생성 중입니다...
        </div>
        <AppTextarea v-else v-model="editedContent" :rows="6" class="w-full" />
      </div>
      <div class="mb-4 text-right text-xs text-gray-500">{{ editedContent.length }} / 500자</div>
    </div>
    <div class="flex gap-2 border-t border-gray-200 p-4">
      <AppButton label="취소" color="neutral" variant="outline" class="flex-1" @click="emit('close')" />
      <AppButton
        label="답글 등록"
        icon="i-lucide-send"
        class="flex-1"
        :disabled="!editedContent.trim() || isGenerating"
        @click="handleSubmit"
      />
    </div>
  </div>
</template>
