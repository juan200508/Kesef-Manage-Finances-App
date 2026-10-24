import { api } from '../../api/client'
import type { Movement, MovementCreateInput, MovementType, MovementUpdateInput } from '../../api/types'

export interface MovementFilters {
    types: MovementType[]
    categoryIds: string[]
    from: string // 'YYYY-MM-DD' o ''
    to: string
}

export const EMPTY_FILTERS: MovementFilters = { types: [], categoryIds: [], from: '', to: '' }

export async function getMovements(filters: MovementFilters) {
    const { data } = await api.get<Movement[]>('/movements', {
        params: {
            movement_type: filters.types,
            category_id: filters.categoryIds,
            // El día completo en hora local, convertido a UTC
            start_date: filters.from ? new Date(`${filters.from}T00:00:00`).toISOString() : undefined,
            end_date: filters.to ? new Date(`${filters.to}T23:59:59.999`).toISOString() : undefined,
        },
        paramsSerializer: { indexes: null }, // ?movement_type=A&movement_type=B
    })
    return data
}

export async function createMovement(input: MovementCreateInput) {
    const { data } = await api.post<Movement>('/movements', input)
    return data
}

export async function updateMovement(id: string, input: MovementUpdateInput) {
    const { data } = await api.put<Movement>(`/movements/${id}`, input)
    return data
}

export async function deleteMovement(id: string) {
    await api.delete(`/movements/${id}`)
}