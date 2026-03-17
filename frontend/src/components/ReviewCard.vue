<script setup lang="ts">
import type { Review } from '@/types/review'
import AppAvatar from '@/components/ui/AppAvatar.vue'
import AppBadge from '@/components/ui/AppBadge.vue'
import { Star, CornerDownRight } from 'lucide-vue-next'

defineProps<{
  review: Review
  selected?: boolean
}>()

const emit = defineEmits<{ select: [review: Review] }>()

const formatDate = (dateString: string) => {
  return new Intl.DateTimeFormat('ko-KR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(dateString))
}
</script>

<template>
  <div
    class="cursor-pointer rounded-lg border p-4 transition-all hover:shadow-md"
    :class="[
      selected ? 'border-primary bg-gray-50' : 'border-gray-200 bg-white',
    ]"
    @click="emit('select', review)"
  >
    <div class="flex items-start justify-between gap-3">
      <div class="flex items-center gap-3">
        <AppAvatar :src="review.avatarUrl" :alt="review.author" size="md" />
        <div>
          <div class="flex items-center gap-2">
            <span class="font-medium text-gray-900">{{ review.author }}</span>
            <AppBadge v-if="review.replied" color="success" variant="subtle" size="xs">답변 완료</AppBadge>
            <AppBadge v-else color="warning" variant="subtle" size="xs">답변 대기</AppBadge>
          </div>
          <div class="mt-1 flex items-center gap-1">
            <Star
              v-for="i in 5"
              :key="i"
              class="size-4"
              :class="i <= review.rating ? 'text-yellow-400' : 'text-gray-300'"
            />
            <span class="ml-1 text-sm text-gray-500">{{ formatDate(review.date) }}</span>
          </div>
        </div>
      </div>
    </div>
    <p class="mt-3 text-sm text-gray-700 line-clamp-2">{{ review.content }}</p>
    <div v-if="review.replied && review.replyContent" class="mt-3 rounded-md bg-gray-100 p-3">
      <div class="mb-1 flex items-center gap-2 text-xs text-gray-500">
        <CornerDownRight class="size-3" />
        <span>병원 답변</span>
      </div>
      <p class="line-clamp-2 text-sm text-gray-700">{{ review.replyContent }}</p>
    </div>
  </div>
</template>
