import { api } from '../../api/client'
import type { Category, CategoryInput } from '../../api/types'

export async function getCategories() {
    const { data } = await api.get<Category[]>('/categories')
    return data
}

export async function createCategory(input: CategoryInput) {
    const { data } = await api.post<Category>('/categories', input)
    return data
}

export async function updateCategory(id: string, input: CategoryInput) {
    const { data } = await api.put<Category>(`/categories/${id}`, input)
    return data
}

export async function deleteCategory(id: string) {
    await api.delete(`/categories/${id}`)
}