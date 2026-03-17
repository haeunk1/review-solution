<script setup lang="ts">
import { computed, watch, ref } from 'vue'
import type { Review, ReplyOption } from '@/types/review'
import AppButton from '@/components/ui/AppButton.vue'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import AppTextarea from '@/components/ui/AppTextarea.vue'
import { Star } from 'lucide-vue-next'
import { useToast } from '@/composables/useToast'

const props = defineProps<{ review: Review }>()
const emit = defineEmits<{ submit: [reviewId: string, content: string]; close: [] }>()
const toast = useToast()

const replyOptions = computed<ReplyOption[]>(() => [
  {
    id: 'thank',
    type: 'thank',
    label: '감사형',
    content: `${props.review.author}님, 소중한 리뷰 감사합니다. 저희 병원을 방문해 주시고 좋은 경험을 해주셔서 기쁩니다. 앞으로도 최선의 진료와 서비스로 보답하겠습니다. 다음 방문 시에도 편안한 진료 받으실 수 있도록 하겠습니다.`,
  },
  {
    id: 'inform',
    type: 'inform',
    label: '정보제공형',
    content: `${props.review.author}님, 리뷰 감사합니다. 말씀해 주신 시술은 개인의 피부 상태에 따라 결과가 다를 수 있으며, 보통 2-3회 시술 후 최적의 효과를 기대하실 수 있습니다. 추가적인 문의 사항이 있으시면 언제든 연락 주세요.`,
  },
  {
    id: 'inquiry',
    type: 'inquiry',
    label: '문의유도형',
    content: `${props.review.author}님, 소중한 의견 감사합니다. 더 나은 서비스를 위해 노력하겠습니다. 추가적인 문의나 상담이 필요하시면 02-1234-5678로 연락 주시거나, 카카오톡 채널을 통해 편하게 문의해 주세요.`,
  },
])

const selectedOption = ref<ReplyOption>(replyOptions.value[0])
const editedContent = ref(replyOptions.value[0].content)
const isGenerating = ref(false)

watch(
  () => selectedOption.value,
  (option) => {
    editedContent.value = option.content
  }
)

const selectOption = (option: ReplyOption) => {
  selectedOption.value = option
}

const regenerate = async () => {
  isGenerating.value = true
  await new Promise((resolve) => setTimeout(resolve, 1000))
  editedContent.value = `${props.review.author}님, 진심으로 감사드립니다. 저희 청담피부과의원을 찾아주셔서 감사합니다. 고객님의 만족이 저희의 가장 큰 보람입니다. 앞으로도 더 좋은 진료와 서비스로 보답하겠습니다. 건강한 피부를 위해 항상 함께하겠습니다.`
  isGenerating.value = false
}

const handleSubmit = () => {
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
      <div class="mb-6 rounded-lg bg-gray-100 p-4">
        <div class="mb-2 flex items-center gap-3">
          <AppAvatar :src="review.avatarUrl" :alt="review.author" size="sm" />
          <div>
            <span class="font-medium text-gray-900">{{ review.author }}</span>
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
      </div>
      <div class="mb-4">
        <label class="mb-2 block text-sm font-medium text-gray-900">답글 유형 선택</label>
        <div class="flex flex-wrap gap-2">
          <AppButton
            v-for="option in replyOptions"
            :key="option.id"
            :label="option.label"
            :color="selectedOption.id === option.id ? 'primary' : 'neutral'"
            :variant="selectedOption.id === option.id ? 'solid' : 'outline'"
            size="sm"
            @click="selectOption(option)"
          />
        </div>
      </div>
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
            @click="regenerate"
          />
        </div>
        <AppTextarea v-model="editedContent" :rows="6" class="w-full" />
      </div>
      <div class="mb-4 text-right text-xs text-gray-500">{{ editedContent.length }} / 500자</div>
    </div>
    <div class="flex gap-2 border-t border-gray-200 p-4">
      <AppButton label="취소" color="neutral" variant="outline" class="flex-1" @click="emit('close')" />
      <AppButton label="답글 등록" icon="i-lucide-send" class="flex-1" @click="handleSubmit" />
    </div>
  </div>
</template>
