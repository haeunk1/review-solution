<template>
  <button
    type="button"
    :class="buttonClass"
    :disabled="loading"
    @click="$emit('click')"
  >
    <component v-if="icon && !loading" :is="iconComponent" class="size-4 shrink-0" />
    <span v-if="loading" class="size-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
    <span v-if="label" :class="icon ? 'ml-2' : ''">{{ label }}</span>
    <component v-if="trailingIcon && !loading" :is="trailingIconComponent" class="ml-2 size-4 shrink-0" />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import * as Lucide from 'lucide-vue-next'

const props = withDefaults(
  defineProps<{
    label?: string
    icon?: string
    trailingIcon?: string
    color?: 'primary' | 'neutral' | 'success'
    variant?: 'solid' | 'ghost' | 'outline'
    size?: 'sm' | 'xs' | 'default'
    block?: boolean
    loading?: boolean
  }>(),
  { color: 'neutral', variant: 'solid', size: 'default', block: false, loading: false }
)

const iconComponent = computed(() => (props.icon ? (Lucide as Record<string, unknown>)[toPascal(props.icon)] : null))
const trailingIconComponent = computed(() =>
  props.trailingIcon ? (Lucide as Record<string, unknown>)[toPascal(props.trailingIcon)] : null
)
function toPascal(name: string) {
  const base = name.replace(/^i-lucide-/, '')
  return base.split('-').map(s => s.charAt(0).toUpperCase() + s.slice(1)).join('')
}

const buttonClass = computed(() => {
  const base = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50'
  const sizeClass =
    props.size === 'xs' ? 'h-7 px-2 text-xs' : props.size === 'sm' ? 'h-8 px-3 text-sm' : 'h-10 px-4 py-2 text-sm'
  const colorClass =
    props.variant === 'solid' && props.color === 'primary'
      ? 'bg-primary text-primary-foreground hover:bg-primary/90'
      : props.variant === 'solid' && props.color === 'neutral'
        ? 'bg-gray-100 text-gray-900 hover:bg-gray-200'
        : props.variant === 'ghost'
          ? 'hover:bg-gray-100'
          : 'border border-gray-300 bg-transparent hover:bg-gray-50'
  const blockClass = props.block ? 'w-full' : ''
  return [base, sizeClass, colorClass, blockClass].filter(Boolean).join(' ')
})

defineEmits<{ click: [] }>()
</script>
