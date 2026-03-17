import { ref } from 'vue'

export interface ToastItem {
  id: string
  title: string
  color?: string
}

const toasts = ref<ToastItem[]>([])

let id = 0
function genId() {
  return String(++id)
}

export function useToast() {
  const add = (options: { title: string; color?: string }) => {
    const item: ToastItem = {
      id: genId(),
      title: options.title,
      color: options.color ?? 'success',
    }
    toasts.value = [...toasts.value, item]
    setTimeout(() => {
      toasts.value = toasts.value.filter(t => t.id !== item.id)
    }, 3000)
  }
  return { toasts, add }
}

export function getToasts() {
  return toasts
}
