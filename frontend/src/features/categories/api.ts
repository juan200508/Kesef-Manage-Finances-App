import { api } from '../../api/client'
import type { Category } from '../../api/types'

export async function getCategories() {
    const { data } = await api.get<Category[]>('/categories')
    return data
}