import apiClient from './client'

export const reviewsApi = {
  collect: (hospitalId: string) =>
    apiClient.post(`/reviews/collect/${hospitalId}`),
}
